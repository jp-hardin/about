# Turns each page of an industry report deck into a site-native report section: the same words, links, tables and
# logos as the deck, set in the site's report styles, with the deck's charts redrawn as SVG from their data.
# The deck's arrangement is kept loosely: elements that sit side by side on the page become columns that
# stack on narrow screens, and filled panels become cards.
import re
from deckhtml import Deck, X, X1, n, esc

TOL = 2.0        # points of overlap allowed between neighbors when finding rows and columns
ARTICLE = 690    # width of the report column on a wide screen, in CSS pixels
MIN_COL = 165    # narrowest column worth keeping side by side; narrower columns wrap


def luminance(css):
    m = re.match(r'#([0-9a-f]{6})', css or '')
    if not m:
        m2 = re.match(r'rgba?\((\d+),(\d+),(\d+)', css or '')
        if not m2:
            return 1.0
        r, g, b = (int(v) / 255 for v in m2.groups())
    else:
        h = m.group(1)
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def plain(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)).strip()


class WebDeck:
    def __init__(self, prs, media_dir, media_url, link_map=None):
        self.prs = prs
        self.d = Deck(prs, media_dir, media_url, link_map)
        self.W, self.H = self.d.W, self.d.H

    # -- one page --------------------------------------------------------
    def page(self, slide, num):
        boxes = self.d.shapes(X1(slide._element, './p:cSld/p:spTree'), slide.part, num)
        self.link_buttons(boxes)
        title = subtitle = None
        part = None
        foot = []
        keep = []
        texts = [b for b in boxes if getattr(b, 'paras', None)]
        for b in boxes:
            paras = getattr(b, 'paras', None) or []
            txt = ' '.join(p['text'] for p in paras if not p['empty']).strip()
            if paras:
                if re.fullmatch(r'0\d', txt) and max(p['size'] for p in paras) >= 30:
                    part = txt
                    continue
                if re.fullmatch(r'\d{1,2}', txt) and b.y > self.H * 0.9:
                    continue
                if b.y < 36 and (txt.isupper() or re.fullmatch(r'Q\d \d{4}', txt)) and max(p['size'] for p in paras) <= 9:
                    continue
                if '|' in txt and txt.isupper() and re.search(r'QUARTERLY (SECTOR BRIEF|INDUSTRY REPORT)|Q\d \d{4}', txt) and len(txt) < 60:
                    continue      # running header or footer
                if title is None and (b.ph == 'title' or (b.y < self.H * 0.2 and not txt.isupper() and len(txt) < 120
                                                          and max(p['size'] for p in paras) >= 14)) and num > 1:
                    title = b
                    continue
                if title is not None and subtitle is None and not any(getattr(k, 'paras', None) for k in keep) and b.y < self.H * 0.25 and not txt.isupper() \
                        and max(p['size'] for p in paras) < 14 and part is None:
                    subtitle = b
                    continue
                if part is not None and title is None and not txt.isupper() and len(txt) < 60 and max(p['size'] for p in paras) >= 20:
                    title = b
                    continue
                if b.y > self.H * 0.88 and max(p['size'] for p in paras) <= 8 and not b.container:
                    foot.append(b)
                    continue
            keep.append(b)
        keep = self.frames(keep)
        for b in keep:
            self.fit_text(b)
        keep = self.into_charts(keep)
        keep = self.bar_rows(keep)
        # Drop decoration: rules, unlabeled pictures, empty shapes. Filled shapes stay as possible cards.
        items = []
        for b in keep:
            if b.cls == 'ln' or b.cls == 'cg':
                continue
            if b.cls.startswith('pc') and not self.meaningful(b):
                continue
            if b.cls.startswith('sh') and not getattr(b, 'paras', None) and b.w <= 16 and b.h <= 10 and getattr(b, 'fill', None):
                b.cls, b.container = 'sw', False          # a legend key (a dot, a square or a short line)
                items.append(b)
                continue
            if b.cls.startswith('sh') and not getattr(b, 'paras', None) and not b.container:
                continue
            items.append(b)
        for b in items:
            b.children = []
        roots = self.d.tree(items)
        roots = self.prune(roots)
        span = (max(b.x + b.w for b in roots) - min(b.x for b in roots)) if roots else self.W
        body = self.layout(roots, ARTICLE / max(span, 1))
        t_html = self.inline(title) if title else ''
        s_html = self.inline(subtitle) if subtitle else ''
        f_html = ''.join(self.paras_html(b.paras, fine=True) for b in foot)
        text = ' '.join(plain(x) for x in (t_html, s_html, body, f_html))
        return dict(num=num, title=plain(t_html), title_html=t_html, subtitle=s_html, body=body, foot=f_html, part=part, text=text)

    @staticmethod
    def link_buttons(boxes):
        """A link set on a whole shape (a button, or a clear shape laid over one) goes on the words it holds."""
        def inside(t, b):
            cx, cy = t.x + t.w / 2, t.y + t.h / 2
            return b.x - 1 <= cx <= b.x + b.w + 1 and b.y - 1 <= cy <= b.y + b.h + 1
        texts = [t for t in boxes if getattr(t, 'paras', None)]
        for b in boxes:
            href = getattr(b, 'href', None)
            if not href or getattr(b, 'paras', None):
                continue
            for t in texts:
                if not getattr(t, 'href', None) and inside(t, b) and t.w <= b.w + 2 and t.h <= b.h + 2:
                    t.href = href
        for t in texts:
            href = getattr(t, 'href', None)
            if not href:
                continue
            tgt = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
            for p in t.paras:
                if not p['empty'] and '<a ' not in p['sem']:
                    p['sem'] = f'<a href="{esc(href)}"{tgt}>{p["sem"]}</a>'

    @staticmethod
    def frames(boxes):
        """Card outlines drawn as four thin rectangles become one outlined card."""
        thin = [b for b in boxes if b.cls.startswith('sh') and not getattr(b, 'paras', None) and getattr(b, 'fill', None) and (b.h <= 1.6 or b.w <= 1.6)]
        hz = [b for b in thin if b.h <= 1.6 and b.w > 20]
        vt = [b for b in thin if b.w <= 1.6 and b.h > 20]
        used, out = set(), []
        from deckhtml import Box
        for top in hz:
            for bot in hz:
                if bot is top or id(top) in used or id(bot) in used or abs(top.x - bot.x) > 1 or abs(top.w - bot.w) > 1 or bot.y <= top.y + 10:
                    continue
                lefts = [v for v in vt if abs(v.x - top.x) <= 1.5 and abs(v.y - top.y) <= 1.5 and abs(v.y + v.h - bot.y - bot.h) <= 2]
                rights = [v for v in vt if abs(v.x + v.w - top.x - top.w) <= 1.5 and abs(v.y - top.y) <= 1.5 and abs(v.y + v.h - bot.y - bot.h) <= 2]
                if lefts and rights:
                    f = Box(top.x, top.y, top.w, bot.y + bot.h - top.y, '', 'sh', container=True)
                    f.fill, f.line, f.paras, f.ph, f.geom, f.style = None, (0.75, top.fill, 'solid'), [], None, 'rect', ''
                    out.append(f)
                    used.update({id(top), id(bot), id(lefts[0]), id(rights[0])})
                    break
        if not out:
            return boxes
        res = []
        for b in boxes:
            if id(b) in used:
                continue
            res.append(b)
        # frames go first so they sit under their contents
        return out + res

    @staticmethod
    def fit_text(b):
        """A one-line label in a wide box takes only the width of its text, so neighbors in a grid separate cleanly."""
        paras = [p for p in (getattr(b, 'paras', None) or []) if not p['empty']]
        if b.container or len(paras) != 1 or len(paras[0]['text']) > 40:
            return
        p = paras[0]
        b.ox, b.ow = b.x, b.w
        tw = len(p['text']) * p['size'] * 0.52 + 2
        if tw >= b.w:
            return
        if p['align'] == 'r':
            b.x += b.w - tw
        elif p['align'] == 'ctr':
            b.x += (b.w - tw) / 2
        b.w = tw

    def into_charts(self, boxes):
        """Short labels set around a chart (axis values drawn as text boxes) and shaded bands behind it are drawn
        into the chart's SVG, where they belong."""
        charts = [b for b in boxes if b.cls == 'ch']
        if not charts:
            return boxes
        taken = set()
        for ch in charts:
            extra, before, labels = [], [], []
            minx = 0.0
            maxx = ch.w
            for b in boxes:
                if b is ch or id(b) in taken:
                    continue
                cx, cy = b.x + b.w / 2, b.y + b.h / 2
                paras = getattr(b, 'paras', None) or []
                txt = ' '.join(p['text'] for p in paras).strip()
                inside = ch.x - 40 <= cx <= ch.x + ch.w + 10 and ch.y - 2 <= cy <= ch.y + ch.h + 2
                if not inside:
                    continue
                if paras and not b.container and len(txt) <= 8 and len(paras) == 1:
                    p = paras[0]
                    anchor = {'r': 'end', 'ctr': 'middle'}.get(p['align'], 'start')
                    x = (b.x + b.w if anchor == 'end' else b.x + b.w / 2 if anchor == 'middle' else b.x) - ch.x
                    y = b.y + b.h / 2 - ch.y
                    minx = min(minx, b.x - ch.x)
                    maxx = max(maxx, b.x + b.w - ch.x)
                    labels.append(txt)
                    extra.append(f'<text x="{n(x)}" y="{n(y)}" font-size="{n(p["size"])}" fill="{p["color"] or "#333"}" '
                                 f'text-anchor="{anchor}" dominant-baseline="middle">{esc(txt)}</text>')
                    taken.add(id(b))
                elif not paras and b.cls.startswith('sh') and getattr(b, 'fill', None) and not b.children:
                    pass
            for b in boxes:
                # a shaded band drawn across the chart (estimate years, say): drawn inside the chart, clipped to it
                if id(b) in taken or b is ch or getattr(b, 'paras', None) or not b.cls.startswith('sh') or not getattr(b, 'fill', None):
                    continue
                x0, y0 = max(b.x, ch.x), max(b.y, ch.y)
                x1, y1 = min(b.x + b.w, ch.x + ch.w), min(b.y + b.h, ch.y + ch.h)
                if x1 - x0 > 2 and y1 - y0 > 2 and (x1 - x0) * (y1 - y0) >= 0.3 * b.w * b.h and b.w * b.h < 0.6 * ch.w * ch.h:
                    before.append(f'<rect x="{n(x0 - ch.x)}" y="{n(y0 - ch.y)}" width="{n(x1 - x0)}" height="{n(y1 - y0)}" fill="{b.fill}"/>')
                    taken.add(id(b))
            if extra:
                # the deck sets this chart's axis labels beside it; the phone drawing shows them on its own axis
                from deckhtml import Chart
                code = None
                for lab in labels:
                    m = re.match(r'^([^\d\-−]*)(-|−)?([\d,]+)(\.\d+)?(.*)$', lab)
                    if m:
                        dec = '.' + '0' * (len(m.group(4)) - 1) if m.group(4) else ''
                        code = (f'"{m.group(1)}"' if m.group(1) else '') + '0' + dec + (f'"{m.group(5)}"' if m.group(5) else '')
                        break
                ch.html_m = Chart(self.d, ch.cs, ch.w, ch.h, mobile=True, show_val=True, val_code=code).svg()[0]
            if extra or before:
                h = ch.html
                h = re.sub(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', lambda m: f'viewBox="{n(minx)} 0 {n(maxx - minx)} {m.group(2)}"', h, count=1)
                h = re.sub(r'(<svg[^>]*>)', lambda m: m.group(1) + ''.join(before), h, count=1)
                ch.html = h.replace('</svg>', ''.join(extra) + '</svg>')
        return [b for b in boxes if id(b) not in taken]

    def bar_rows(self, boxes):
        """Bar charts drawn with plain shapes: each bar with the label and value beside it becomes one row."""
        def is_bar(b):
            return (b.cls.startswith('sh') and not getattr(b, 'paras', None) and getattr(b, 'fill', None)
                    and 4 <= b.h <= 18 and b.w >= 0.3 and not (b.w <= 10 and b.h <= 10 and b.w > 0.3 * b.h and b.w < 2 * b.h))
        texts_all = [t for t in boxes if getattr(t, 'paras', None)]
        def holds_text(b):
            return any(b.x <= t.x + t.w / 2 <= b.x + b.w and b.y <= t.y + t.h / 2 <= b.y + b.h for t in texts_all)
        cands = [b for b in boxes if is_bar(b) and not holds_text(b)]
        if len(cands) < 3:
            return boxes
        edges = {}
        for b in cands:
            for e in (round(b.x, 0), round(b.x + b.w, 0)):
                edges[e] = edges.get(e, 0) + 1
        groups = []
        used = set()
        for zero, cnt in sorted(edges.items(), key=lambda kv: -kv[1]):
            if cnt < 3:
                break
            g = [b for b in cands if id(b) not in used and (abs(b.x - zero) <= 1.2 or abs(b.x + b.w - zero) <= 1.2)]
            if len(g) >= 3 and len({round(b.w) for b in g}) >= max(2, len(g) // 2):   # real bars differ in length
                groups.append((zero, g))
                used.update(id(b) for b in g)
        if not groups:
            return boxes
        texts = [b for b in boxes if getattr(b, 'paras', None) and not b.container]
        taken, rows = set(), []
        for zero, g in groups:
            lo = min(b.x for b in g)
            hi = max(b.x + b.w for b in g)
            span = max(hi - lo, 1)
            lo, hi = lo - span * 0.12, hi + span * 0.12
            span = hi - lo
            for bar in g:
                cy = bar.y + bar.h / 2
                near = [t for t in texts if id(t) not in taken and t.y - 6 <= cy <= t.y + t.h + 6
                        and lo - span * 1.6 <= t.x + t.w / 2 <= hi + span * 0.6]
                num = [t for t in near if re.fullmatch(r'[−\-+$]?[\d.,]+[%x]?[BMK]?', ' '.join(p['text'] for p in t.paras).strip())]
                lab = [t for t in near if t not in num and t.x + t.w <= lo + span * 0.2]
                value = min(num, key=lambda t: abs(t.x + t.w / 2 - (bar.x + bar.w / 2))) if num else None
                label = min(lab, key=lambda t: abs(t.x + t.w - lo)) if lab else None
                parts = [x for x in (label, bar, value) if x]
                x0, y0 = min(x.x for x in parts), min(x.y for x in parts)
                x1, y1 = max(x.x + x.w for x in parts), max(x.y + x.h for x in parts)
                from deckhtml import Box
                r = Box(x0, y0, x1 - x0, y1 - y0, '', 'br')
                r.label = ' '.join(p['sem'] for p in label.paras if not p['empty']) if label else ''
                r.value = ' '.join(p['sem'] for p in value.paras if not p['empty']) if value else ''
                r.left, r.width = (bar.x - lo) / span * 100, bar.w / span * 100
                r.zero = (zero - lo) / span * 100
                r.fill = bar.fill
                r.paras = []
                r.text = plain(r.label + ' ' + r.value)
                rows.append(r)
                taken.update(id(x) for x in parts)
        out = [b for b in boxes if id(b) not in taken]
        # keep deck order: put each row where its bar was
        return out + rows

    @staticmethod
    def meaningful(pic):
        """Company logos (alt text that is a name) and people's photos stay; scenery, icons and the Benchmark mark go."""
        alt = (getattr(pic, 'alt', '') or '').strip()
        if not alt or alt == 'Benchmark International':
            return False
        if pic.geom == 'ellipse':
            return True
        words = re.findall(r"[A-Za-z][\w'’]*", alt)
        return bool(words) and all(w[0].isupper() or w.lower() in ('and', 'of', 'the', '&') for w in words) and len(alt) <= 60 \
            and not re.match(r'(A|An|The) ', alt)

    def prune(self, boxes):
        out = []
        for b in boxes:
            b.children = self.prune(b.children)
            if b.cls.startswith('sh') and not getattr(b, 'paras', None) and not b.children:
                continue
            out.append(b)
        return out

    # -- arrangement -----------------------------------------------------
    def layout(self, items, scale):
        """Rows and columns from positions. scale is CSS pixels per deck point at the widest layout."""
        if not items:
            return ''
        if len(items) == 1:
            return self.render(items[0], scale)
        # a legend key sits on its text line: compare by vertical center so it joins that line
        def top(b):
            return b.y + b.h / 2 - 5 if b.cls == 'sw' else b.y

        def bottom(b):
            return b.y + b.h / 2 + 5 if b.cls == 'sw' else b.y + b.h
        srt = sorted(items, key=lambda b: (top(b), b.x))
        bands = []
        for b in srt:
            if bands and top(b) < bands[-1]['bottom'] - TOL:
                bands[-1]['items'].append(b)
                bands[-1]['bottom'] = max(bands[-1]['bottom'], bottom(b))
            else:
                bands.append({'items': [b], 'bottom': bottom(b)})
        # A run of aligned grid rows (column headings and values) stays together as one band.
        k = 0
        while k < len(bands):
            j = k
            while j < len(bands) and self.grid_band(bands[j]['items']):
                j += 1
            if j - k >= 2 and self.aligned([bd['items'] for bd in bands[k:j]]):
                bands[k:j] = [{'items': [x for bd in bands[k:j] for x in bd['items']], 'bottom': bands[j - 1]['bottom'], 'grid': [bd['items'] for bd in bands[k:j]]}]
            k += 1
        if len(bands) == 1 and bands[0].get('grid'):
            return self.grid(bands[0]['grid'])
        # Cut along the widest white space first: across the page (rows) or down it (columns).
        hgap = max((min(x.y for x in bands[k + 1]['items']) - bands[k]['bottom'] for k in range(len(bands) - 1)), default=-1)
        xs = sorted(items, key=lambda b: b.x)
        cols0, right = [], None
        for b in xs:
            if right is not None and b.x >= right - TOL:
                cols0.append(b.x - right)
            right = b.x + b.w if right is None else max(right, b.x + b.w)
        vgap = max(cols0, default=-1)
        grid_rows = sum(1 for bd in bands if self.grid_band(bd['items'])) + sum(len(bd['grid']) for bd in bands if bd.get('grid'))
        if len(bands) > 1 and vgap > 0 and vgap > hgap * 1.5 and vgap >= 8 and hgap < 10 and grid_rows < 3:
            bands = [{'items': items, 'bottom': max(b.y + b.h for b in items)}]
        elif len(bands) > 2:
            # cut only at the wider gaps here; the narrower ones are decided inside each part
            gaps = [min(x.y for x in bands[k + 1]['items']) - bands[k]['bottom'] for k in range(len(bands) - 1)]
            cut = max(gaps) * 0.6
            if max(gaps) >= 8 and min(gaps) < cut:
                merged, cur = [], {'items': list(bands[0]['items']), 'bottom': bands[0]['bottom']}
                for k, g in enumerate(gaps):
                    nxt = bands[k + 1]
                    if g >= cut:
                        merged.append(cur)
                        cur = {'items': list(nxt['items']), 'bottom': nxt['bottom']}
                    else:
                        cur['items'] += nxt['items']
                        cur['bottom'] = max(cur['bottom'], nxt['bottom'])
                merged.append(cur)
                if 1 < len(merged) < len(bands):
                    return '\n'.join(self.layout(bd['items'], scale) for bd in merged)
        if len(bands) == 1 and self.line_band(items):
            return self.line_row(items)
        if len(bands) > 1:
            out, i = [], 0
            while i < len(bands):
                if bands[i].get('grid'):
                    out.append(self.grid(bands[i]['grid']))
                    i += 1
                    continue
                j = i
                while j < len(bands) and self.grid_band(bands[j]['items']):
                    j += 1
                if j - i >= 2 and self.aligned([bd['items'] for bd in bands[i:j]]):
                    out.append(self.grid([bd['items'] for bd in bands[i:j]]))
                    i = j
                    continue
                out.append(self.layout(bands[i]['items'], scale))
                i += 1
            return '\n'.join(out)
        if self.legend_band(items):
            return self.legend(items)
        if len(items) >= 2 and all(self.chip(b) for b in items):
            return '<p class="dchips">' + ''.join(self.chip_html(b) for b in sorted(items, key=lambda b: b.x)) + '</p>'
        srt = sorted(items, key=lambda b: (b.x, b.y))
        cols = []
        for b in srt:
            if cols and b.x < cols[-1]['right'] - TOL:
                cols[-1]['items'].append(b)
                cols[-1]['right'] = max(cols[-1]['right'], b.x + b.w)
                cols[-1]['left'] = min(cols[-1]['left'], b.x)
            else:
                cols.append({'items': [b], 'right': b.x + b.w, 'left': b.x})
        # Neighboring columns whose items sit on the same lines are one list (a ticker, a name, a value): keep them together.
        merged = [cols[0]]
        orig_l = lambda c: min(getattr(b, 'ox', b.x) for b in c['items'])
        orig_r = lambda c: max(getattr(b, 'ox', b.x) + getattr(b, 'ow', b.w) for b in c['items'])
        for c in cols[1:]:
            prev = merged[-1]
            ys = [b.y + b.h / 2 for b in prev['items'] if not b.container or self.chip(b)]
            hits = sum(1 for b in c['items'] if any(abs(b.y + b.h / 2 - y) <= 3 for y in ys))
            small = min(len(prev['items']), len(c['items']))
            close = orig_l(c) - orig_r(prev) <= 10
            if small >= 3 and hits >= 3 and hits >= 0.6 * small and close:
                prev['items'] += c['items']
                prev['right'] = max(prev['right'], c['right'])
            else:
                merged.append(c)
        if len(merged) < len(cols) and len(merged) > 1:
            cols = merged
        elif len(merged) == 1 and len(cols) > 1:
            # one list across the whole width: read it row by row
            rows = []
            for b in sorted(items, key=lambda b: b.y + b.h / 2):
                if rows and abs(b.y + b.h / 2 - rows[-1]['c']) <= 3:
                    rows[-1]['items'].append(b)
                else:
                    rows.append({'items': [b], 'c': b.y + b.h / 2})
            if len(rows) > 1:
                return '\n'.join(self.layout(r['items'], scale) for r in rows)
        if len(cols) == 1:
            return '\n'.join(self.render(b, scale) for b in items)      # overlapping elements: deck order
        widths = [c['right'] - c['left'] for c in cols]
        tot = sum(widths)
        textlen = [sum(len(' '.join(p['text'] for p in getattr(b, 'paras', []) or [])) for b in c['items']) for c in cols]
        # A short column beside another (a figure and its label, a label and its value) stays side by side.
        tight = len(cols) == 2 and min(textlen) <= 12 and not any(b.container for c in cols for b in c["items"])
        if tight:
            short = textlen.index(min(textlen))
            inner = ''.join(f'<div class="dcol{" dcol--fit" if i == short else ""}">{self.layout(c["items"], scale)}</div>' for i, c in enumerate(cols))
            return f'<div class="drow drow--tight">{inner}</div>'
        # Columns keep the deck's proportions where they fit, and wrap onto the next line when a column would be
        # narrower than its content needs (charts and tables need more room than a paragraph).
        avail = tot * scale
        gap = 26
        inner = []
        for c, w in zip(cols, widths):
            frac = w / tot
            need = self.need(c['items'])
            inner.append(f'<div class="dcol" style="flex:{n(frac * 10, 2)} 1 {n(need, 0)}px">{self.layout(c["items"], max(scale, need / max(w, 1)))}</div>')
        if len(cols) >= 3 and max(widths) / max(min(widths), 1) < 1.3:
            need = max(self.need(c['items']) for c in cols)
            inner = [f'<div class="dcol">{self.layout(c["items"], max(scale, need / max(w, 1)))}</div>' for c, w in zip(cols, widths)]
            return f'<div class="drow drow--tiles" style="--min:{n(need, 0)}px">{"".join(inner)}</div>'
        return f'<div class="drow">{"".join(inner)}</div>'

    def need(self, items):
        """Narrowest comfortable width, in CSS pixels, for a column holding these elements."""
        best = 0
        for b in items:
            if getattr(b, 'paras', None) and not b.container:
                longest = max((len(w) for p in b.paras for w in p['text'].split()), default=0)
                total = sum(len(p['text']) for p in b.paras)
                best = max(best, min(MIN_COL, 24 + 8 * max(longest, min(total, 18))))
            if b.cls in ('br',):
                best = max(best, 280)
            if self.chip(b):
                best = max(best, 60)
                continue
            if b.cls.startswith('pc') or b.cls == 'sw':
                best = max(best, min(MIN_COL, b.w * 1.5))
            if b.cls in ('ch', 'tb'):
                best = max(best, 300)
            elif b.container and b.children:
                best = max(best, 200, self.need(b.children))
        return best or MIN_COL

    # -- small structures ------------------------------------------------
    @staticmethod
    def short(b, limit=22):
        paras = [p for p in (getattr(b, 'paras', None) or []) if not p['empty']]
        return not b.container and 1 <= len(paras) <= 2 and len(' '.join(p['text'] for p in paras)) <= limit

    def grid_band(self, items):
        """A row of three or more short cells (values, year labels, column headings, legend keys)."""
        cells = [b for b in items if b.cls != 'sw']
        return len(cells) >= 3 and all(self.short(b, 34) for b in cells)

    @staticmethod
    def aligned(rows):
        """Rows whose cells line up in the same columns."""
        counts = {len([b for b in r if b.cls != 'sw']) for r in rows}
        if max(counts) - min(counts) > 1:
            return False
        ref = sorted(rows, key=lambda r: -len(r))[0]
        cols = sorted(b.x + b.w / 2 for b in ref if b.cls != 'sw')
        for r in rows:
            for b in r:
                if b.cls == 'sw':
                    continue
                if min(abs(b.x + b.w / 2 - c) for c in cols) > 45:
                    return False
        return True

    def grid(self, rows):
        ref = sorted(rows, key=lambda r: -len([b for b in r if b.cls != 'sw']))[0]
        cols = sorted(b.x + b.w / 2 for b in ref if b.cls != 'sw')
        has_sw = any(b.cls == 'sw' for r in rows for b in r)
        html_rows = []
        for k, r in enumerate(rows):
            cells = [''] * len(cols)
            sw = ''
            for b in sorted(r, key=lambda b: b.x):
                if b.cls == 'sw':
                    sw += self.render(b)
                    continue
                i = min(range(len(cols)), key=lambda i: abs(b.x + b.w / 2 - cols[i]))
                cells[i] = (cells[i] + ' ' if cells[i] else '') + ' '.join(p['sem'] for p in b.paras if not p['empty'])
            head = k == 0 and not any(re.search(r'\d', plain(c)) for c in cells)
            tag = 'th' if head else 'td'
            lead = f'<{tag} class="dgrid-k">{sw}</{tag}>' if has_sw else ''
            html_rows.append('<tr>' + lead + ''.join(
                f'<{tag}{" class=" + chr(34) + "dgrid-n" + chr(34) if re.search(r"[A-Za-z]{3}", plain(c)) and not head else ""}>{c}</{tag}>' for c in cells) + '</tr>')
        return f'<div class="dgrid-wrap"><table class="dgrid"><tbody>{"".join(html_rows)}</tbody></table></div>'

    def chip(self, b):
        """A small filled box holding a short code or name (a ticker, a tag)."""
        if not b.container or b.w > 90 or b.h > 24:
            return False
        kids = b.children
        texts = [p for p in (getattr(b, 'paras', None) or []) if not p['empty']]
        if kids and all(self.short(k, 24) for k in kids) and len(kids) == 1:
            return True
        return bool(texts) and not kids and len(' '.join(p['text'] for p in texts)) <= 24

    def chip_html(self, b):
        src = b.children[0] if b.children else b
        txt = ' '.join(p['sem'] for p in src.paras if not p['empty'])
        dark = b.fill and luminance(b.fill) < 0.35
        return f'<span class="dchip{" dchip--dark" if dark else ""}">{txt}</span>'

    def line_band(self, items):
        """One line of a list: a ticker or key, a name, a figure."""
        if not 2 <= len(items) <= 4:
            return False
        if not all(self.chip(b) or b.cls == 'sw' or self.short(b, 44) for b in items):
            return False
        texts = [' '.join(p['text'] for p in b.paras) for b in items if getattr(b, 'paras', None) and not b.container]
        return any(self.chip(b) or b.cls == 'sw' for b in items) or any(re.search(r'\d', t) and len(t) <= 12 for t in texts)

    def line_row(self, items):
        cells = []
        items = sorted(items, key=lambda b: b.x)
        lens = [len(' '.join(p['text'] for p in (b.paras or []))) if getattr(b, 'paras', None) and not b.container else 0 for b in items]
        grow = lens.index(max(lens))
        for i, b in enumerate(items):
            if self.chip(b):
                inner = self.chip_html(b)
            elif b.cls == 'sw':
                inner = self.render(b)
            else:
                inner = '<br>'.join(p['sem'] for p in b.paras if not p['empty'])
            num = re.fullmatch(r'[−\-+$~]?[\d.,]+\s?[%xX]?[BMKT]?', plain(inner)) is not None
            cells.append(f'<div class="dline-c{" dline-c--grow" if i == grow else ""}{" dline-c--num" if num else ""}">{inner}</div>')
        return f'<div class="dline">{"".join(cells)}</div>'

    def legend_band(self, items):
        return any(b.cls == 'sw' for b in items) and all(b.cls == 'sw' or self.short(b, 40) for b in items) and len(items) >= 2

    def legend(self, items):
        entries = []          # [swatch html, text html]
        for b in sorted(items, key=lambda b: b.x):
            if b.cls == 'sw':
                entries.append([self.render(b), ''])
            else:
                txt = ' '.join(p['sem'] for p in b.paras if not p['empty'])
                if entries and not entries[-1][1]:
                    entries[-1][1] = txt
                else:
                    entries.append(['', txt])
        return '<p class="dlegend">' + ''.join(f'<span class="dlegend-i">{a}{t}</span>' for a, t in entries) + '</p>'

    def render(self, b, scale=1.0):
        if b.cls == 'br':
            return (f'<div class="dbar"><span class="dbar-l">{b.label}</span><span class="dbar-t" style="--z:{n(b.zero, 2)}%">'
                    f'<i style="left:{n(b.left, 2)}%;width:{n(max(b.width, 0.4), 2)}%;background:{b.fill}"></i></span>'
                    f'<span class="dbar-v">{b.value}</span></div>')
        if b.cls == 'sw':
            shape = ' dsw--round' if b.geom == 'ellipse' else ' dsw--diamond' if b.geom == 'diamond' else ' dsw--line' if b.h < 4 else ''
            return f'<span class="dsw{shape}" style="background:{b.fill}" aria-hidden="true"></span>'
        if b.cls == 'ch':
            data = f'<details class="rdata"><summary>Chart data</summary>{b.data_table}</details>' if getattr(b, 'data_table', '') else ''
            svg = re.sub(r'font-size="([\d.]+)"', lambda m: f'font-size="{n(float(m.group(1)) * 1.25, 2)}"', b.html)
            svg = svg.replace('<svg ', '<svg class="svg-d" ', 1)
            mob = getattr(b, 'html_m', '')
            if mob:
                mob = mob.replace('<svg ', '<svg class="svg-m" aria-hidden="true" ', 1).replace(' role="img"', '', 1)
            return f'<figure class="dchart" style="--cw:{n(b.w * 1.9, 0)}px">{svg}{mob}{data}</figure>'
        if b.cls == 'tb':
            return self.table(b)
        if b.cls.startswith('pc'):
            cls = 'dperson' if b.geom == 'ellipse' else 'dlogo'
            w = min(b.w * 1.5, 360)
            return f'<img class="{cls}" src="{esc(b.url)}" alt="{esc(b.alt)}" loading="lazy" decoding="async" style="--w:{n(w)}px">'
        if self.chip(b):
            return '<p class="dchips">' + self.chip_html(b) + '</p>'
        own = self.paras_html(b.paras) if getattr(b, 'paras', None) else ''
        if own and not (b.container and (b.children or own)):
            return f'<div class="dtx">{own}</div>'
        if b.container and (b.children or own):
            lum = luminance(b.fill) if b.fill else 1.0
            kind = 'dark' if b.fill and lum < 0.35 else 'paper' if b.fill and lum < 0.985 else 'line'
            if kind == 'line' and not b.line and b.fill:
                kind = 'plain'
            style = f' style="--card:{b.fill}"' if b.fill and kind in ('dark', 'paper') else ''
            inner_scale = max(0.2, (b.w * scale - 48) / max(b.w, 1))
            kids = self.layout(b.children, inner_scale) if b.children else ''
            return f'<div class="dcard dcard--{kind}"{style}>{own}{kids}</div>'
        return own

    # -- text ------------------------------------------------------------
    def inline(self, b):
        return ' '.join(p['sem'] for p in b.paras if not p['empty'])

    def paras_html(self, paras, fine=False):
        out, ul = [], []

        def flush():
            if ul:
                out.append('<ul class="rlist">' + ''.join(f'<li>{x}</li>' for x in ul) + '</ul>')
                ul.clear()
        for p in paras:
            if p['empty']:
                continue
            t, h, sz = p['text'].strip(), p['sem'], p['size']
            if p['bullet']:
                ul.append(h)
                continue
            flush()
            letters = [c for c in t if c.isalpha()]
            if not fine and (p['caps'] or (letters and t == t.upper())) and len(t) < 90 and sz <= 10.5 and len(letters) > 2:
                out.append(f'<p class="dlabel">{h}</p>')
            elif fine or sz <= 7:
                out.append(f'<p class="fine">{h}</p>')
            elif sz >= 15 and len(t) <= 18 and re.search(r'\d', t):
                out.append(f'<p class="dnum">{h}</p>')
            elif t[:1] in '“"‘' and len(t) > 40:
                out.append(f'<blockquote class="dquote">{h}</blockquote>')
            elif p['bold'] and len(t) < 140 and sz >= 9:
                out.append(f'<h3 class="dh{" dh--lg" if sz >= 13 else ""}">{h}</h3>')
            elif sz >= 13 and len(t) < 260:
                out.append(f'<p class="dlead">{h}</p>')
            else:
                out.append(f'<p>{h}</p>')
        flush()
        return '\n'.join(out)

    def table(self, b):
        rows = []
        for i, tr in enumerate(X(b.tbl, './a:tr')):
            cells = []
            for tc in X(tr, './a:tc'):
                if tc.get('hMerge') == '1' or tc.get('vMerge') == '1':
                    continue
                self.d.text_html(X1(tc, './a:txBody'), [X1(tc, './a:txBody/a:lstStyle'), self.d.default_style], b.part.rels, 0)
                inner = '<br>'.join(p['sem'] for p in self.d.last_meta if not p['empty'])
                span = f' colspan="{tc.get("gridSpan")}"' if tc.get('gridSpan') else ''
                tag = 'th' if i == 0 else 'td'
                cells.append(f'<{tag}{span}>{inner}</{tag}>')
            if any(plain(c) for c in cells):
                rows.append(cells)
        if not rows:
            return ''
        head = '<tr>' + ''.join(rows[0]) + '</tr>'
        body = ''.join('<tr>' + ''.join(r) + '</tr>' for r in rows[1:])
        return f'<div class="rtable-wrap"><table class="rtable dtable"><thead>{head}</thead><tbody>{body}</tbody></table></div>'

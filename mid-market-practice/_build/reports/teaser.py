"""Teaser summaries for the online reports.

Online each report section is a short, crawlable summary of the deck page: its finding, a lead paragraph, the key points
(each heading with its first sentence or two), the deals and buyers it names and its headline figures, all as plain
text. A chart becomes one line of its values ("Building Products & Construction +21.8%, ..."), so the figures stay
readable to search engines and AI assistants; the charts themselves, pictures, logos and long tables stay in the PDF.
Each section ends with a line saying what the full section adds and a button to download the report.
"""
import html
import re
from lxml import html as LH

DROP = {'figure', 'svg', 'img', 'picture', 'details', 'blockquote', 'script', 'style', 'table'}
DROP_CLASS = re.compile(r'\b(wfine|wmeta|wlink|wkick|wnotes|wdata|fine|rfilter|wsub|wstats|dbar)\b')
MAX_POINTS, MAX_DEALS, MAX_LEAD = 7, 6, 2
_N = r'[−+\-$]?[\d.,]+\s*(?:%|x|pts|B|M|bn|GW|weeks|months)?'
NUMERIC = re.compile(rf'^{_N}(?: to {_N})?$')


def text(el):
    return re.sub(r'\s+', ' ', ''.join(el.itertext())).replace('\xa0', ' ').strip()


def sentences(t, n=2, limit=300):
    """The first n sentences of t, kept under limit characters (at least one whole sentence)."""
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9“"$(])', t.strip())
    out = ''
    for p in parts[:n]:
        if out and len(out) + len(p) + 1 > limit:
            break
        out = (out + ' ' + p).strip()
    return out


def fix_caps(s):
    return s.title().replace("'S ", "'s ").replace('’S ', '’s ') if s.isupper() and len(s) > 4 else s


def clean_heading(t):
    return fix_caps(t.strip().rstrip(':').strip())


def caps_label(t):
    """A leading all-caps label run into its sentence ("WHAT BUYERS ASK FOR A bill of ...") as (label, sentence)."""
    w = t.split(' ')
    k = 0
    while k < len(w) and w[k].isupper() and len(re.sub(r'\W', '', w[k])) > 0:
        if len(w[k]) == 1 and k + 1 < len(w) and w[k + 1][:1].islower():
            break
        k += 1
    if k < 2 or k >= len(w):
        return '', t
    return ' '.join(w[:k]).capitalize(), ' '.join(w[k:])


def deals_from(table):
    """'Acquirer acquired Target, Month Year' lines from a transactions table (a cell with 'acquired by' in it)."""
    out = []
    for tr in table.xpath('.//tbody/tr'):
        cells = tr.xpath('./td|./th')
        for i, c in enumerate(cells):
            lines = [x.strip() for x in c.itertext() if x.strip()]
            low = [x.lower() for x in lines]
            if 'acquired by' not in low:
                continue
            k = low.index('acquired by')
            target, buyer = ' '.join(lines[:k]), (lines[k + 1] if k + 1 < len(lines) else '')
            backer = lines[k + 2] if k + 2 < len(lines) else ''
            first = [x.strip() for x in cells[0].itertext() if x.strip()] if i > 0 else []
            when = first[0] if first and re.search(r'\d{4}', first[0]) else ''
            line = f'{fix_caps(buyer)}{f" ({backer})" if backer else ""} acquired {fix_caps(target)}'
            out.append(line + (f', {fix_caps(when)}' if when else ''))
            break
    return out


def pairs_line(pairs):
    return ', '.join(f'{a} {b}'.strip() for a, b in pairs)


def number(v):
    n = re.sub(r'[^\d.\-−]', '', v.replace(',', '')).replace('−', '-')
    try:
        return float(n)
    except ValueError:
        return None


TIME = re.compile(r"(?:^|\s)(?:19|20)\d\d\b|^(?:Now|Today)$|\bQ[1-4]\b|^[A-Z][a-z]{2,8}\.? ?'?\d{2,4}$")


MONTHS = {m[:3]: m for m in ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                               'October', 'November', 'December')}


def month(l):
    """'Oct 21' or '2021-10' as 'October 2021'."""
    iso = re.match(r'((?:19|20)\d\d)-(\d\d)$', l)
    if iso and 1 <= int(iso.group(2)) <= 12:
        return f'{list(MONTHS.values())[int(iso.group(2)) - 1]} {iso.group(1)}'
    m = re.match(r"([A-Z][a-z]{2})[a-z]*\.? ?'?(\d{2}|\d{4})$", l)
    if not m or m.group(1) not in MONTHS:
        return l
    y = m.group(2)
    return f'{MONTHS[m.group(1)]} {"20" + y if len(y) == 2 else y}'


def summarize(pairs, rate=False):
    """A chart's values as a sentence: over time, where it started and ended and its high and low; across
    categories, which is highest and lowest."""
    vals = [(l, v, number(v)) for l, v in pairs if number(v) is not None]
    if len(vals) < 2:
        return pairs_line(pairs)
    if all(re.search(r'year', l, re.I) for l, _, _ in vals):
        return ''
    hi, lo = max(vals, key=lambda x: x[2]), min(vals, key=lambda x: x[2])
    if all(TIME.search(l) for l, _, _ in vals):
        (l0, v0, n0), (l1, v1, n1) = vals[0], vals[-1]
        if len(vals) > 12:
            # a long monthly series: the change since it starts and when it peaked or bottomed
            l0, hl, ll = month(l0), month(hi[0]), month(lo[0])
            if rate:      # a rate or index in percent: the change in points
                ch = n1 - n0
                out = f'{"Up" if ch > 0 else "Down"} {abs(ch):.1f} points since {l0}' if round(ch, 1) else f'About level with {l0}'
            else:
                ch = (n1 - n0) / abs(n0) * 100 if n0 else 0
                out = f'{"Up" if ch > 0 else "Down"} {abs(ch):.0f}% since {l0}' if round(ch) else f'About level with {l0}'
            extra = []
            if hi[0] not in (vals[0][0], l1):
                extra.append(f'peaking in {hl}')
            if lo[0] not in (vals[0][0], l1):
                extra.append(f'with its low in {ll}')
            return out + (', ' + ' and '.join(extra) if extra else '') + '.'

        when = lambda l: l.lower() if l in ('Now', 'Today') else f'in {month(l)}'
        out = f'{"Up" if n1 > n0 else "Down" if n1 < n0 else "Level"} from {v0} {when(l0)} to {v1} {when(l1)}'
        extra = []
        if hi[0] not in (l0, l1):
            extra.append(f'a high of {hi[1]} {when(hi[0])}')
        if lo[0] not in (l0, l1):
            extra.append(f'a low of {lo[1]} {when(lo[0])}')
        return out + (', with ' + ' and '.join(extra) if extra else '') + '.'
    if len(vals) <= 3:
        return pairs_line([(l, v) for l, v, _ in vals]) + '.'
    ranked = sorted(vals, key=lambda x: -x[2])
    nxt = ranked[1:3] if len(ranked) > 4 else ranked[1:2]
    return (f'{hi[0]} is highest at {hi[1]}, followed by ' + ' and '.join(f'{l} at {v}' for l, v, _ in nxt)
            + f'; {lo[0]} is lowest at {lo[1]}.')


def chart_line(fig, rate=False):
    """A summary sentence of a chart from its data table (one series), or ''."""
    t = fig.xpath('.//details[contains(@class,"wdata")]//table')
    if not t:
        return ''
    rows = t[0].xpath('.//tbody/tr')
    out = []
    for r in rows:
        cells = [text(c) for c in r.xpath('./th|./td')]
        if len(cells) != 2:
            return ''
        out.append((cells[0], cells[1]))
    return summarize(out, rate) if out else ''




def small_table_line(t):
    """A short two-column table (or a header row over one row of values) as one line."""
    rows = [[text(c) for c in r.xpath('./th|./td')] for r in t.xpath('.//tr')]
    if 2 <= len(rows) <= 6 and all(len(r) == 2 for r in rows):
        return pairs_line([(a, b) for a, b in rows])
    if len(rows) == 2 and len(rows[0]) == len(rows[1]) <= 6:
        return pairs_line(list(zip(rows[0], rows[1])))
    return ''


def rank_line(pairs):
    """Names with values: all of them when few, otherwise the highest five and the lowest three."""
    vals = [(l, v, number(v)) for l, v in pairs if number(v) is not None]
    if len(vals) <= 8:
        return summarize(pairs)
    vals.sort(key=lambda x: -x[2])
    top = ', '.join(f'{l} ({v})' for l, v, _ in vals[:5])
    low = ', '.join(f'{l} ({v})' for l, v, _ in vals[-3:])
    return f'The highest are {top}; the lowest are {low}.'


def point_before(el, head, body):
    """A heading and a sentence placed before el, read as one key point."""
    h = LH.Element('h4')
    h.text = head
    p = LH.Element('p')
    p.set('class', 'wlead wkeep')
    p.text = body
    el.addprevious(h)
    el.addprevious(p)


def grids(root):
    """Runs of column rows used as a table (short text in every column) read as rows: a row label with its values
    under the header row's names, or, for name and value pairs, one line of who is highest and lowest."""
    rows = root.xpath('.//div[contains(@class,"wcols")][not(ancestor::div[contains(@class,"wcols")])]')
    groups, cur = [], []
    for r in rows:
        cols = r.xpath('./div[contains(@class,"wcol")]')
        cells = [text(c) for c in cols]
        tabular = len(cols) >= 2 and all(len(c) < 45 for c in cells) and not r.xpath('.//p[string-length(normalize-space()) > 60]')
        if tabular and cur and cur[-1][0].getnext() is r:
            cur.append((r, cells))
        else:
            if len(cur) >= 2:
                groups.append(cur)
            cur = [(r, cells)] if tabular else []
    if len(cur) >= 2:
        groups.append(cur)
    for g in groups:
        first = g[0][0]
        anchor = LH.Element('div')
        first.addprevious(anchor)
        cells = [c for _, c in g]
        numeric = lambda x: bool(NUMERIC.match(x.replace(' / ', '').replace('/', '')))
        pairs = [c for c in cells if len(c) == 2 and not numeric(c[0]) and numeric(c[1])]
        if len(pairs) >= 3 and len(pairs) >= len(cells) - 1:
            para(root, anchor, rank_line([(a, b) for a, b in pairs]))
        else:
            head, plain_rows = None, [c for c in cells if all(numeric(x) or not x for x in c)]
            low = lambda h: (h[0].lower() + h[1:]) if h[:2] != h[:2].upper() else h
            for c in cells:
                if not any(numeric(x) for x in c if x):
                    head = c                     # a header row (the last one before the figures counts)
                elif head and len(c) == len(head) and all(numeric(x) or not x for x in c):
                    if len(plain_rows) == 1:     # several unlabeled rows under one header cannot be told apart
                        para(root, anchor, ', '.join(f'{h} {v}' for h, v in zip(head, c) if v) + '.')
                elif head and len(c) == len(head) and not numeric(c[0]):
                    point_before(anchor, c[0], ', '.join(f'{low(h)} {v}' for h, v in zip(head[1:], c[1:]) if v) + '.')
        for r, _ in g:
            r.drop_tree()
        anchor.drop_tree()


def mega_card(c, root):
    """A deal tile that holds a whole slide (several deals run together): its full sentences become points and the
    short deal descriptions one list."""
    descs, ours = [], False
    for p in c.xpath('.//p[contains(@class,"wfine")]'):
        t = re.sub(r'^WHAT IT SHOWS\s*', '', text(p))
        a = p.xpath('./a')
        if a and len(t) < 120 and t == text(a[0]):
            descs.append(t[0].lower() + t[1:])
            ours = ours or 'benchmarkintl.com' in (a[0].get('href') or '')
        elif len(t) > 60 and t[-1] in '.)':
            q = LH.Element('p')
            q.set('class', 'wlead')
            q.text = sentences(t, 1)
            c.addprevious(q)
    if descs:
        head = 'Sales we advised include' if ours else 'Transactions include'
        point_before(c, head, '; '.join(descs[:10]) + (f'; and {len(descs) - 10} more in the full report' if len(descs) > 10 else ''))
    c.drop_tree()


def para(root_el, before, txt):
    p = LH.Element('p')
    p.set('class', 'wsum')
    p.text = txt
    before.addprevious(p)
    return p


def teaser(body, sub=''):
    """(teaser html, what the full section adds) for a section body already in the web vocabulary."""
    root = LH.fragment_fromstring(body or '<p></p>', create_parent='div')
    n_charts = len(root.xpath('.//figure')) + (1 if root.xpath('.//*[contains(@class,"dbar")]') else 0)
    has_quotes = bool(root.xpath('.//blockquote'))
    deals = []
    stats = root.xpath('.//div[contains(@class,"wstats")]')
    stats_html = LH.tostring(stats[0], encoding='unicode') if stats else ''

    # charts, short tables, name lists and figure-with-label pairs become plain lines (class wsum)
    for fig in root.xpath('.//figure'):
        box = (fig.xpath('ancestor::div[contains(@class,"wcard")]') or [fig.getparent()])[-1]
        data = fig.xpath('.//details[contains(@class,"wdata")]//td')
        nums = [n for n in (number(text(c)) for c in data) if n is not None]
        words = text(box).replace(text(fig), '')
        heading = (box.xpath('.//h4') or [box])[0]
        rate = ' pts' in words or bool(re.search(r'\b(rate|yield|utilization|unemployment|growth|margin)\b', text(heading), re.I))
        line = '' if len(nums) > 12 and ('change' in text(heading).lower() or min(nums) < 0 or 'Since ' in words) else chart_line(fig, rate)
        if line:
            para(root, fig, line)
    bars = root.xpath('.//div[contains(@class,"dbar")]')
    if bars:
        vals = []
        for b in bars:
            l, v = b.xpath('.//*[contains(@class,"dbar-l")]'), b.xpath('.//*[contains(@class,"dbar-v")]')
            if l and v and text(l[0]):
                n = re.sub(r'[^\d.\-−]', '', text(v[0])).replace('−', '-')
                try:
                    vals.append((float(n), text(l[0]), text(v[0])))
                except ValueError:
                    pass
        if len(vals) > 8:
            vals.sort(reverse=True)
            top = ', '.join(f'{l} ({v})' for _, l, v in vals[:5])
            low = ', '.join(f'{l} ({v})' for _, l, v in vals[-3:])
            para(root, bars[0], f'The highest are {top}; the lowest are {low}.')
        elif vals:
            para(root, bars[0], summarize([(l, v) for _, l, v in vals]))
    tables = root.xpath('.//table[not(ancestor::details[contains(@class,"wdata")])]')
    n_rows, n_big = 0, 0
    for t in tables:
        d = deals_from(t)
        if d:
            deals += d
            continue
        line = small_table_line(t)
        if line:
            para(root, t.getparent() if 'rtable-wrap' in (t.getparent().get('class') or '') else t, line)
        else:
            n_rows += len(t.xpath('.//tbody/tr'))
            n_big += 1
            names = []
            for r in t.xpath('.//tbody/tr'):
                cs = r.xpath('./td|./th')
                if len(cs) < 2 or not any(text(x) for x in cs[1:]):
                    continue                      # a group heading row
                n = ' '.join(x.strip() for x in cs[0].itertext() if x.strip())
                n = re.sub(r'\s+[A-Z]{1,5}(?:\.[A-Z]{1,2})?$', '', n) if ' ' in n else n
                if n and not n.isupper() and not re.search(r'\d', n) and not re.search(r'\b(median|average)\b', n, re.I):
                    names.append(n)
            if len(names) >= 5:
                wrap = t.getparent() if 'rtable-wrap' in (t.getparent().get('class') or '') else t
                point_before(wrap, f'Companies covered ({len(names)})', ', '.join(names) + '.')
    for c in root.xpath('.//div[contains(@class,"wdeal")]'):
        if len(c.xpath('.//p')) > 7:
            mega_card(c, root)
            continue
        get = lambda x: [text(e) for e in c.xpath(x)]
        target, acq = (get('.//h4') or [''])[0], (get('.//*[contains(@class,"wacq")]') or [''])[0]
        buyer = re.sub(r'^acquired by\s*', '', acq, flags=re.I)
        when = next((m for m in get('.//*[contains(@class,"wmeta")]') if re.search(r'\d{4}', m)), '')
        about = get('.//p[contains(@class,"wfine")]')
        headline = get('.//p[contains(@class,"wfine")]/strong')
        if buyer:
            # the card's own headline when it has one ("Korn Ferry agrees to buy AMS at about 11 times EBITDA")
            if headline:
                line = headline[0]
            elif target and target != buyer:
                line = f'{buyer} acquired {target}'
            else:
                line = f'{buyer} acquired {about[0] if about else "a company"}'
            if when:
                line += f', {when}'
            if not headline and about and target and target != buyer:
                line += f' ({about[0][0].lower() + about[0][1:]})'
            deals.append(line)
        c.drop_tree()
    grids(root)
    for h in root.xpath('.//div[contains(@class,"wcol")]/h4[contains(@class,"wh")]'):
        col = h.getparent()
        nxt = col.getnext()
        if NUMERIC.match(text(h)) and nxt is not None and 'wcol' in (nxt.get('class') or '') and nxt.xpath('./p'):
            # a figure beside its label: a key point of its own
            row = col.getparent()
            fig = LH.Element('h4')
            fig.text = text(h)
            lab = LH.Element('p')
            lab.set('class', 'wlead')
            lab.text = text(nxt.xpath('./p')[0])
            row.addprevious(fig)
            row.addprevious(lab)
            row.drop_tree()
    for n in root.xpath('.//p[contains(@class,"wnum")]'):
        nxt = n.getnext()
        if nxt is not None and nxt.tag == 'p' and not (nxt.get('class') or '') and not re.search(r'\d{4}$', text(nxt)) \
                and not text(nxt).endswith('.'):     # a label, not a sentence that happens to follow the figure
            n.tag, n.attrib['class'] = 'h4', 'wfig-n'
            nxt.set('class', 'wlead')
    for ul in root.xpath('.//ul[contains(@class,"wnames")]'):
        para(root, ul, ', '.join(text(li) for li in ul.xpath('./li')))
        ul.drop_tree()
    for el in root.xpath('.//p[contains(@class,"wnum")]|.//h4[contains(@class,"wh")]'):
        t = text(el)
        nxt = el.getnext()
        if NUMERIC.match(t) and nxt is not None and 'wfine' in (nxt.get('class') or ''):
            label = text(nxt)
            para(root, el, f'{t} {label}' if not re.search(r'\d{4}', label) else f'{t} ({label})')
            el.drop_tree()
        elif el.tag == 'h4' and NUMERIC.match(t):
            el.drop_tree()
    for q in root.xpath('.//blockquote'):
        nxt = q.getnext()
        if nxt is not None and nxt.tag == 'p' and len(text(nxt)) < 160:
            nxt.drop_tree()        # the quote's attribution
    for el in list(root.iter()):
        if el.getparent() is None:
            continue
        cls = el.get('class') or ''
        if el.tag in DROP or DROP_CLASS.search(cls):
            el.drop_tree()

    lead, points, seen = [], [], {sub.lower()} if sub else set()
    pending, context = None, None
    card = lambda el: (el.xpath('ancestor::div[contains(@class,"wcard")]') or [None])[0]
    for el in root.iter('h3', 'h4', 'p', 'li'):
        t = text(el)
        if not t or t.lower() in seen:
            continue
        if el.tag in ('h3', 'h4'):
            h = clean_heading(t)
            if pending is not None and not pending['b']:
                # a heading straight after another: the first one groups the ones that follow in its card
                points.remove(pending)
                context = (pending['raw'], pending['card'])
            if context and context[1] is not None and context[1] is card(el) and context[0] != h:
                h = f'{context[0]}: {h[0].lower() + h[1:] if not h[:2].isupper() else h}'
            elif context and context[1] is not card(el):
                context = None
            pending = {'h': h, 'raw': clean_heading(t), 'b': '', 'card': card(el), 'names': False}
            points.append(pending)
            continue
        if el.tag == 'li' and el.xpath('ancestor::li'):
            continue
        if re.search(r'\b(Chief Executive|CEO|Chair(man|woman)?|President|Founder|CFO)\b', t) and len(t) < 140 and t[-1] not in '.!?':
            continue                              # a quote's attribution
        label, t = caps_label(t)
        if label and el.tag != 'li':
            pending = {'h': label, 'raw': label, 'b': '', 'card': card(el), 'names': False}
            points.append(pending)
        is_sum = 'wsum' in (el.get('class') or '')
        s = t if is_sum or 'wkeep' in (el.get('class') or '') else sentences(t)
        if not is_sum and len(s) < 25 and 'wlead' not in (el.get('class') or ''):
            continue
        seen.add(t.lower())
        if pending is not None and (not pending['b'] or is_sum):
            if pending['b']:
                sentence_ = s[-1:] == '.' and s[:1].isupper()
                pending['b'] += (' ' if pending['b'][-1] in '.!?' else '. ' if sentence_ else ': ') + s
            else:
                pending['b'] = s
            pending['names'] = pending['names'] or is_sum
        elif not points and len(lead) < MAX_LEAD:
            lead.append(s)
        elif is_sum and points:
            points[-1]['b'] += ('. ' if points[-1]['b'] and points[-1]['b'][-1] not in '.!?' else ' ') + s
        else:
            pending = {'h': '', 'raw': '', 'b': s, 'card': card(el), 'names': False}
            points.append(pending)
    points = [p for p in points if p['b'] or len(p['h']) > 40]
    limit = 16 if sum(p['names'] for p in points) > 6 else MAX_POINTS
    points = points[:limit]

    out = [f'<p>{html.escape(x, quote=False)}</p>' for x in lead]
    if stats_html:
        out.append(stats_html)
    if points:
        def point(p):
            b = p['b'] or p['h']
            b = b if b[-1] in '.!?)”' else b + '.'
            if p['h'] and p['b'] and b.lower().startswith('acquired by'):
                return f'<li><strong>{html.escape(p["h"].rstrip("."), quote=False)}</strong>, {html.escape(b[0].lower() + b[1:], quote=False)}</li>'
            head = ''
            if p['h'] and p['b']:
                h = p['h'] if p['h'][-1] in '.!?' else p['h'] + '.'
                head = f'<strong>{html.escape(h, quote=False)}</strong> '
            return f'<li>{head}{html.escape(b, quote=False)}</li>'
        out.append('<ul class="wpoints">' + ''.join(point(p) for p in points) + '</ul>')
    if deals:
        more = len(deals) - MAX_DEALS
        out.append('<p class="wdeals-h"><strong>Transactions in this section</strong></p><ul class="wdeals">'
                   + ''.join(f'<li>{html.escape(d, quote=False)}</li>' for d in deals[:MAX_DEALS])
                   + (f'<li>and {more} more in the full report</li>' if more > 0 else '') + '</ul>')
    adds = []
    if n_charts:
        adds.append('the charts')
    if deals:
        adds.append('the terms and multiples for each deal')
    if n_big:
        adds.append('the full table' if n_big == 1 else 'the full tables')
    if has_quotes:
        adds.append('the quotes')
    return '\n'.join(out), adds

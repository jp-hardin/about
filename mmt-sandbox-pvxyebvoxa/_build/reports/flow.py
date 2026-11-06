# Turns a page body laid out like its deck page (rows, columns and cards side by side) into one reading column in the
# site's original report style: headings, paragraphs, lists, call-outs, figure strips, quotes, tables and charts in
# reading order. Groups of small cards (deal cards, logos) stay in a grid; everything else stacks.
import copy, re
from lxml import html as LH, etree


def cls(el):
    return (el.get('class') or '').split()


def has(el, c):
    return c in cls(el)


def unwrap(el):
    """Replaces el with its children, keeping its text and tail."""
    parent = el.getparent()
    if parent is None:
        return
    i = parent.index(el)
    kids = list(el)
    if el.text and el.text.strip():
        if i > 0:
            prev = parent[i - 1]
            prev.tail = (prev.tail or '') + el.text
        else:
            parent.text = (parent.text or '') + el.text
    for k in kids:
        parent.insert(i, k)
        i += 1
    if el.tail:
        if kids:
            kids[-1].tail = (kids[-1].tail or '') + el.tail
        elif i > 0:
            parent[i - 1].tail = (parent[i - 1].tail or '') + el.tail
        else:
            parent.text = (parent.text or '') + el.tail
    parent.remove(el)


def text(el):
    return ' '.join(''.join(el.itertext()).split())


def in_tiles(el):
    p = el.getparent()
    while p is not None:
        if has(p, 'drow--tiles') or has(p, 'drow--tight') or p.tag in ('td', 'th'):
            return True
        p = p.getparent()
    return False


def stats_only(card):
    """A card that holds only figures and their labels (and perhaps a heading) reads as a figure strip."""
    nums = card.xpath('.//p[contains(concat(" ", @class, " "), " dnum ")]')
    if len(nums) < 2:
        return False
    other = [p for p in card.xpath('.//p|.//h3|.//blockquote|.//li')
             if not has(p, 'dnum') and not has(p, 'dlabel') and len(text(p)) > 160]
    return len(other) <= 1


def figure_strip(card):
    """Pairs each figure with the text after it: <div class="rstats"> of <div class="rstat">."""
    items, head, notes = [], [], []
    blocks = [b for b in card.iter() if b.tag in ('p', 'h3', 'h4') and b is not card]
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if has(b, 'dnum'):
            label = []
            j = i + 1
            while j < len(blocks) and not has(blocks[j], 'dnum'):
                if label and (len(text(blocks[j])) > 160 or has(blocks[j], 'fine')):
                    notes.append(blocks[j])
                else:
                    label.append(blocks[j])
                j += 1
            items.append((b, label))
            i = j
            continue
        if not items:
            head.append(b)
        i += 1
    out = etree.Element('div')
    out.set('class', 'rstats-wrap')
    for h in head:
        e = etree.SubElement(out, 'p')
        e.set('class', 'rstats-head')
        e.text = text(h)
    strip = etree.SubElement(out, 'div')
    strip.set('class', 'rstats')
    for num, label in items:
        st = etree.SubElement(strip, 'div')
        st.set('class', 'rstat')
        n = etree.SubElement(st, 'div')
        n.set('class', 'stat-num')
        n.text = text(num)
        lab = etree.SubElement(st, 'div')
        lab.set('class', 'rstat-label')
        for k, l in enumerate(label):
            l.tag = 'span'
            l.attrib.pop('class', None)
            if k:
                l.text = ' ' + (l.text or '')
            lab.append(l)
    for nt in notes:
        nt.set('class', 'rstats-fine' if has(nt, 'fine') else 'rstats-note')
        nt.tag = 'p'
        out.append(nt)
    return out


def tables(root):
    """Rows laid out as columns under a row of column headings (a deal list) become a real table."""
    def cols(row):
        return row.xpath('./div[contains(concat(" ", @class, " "), " dcol ")]')

    def heading_row(row):
        cs = cols(row)
        return len(cs) >= 3 and all(0 < len(text(c)) <= 32 and text(c) == text(c).upper() for c in cs)
    for head in root.xpath('.//div[@class="drow"]'):
        if head.getparent() is None or not heading_row(head):
            continue
        n_cols = len(cols(head))
        rows, cur = [], head.getnext()
        while cur is not None and cur.tag == 'div' and has(cur, 'drow') and len(cols(cur)) == n_cols:
            rows.append(cur)
            cur = cur.getnext()
        if len(rows) < 2:
            continue
        names = [text(c) for c in cols(head)]
        tbl = LH.fragment_fromstring('<div class="rtable-wrap"><table class="rtable rtable--flow"><thead><tr></tr></thead><tbody></tbody></table></div>')
        tr = tbl.find('.//thead/tr')
        for nm in names:
            th = etree.SubElement(tr, 'th')
            th.set('scope', 'col')
            th.text = nm.capitalize() if nm.isupper() else nm
        body = tbl.find('.//tbody')
        for r in rows:
            row = etree.SubElement(body, 'tr')
            for nm, c in zip(names, cols(r)):
                td = etree.SubElement(row, 'td')
                td.set('data-label', nm.capitalize() if nm.isupper() else nm)
                td.text = c.text
                for k in list(c):
                    td.append(k)
                for d in td.xpath('.//div[contains(concat(" ", @class, " "), " dtx ") or contains(concat(" ", @class, " "), " dcard ") or contains(concat(" ", @class, " "), " dcol ")]'):
                    unwrap(d)
        # column widths follow how much each column holds, as in the original report tables
        lens = [[len(text(td)) for td in tr.findall('td')] for tr in body.findall('tr')]
        w = [max(len(nm) * 0.75, max(len(x) for x in nm.split()) * 1.3, (sum(r[k] for r in lens) / len(lens)) ** 0.7, 9) for k, nm in enumerate(names)]
        cg = etree.Element('colgroup')
        for x in w:
            etree.SubElement(cg, 'col').set('style', f'width:{x / sum(w) * 100:.1f}%')
        tbl.find('.//table').insert(0, cg)
        tbl.tail = rows[-1].tail
        head.getparent().replace(head, tbl)
        for r in rows:
            r.getparent().remove(r)


def flow(body):
    if not body.strip():
        return body
    root = LH.fragment_fromstring(body, create_parent='div')
    tables(root)

    # 0. A grid of cards that hold real reading (perspectives, articles, deal write-ups) stacks; each card becomes a
    #    titled block. Grids of short cards (names, logos, figures) stay a grid.
    for row in root.xpath('.//div[contains(concat(" ", @class, " "), " drow--tiles ")]'):
        # a long dark card (a figure panel or a message) leaves the grid and goes ahead of it
        for card in row.xpath('./div/div[contains(concat(" ", @class, " "), " dcard--dark ")]'):
            if len(text(card)) > 160:
                col = card.getparent()
                col.remove(card)
                card.tail = None
                row.addprevious(card)
                if not len(col) and not text(col):
                    row.remove(col)
        cols = row.xpath('./div[contains(concat(" ", @class, " "), " dcol ")]')
        cards = row.xpath('./div/div[contains(concat(" ", @class, " "), " dcard ")]')
        units, limit = (cards, 220) if cards else (cols, 160)
        if units and max(len(text(c)) for c in units) > limit:
            row.set('class', 'drow')
            for card in row.xpath('.//div[contains(concat(" ", @class, " "), " dcard ")]'):
                if not has(card, 'dcard--dark'):
                    card.set('class', 'rsub')
                    card.attrib.pop('style', None)

    # 1. Dark cards: a strip of figures, or a call-out.
    for card in root.xpath('.//div[contains(concat(" ", @class, " "), " dcard--dark ")]'):
        if in_tiles(card):
            continue
        if stats_only(card):
            strip = figure_strip(card)
            strip.tail = card.tail
            card.getparent().replace(card, strip)
        else:
            card.set('class', 'rnote')
            card.attrib.pop('style', None)

    # 2. Other cards outside a tile grid add nothing but a box: their contents join the column.
    for card in root.xpath('.//div[contains(concat(" ", @class, " "), " dcard ")]'):
        if not in_tiles(card):
            unwrap(card)

    # 3. Rows and columns stack, except tile grids and tight pairs (a figure beside its label, a logo beside a name).
    for row in root.xpath('.//div[contains(concat(" ", @class, " "), " drow ")]'):
        if has(row, 'drow--tiles') or has(row, 'drow--tight'):
            continue
        for col in row.xpath('./div[contains(concat(" ", @class, " "), " dcol ")]'):
            unwrap(col)
        unwrap(row)
    for tx in root.xpath('.//div[@class="dtx"]'):
        if not in_tiles(tx):
            unwrap(tx)

    # 4. Loose figures with their labels, one after another, become a strip as well.
    nums = [p for p in root.xpath('.//p[contains(concat(" ", @class, " "), " dnum ")]')]
    for p in nums:
        parent = p.getparent()
        if parent is None or in_tiles(p) or has(parent, 'dtx') or parent.tag != 'div' and parent is not root:
            continue
        run, cur = [], p
        while cur is not None and cur.tag == 'p' and (has(cur, 'dnum') or (run and not has(cur, 'dlabel') and len(text(cur)) < 160 and not has(run[-1], 'dlabel') and has(run[-1], 'dnum'))):
            run.append(cur)
            cur = cur.getnext()
        if sum(1 for r in run if has(r, 'dnum')) >= 2:
            box = etree.Element('div')
            for r in run:
                box.append(copy.deepcopy(r))
            strip = figure_strip(box)
            strip.tail = run[-1].tail
            parent.replace(run[0], strip)
            for r in run[1:]:
                parent.remove(r)

    for dl in root.xpath('.//div[contains(concat(" ", @class, " "), " dline ")]'):
        cells = list(dl)
        if len(cells) < 2 or not all(has(c, 'dline-c--num') for c in cells):
            continue
        labels, cur = [], dl.getnext()
        while cur is not None and cur.tag == 'p' and not cls(cur) and len(labels) < len(cells):
            labels.append(cur)
            cur = cur.getnext()
        if len(labels) != len(cells):
            continue
        box = etree.Element('div')
        for c, l in zip(cells, labels):
            num = etree.SubElement(box, 'p')
            num.set('class', 'dnum')
            num.text = text(c)
            box.append(copy.deepcopy(l))
        strip = figure_strip(box)
        strip.set('class', 'rstats-wrap rstats-wrap--light')
        strip.tail = labels[-1].tail
        parent = dl.getparent()
        parent.replace(dl, strip)
        for l in labels:
            l.getparent().remove(l)

    # 5. Text roles in the original report style.
    for el in root.iter():
        c = cls(el)
        if el.tag == 'p' and 'dlabel' in c and not in_tiles(el):
            el.tag = 'h4'
            el.set('class', 'rh4')
        elif el.tag == 'h3' and 'dh' in c and not in_tiles(el):
            el.set('class', 'rh3')
        elif el.tag == 'p' and 'dlead' in c:
            el.set('class', 'rlead')
    for q in root.xpath('.//blockquote[contains(concat(" ", @class, " "), " dquote ")]'):
        if in_tiles(q):
            continue
        fig = etree.Element('figure')
        fig.set('class', 'rquote')
        fig.tail = q.tail
        q.tail = None
        q.attrib.pop('class', None)
        q.getparent().replace(q, fig)
        fig.append(q)
        inner = (q.text or '') + ''.join(LH.tostring(k, encoding='unicode') for k in q)
        inner = re.sub(r'</?em>', '', inner)
        k = inner.rfind('\u201d')
        if 0 < k < len(inner) - 3 and len(re.sub(r'<[^>]+>', '', inner[k + 1:]).strip()) < 160:
            body, who = inner[:k + 1], inner[k + 1:].strip()
            nq = LH.fragment_fromstring(body, create_parent='blockquote')
            fig.replace(q, nq)
            cap = LH.fragment_fromstring(who, create_parent='figcaption')
            fig.append(cap)
            continue
        nxt = fig.getnext()
        if nxt is not None and nxt.tag == 'p' and len(text(nxt)) < 260 and not cls(nxt):
            cap = etree.SubElement(fig, 'figcaption')
            cap.text, cap.tail = nxt.text, None
            for k in list(nxt):
                cap.append(k)
            fig.tail = (fig.tail or '') + (nxt.tail or '')
            nxt.getparent().remove(nxt)

    out = (root.text or '') + ''.join(LH.tostring(k, encoding='unicode') for k in root)
    return re.sub(r'\n{2,}', '\n', out)

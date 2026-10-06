# -*- coding: utf-8 -*-
# Shared content model for the Consumer Q4 2026 sector report.
# Reads content.md and turns it into sections of simple blocks that web.py and pdf.py both render.
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SLUG = 'consumer-q4-2026'
TITLE = 'Consumer Q4 2026 M&A Sector Report'
AS_OF = 'October 5, 2026'
BYLINE = 'October 2026 - Jared Hardin | Managing Director | Benchmark International'
NOTE = (f'Information as of {AS_OF}. Public-company multiples are reference points, '
        'and a private company&#39;s price depends on the business itself.')

# Headline figures shown under the page title and on the PDF cover. Each one appears in content.md.
FIGS = [
    ('$120B+', 'Committed by strategic acquirers to three consumer transactions since November 2025'),
    ('75%', 'Share of US private equity buyouts in the second quarter of 2026 that were add-on acquisitions'),
    ('$6.38', 'Price of a gallon of diesel on September 28, against about $3.75 a year earlier'),
    ('9x to 17x', 'EBITDA multiples of public food, consumer staples and restaurant companies'),
]

# The four focus segments become their own sections. Stat bands and illustrations are keyed by section id.
SECTION_IDS = {
    'Overview': 'overview',
    'Where We Focus': 'focus',
    'Food & Beverage': 'food-beverage',
    'Consumer Brands & Products': 'consumer-brands',
    'Foodservice & Distribution': 'foodservice',
    'Consumer Services & Retail': 'consumer-services',
    'Selected Transactions': 'transactions',
    "What We're Seeing in Consumer": 'market',
    'What Buyers Value': 'value',
    'Who Is Buying': 'buyers',
    'For Owners and Their Advisors': 'owners',
    'Sources': 'sources',
}
SEGMENTS = ['food-beverage', 'consumer-brands', 'foodservice', 'consumer-services']
BANDS = {
    'food-beverage': ('food', 'Line illustration of a bottle and an ear of wheat', [
        ('42,708', 'Food and beverage processing establishments in the United States'),
        ('21.3%', 'Private label share of dollar sales in 2025'),
        ('14.6x', 'Multiple of operating income Sysco stated for Jetro Restaurant Depot')]),
    'consumer-brands': ('brands', 'Line illustration of a shopping bag and a price tag', [
        ('7%', 'Growth in both prestige and mass beauty sales in the first half of 2026'),
        ('17.1%', 'E-commerce share of retail sales in the second quarter of 2026'),
        ('12.5%', 'Section 301 tariff on goods from China and Vietnam since July 24')]),
    'foodservice': ('service', 'Line illustration of a delivery truck', [
        ('$1.55T', 'Restaurant and foodservice sales forecast for 2026'),
        ('2.0%', 'Growth in equipment and supplies sales through manufacturers&#39; agents in the second quarter'),
        ('91%', 'Equipment manufacturers reporting negative effects from tariffs')]),
    'consumer-services': ('store', 'Line illustration of a storefront with an awning', [
        ('$3.1B', 'Enterprise value of the Mister Car Wash take-private'),
        ('23.1%', 'Record share of collision claims declared total losses'),
        ('$83.5B', 'US equipment rental revenue forecast for 2026')]),
}

# Public-market chart (NYU Stern, Damodaran, January 2026). Values match the figures quoted in content.md.
CHART = [('Restaurant / dining', 17.49), ('Beverage (soft)', 16.90), ('Household products', 13.17),
         ('Food wholesalers', 11.08), ('Food processing', 10.01), ('Retail (grocery and food)', 8.94),
         ('Beverage (alcoholic)', 8.61)]
CHART_REF = ('Total US public market', 19.73)
CHART_MAX = 22.0
CHART_CAPTION = 'NYU Stern (Damodaran), enterprise value multiples by sector, US public companies, data as of January 2026'

CONTACT = dict(name='Jared Hardin', role='Managing Director', firm='Benchmark International',
               phone='813-771-6675', tel='8137716675', email='j.hardin@benchmarkintl.com')


def esc(s):
    return html.escape(s, quote=False)


_LINK = re.compile(r'\[([^\]]+)\]\((https?://[^\s)]+)\)')


def _bold(s):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', esc(s))


def inline(s):
    """Markdown inline text to HTML: links, bold, escaping."""
    out, pos = [], 0
    for m in _LINK.finditer(s):
        out.append(_bold(s[pos:m.start()]))
        out.append(f'<a href="{html.escape(m.group(2), quote=True)}">{_bold(m.group(1))}</a>')
        pos = m.end()
    out.append(_bold(s[pos:]))
    return ''.join(out)


def plain(h):
    return html.unescape(re.sub(r'<[^>]+>', '', h)).strip()


def parse(md):
    """Returns a list of blocks: ('h2'|'h3'|'label', text), ('p', html), ('ul', [html]),
    ('table', head, rows), ('chart',)."""
    blocks, lines, i = [], md.split('\n'), 0
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1
        elif l.startswith('### '):
            blocks.append(('h3', l[4:].strip())); i += 1
        elif l.startswith('## '):
            blocks.append(('h2', l[3:].strip())); i += 1
        elif l.strip() == '{{chart}}':
            blocks.append(('chart',)); i += 1
        elif l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip()[1:-1].split('|')]); i += 1
            head, body = rows[0], [r for r in rows[2:]]
            n = len(head)
            assert all(len(r) == n for r in body), ('ragged table', head)
            blocks.append(('table', [inline(c) for c in head], [[inline(c) for c in r] for r in body]))
        elif l[:2] in ('- ', '* '):
            items = []
            while i < len(lines) and lines[i][:2] in ('- ', '* '):
                items.append(inline(lines[i][2:].strip())); i += 1
            if blocks and blocks[-1][0] == 'ul':
                blocks[-1][1].extend(items)  # lists split only by a blank line read as one list
            else:
                blocks.append(('ul', items))
        elif re.fullmatch(r'\*\*[^*]+\*\*', l.strip()):
            blocks.append(('label', l.strip()[2:-2])); i += 1
        else:
            blocks.append(('p', inline(l.strip()))); i += 1
    return blocks


def sections():
    """Groups the blocks into the twelve report sections, in document order."""
    blocks = parse(open(os.path.join(ROOT, 'content.md'), encoding='utf-8').read())
    secs, in_focus = [], False
    for b in blocks:
        if b[0] == 'h2' or (b[0] == 'h3' and in_focus and b[1] in SECTION_IDS):
            if b[0] == 'h2':
                in_focus = b[1] == 'Where We Focus'
            secs.append({'id': SECTION_IDS[b[1]], 'title': b[1], 'blocks': []})
        else:
            secs[-1]['blocks'].append(b)
    assert [s['id'] for s in secs] == list(SECTION_IDS.values()), [s['id'] for s in secs]
    return secs


def col_widths(head, rows, head_room=0.95):
    """Column widths in percent, weighted by how much text each column carries.
    head_room is the percent of table width allowed per character of a header word."""
    n = len(head); w = []
    for c in range(n):
        cells = [plain(r[c]) for r in rows] + [plain(head[c])]
        longest_word = max((len(x) for cell in cells for x in cell.split()), default=4)
        # Headers are set in spaced capitals, so a header word needs about half again its length.
        head_word = max((len(x) for x in plain(head[c]).split()), default=4) * 1.55
        avg = sum(len(x) for x in cells) / len(cells)
        w.append(max(min(avg, 70), longest_word * 1.15, head_word, 9))
    tot = sum(w)
    pct = [x / tot * 100 for x in w]
    # A column is never narrower than its header needs, and the wider columns give up the difference.
    floor = [max((len(x) for x in plain(head[c]).split()), default=4) * head_room + 2.2 for c in range(n)]
    short = sum(max(f - p, 0) for f, p in zip(floor, pct))
    spare = sum(max(p - f, 0) for f, p in zip(floor, pct))
    if short and spare > short:
        pct = [f if p < f else p - (p - f) * short / spare for f, p in zip(floor, pct)]
    return pct


def lead_text():
    """First paragraph of the Overview, used as the opening statement."""
    return next(b[1] for b in sections()[0]['blocks'] if b[0] == 'p')

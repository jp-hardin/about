# Builds the downloadable PDF from content.md in the print brand (Cinzel, Newsreader, Quicksand; gold and charcoal).
# Usage: python3 pdf.py   (needs Playwright with Chromium: pip install playwright && playwright install chromium)
# Fonts are bundled in fonts/ (SIL Open Font License) so the build needs no network access.
import os, re, sys, asyncio
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ROOT, '..', '..', '..'))
sys.path.insert(0, ROOT)
import report as R

PUBLIC = R.SLUG.rsplit('-', 2)[0] + '-industry-report-' + '-'.join(R.SLUG.rsplit('-', 2)[1:])
OUT = os.path.join(SITE, 'insights', f'{PUBLIC}.pdf')
AST = os.path.relpath(os.path.join(SITE, 'assets', 'img'), ROOT)
RUN = 'CONSUMER \\00B7  Q4 2026'
# Sections that continue on the same page as the one before them. Every other section starts a new page.
FLOW_ON = {'focus', 'consumer-brands', 'foodservice', 'consumer-services', 'value', 'buyers', 'owners'}

F = [('Cinzel', 'cinzel', 400, 'normal'), ('Cinzel', 'cinzel', 500, 'normal')]
F += [('Newsreader', 'newsreader', w, s) for w in (500, 600) for s in ('normal', 'italic')]
F += [('Quicksand', 'quicksand', w, 'normal') for w in (400, 500, 600, 700)]
FACE = ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};font-style:{s};src:url('fonts/{f}-latin-{w}-{s}.woff2') format('woff2')}}" for n, f, w, s in F)

CSS = FACE + '''
@page { size: 8.5in 11in; margin: 0.95in 0.5in 0.9in;
  @top-right { content: "''' + RUN + '''"; font-family: 'Cinzel', Georgia, serif; font-size: 9pt; letter-spacing: 0.8px; color: #6D7681; vertical-align: bottom; padding-bottom: 20px; }
  @bottom-center { content: "BENCHMARKINTL.COM"; font-family: 'Quicksand', sans-serif; font-weight: 700; font-size: 6.4pt; letter-spacing: 3.6px; color: #333333; vertical-align: top; padding-top: 30px; }
  @bottom-right { content: counter(page, decimal-leading-zero); font-family: 'Quicksand', sans-serif; font-weight: 700; font-size: 6.4pt; letter-spacing: 2px; color: #333333; vertical-align: top; padding-top: 30px; }
}
@page full { margin: 0; @top-right { content: none } @bottom-center { content: none } @bottom-right { content: none } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: 'Quicksand', 'Avenir Next', 'Segoe UI', sans-serif; font-size: 11.8px; line-height: 19px; letter-spacing: 0.3px; color: #333333; }
a { color: #8C6239; text-decoration-thickness: 0.5px; text-underline-offset: 2px; }
p { margin: 0 0 11px; orphans: 3; widows: 3; }
strong { font-weight: 700; color: #262626; }
.serif { font-family: 'Newsreader', Georgia, serif; }
.cinzel { font-family: 'Cinzel', Georgia, serif; }

.full { page: full; position: relative; width: 816px; height: 1056px; overflow: hidden; break-after: page; font-size: 12.2px; line-height: 20px; letter-spacing: 0.4px; }
.full .knot { position: absolute; left: 310px; top: 600px; width: 506px; height: 718px; opacity: 0.3; }
.foot { position: absolute; left: 0; bottom: 38px; width: 816px; text-align: center; font-weight: 700; font-size: 8.5px; line-height: 12px; letter-spacing: 3.6px; }
.fig { display: flex; flex-direction: column; gap: 4px; }
.fig b { font-family: 'Newsreader', Georgia, serif; font-weight: 600; font-size: 28px; line-height: 32px; letter-spacing: 0; color: #B68757; }
.fig span { font-size: 10.6px; line-height: 14.5px; letter-spacing: 0.3px; }
.eye { font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 2.4px; text-transform: uppercase; }
h2 { margin: 0; font-family: 'Newsreader', Georgia, serif; font-weight: 600; font-size: 23px; line-height: 29px; letter-spacing: 0; color: #B68757; }
h3 { margin: 18px 0 9px; font-family: 'Newsreader', Georgia, serif; font-weight: 600; font-size: 16.5px; line-height: 22px; letter-spacing: 0; color: #B68757; break-after: avoid; }
h4 { margin: 14px 0 6px; font-weight: 700; font-size: 9px; line-height: 14px; letter-spacing: 1.6px; text-transform: uppercase; break-after: avoid; }

.sec { break-before: page; }
.sec.on { break-before: auto; margin-top: 30px; }
.sh { display: flex; align-items: baseline; gap: 16px; padding-bottom: 9px; margin-bottom: 14px; border-bottom: 1px solid #B68757; break-after: avoid; }
.sh .n { font-family: 'Newsreader', Georgia, serif; font-weight: 500; font-size: 23px; line-height: 29px; color: #C9C2B8; }
.cols { column-count: 2; column-gap: 30px; text-align: justify; hyphens: auto; margin-bottom: 4px; }
.cols h3:first-child { margin-top: 0; }
.one { text-align: justify; hyphens: auto; }
ul { list-style: none; margin: 0 0 11px; padding: 0; }
li { position: relative; padding: 0 0 0 15px; margin: 0 0 9px; break-inside: avoid; }
li::before { content: ''; position: absolute; left: 0; top: 7px; width: 6px; height: 6px; background: #B68757; }

.band { display: flex; align-items: center; margin: 4px 0 16px; background: #2E2E2E; color: #FFFFFF; break-inside: avoid; }
.band .cells { flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 18px; padding: 0 8px 0 20px; }
.band .fig span { color: #FFFFFF; }
.band img { display: block; width: 236px; height: 112px; }

table { width: 100%; border-collapse: collapse; table-layout: fixed; margin: 6px 0 16px; font-size: 10.4px; line-height: 14.6px; letter-spacing: 0.15px; }
thead th { text-align: left; vertical-align: bottom; padding: 0 12px 6px 0; border-bottom: 2px solid #B68757; font-weight: 700; font-size: 8.2px; line-height: 12px; letter-spacing: 1.4px; text-transform: uppercase; }
tbody th, tbody td { text-align: left; vertical-align: top; padding: 5px 12px 5px 0; border-bottom: 1px solid #D9D3CA; font-weight: 400; overflow-wrap: break-word; }
tbody th { font-weight: 700; }
tbody th a { font-weight: 700; }
tr { break-inside: avoid; }
table.keep { break-inside: avoid; }
thead { display: table-header-group; }

.chart { margin: 8px 0 16px; padding: 16px 20px 12px; background: #F7F4EF; border-top: 2px solid #B68757; break-inside: avoid; }
.crow { display: grid; grid-template-columns: 190px 1fr; align-items: center; column-gap: 12px; }
.crow .cl { font-weight: 700; font-size: 10.8px; }
.ct { position: relative; height: 24px; margin-right: 46px; }
.ct i { position: absolute; display: block; }
.ct .bar { left: 0; top: 6px; height: 12px; background: #B68757; }
.ct .ref { top: 0; bottom: 0; border-left: 1px dashed #6D7681; }
.ct b { position: absolute; top: 2px; padding-left: 6px; font-size: 10.4px; font-weight: 700; }
.chart .key { margin: 8px 0 0; font-size: 9.6px; line-height: 14px; color: #5A5A5A; }
.chart .key i { display: inline-block; height: 11px; border-left: 1px dashed #6D7681; margin-right: 7px; vertical-align: -2px; }

.sources { font-size: 9.6px; line-height: 14.2px; letter-spacing: 0.1px; }
.sources .cols { text-align: left; hyphens: manual; }
.sources li { margin-bottom: 6px; padding-left: 12px; }
.sources li::before { top: 5px; width: 5px; height: 5px; }
'''


def table(head, rows):
    cols = ''.join(f'<col style="width:{w:.1f}%">' for w in R.col_widths(head, rows))
    keep = ' class="keep"' if len(rows) <= 9 else ''      # short tables stay on one page
    o = [f'<table{keep}><colgroup>{cols}</colgroup><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr></thead><tbody>']
    for r in rows:
        o.append('<tr>' + ''.join((f'<th>{c}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(r)) + '</tr>')
    o.append('</tbody></table>')
    return ''.join(o)


def chart():
    pc = lambda v: f'{v / R.CHART_MAX * 100:.2f}%'
    label, ref = R.CHART_REF
    rows = ''.join(f'<div class="crow"><div class="cl">{R.esc(n)}</div><div class="ct"><i class="ref" style="left:{pc(ref)}"></i>'
                   f'<i class="bar" style="width:{pc(v)}"></i><b style="left:{pc(v)}">{v:.1f}x</b></div></div>' for n, v in R.CHART)
    return (f'<div class="chart">{rows}<p class="key"><i></i>{R.esc(label)}, {ref:.1f}x. '
            f'{R.esc(R.CHART_CAPTION)}.</p></div>')


def figs(items):
    return ''.join(f'<div class="fig"><b>{a}</b><span>{b}</span></div>' for a, b in items)


def band(sid):
    icon, alt, items = R.BANDS[sid]
    return f'<div class="band"><div class="cells">{figs(items)}</div><img src="art/{icon}.svg" alt="{alt}"></div>'


def render(sec):
    """Text runs are set in two columns; tables, bands and the chart span the full width."""
    sid, out, run, seen_p = sec['id'], [], [], False

    def flush():
        if run:
            n = sum(len(R.plain(x)) for x in run)
            out.append(f'<div class="{"cols" if n > 520 else "one"}">{"".join(run)}</div>')
            run.clear()

    for b in sec['blocks']:
        k = b[0]
        if k == 'p':
            if sid == 'overview' and not seen_p:
                seen_p = True      # the opening paragraph is printed on the cover as the quarter in brief
                continue
            run.append(f'<p>{b[1]}</p>')
            if not seen_p and sid in R.BANDS:
                flush(); out.append(band(sid))
            seen_p = True
        elif k == 'h3':
            flush(); out.append(f'<h3>{R.esc(b[1])}</h3>')
        elif k == 'label':
            run.append(f'<h4>{R.esc(b[1])}</h4>')
        elif k == 'ul':
            run.append('<ul>' + ''.join(f'<li>{x}</li>' for x in b[1]) + '</ul>')
        elif k == 'table':
            flush(); out.append(table(b[1], b[2]))
        elif k == 'chart':
            flush(); out.append(chart())
    flush()
    return ''.join(out)


C = R.CONTACT
cover = f'''<div class="full">
<img class="knot" src="art/knot.png" alt="">
<img src="art/cover.svg" alt="Four line illustrations: a bottle and an ear of wheat, a shopping bag, a delivery truck and a storefront" style="position: absolute; left: 0; top: 0; width: 816px; height: 590px">
<img src="{AST}/brand/benchmark-logo-white.png" alt="Benchmark International" style="position: absolute; left: 293px; top: 42px; width: 230px">
<div style="position: absolute; left: 48px; top: 334px; width: 720px; display: grid; grid-template-columns: repeat(4, 1fr); text-align: center; color: #FFFFFF; font-weight: 700; font-size: 8px; line-height: 14px; letter-spacing: 2px; text-transform: uppercase">
<div>Food &amp;<br>Beverage</div><div>Consumer Brands<br>&amp; Products</div><div>Foodservice &amp;<br>Distribution</div><div>Consumer Services<br>&amp; Retail</div>
</div>
<div style="position: absolute; left: 48px; top: 400px; width: 720px; color: #FFFFFF">
<h1 class="cinzel" style="margin: 0; font-weight: 400; font-size: 46px; line-height: 54px; letter-spacing: 2px">CONSUMER</h1>
<div style="height: 1px; background: #B68757; margin: 13px 0 11px"></div>
<div class="serif" style="font-style: italic; font-weight: 600; font-size: 24px; line-height: 31px; letter-spacing: 0">Q4 2026 M&amp;A Sector Report</div>
</div>
<div data-fit="398" style="position: absolute; left: 48px; top: 606px; width: 720px; height: 398px; display: flex; flex-direction: column; gap: 9px">
<div class="eye" style="letter-spacing: 2px">{R.esc(R.BYLINE)}</div>
<h2 style="font-size: 21px; line-height: 27px">The quarter in brief</h2>
<p style="margin: 0; text-align: justify; font-size: 11.6px; line-height: 18.6px">{R.lead_text()}</p>
<div style="display: grid; grid-template-columns: repeat(4, 1fr); column-gap: 22px; padding: 11px 0 12px; border-top: 1px solid #B68757; border-bottom: 1px solid #B68757">{figs(R.FIGS)}</div>
<div style="font-size: 10px; line-height: 14px; letter-spacing: 0.2px">{R.NOTE}</div>
</div>
<div class="foot">BENCHMARKINTL.COM</div>
</div>'''

OFFICES = [('AMERICAS', '4030 West Boy Scout Blvd.', 'Suite 500, Tampa, FL 33607', '+1 813 898 2350', 'US@BENCHMARKINTL.COM'),
           ('EUROPE', 'One New Bailey, 4 Stanley St.', 'Manchester, M3 5JL', '+44 (0) 161 359 4400', 'UK@BENCHMARKINTL.COM'),
           ('AFRICA', 'Airport Office Park, Freight Rd., Ground Floor', 'Runway 01, Cape Town Airport, 7525', '+27 (0) 21 300 2055', 'AFRICA@BENCHMARKINTL.COM')]
offices = ''.join(
    f'<div style="display: flex; flex-direction: column; align-items: center"><div class="cinzel" style="font-size: 23px; line-height: 34px; letter-spacing: 4px; margin-bottom: 6px">{a}</div>'
    f'<div>{b}</div><div>{c}</div><div>{d}</div><a href="mailto:{m}" style="margin-top: 4px; color: #C99A68; font-weight: 700; font-size: 8.5px; letter-spacing: 2px">{m}</a></div>'
    for a, b, c, d, m in OFFICES)
contact = f'''<div class="full" style="break-before: page">
<img class="knot" src="art/knot.png" alt="">
<div style="position: absolute; left: 0; top: 40px; width: 432px; height: 1px; background: #6D7681"></div>
<div class="cinzel" style="position: absolute; right: 48px; top: 30px; font-size: 12px; line-height: 20px; letter-spacing: 0.8px; color: #6D7681">CONSUMER &middot; Q4 2026</div>
<div style="position: absolute; left: 48px; top: 250px; width: 720px; display: flex; flex-direction: column; gap: 20px">
<div class="eye">Benchmark International Mid-Market</div>
<h2>Considering a transaction in consumer?</h2>
<p style="margin: 0; max-width: 560px">Our first step is always a confidential conversation exploring your goals, your company and your options.</p>
<div style="margin-top: 14px; display: flex; align-items: center; gap: 22px; padding: 22px 0; border-top: 1px solid #B68757; border-bottom: 1px solid #B68757">
<img src="{AST}/team/jared-hardin.jpg" alt="{C["name"]}" style="display: block; width: 92px; height: 92px; border-radius: 50%; object-fit: cover">
<div style="display: flex; flex-direction: column; gap: 2px">
<div style="font-weight: 700; font-size: 12px; line-height: 20px; letter-spacing: 2.6px">{C["name"].upper()}</div>
<div>{C["role"]}</div><div>{C["firm"]}</div><div>{C["phone"]}</div><div><a href="mailto:{C["email"]}">{C["email"]}</a></div>
</div>
</div>
</div>
<div style="position: absolute; left: 0; top: 839px; width: 816px; height: 217px; background: #303030; color: #FFFFFF">
<div style="position: absolute; left: 0; top: 26px; width: 816px; text-align: center; font-weight: 700; font-size: 10px; line-height: 14px; letter-spacing: 4px; color: #B68757">HEADQUARTERS</div>
<div style="position: absolute; left: 48px; top: 52px; width: 720px; height: 1px; background: #B68757"></div>
<div style="position: absolute; left: 48px; top: 70px; width: 720px; display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 24px; text-align: center; font-size: 9.5px; line-height: 16px; letter-spacing: 0.5px">{offices}</div>
</div>
</div>'''

secs = R.sections()
body = [cover]
for i, s in enumerate(secs, 1):
    cls = 'sec' + (' on' if s['id'] in FLOW_ON else '') + (' sources' if s['id'] == 'sources' else '')
    eye = '<div class="eye">Where We Focus</div>' if s['id'] in R.SEGMENTS else ''
    if s['id'] == 'sources':
        body.append(contact)      # the contact page sits at the end of the report, with the sources as the final pages
    body.append(f'<section class="{cls}" id="{s["id"]}"><div class="sh"><span class="n">{i:02d}</span><div>{eye}<h2>{R.esc(s["title"])}</h2></div></div>{render(s)}</section>')
doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{R.esc(R.TITLE)}</title><style>{CSS}</style></head><body>{"".join(body)}</body></html>'
for bad in ('{{', '**', '](http'):
    assert bad not in doc.split('</style>', 1)[1], bad
tmp = os.path.join(ROOT, '_pdf.html')
open(tmp, 'w', encoding='utf-8').write(doc)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        over = await pg.evaluate("()=>[...document.querySelectorAll('[data-fit]')].map(e=>[e.scrollHeight,+e.dataset.fit]).filter(x=>x[0]>x[1]+1)")
        fonts = await pg.evaluate("[...document.fonts].filter(f=>f.status=='loaded').length")
        await pg.pdf(path=OUT, width='8.5in', height='11in', print_background=True, prefer_css_page_size=True)
        await b.close()
        for got, fit in over:
            print(f'note: the cover text runs {got - fit}px past its frame')
        n = len(re.findall(rb'/Type\s*/Page\b(?!s)', open(OUT, 'rb').read()))
        print('fonts loaded', fonts, '| wrote', os.path.relpath(OUT, SITE), round(os.path.getsize(OUT) / 1024), 'KB,', n, 'pages')

asyncio.run(main())
if '--keep' not in sys.argv:
    os.remove(tmp)

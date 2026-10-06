# Appends the Important Disclosures page to a sector report PDF as its last page.
# The text is DISCLOSURES in _build/build.py, the same text shown on disclosures.html.
# Called at the end of each report's pdf.py: disclosures.append(OUT, 'Industrial', 'Q4 2026').
# Needs Playwright with Chromium and pypdf (pip install playwright pypdf).
import html, io, os, sys
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(SITE, '_build'))
import build as site  # noqa: E402

FONTS = 'healthcare-q4-2026/fonts'  # relative to the temporary page written in this folder
F = [('Newsreader', 'newsreader', 500, 'normal'), ('Quicksand', 'quicksand', 500, 'normal'), ('Quicksand', 'quicksand', 700, 'normal')]
FACE = ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};font-style:{s};src:url('{FONTS}/{f}-latin-{w}-{s}.woff2') format('woff2')}}" for n, f, w, s in F)

CSS = FACE + '''
@page { size: 816px 1056px; margin: 0; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; }
.pg { position: relative; width: 816px; height: 1056px; overflow: hidden; padding: 64px 72px 0; font: 500 10.6px/1.62 'Quicksand', Arial, sans-serif; color: #444; background: #fff; }
.run { font-weight: 700; font-size: 8px; letter-spacing: 0.2em; text-transform: uppercase; color: #a57a4e; text-align: right; }
h1 { font: 500 34px/1.1 'Newsreader', Georgia, serif; color: #231f20; margin: 34px 0 14px; }
.rule { width: 56px; height: 2px; background: #bc9163; margin: 0 0 24px; }
p { margin: 0 0 11px; text-align: left; position: relative; }
.foot { position: absolute; left: 72px; right: 72px; bottom: 40px; display: flex; justify-content: space-between; font-weight: 700; font-size: 8px; letter-spacing: 0.2em; text-transform: uppercase; color: #736f70; }
.foot b { color: #a57a4e; letter-spacing: 0; font-size: 10px; }
'''


def page_html(sector, period, number):
    paras = ''.join(f'<p>{html.escape(p)}</p>' for p in site.DISCLOSURES)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Important Disclosures</title><style>{CSS}</style></head><body>'
            f'<div class="pg"><div class="run">{html.escape(sector)} &nbsp;&middot;&nbsp; {html.escape(period)}</div>'
            f'<h1>Important Disclosures</h1><div class="rule"></div>{paras}'
            f'<div class="foot"><span>benchmarkintl.com</span><b>{number}</b></div></div></body></html>')


def append(pdf_path, sector, period):
    reader = PdfReader(pdf_path)
    number = len(reader.pages) + 1
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 816, 'height': 1056})
        tmp = os.path.join(HERE, '_disclosures.html')
        open(tmp, 'w', encoding='utf-8').write(page_html(sector, period, number))
        pg.goto('file://' + tmp)
        pg.evaluate('document.fonts.ready')
        loaded = pg.evaluate("[...document.fonts].filter(f => f.status == 'loaded').length")
        assert loaded == len(F), f'only {loaded} of {len(F)} fonts loaded'
        over = pg.evaluate("document.querySelector('.pg p:last-of-type').getBoundingClientRect().bottom - (1056 - 72)")
        assert over <= 0, f'disclosures text runs {over:.0f}px into the footer'
        data = pg.pdf(width='816px', height='1056px', print_background=True, prefer_css_page_size=True)
        b.close()
        os.remove(tmp)
    extra = PdfReader(io.BytesIO(data))
    assert len(extra.pages) == 1, 'disclosures should fit on one page'
    w = PdfWriter(clone_from=reader)
    w.add_page(extra.pages[0])
    with open(pdf_path, 'wb') as f:
        w.write(f)
    print('appended Important Disclosures as page', number)

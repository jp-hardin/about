# Builds the downloadable PDF from the print pages in pages/.
# Fonts come from ../healthcare-q4-2026/fonts (SIL Open Font License), so the build needs no network access.
import re, os, glob, asyncio
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ROOT, '..', '..', '..'))
SLUG = 'business-services-q4-2026'
PUBLIC = SLUG.rsplit('-', 2)[0] + '-industry-report-' + '-'.join(SLUG.rsplit('-', 2)[1:])
OUT = os.path.join(SITE, 'insights', f'{PUBLIC}.pdf')
FONTS = '../healthcare-q4-2026/fonts'
AST = os.path.relpath(os.path.join(SITE, 'assets', 'img'), ROOT)
# Images the design canvas stores as uploads, mapped to the copies kept in this repo.
IMG = {
    '4aa1fb4e371d7b1d36d8bd5008f28cd9': 'art/knot.png',
    '92cd28b11f6cc05be2f329fdddf8bb67': f'{AST}/brand/benchmark-logo-white.png',
    'de9567aa819b281813dcb69f7fd19f18': f'{AST}/team/jared-hardin.jpg',
    '4702e4e68e821c3cd441c036b4ca508f': 'art/cover5.svg',
    'bc86f994d13c874e1996a1d9f68954ea': 'art/band-cf.svg',
    '1cc74672419c59e59e27d6596abefb0f': 'art/band-marketing.svg',
    'a941a71230b9de51bebd7ac520ef7f54': 'art/band-en.svg',
    'd2e39f928b0881c55c7a8d16cbdbdfb3': 'art/band-fi.svg',
    '622e0f3812b574359062417c12eb7668': 'art/band-staffing.svg',
    'e5f57fbb67abaa53e65d06126f905958': 'art/banner-fi.svg',
    '21a0e8f569577bf92e18bab5e93a328c': 'art/banner-cf.svg',
    '1cf208339fad8f016ff8b1994c05e6ea': 'art/banner-mk.svg',
    '6497b34887331289c5f58585076bbc90': 'art/banner-en.svg',
    '83bfbba9fadda216554fa95403c0f0d0': 'art/banner-st.svg',
    'f10823ce49a2687d39adebc578baa822': 'art/plate-deal.svg',
    '8c294e80f84889a59fa606544143456e': 'art/plate-prep.svg',
    'dc11db870a3b6c0df7bc69c785fbf766': 'art/plate-close.svg',
}

def order():
    fs = sorted(glob.glob(os.path.join(ROOT, 'pages', 'P*.dc.html')))
    return [os.path.join(ROOT, 'pages', 'Main.dc.html')] + fs

F = [('Cinzel', 'cinzel', 400, 'normal'), ('Cinzel', 'cinzel', 500, 'normal')]
F += [('Newsreader', 'newsreader', w, s) for w in (500, 600) for s in ('normal', 'italic')]
F += [('Quicksand', 'quicksand', w, 'normal') for w in (400, 500, 600, 700)]
face = ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};font-style:{s};src:url('{FONTS}/{f}-latin-{w}-{s}.woff2') format('woff2')}}" for n, f, w, s in F)

pgs = []
for f in order():
    h = open(f, encoding='utf-8').read()
    m = re.search(r'</helmet>\s*(.*)\s*</x-dc>', h, re.S); assert m, f
    pgs.append(f'<div class="pg" data-fn="{os.path.basename(f)}">{m.group(1)}</div>')
doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Business Services Q4 2026 M&amp;A Sector Report</title>'
       f'<style>{face}@page{{size:816px 1056px;margin:0}}body{{margin:0}}.pg{{break-after:page;width:816px;height:1056px;overflow:hidden}}'
       'a{color:#8C6239;text-decoration-thickness:.5px;text-underline-offset:2px}</style></head><body>' + '\n'.join(pgs) + '</body></html>')
for k, v in IMG.items(): doc = doc.replace('/_blob/' + k, v)
assert '/_blob/' not in doc, re.findall(r'/_blob/\w+', doc)[:3]
doc = doc.replace('border-radius: 50%">', 'border-radius: 50%; object-fit: cover">')
tmp = os.path.join(ROOT, '_pdf.html'); open(tmp, 'w', encoding='utf-8').write(doc)

CHECK = """()=>[...document.querySelectorAll('.pg')].map(pg=>{
  const box=[...pg.firstElementChild.children].find(e=>/flex-direction: column/.test(e.getAttribute('style')||'')&&/left: 48px/.test(e.getAttribute('style')||'')&&/[^-]height: \\d+px/.test(e.getAttribute('style')||''));
  if(!box) return null; const r=box.getBoundingClientRect(); let b=r.top;
  for(const c of box.children){const x=c.getBoundingClientRect().bottom; if(x>b) b=x;}
  return [pg.dataset.fn, Math.round(r.bottom-b)];
}).filter(x=>x&&x[1]<0)"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 816, 'height': 1056})
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        over = await pg.evaluate(CHECK)
        fonts = await pg.evaluate("[...document.fonts].filter(f=>f.status=='loaded').length")
        await pg.pdf(path=OUT, width='816px', height='1056px', print_background=True, prefer_css_page_size=True)
        await b.close()
        for fn, spare in over: print(f'OVER: {fn} runs {-spare}px past its text frame')
        print('pages', len(pgs), '| fonts loaded', fonts, '| wrote', os.path.relpath(OUT, SITE), round(os.path.getsize(OUT) / 1024), 'KB')
asyncio.run(main()); os.remove(tmp)

# Last page: Important Disclosures (text in _build/build.py, page in ../disclosures.py)
import sys; sys.path.insert(0, os.path.dirname(ROOT)); import disclosures
disclosures.append(OUT, 'Business Services', 'Q4 2026')

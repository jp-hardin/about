# Builds the downloadable PDF from the print pages in root/project (run gen.py first).
# Fonts come from ../healthcare-q4-2026/fonts (SIL Open Font License), so the build needs no network access.
import re, os, json, asyncio
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ROOT, '..', '..', '..'))
PROJ = os.path.join(ROOT, 'root', 'project')
SLUG = 'technology-q4-2026'
PUBLIC = SLUG.rsplit('-', 2)[0] + '-industry-report-' + '-'.join(SLUG.rsplit('-', 2)[1:])
OUT = os.path.join(SITE, 'insights', f'{PUBLIC}.pdf')
FONTS = '../healthcare-q4-2026/fonts'
AST = os.path.relpath(os.path.join(SITE, 'assets', 'img'), ROOT)
# Images the design canvas stores as uploads, mapped to the copies kept in this repo.
IMG = {
    'a4e9bce348ee211dfa63f50c5b5de181': 'art/logo.png',
    '91834fbbbc00b31f5c36c7319ad1e129': 'art/knot.png',
    'a4627b44afa321c0e5263a218e5cb43d': f'{AST}/team/jared-hardin.jpg',
}
# Photographs from the approved library, prepared for this report in assets/img/industries/technology.
PH = f'{AST}/industries/technology'
IMG.update({
    '151e0ff33db32361cea2a3f8a833e3e9': f'{PH}/rpt-cover-datacenter.jpg',
    'cddf308fc92bfee28a88f35f8cf7ca67': f'{PH}/rpt-server-racks.jpg',
    '643493205d756d338b787cd3b5150ce7': f'{PH}/rpt-keyboard.jpg',
    'a2ae072ce129acce7f045e44978fe69e': f'{PH}/rpt-telecom-masts.jpg',
    'e5a9e07bcb6a0f7f6dfde3725f5af1c7': f'{PH}/rpt-network-cables.jpg',
    'c2db878093ab396ade901a47de706d38': f'{PH}/rpt-circuit-board.jpg',
    '7c2230130aa40114760060efc60c52a4': f'{PH}/rpt-satellite-dish.jpg',
    'c8d2f2cd3c854c01714578371dfe2936': f'{PH}/rpt-laptop-repair.jpg',
    'c32355433303fcff161324c3a5b9388d': f'{PH}/rpt-team-laptops.jpg',
})

F = [('Cinzel', 'cinzel', 400, 'normal'), ('Cinzel', 'cinzel', 500, 'normal')]
F += [('Newsreader', 'newsreader', w, s) for w in (500, 600) for s in ('normal', 'italic')]
F += [('Quicksand', 'quicksand', w, 'normal') for w in (400, 500, 600, 700)]
face = ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};font-style:{s};src:url('{FONTS}/{f}-latin-{w}-{s}.woff2') format('woff2')}}" for n, f, w, s in F)

order = json.load(open(os.path.join(PROJ, 'canvas.json')))['order']
pgs = []
for fn in order:
    h = open(os.path.join(PROJ, fn), encoding='utf-8').read()
    m = re.search(r'</helmet>\s*(.*)\s*</x-dc>', h, re.S); assert m, fn
    pgs.append(f'<div class="pg" data-fn="{fn}">{m.group(1)}</div>')
doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Technology Q4 2026 M&amp;A Sector Report</title>'
       f'<style>{face}@page{{size:816px 1056px;margin:0}}body{{margin:0}}.pg{{break-after:page;width:816px;height:1056px;overflow:hidden}}'
       'a{color:#8C6239;text-decoration-thickness:.5px;text-underline-offset:2px}</style></head><body>' + '\n'.join(pgs) + '</body></html>')
for k, v in IMG.items(): doc = doc.replace('/_blob/' + k, v)
assert '/_blob/' not in doc, re.findall(r'/_blob/\w+', doc)[:3]
doc = doc.replace('border-radius: 50%">', 'border-radius: 50%; object-fit: cover">')
tmp = os.path.join(ROOT, '_pdf.html'); open(tmp, 'w', encoding='utf-8').write(doc)

# Each text frame carries its height in data-fit; a page is over when its content ends below that.
CHECK = """()=>[...document.querySelectorAll('[data-fit]')].map(el=>{
  const top=el.getBoundingClientRect().top; let b=0;
  el.querySelectorAll('*').forEach(c=>{const r=c.getBoundingClientRect(); if(r.height>0&&r.bottom-top>b) b=r.bottom-top;});
  return [el.closest('.pg').dataset.fn, Math.round(b)-(+el.dataset.fit)];
}).filter(x=>x[1]>0)"""

async def main():
    async with async_playwright() as p:
        try: b = await p.chromium.launch()
        except Exception: b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = await b.new_page(viewport={'width': 816, 'height': 1056})
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        over = await pg.evaluate(CHECK)
        fonts = await pg.evaluate("[...document.fonts].filter(f=>f.status=='loaded').length")
        broken = await pg.evaluate("[...document.images].filter(i=>!i.naturalWidth).map(i=>i.getAttribute('src'))")
        await pg.pdf(path=OUT, width='816px', height='1056px', print_background=True, prefer_css_page_size=True)
        await b.close()
        for fn, extra in over: print(f'OVER: {fn} runs {extra}px past its text frame')
        assert not broken, broken
        print('pages', len(pgs), '| fonts loaded', fonts, '| wrote', os.path.relpath(OUT, SITE), round(os.path.getsize(OUT) / 1024), 'KB')
asyncio.run(main())
if not os.environ.get('KEEP'): os.remove(tmp)

# Last page: Important Disclosures (text in _build/build.py, page in ../disclosures.py)
import sys; sys.path.insert(0, os.path.dirname(ROOT)); import disclosures
disclosures.append(OUT, 'Technology', 'Q4 2026')

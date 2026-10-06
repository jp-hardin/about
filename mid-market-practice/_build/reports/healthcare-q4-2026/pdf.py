# Builds the downloadable PDF of the print layout from preview.html (run gen.py first).
# Fonts are bundled in fonts/ (SIL Open Font License) so the build needs no network access.
import re, os, asyncio
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ROOT, '..', '..', '..'))
SLUG = 'healthcare-q4-2026'
PUBLIC = SLUG.rsplit('-', 2)[0] + '-industry-report-' + '-'.join(SLUG.rsplit('-', 2)[1:])
OUT = os.path.join(SITE, 'insights', f'{PUBLIC}.pdf')
h = open(os.path.join(ROOT, 'preview.html')).read()
i = h.find('<div class="pg" data-fn="ONEPAGER"')
if i >= 0: h = h[:i] + '</body></html>'
F = [('Cinzel', 'cinzel', 400, 'normal'), ('Cinzel', 'cinzel', 500, 'normal')]
F += [('Newsreader', 'newsreader', w, s) for w in (500, 600) for s in ('normal', 'italic')]
F += [('Quicksand', 'quicksand', w, 'normal') for w in (400, 500, 600, 700)]
face = ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};font-style:{s};src:url('fonts/{f}-latin-{w}-{s}.woff2') format('woff2')}}" for n, f, w, s in F)
h, n = re.subn(r'<link href="https://fonts\.googleapis\.com[^>]*>', f'<style>{face}</style>', h); assert n == 1
img = 'art'; ast = os.path.relpath(os.path.join(SITE, 'assets', 'img'), ROOT)
for k, v in {'/_blob/0ec74a82d64ca48c5a0589fe8fbe222d': f'{img}/knot.png', '/_blob/4dd1bb932520e4f56865210abba6a736': f'{ast}/brand/benchmark-logo-white.png',
             '/_blob/70432026c2e1430aa486f0faff90dbbc': f'{ast}/team/jared-hardin.jpg'}.items(): h = h.replace(k, v)
# The checklist and signed-agreement illustrations exist only in the design canvas, so these two blocks close up without them.
h, n1 = re.subn(r'<div style="width: 280px; position: relative"><img src="/_blob/1d7f[^>]*><div[^>]*></div></div>', '', h)
h = h.replace('<div style="width: 408px; display: flex; flex-direction: column; gap: 14px; text-align: justify">', '<div style="width: 720px; display: flex; flex-direction: column; gap: 14px; text-align: justify">')
h, n2 = re.subn(r'<div style="width: 344px; display: flex; flex-direction: column">\s*<img src="/_blob/1053[^>]*>\s*<div[^>]*></div>\s*</div>', '', h)
assert n1 == 1 and n2 == 1 and '/_blob/' not in h, (n1, n2)
h = h.replace('border-radius: 50%">', 'border-radius: 50%; object-fit: cover">')
tmp = os.path.join(ROOT, '_pdf.html'); open(tmp, 'w').write(h)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        over = await pg.evaluate("""()=>[...document.querySelectorAll('[data-fit]')].map(e=>[e.closest('.pg').dataset.fn,e.scrollHeight,+e.dataset.fit]).filter(x=>x[1]>x[2]+1)""")
        fonts = await pg.evaluate("[...document.fonts].filter(f=>f.status=='loaded').length")
        await pg.pdf(path=OUT, width='8.5in', height='11in', print_background=True, prefer_css_page_size=True)
        await b.close()
        for fn, got, fit in over: print(f'note: {fn} runs {got - fit}px past its text frame (about 40px of clearance exists above the footer)')
        print('fonts loaded', fonts, '| wrote', os.path.relpath(OUT, SITE), round(os.path.getsize(OUT) / 1024), 'KB')
asyncio.run(main()); os.remove(tmp)

# Last page: Important Disclosures (text in _build/build.py, page in ../disclosures.py)
import sys; sys.path.insert(0, os.path.dirname(ROOT)); import disclosures
disclosures.append(OUT, 'Healthcare', 'Q4 2026')

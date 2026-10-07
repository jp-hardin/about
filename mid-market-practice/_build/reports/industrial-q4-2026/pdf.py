# Builds the downloadable PDF from report.md: a Letter-size print layout in the report brand.
# Needs Playwright with Chromium (pip install playwright && playwright install chromium).
# Fonts are bundled in fonts/ (SIL Open Font License) so the build needs no network access.
import os, re, asyncio
from playwright.async_api import async_playwright
from render import ROOT, SLUG, AS_OF, FIGS, SEGMENTS, groups, esc
SITE = os.path.normpath(os.path.join(ROOT, '..', '..', '..'))
PUBLIC = SLUG.rsplit('-', 2)[0] + '-industry-report-' + '-'.join(SLUG.rsplit('-', 2)[1:])
OUT = os.path.join(SITE, 'insights', f'{PUBLIC}.pdf')
IMG = os.path.relpath(os.path.join(SITE, 'assets', 'img'), ROOT)

F = [('Cinzel', 'cinzel', 400, 'normal'), ('Cinzel', 'cinzel', 500, 'normal')]
F += [('Newsreader', 'newsreader', w, s) for w in (500, 600) for s in ('normal', 'italic')]
F += [('Quicksand', 'quicksand', w, 'normal') for w in (400, 500, 600, 700)]
face = ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};font-style:{s};src:url('fonts/{f}-latin-{w}-{s}.woff2') format('woff2')}}" for n, f, w, s in F)

CSS = face + '''
:root { --ink:#231f20; --charcoal:#2a2a2a; --graphite:#444; --gold:#bc9163; --gold-deep:#a57a4e; --sand:#c3bdb6; --paper:#faf7f3; --line:#e2dbd3; --muted:#736f70; }
@page { size: 8.5in 11in; margin: 0.8in 0.72in 0.82in;
  @bottom-left { content: "INDUSTRIAL  \\00B7  Q4 2026  \\00B7  BENCHMARK INTERNATIONAL"; font: 600 6.6pt 'Quicksand'; letter-spacing: 0.16em; color: #736f70; }
  @bottom-right { content: counter(page); font: 600 8pt 'Quicksand'; color: #a57a4e; } }
@page cover { margin: 0; @bottom-left { content: none; } @bottom-right { content: none; } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 500 9.2pt/1.55 'Quicksand', Arial, sans-serif; color: var(--graphite); }
a { color: var(--gold-deep); text-decoration: none; }
p { margin: 0 0 8pt; }
strong { color: var(--ink); font-weight: 700; }
.cover { page: cover; break-after: page; height: 11in; background: var(--ink); color: #fff; padding: 0.9in 0.85in; display: flex; flex-direction: column; position: relative; overflow: hidden; }
.cover::before { content: ""; position: absolute; inset: 0; background: url('IMG/industries/industrial/hero.jpg') 50% 50%/cover no-repeat; }
.cover::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(35,31,32,0.72) 0%, rgba(35,31,32,0.5) 30%, rgba(35,31,32,0.78) 55%, rgba(35,31,32,0.94) 78%, rgba(35,31,32,0.97) 100%); }
.cover > * { position: relative; z-index: 1; }
.cover img.logo { width: 2.1in; }
.cover .tag { font: 600 7.5pt 'Quicksand'; letter-spacing: 0.3em; text-transform: uppercase; color: var(--gold); margin-top: 8pt; }
.cover .mid { margin-top: auto; }
.cover .eyebrow { font: 600 8.5pt 'Quicksand'; letter-spacing: 0.26em; text-transform: uppercase; color: var(--gold); margin: 0 0 14pt; }
.cover h1 { font: 400 46pt/1.05 'Cinzel', Georgia, serif; letter-spacing: 0.02em; margin: 0; }
.cover h1 em { font-style: normal; color: var(--gold); display: block; font-size: 30pt; margin-top: 8pt; }
.cover .lead { font: 500 13pt/1.5 'Newsreader', Georgia, serif; color: var(--sand); max-width: 5.2in; margin: 22pt 0 0; }
.cover .by { font: 600 7.5pt 'Quicksand'; letter-spacing: 0.2em; text-transform: uppercase; color: var(--sand); margin-top: 26pt; }
.cover .figs { display: grid; grid-template-columns: repeat(4, 1fr); border-top: 1px solid rgba(255,255,255,0.18); margin-top: 0.7in; }
.cover .fig { padding: 16pt 12pt 0 0; }
.cover .fig + .fig { padding-left: 12pt; border-left: 1px solid rgba(255,255,255,0.18); }
.cover .fig b { display: block; font: 500 22pt/1.1 'Newsreader', Georgia, serif; color: var(--gold); }
.cover .fig span { display: block; font-size: 7.4pt; line-height: 1.45; color: var(--sand); margin-top: 5pt; }
.cover .asof { font-size: 6.8pt; color: #8f8a86; margin-top: 16pt; }
.toc { break-after: page; }
.toc h2 { font: 400 20pt 'Cinzel', Georgia, serif; color: var(--ink); letter-spacing: 0.04em; margin: 0 0 18pt; }
.toc ol { list-style: none; margin: 0; padding: 0; }
.toc li { display: grid; grid-template-columns: 34pt 1fr; padding: 9pt 0; border-bottom: 1px solid var(--line); font: 500 12pt 'Newsreader', Georgia, serif; color: var(--ink); }
.toc li span { font: 700 8pt 'Quicksand'; letter-spacing: 0.1em; color: var(--gold); padding-top: 3pt; }
.toc a { color: inherit; }
.rsec { break-before: page; }
.rsec-head { display: flex; align-items: baseline; gap: 14pt; border-bottom: 2px solid var(--gold); padding-bottom: 8pt; margin-bottom: 16pt; }
.rsec-num { font: 500 20pt 'Newsreader', Georgia, serif; color: var(--sand); }
.rsec-head h2 { font: 400 19pt/1.2 'Cinzel', Georgia, serif; letter-spacing: 0.03em; color: var(--ink); margin: 0; }
.rlead { font: 500 12pt/1.5 'Newsreader', Georgia, serif; color: var(--ink); margin-bottom: 10pt; }
.rtag { font: 500 italic 10.5pt/1.45 'Newsreader', Georgia, serif; color: var(--charcoal); margin: -2pt 0 8pt; }
.eyebrow { font: 700 6.8pt 'Quicksand'; letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold-deep); margin: 14pt 0 6pt; }
.rh3 { font: 500 14pt/1.3 'Newsreader', Georgia, serif; color: var(--ink); margin: 18pt 0 8pt; break-after: avoid; }
.rh3-num { font: 700 7pt 'Quicksand'; letter-spacing: 0.14em; color: var(--gold); margin-right: 9pt; vertical-align: middle; }
.rh4 { font: 700 7.2pt 'Quicksand'; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink); margin: 14pt 0 5pt; break-after: avoid; }
.rh4--sub { color: var(--gold-deep); }
.rsub { border-top: 1px solid var(--line); padding-top: 8pt; margin-top: 4pt; }
.rsub .rh4 { margin: 0 0 4pt; }
.rlist { list-style: none; margin: 0 0 8pt; padding: 0; }
.rlist li { position: relative; padding: 0 0 6pt 13pt; }
.rlist li::before { content: ""; position: absolute; left: 0; top: 0.66em; width: 6px; height: 1.5px; background: var(--gold); }
.rstats { display: grid; grid-template-columns: repeat(3, 1fr); background: var(--ink); color: #fff; margin: 0 0 14pt; break-inside: avoid; }
.rstat { padding: 13pt 14pt; }
.rstat + .rstat { border-left: 1px solid rgba(255,255,255,0.14); }
.stat-num { font: 500 19pt/1.1 'Newsreader', Georgia, serif; color: var(--gold); }
.rstat-label { font-size: 7.4pt; line-height: 1.45; color: var(--sand); margin-top: 4pt; }
.rquote { margin: 12pt 0; padding: 12pt 16pt; background: var(--paper); border-left: 2.5px solid var(--gold); break-inside: avoid; }
.rquote blockquote { margin: 0 0 5pt; font: 500 italic 11pt/1.5 'Newsreader', Georgia, serif; color: var(--charcoal); }
.rquote figcaption { font-size: 7.4pt; }
.rnote { margin: 14pt 0 0; padding: 12pt 16pt 5pt; background: var(--paper); border-top: 2.5px solid var(--gold); break-inside: avoid; }
.rnote .eyebrow { margin-top: 0; }
.rtable-wrap { margin: 8pt 0 12pt; }
.rtable { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 7.7pt; line-height: 1.42; }
.rtable thead { display: table-header-group; }
.rtable tr { break-inside: avoid; }
.rtable th, .rtable td { text-align: left; vertical-align: top; padding: 5pt 8pt 5pt 0; border-bottom: 1px solid var(--line); font-weight: 500; overflow-wrap: break-word; }
.rtable thead th { font: 700 6.2pt 'Quicksand'; letter-spacing: 0.13em; text-transform: uppercase; color: var(--ink); border-bottom: 1.5px solid var(--gold); vertical-align: bottom; }
.rtable tbody th { font-weight: 700; color: var(--ink); }
.rtable--dark thead th { background: var(--ink); color: #fff; border-bottom: 0; padding: 6pt 8pt; }
.rtable--dark tbody th, .rtable--dark tbody td { padding-left: 8pt; }
.rtable .rtotal > * { font-weight: 700; color: var(--ink); border-bottom: 1.5px solid var(--gold); }
figure { margin: 0; }
.rchart { margin: 10pt 0 12pt; padding: 14pt 16pt 8pt; background: var(--paper); border-top: 2.5px solid var(--gold); break-inside: avoid; }
.rchart figcaption strong { display: block; font: 500 12pt 'Newsreader', Georgia, serif; color: var(--ink); }
.rchart figcaption span { display: block; font-size: 7.6pt; color: var(--muted); margin: 2pt 0 4pt; }
.rchart svg { display: block; width: 100%; height: auto; overflow: visible; }
.cgrid { stroke: var(--line); } .cref { stroke: var(--muted); stroke-dasharray: 4 4; }
.cline { fill: none; stroke: var(--gold-deep); stroke-width: 2; stroke-linejoin: round; }
.cdot { fill: var(--gold-deep); stroke: var(--paper); stroke-width: 2; } .chit { fill: none; }
.caxis { font: 500 11.5px 'Quicksand'; fill: var(--muted); } .cval { font: 700 12.5px 'Quicksand'; fill: var(--ink); }
.rdata { display: none; }
.fine, .fine p { font-size: 7.2pt; line-height: 1.5; color: var(--muted); }
.rsec--sources .fine { font-size: 6.9pt; }
.rsec--sources .fine .rlist { columns: 2; column-gap: 22pt; }
.rsec--sources .fine .rlist li { padding: 3pt 0; border-bottom: 1px solid var(--line); break-inside: avoid; }
.rsec--sources .fine .rlist li::before { display: none; }
.contact { break-before: page; }
.contact .card { display: grid; grid-template-columns: 1.25in 1fr; gap: 22pt; align-items: center; background: var(--paper); border-top: 2.5px solid var(--gold); padding: 22pt 24pt; margin-top: 16pt; }
.contact img { width: 1.25in; height: 1.25in; border-radius: 50%; object-fit: cover; }
.contact h3 { font: 500 18pt 'Newsreader', Georgia, serif; color: var(--ink); margin: 0 0 2pt; }
.contact .role { font: 700 7pt 'Quicksand'; letter-spacing: 0.18em; text-transform: uppercase; color: var(--gold-deep); margin: 0 0 8pt; }
.contact .card p { margin: 0; font-size: 10pt; }
'''.replace('IMG/', IMG + '/')

G = groups()
order = [g for g in G if g[0] != 'sources'] + ['contact'] + [g for g in G if g[0] == 'sources']
secs, toc, n = [], [], 0
for g in order:
    n += 1
    if g == 'contact':
        toc.append(f'<li><span>{n:02d}</span><a href="#contact">Considering a Transaction in Industrial?</a></li>')
        secs.append(f'''<section class="rsec contact" id="contact"><div class="rsec-head"><span class="rsec-num">{n:02d}</span><h2>Considering a Transaction in Industrial?</h2></div>
<p class="rlead">The first step is a confidential conversation about your goals, your company and your options, with no pressure and no commitment.</p>
<div class="card"><img src="{IMG}/team/jared-hardin.jpg" alt="Jared Hardin"><div><h3>Jared Hardin</h3><p class="role">Managing Director, Benchmark International</p>
<p><a href="tel:8137716675">813-771-6675</a> &nbsp;|&nbsp; <a href="mailto:j.hardin@benchmarkintl.com">j.hardin@benchmarkintl.com</a></p>
<p style="margin-top:6pt"><a href="https://jp-hardin.github.io/about/mid-market-practice/industries/industrial.html">Benchmark Capital Markets, Industrial</a></p></div></div></section>''')
        continue
    aid, title, inner = g
    toc.append(f'<li><span>{n:02d}</span><a href="#{aid}">{esc(title)}</a></li>')
    secs.append(f'<section class="rsec rsec--{aid}" id="{aid}"><div class="rsec-head"><span class="rsec-num">{n:02d}</span><h2>{esc(title)}</h2></div>\n{inner}\n</section>')
figs = ''.join(f'<div class="fig"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in FIGS)
doc = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Industrial Q4 2026 M&amp;A Sector Report | Benchmark International</title><style>{CSS}</style></head><body>
<section class="cover"><img class="logo" src="{IMG}/brand/benchmark-logo-white.png" alt="Benchmark International"><p class="tag">Benchmark Capital Markets</p>
<div class="mid"><p class="eyebrow">M&amp;A Sector Report &nbsp;|&nbsp; October 2026</p><h1>Industrial<em>Q4 2026</em></h1>
<p class="lead">{' &middot; '.join(esc(t) for _, t in SEGMENTS)}</p><p class="by">Jared Hardin, Managing Director, Benchmark International</p>
<div class="figs">{figs}</div><p class="asof">Information as of {AS_OF}. Multiples from public companies and larger transactions are reference points, and a private company&#39;s price depends on the business itself.</p></div></section>
<section class="toc"><h2>Contents</h2><ol>{''.join(toc)}</ol></section>
{chr(10).join(secs)}
</body></html>'''
doc = re.sub(r' target="_blank" rel="noopener"', '', doc)
tmp = os.path.join(ROOT, '_pdf.html'); open(tmp, 'w', encoding='utf-8').write(doc)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready')
        fonts = await pg.evaluate("[...document.fonts].filter(f=>f.status=='loaded').length")
        await pg.pdf(path=OUT, print_background=True, prefer_css_page_size=True)
        await b.close()
        print('fonts loaded', fonts, '| wrote', os.path.relpath(OUT, SITE), round(os.path.getsize(OUT) / 1024), 'KB')
asyncio.run(main())
if not os.environ.get('KEEP_HTML'): os.remove(tmp)

# Last page: Important Disclosures (text in _build/build.py, page in ../disclosures.py)
import sys; sys.path.insert(0, os.path.dirname(ROOT)); import disclosures
disclosures.append(OUT, 'Industrial', 'Q4 2026')

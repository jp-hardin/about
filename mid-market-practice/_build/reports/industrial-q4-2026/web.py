# Builds the site-native report page from report.md.
# Usage: python3 web.py
import os, sys
from render import ROOT, SLUG, AS_OF, FIGS, groups, esc
SITE = os.path.normpath(os.path.join(ROOT, '..', '..', '..'))
sys.path.insert(0, os.path.join(SITE, '_build'))
import build as site

secs, toc = [], []
for i, (aid, title, inner) in enumerate(groups(), 1):
    secs.append(f'<section class="rsec rsec--{aid}" id="{aid}">\n<div class="rsec-head"><span class="rsec-num">{i:02d}</span><h2 class="h2">{esc(title)}</h2></div>\n<div class="rblock">{inner}</div>\n</section>')
    toc.append(f'<li><a href="#{aid}"><span>{i:02d}</span>{esc(title)}</a></li>')

root = '../'
PUBLIC = SLUG.rsplit('-', 2)[0] + '-industry-report-' + '-'.join(SLUG.rsplit('-', 2)[1:])  # e.g. healthcare-industry-report-q4-2026
PDF = f'{PUBLIC}.pdf'
dl = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 11l5 5 5-5M5 20h14"/></svg>'
stats = ''.join(f'<div class="stat"><div class="stat-num">{esc(a)}</div><div class="stat-label">{esc(b)}</div></div>' for a, b in FIGS)
desc = 'Q4 2026 M&A sector report for manufacturing and industrial technology, industrial distribution and services, building products and construction services, energy, power and environmental services, and transportation and logistics, from the Benchmark International Middle Market team.'
page = site.head('Industrial Q4 2026 M&A Sector Report', desc, root).replace('</head>', f'<link rel="stylesheet" href="{root}assets/css/report.css">\n</head>')
page += site.header(root, 'industries')
page += f'''
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Middle Market</a> / <a href="{root}industries/index.html">Industries</a> / <a href="{root}industries/industrial.html">Industrial</a> / Q4 2026 Sector Report</div>
    <p class="eyebrow">M&amp;A Sector Report &nbsp;|&nbsp; October 2026</p>
    <h1 class="display">Industrial <em>Q4 2026</em></h1>
    <p class="lead">Manufacturing and industrial technology, distribution and services, building products and construction services, energy, power and environmental services, and transportation and logistics: the order books, the deal market and what acquirers are paying for.</p>
    <p class="rbyline">Jared Hardin, Managing Director, Benchmark International</p>
    <div class="btn-row"><a class="btn" href="{PDF}" download>{dl} Download the PDF</a><a class="btn btn--light" href="{root}index.html#form">Discuss Your Business</a></div>
  </div>
</section>

<section class="section--dark section--tight">
  <div class="wrap">
    <div class="stats rhero-stats">{stats}</div>
    <p class="note">Information as of {AS_OF}. Multiples from public companies and larger transactions are reference points, and a private company&#39;s price depends on the business itself.</p>
  </div>
</section>

<div class="wrap rlayout">
  <aside class="rtoc" aria-label="Report contents">
    <p class="eyebrow">Contents</p>
    <ol>{''.join(toc)}</ol>
    <a class="btn" href="{PDF}" download>{dl} Download PDF</a>
  </aside>
  <article class="report">
{chr(10).join(secs)}
    <aside class="rauthor">
      <img src="{root}assets/img/team/jared-hardin.jpg" alt="Jared Hardin" width="120" height="120" loading="lazy">
      <div>
        <p class="eyebrow">Considering a transaction in industrial?</p>
        <h3>Jared Hardin</h3>
        <p class="role">Managing Director, Benchmark International</p>
        <p><a href="tel:8137716675">813-771-6675</a> &nbsp;|&nbsp; <a href="mailto:j.hardin@benchmarkintl.com">j.hardin@benchmarkintl.com</a></p>
        <div class="btn-row"><a class="btn" href="{root}index.html#form">Start the Conversation</a><a class="btn btn--ghost" href="{PDF}" download>{dl} Download the PDF</a></div>
      </div>
    </aside>
  </article>
</div>

'''
page += site.cta(root)
page += site.footer(root)
page = site.report_extras(page, 'industrial', root)
for bad in ('{{', '@@', '—', '**'):
    i = page.find(bad)
    assert i < 0, (bad, page[max(0, i - 200):i + 200])
out = os.path.join(SITE, 'insights', f'{PUBLIC}.html')
open(out, 'w', encoding='utf-8').write(page)
print('wrote', os.path.relpath(out, SITE), round(len(page) / 1024), 'KB', len(secs), 'sections')

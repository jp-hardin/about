# Builds the site-native report page from the same content as the print layout.
# Usage: python3 web.py   (run gen.py and pdf.py as well if the PDF should change)
import re, os, sys, html
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ROOT, '..', '..', '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(SITE, '_build'))
import build as site
import lib
lib.WEB = True  # every building block now returns semantic HTML styled by assets/css/report.css
from report import PAGES, BRIEF, FIGS, source_groups, sources_pages

SLUG = 'technology-q4-2026'
esc = lambda t: html.escape(t, quote=False)
norm = lambda t: re.sub(r'[^a-z0-9]+', ' ', t.lower().replace('&', 'and')).strip()

# Build in page order so the sources list keeps the order of first use. The cover and contact pages are print only.
lib.section('Cover')
brief = lib.md(BRIEF)
body = {stem: f() for stem, _, f in PAGES if stem not in ('Main', 'P20')}
body['SRC'] = sources_pages(0, source_groups(), None)[0]

p2a, p2b = body['P02'].split('<h3 class="rh3">Deal market', 1)
p2b = '<h3 class="rh3">Deal market' + p2b
def drop_h3(h): return re.sub(r'<h3 class="rh3">.*?</h3>', '', h, count=1)

AREAS = [('managed-it-cloud', 'Managed IT & Cloud Services', ['P05', 'P06']),
         ('cybersecurity', 'Cybersecurity', ['P07', 'P08']),
         ('telecom-ucaas', 'Telecom & UCaaS', ['P09', 'P10']),
         ('systems-integration', 'Systems Integration', ['P11', 'P12']),
         ('electronics-hardware', 'Electronics & Hardware', ['P13', 'P14']),
         ('government-technology', 'Government Technology', ['P15', 'P16'])]
# Site sections: (anchor, title, blocks).
GROUPS = [('brief', 'The Quarter in Brief', [f'<p class="rlead">{brief}</p>', p2a]),
          ('deal-market', 'Deal Market, Financing and Demand', [p2b, body['P03']]),
          ('policy', 'Policy, Trade and Tax', [body['P04']])]
GROUPS += [(a, t, [body[f] for f in fs]) for a, t, fs in AREAS]
GROUPS += [('valuation', 'Valuation', [body['P17']]),
           ('benchmark', "Benchmark International's Activity", [drop_h3(body['P18'])]),
           ('buyers', 'What Buyers Reward and Discount', [drop_h3(body['P19'])]),
           ('sources', 'Sources', [body['SRC']])]

secs, toc = [], []
for i, (aid, title, blocks) in enumerate(GROUPS, 1):
    inner = ''
    for b in blocks:
        # A label that only repeats the section title is dropped, because the section head already carries it.
        b = re.sub(r'<p class="eyebrow">([^<]*)</p>\n?', lambda m: '' if norm(html.unescape(m.group(1))) == norm(title) else m.group(0), b)
        inner += f'<div class="rblock">{b}</div>\n'
    secs.append(f'<section class="rsec rsec--{aid}" id="{aid}">\n<div class="rsec-head"><span class="rsec-num">{i:02d}</span><h2 class="h2">{esc(title)}</h2></div>\n{inner}</section>')
    toc.append(f'<li><a href="#{aid}"><span>{i:02d}</span>{esc(title)}</a></li>')

root = '../'
PUBLIC = SLUG.rsplit('-', 2)[0] + '-industry-report-' + '-'.join(SLUG.rsplit('-', 2)[1:])  # e.g. healthcare-industry-report-q4-2026
PDF = f'{PUBLIC}.pdf'
dl = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 11l5 5 5-5M5 20h14"/></svg>'
stats = ''.join(f'<div class="stat"><div class="stat-num">{esc(a)}</div><div class="stat-label">{esc(b)}</div></div>' for a, b in FIGS)
desc = 'Q4 2026 M&A sector report for managed IT and cloud services, cybersecurity, telecom and UCaaS, systems integration, electronics and hardware, and government technology, from the Benchmark International Mid-Market team.'
page = site.head('Technology Q4 2026 M&A Sector Report', desc, root).replace('</head>', f'<link rel="stylesheet" href="{root}assets/css/report.css">\n</head>')
page += site.header(root, 'industries')
page += f'''
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Mid-Market</a> / <a href="{root}industries/index.html">Industries</a> / <a href="{root}industries/technology.html">Technology</a> / Q4 2026 Sector Report</div>
    <p class="eyebrow">M&amp;A Sector Report &nbsp;|&nbsp; October 2026</p>
    <h1 class="display">Technology <em>Q4 2026</em></h1>
    <p class="lead">Managed IT and cloud services, cybersecurity, telecom and UCaaS, systems integration, electronics and hardware, and government technology: the deal market, the policy calendar and what buyers are paying for.</p>
    <p class="rbyline">Jared Hardin, Managing Director, Benchmark International</p>
    <div class="btn-row"><a class="btn" href="{PDF}" download>{dl} Download the PDF</a><a class="btn btn--light" href="{root}index.html#form">Discuss Your Business</a></div>
  </div>
</section>

<section class="section--dark section--tight">
  <div class="wrap">
    <div class="stats rhero-stats">{stats}</div>
    <p class="note">Information as of October 5, 2026. Public-company multiples are reference points, and a private company&#39;s price depends on the business itself.</p>
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
        <p class="eyebrow">Considering a transaction in technology?</p>
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
for bad in ('style="position', '/_blob/', 'text-align: justify', 'font-size: 1', '[[', ']]'):
    i = page.find(bad)
    assert i < 0, (bad, page[max(0, i - 200):i + 200])
out = os.path.join(SITE, 'insights', f'{PUBLIC}.html')
open(out, 'w', encoding='utf-8').write(page)
print('wrote', os.path.relpath(out, SITE), round(len(page) / 1024), 'KB', len(secs), 'sections')

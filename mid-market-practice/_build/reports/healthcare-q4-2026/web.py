# Builds the site-native report page from the content in gen.py.
# Usage: python3 web.py   (run gen.py and pdf.py first if the print version or PDF also changed)
import re, os, sys, html
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ROOT, '..', '..', '..'))
sys.path.insert(0, os.path.join(SITE, '_build'))
import build as site

SLUG = 'healthcare-q4-2026'
src = open(os.path.join(ROOT, 'gen.py')).read().split('# ---------- emit ----------')[0]
ns = {'WEB': True, '__file__': os.path.join(ROOT, 'gen.py')}
exec(compile(src, 'gen.py', 'exec'), ns)
body = {fn: b for fn, _, b in ns['pages']}

def chart():
    grp, MAX = ns['grp'], 40.0
    pc = lambda v: f'{v / MAX * 100:.2f}%'
    rows = []
    for name, cs in grp:
        vals = [c[2] for c in cs]; med = ns['MED'][name][0]
        dots = ''.join(f'<i class="dot" style="left:{pc(v)}" title="{html.escape(c[0])} {v:.1f}x"></i>' for c in cs for v in [c[2]])
        rows.append(f'<div class="mrow"><div class="mlabel">{html.escape(name)}</div><div class="mtrack"><i class="mavg" style="left:{pc(7.0)}"></i>'
                    f'<i class="mrange" style="left:{pc(min(vals))};width:{pc(max(vals) - min(vals))}"></i>{dots}'
                    f'<i class="mmed" style="left:{pc(med)}"><b>{med:.1f}x</b></i></div></div>')
    axis = ''.join(f'<span style="left:{pc(v)}">{v}x</span>' for v in (0, 10, 20, 30, 40))
    return ('<div class="mchart" role="img" aria-label="Enterprise value to trailing EBITDA for listed companies in each focus area, with the median marked">'
            + ''.join(rows) + f'<div class="mrow mrow--axis"><div class="mlabel"></div><div class="mtrack maxis">{axis}</div></div>'
            '<p class="mkey"><span><i class="dot"></i> One listed company</span><span><i class="kmed"></i> Median</span><span><i class="kavg"></i> Private mid-market average, all industries, 7.0x</span></p></div>')

def clean(h):
    h = re.sub(r'<img\b[^>]*>', '', h)
    h = re.sub(r'<span style="font-weight: 700">(.*?)</span>', r'<strong>\1</strong>', h)
    h = re.sub(r'<div style="font-size: 1[01](\.\d)?px[^"]*">', '<div class="fine">', h)
    h = re.sub(r'<div style="column-count: 2[^"]*font-size[^"]*">', '<div class="fine cols">', h)
    h = re.sub(r'<div style="[^"]*font-weight: 700; font-size: 9\.5px[^"]*">', '<div class="fine">', h)
    h = re.sub(r'(<(?!col\b)\w+)((?:\s+(?!style=)[\w-]+="[^"]*")*)\s+style="[^"]*"', r'\1\2', h)
    h = re.sub(r'<div>\s*</div>', '', h)
    h = h.replace('@@CHART@@', chart())
    h = re.sub(r'<a href="(https?://[^"]+)"', r'<a target="_blank" rel="noopener" href="\1"', h)
    return ns['esc'](h)

p2a, p2b = body['P02.dc.html'].split('<h3 class="rh3">Deal market', 1)
p2b = '<h3 class="rh3">Deal market' + p2b
def drop_h3(h): return re.sub(r'<h3 class="rh3">.*?</h3>', '', h, count=1)
AREAS = [('provider-services', 'Provider Services', ['P05.dc.html', 'P06.dc.html', 'X-prov']),
         ('life-sciences', 'Life Sciences & Diagnostics', ['P07.dc.html', 'P08.dc.html', 'X-ls']),
         ('medical-products', 'Medical Products & Distribution', ['P09.dc.html', 'P10.dc.html', 'X-mp']),
         ('pharmacy', 'Pharmacy & Healthcare Services', ['P11.dc.html', 'P12.dc.html', 'X-ph'])]
GROUPS = [('brief', 'The Quarter in Brief', [f'<p class="rlead">{ns["BRIEF"]}</p>', p2a]),
          ('deal-market', 'Deal Market and Demand', [p2b, body['P03.dc.html']]),
          ('policy', 'Policy and Price', [body['P04.dc.html'], body['X-policy']])]
GROUPS += [(a, t, [body[f] for f in fs]) for a, t, fs in AREAS]
GROUPS += [('valuation', 'Valuation', [body['P13.dc.html'], body['X-bridge']]),
           ('benchmark', "Benchmark International's Activity", [drop_h3(body['P14.dc.html'])]),
           ('buyers', 'What Buyers Reward and Discount', [drop_h3(body['P15.dc.html'])]),
           ('readiness', 'Seller Readiness', [body['X-ready']]),
           ('sources', 'Sources', [drop_h3(body['P17.dc.html'])])]

secs, toc = [], []
for i, (aid, title, blocks) in enumerate(GROUPS, 1):
    inner = ''
    for b in blocks:
        b = clean(b)
        b = re.sub(r'<p class="eyebrow">' + re.escape(ns['esc'](title)) + r'</p>', '', b)
        inner += f'<div class="rblock">{b}</div>\n'
    secs.append(f'<section class="rsec rsec--{aid}" id="{aid}">\n<div class="rsec-head"><span class="rsec-num">{i:02d}</span><h2 class="h2">{ns["esc"](title)}</h2></div>\n{inner}</section>')
    toc.append(f'<li><a href="#{aid}"><span>{i:02d}</span>{ns["esc"](title)}</a></li>')

root = '../'
PUBLIC = SLUG.rsplit('-', 2)[0] + '-industry-report-' + '-'.join(SLUG.rsplit('-', 2)[1:])  # e.g. healthcare-industry-report-q4-2026
PDF = f'{PUBLIC}.pdf'
dl = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 11l5 5 5-5M5 20h14"/></svg>'
stats = ''.join(f'<div class="stat"><div class="stat-num">{a}</div><div class="stat-label">{b}</div></div>' for a, b in ns['FIGS'])
desc = 'Q4 2026 M&A sector report for healthcare providers, life sciences and diagnostics, medical products and distribution, and pharmacy and healthcare services, from the Benchmark International Mid-Market team.'
page = site.head('Healthcare Q4 2026 M&A Sector Report', desc, root).replace('</head>', f'<link rel="stylesheet" href="{root}assets/css/report.css">\n</head>')
page += site.header(root, 'industries')
page += f'''
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Mid-Market</a> / <a href="{root}industries/index.html">Industries</a> / <a href="{root}industries/healthcare.html">Healthcare</a> / Q4 2026 Sector Report</div>
    <p class="eyebrow">M&amp;A Sector Report &nbsp;|&nbsp; October 2026</p>
    <h1 class="display">Healthcare <em>Q4 2026</em></h1>
    <p class="lead">Provider services, life sciences and diagnostics, medical products and distribution, and pharmacy and healthcare services: the deal market, the policy calendar and what buyers are paying for.</p>
    <p class="rbyline">Jared Hardin, Managing Director, Benchmark International</p>
    <div class="btn-row"><a class="btn" href="{PDF}" download>{dl} Download the PDF</a><a class="btn btn--light" href="{root}index.html#form">Discuss Your Business</a></div>
  </div>
</section>

<section class="section--dark section--tight">
  <div class="wrap">
    <div class="stats rhero-stats">{stats}</div>
    <p class="note">Information as of October 5, 2026. Public-company and larger-platform multiples are reference points, and a private company&#39;s price depends on the business itself.</p>
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
        <p class="eyebrow">Considering a transaction in healthcare?</p>
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
for bad in ('style="position', '/_blob/', '@@'):
    i = page.find(bad)
    assert i < 0, page[max(0, i - 200):i + 200]
out = os.path.join(SITE, 'insights', f'{PUBLIC}.html')
open(out, 'w', encoding='utf-8').write(page)
print('wrote', os.path.relpath(out, SITE), round(len(page) / 1024), 'KB', len(secs), 'sections')

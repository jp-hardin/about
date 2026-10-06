# Builds the site-native report page from content.md.
# Usage: python3 web.py
import os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ROOT, '..', '..', '..'))
sys.path.insert(0, os.path.join(SITE, '_build'))
sys.path.insert(0, ROOT)
import build as site
import report as R


def table(head, rows):
    cols = ''.join(f'<col style="width:{w:.1f}%">' for w in R.col_widths(head, rows, head_room=1.3))
    o = [f'<div class="rtable-wrap"><table class="rtable"><colgroup>{cols}</colgroup><thead><tr>'
         + ''.join(f'<th scope="col">{h}</th>' for h in head) + '</tr></thead><tbody>']
    for r in rows:
        o.append('<tr>' + ''.join(
            (f'<th scope="row" data-label="{R.plain(head[i])}">{c}</th>' if i == 0
             else f'<td data-label="{R.plain(head[i])}">{c}</td>') for i, c in enumerate(r)) + '</tr>')
    o.append('</tbody></table></div>')
    return '\n'.join(o)


def chart():
    pc = lambda v: f'{v / R.CHART_MAX * 100:.2f}%'
    ref_label, ref = R.CHART_REF
    rows = ''.join(
        f'<div class="brow"><div class="blabel">{R.esc(name)}</div>'
        f'<div class="btrack"><i class="bref" style="left:{pc(ref)}"></i><i class="bbar" style="width:{pc(v)}"></i>'
        f'<b style="left:{pc(v)}">{v:.1f}x</b></div></div>' for name, v in R.CHART)
    low, high = min(v for _, v in R.CHART), max(v for _, v in R.CHART)
    return (f'<figure class="bchart" role="img" aria-label="Enterprise value to EBITDA for seven consumer sectors, '
            f'from {low:.1f}x to {high:.1f}x, against {ref:.1f}x for the total US public market">'
            f'{rows}<p class="mkey"><span><i class="kavg"></i> {R.esc(ref_label)}, {ref:.1f}x</span></p>'
            f'<figcaption class="fine">{R.esc(R.CHART_CAPTION)}</figcaption></figure>')


def stats(sid):
    _, _, items = R.BANDS[sid]
    return '<div class="rstats">' + ''.join(
        f'<div class="rstat"><div class="stat-num">{a}</div><div class="rstat-label">{b}</div></div>' for a, b in items) + '</div>'


def render(sec):
    sid, out, first_p = sec['id'], [], True
    if sid == 'sources':
        out.append('<div class="fine">')
    for b in sec['blocks']:
        k = b[0]
        if k == 'p':
            cls = ' class="rlead"' if (sid == 'overview' and first_p) else ''
            out.append(f'<p{cls}>{b[1]}</p>')
            if first_p and sid in R.BANDS:
                out.append(stats(sid))
            first_p = False
        elif k == 'h3':
            out.append(f'<h3 class="rh3">{R.esc(b[1])}</h3>')
        elif k == 'label':
            out.append(f'<h4>{R.esc(b[1])}</h4>' if sid == 'sources' else f'<h4 class="rh4">{R.esc(b[1])}</h4>')
        elif k == 'ul':
            cls = '' if sid == 'sources' else ' class="rlist"'
            out.append(f'<ul{cls}>' + ''.join(f'<li>{x}</li>' for x in b[1]) + '</ul>')
        elif k == 'table':
            out.append(table(b[1], b[2]))
        elif k == 'chart':
            out.append(chart())
    if sid == 'sources':
        out.append('</div>')
    h = '\n'.join(out)
    return re.sub(r'<a href="(https?://[^"]+)"', r'<a target="_blank" rel="noopener" href="\1"', h)


secs, toc = [], []
for i, s in enumerate(R.sections(), 1):
    t = R.esc(s['title'])
    secs.append(f'<section class="rsec rsec--{s["id"]}" id="{s["id"]}">\n<div class="rsec-head"><span class="rsec-num">{i:02d}</span>'
                f'<h2 class="h2">{t}</h2></div>\n<div class="rblock">{render(s)}</div>\n</section>')
    toc.append(f'<li><a href="#{s["id"]}"><span>{i:02d}</span>{t}</a></li>')

root = '../'
PDF = f'{R.SLUG}.pdf'
C = R.CONTACT
dl = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
      'stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 11l5 5 5-5M5 20h14"/></svg>')
stat_html = ''.join(f'<div class="stat"><div class="stat-num">{a}</div><div class="stat-label">{b}</div></div>' for a, b in R.FIGS)
desc = ('Q4 2026 M&A sector report for food and beverage, consumer brands and products, foodservice and distribution, '
        'and consumer services and retail, from the Benchmark International Mid-Market team.')
page = site.head(R.TITLE, desc, root).replace('</head>', f'<link rel="stylesheet" href="{root}assets/css/report.css">\n</head>')
page += site.header(root, 'industries')
page += f'''
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Mid-Market</a> / <a href="{root}industries/index.html">Industries</a> / <a href="{root}industries/consumer.html">Consumer</a> / Q4 2026 Sector Report</div>
    <p class="eyebrow">M&amp;A Sector Report &nbsp;|&nbsp; October 2026</p>
    <h1 class="display">Consumer <em>Q4 2026</em></h1>
    <p class="lead">Food and beverage, consumer brands and products, foodservice and distribution, and consumer services and retail: who is buying, what they are paying for and what an owner can prepare.</p>
    <p class="rbyline">{C["name"]}, {C["role"]}, {C["firm"]}</p>
    <div class="btn-row"><a class="btn" href="{PDF}" download>{dl} Download the PDF</a><a class="btn btn--light" href="{root}index.html#form">Discuss Your Business</a></div>
  </div>
</section>

<section class="section--dark section--tight">
  <div class="wrap">
    <div class="stats rhero-stats">{stat_html}</div>
    <p class="note">{R.NOTE}</p>
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
      <img src="{root}assets/img/team/jared-hardin.jpg" alt="{C["name"]}" width="120" height="120" loading="lazy">
      <div>
        <p class="eyebrow">Considering a transaction in consumer?</p>
        <h3>{C["name"]}</h3>
        <p class="role">{C["role"]}, {C["firm"]}</p>
        <p><a href="tel:{C["tel"]}">{C["phone"]}</a> &nbsp;|&nbsp; <a href="mailto:{C["email"]}">{C["email"]}</a></p>
        <div class="btn-row"><a class="btn" href="{root}index.html#form">Start the Conversation</a><a class="btn btn--ghost" href="{PDF}" download>{dl} Download the PDF</a></div>
      </div>
    </aside>
  </article>
</div>

'''
page += site.cta(root)
page += site.footer(root)
for bad in ('{{', '**', '](http'):
    i = page.find(bad)
    assert i < 0, page[max(0, i - 200):i + 200]
out = os.path.join(SITE, 'reports', f'{R.SLUG}.html')
open(out, 'w', encoding='utf-8').write(page)
print('wrote', os.path.relpath(out, SITE), round(len(page) / 1024), 'KB', len(secs), 'sections')

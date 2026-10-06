# Builds the site-native report page from the print pages in pages/.
# Usage: python3 web.py   (needs beautifulsoup4; run pdf.py as well if the PDF should change)
import re, os, sys, html
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ROOT, '..', '..', '..'))
sys.path.insert(0, os.path.join(SITE, '_build'))
import build as site

SLUG = 'business-services-q4-2026'
esc = lambda t: html.escape(t, quote=False)
norm = lambda t: re.sub(r'[^a-z0-9]+', ' ', t.lower().replace('&', 'and')).strip()

def load(name):
    soup = BeautifulSoup(open(os.path.join(ROOT, 'pages', name + '.dc.html'), encoding='utf-8').read(), 'html.parser')
    root = soup.find('x-dc').find('div', recursive=False)
    for el in root.find_all('div', recursive=False):
        st = el.get('style', '')
        if 'flex-direction: column' in st and 'left: 48px' in st and re.search(r'[^-]height: \d+px', st): return el
    raise SystemExit('no text frame in ' + name)

def st(el): return el.get('style', '') if hasattr(el, 'get') else ''
def kids(el): return [c for c in el.find_all(recursive=False)]

def inline(el):
    h = el.decode_contents().strip()
    h = re.sub(r'\s+style="[^"]*"', '', h)
    h = re.sub(r'<a href="(https?://[^"]+)"', r'<a target="_blank" rel="noopener" href="\1"', h)
    return re.sub(r'\s*\n\s*', ' ', h)

def para(p):
    h = inline(p)
    m = re.match(r'<strong>([^<]+?)\.</strong>\s*', h)
    if m: return f'<h4 class="rh4">{m.group(1)}</h4><p>{h[m.end():]}</p>'
    return f'<p>{h}</p>'

def widths(cols, gap):
    parts = cols.split(); px = [float(p[:-2]) if p.endswith('px') else None for p in parts]
    free = 720 - sum(p for p in px if p) - gap * (len(parts) - 1); nfr = px.count(None) or 1
    w = [p if p else free / nfr for p in px]; tot = sum(w)
    return ''.join(f'<col style="width:{x / tot * 100:.1f}%">' for x in w)

def table(el):
    rows = kids(el); head = rows[0]
    cols = re.search(r'grid-template-columns: ([^;]+)', st(head)).group(1).strip()
    gap = float(re.search(r'column-gap: (\d+)px', st(head)).group(1))
    hs = [inline(c) for c in kids(head)]
    plain = [re.sub(r'<[^>]+>', '', h).replace('"', '&quot;') for h in hs]
    o = [f'<div class="rtable-wrap"><table class="rtable"><colgroup>{widths(cols, gap)}</colgroup><thead><tr>' + ''.join(f'<th scope="col">{h}</th>' for h in hs) + '</tr></thead><tbody>']
    for r in rows[1:]:
        cs = [inline(c) for c in kids(r)]
        if 'font-weight: 700' in st(r): cs = [f'<strong>{c}</strong>' for c in cs]
        o.append('<tr>' + ''.join((f'<th scope="row" data-label="{plain[i]}">{c}</th>' if i == 0 else f'<td data-label="{plain[i]}">{c}</td>') for i, c in enumerate(cs)) + '</tr>')
    o.append('</tbody></table></div>'); return '\n'.join(o)

def band(el):
    out = []
    for s in kids(kids(el)[0]):
        a, b = kids(s); out.append(f'<div class="rstat"><div class="stat-num">{inline(a)}</div><div class="rstat-label">{inline(b)}</div></div>')
    return '<div class="rstats">' + ''.join(out) + '</div>'

def is_table(el):
    k = kids(el)
    return el.name == 'div' and bool(k) and 'border-bottom: 2px solid #B68757' in st(k[0]) and 'grid-template-columns' in st(k[0])

def chart(fig, lists):
    # Row labels and medians are read from the print chart; the dots are read from the company lists beneath it.
    plot = [c for c in kids(fig) if 'position: relative' in st(c)][0]
    labels = [c.get_text(' ', strip=True) for c in kids(plot) if 'width: 190px' in st(c) and c.get_text(strip=True)]
    meds = [float(c.get_text(strip=True)[:-1]) for c in kids(plot) if 'font-weight: 700' in st(c) and re.fullmatch(r'[\d.]+x', c.get_text(strip=True))]
    avg = float(re.search(r'average ([\d.]+)x', plot.get_text(' ', strip=True)).group(1))
    assert len(labels) == len(meds) == len(lists), (labels, meds, list(lists))
    key = {norm(k).split()[0]: v for k, v in lists.items()}
    MAX = 30.0; pc = lambda v: f'{v / MAX * 100:.2f}%'; rows = []
    for name, med in zip(labels, meds):
        cs = key[norm(name).split()[0]]; vals = [v for _, _, v in cs]
        dots = ''.join(f'<i class="dot" style="left:{pc(v)}" title="{html.escape(n)} {v:.1f}x"></i>' for n, _, v in cs)
        rows.append(f'<div class="mrow"><div class="mlabel">{esc(name)}</div><div class="mtrack"><i class="mavg" style="left:{pc(avg)}"></i>'
                    f'<i class="mrange" style="left:{pc(min(vals))};width:{pc(max(vals) - min(vals))}"></i>{dots}'
                    f'<i class="mmed" style="left:{pc(med)}"><b>{med:.1f}x</b></i></div></div>')
    axis = ''.join(f'<span style="left:{pc(v)}">{v}x</span>' for v in (0, 10, 20, 30))
    return ('<div class="mchart" role="img" aria-label="Enterprise value to trailing EBITDA for listed companies in each segment, with the median marked">'
            + ''.join(rows) + f'<div class="mrow mrow--axis"><div class="mlabel"></div><div class="mtrack maxis">{axis}</div></div>'
            f'<p class="mkey"><span><i class="dot"></i> One listed company</span><span><i class="kmed"></i> Median</span><span><i class="kavg"></i> Private mid-market average, all industries, {avg:.1f}x</span></p></div>')

def company_lists(el):
    groups, cur = {}, None
    for col in kids(el):
        for c in kids(col):
            if 'text-transform: uppercase' in st(c): cur = c.get_text(' ', strip=True); groups[cur] = []
            else:
                a = c.find('a'); groups[cur].append((a.get_text(strip=True), a['href'], float(kids(c)[-1].get_text(strip=True)[:-1])))
    return groups

def convert(name, title, drop_h=False):
    out = []; box = load(name); lists = None
    for c in kids(box):
        if 'grid-template-columns: repeat(4, 1fr)' in st(c) and c.find('a'): lists = company_lists(c)
    for c in kids(box):
        s = st(c); txt = c.get_text(' ', strip=True)
        if c.name == 'img': continue
        if c.name == 'h2':
            if not (drop_h or norm(txt) == norm(title)): out.append(f'<h3 class="rh3">{inline(c)}</h3>')
        elif c.name == 'p': out.append(para(c))
        elif c.name == 'figure':
            sub, cap = kids(c)[0], c.find('figcaption')
            out.append(f'<h4 class="rh4">{inline(sub)}</h4>' + chart(c, lists) + f'<p class="fine rcap">{inline(cap)}</p>')
        elif 'text-transform: uppercase' in s and 'font-size: 10.5px' in s:
            nxt = c.find_next_sibling()
            # A label directly above a heading only names the section, which the site section head already does.
            if norm(txt) != norm(title) and not (nxt is not None and nxt.name == 'h2'): out.append(f'<h4 class="rh4">{inline(c)}</h4>')
        elif 'background: #2E2E2E' in s: out.append(band(c))
        elif is_table(c): out.append(table(c))
        elif 'font-style: italic' in str(c) and 'gap: 26px' in s:
            q = [k for k in kids(c) if 'font-style: italic' in st(k)][0]
            out.append(f'<figure class="rquote"><blockquote>{inline(q)}</blockquote></figure>')
        elif 'column-count: 2' in s and 'font-size' not in s:
            out += [para(p) for p in c.find_all('p')]
        elif 'column-count: 2' in s:
            items, o = [], []
            def flush():
                if items: o.append('<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'); items.clear()
            for k in kids(c):
                if k.name == 'p': items.append(inline(k))
                else: flush(); o.append(f'<h4>{inline(k)}</h4>')
            flush(); out.append('\n'.join(o))
        elif lists is not None and 'grid-template-columns: repeat(4, 1fr)' in s:
            out.append('<div class="fine cols">' + ''.join(
                f'<div><strong>{esc(g)}.</strong> ' + ', '.join(f'<a target="_blank" rel="noopener" href="{u}">{esc(n)}</a> {v:.1f}x' for n, u, v in cs) + '</div>'
                for g, cs in lists.items()) + '</div>')
        elif 'display: flex' in s and c.find('p') and 'About the author' not in txt:
            out += [para(p) for p in c.find_all('p')]
        elif 'About the author' in txt: continue
        else: raise SystemExit(f'{name}: unhandled block: {s[:80]} | {txt[:60]}')
    return '\n'.join(out)

# Cover: the opening paragraph and the four headline figures.
cover = load('Main')
BRIEF = inline(cover.find('p'))
FIGS = [(inline(kids(d)[0]), inline(kids(d)[1])) for d in kids([c for c in kids(cover) if 'repeat(4, 1fr)' in st(c)][0])]

# Site sections: (anchor, title, blocks). Each block is a list of print pages that read as one run of text.
GROUPS = [
    ('brief', 'The Quarter in Brief', [['@brief', 'P02']]),
    ('deal-market', 'Deal Market', [['P03', 'P04']]),
    ('commercial-facility', 'Commercial & Facility Services', [['P05', 'P06'], ['P07'], ['P08']]),
    ('marketing-sales-tech', 'Marketing, Sales & Tech-Enabled Services', [['P09', 'P10'], ['P11'], ['P12']]),
    ('engineering', 'Engineering, Architecture & Consulting', [['P13', 'P14'], ['P15']]),
    ('financial-insurance', 'Financial & Insurance Services', [['P16', 'P17'], ['P18']]),
    ('staffing', 'Staffing & Human Capital', [['P19', 'P20'], ['P21']]),
    ('valuation', 'Valuation', [['P22']]),
    ('benchmark', "Benchmark International's Activity", [['P23']]),
    ('buyers', 'What Buyers Reward and Discount', [['P24']]),
    ('readiness', 'Preparing for a Sale', [['P25']]),
    ('sources', 'Sources', [['P26', 'P27', 'P28']]),
]
DROP_H = {'P23', 'P24', 'P26', 'P27', 'P28'}   # pages whose heading repeats the section title

secs, toc = [], []
for i, (aid, title, blocks) in enumerate(GROUPS, 1):
    inner = ''
    for blk in blocks:
        b = '\n'.join(f'<p class="rlead">{BRIEF}</p>' if p == '@brief' else convert(p, title, p in DROP_H) for p in blk)
        if aid == 'sources': b = f'<div class="fine">{b}</div>'
        inner += f'<div class="rblock">{b}</div>\n'
    secs.append(f'<section class="rsec rsec--{aid}" id="{aid}">\n<div class="rsec-head"><span class="rsec-num">{i:02d}</span><h2 class="h2">{esc(title)}</h2></div>\n{inner}</section>')
    toc.append(f'<li><a href="#{aid}"><span>{i:02d}</span>{esc(title)}</a></li>')
body = '\n'.join(secs)

root = '../'
PUBLIC = SLUG.rsplit('-', 2)[0] + '-industry-report-' + '-'.join(SLUG.rsplit('-', 2)[1:])  # e.g. healthcare-industry-report-q4-2026
PDF = f'{PUBLIC}.pdf'
dl = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 11l5 5 5-5M5 20h14"/></svg>'
stats = ''.join(f'<div class="stat"><div class="stat-num">{a}</div><div class="stat-label">{b}</div></div>' for a, b in FIGS)
desc = 'Q4 2026 M&A sector report for commercial and facility services, marketing, sales and tech-enabled services, engineering, architecture and consulting, financial and insurance services, and staffing and human capital, from the Benchmark International Mid-Market team.'
page = site.head('Business Services Q4 2026 M&A Sector Report', desc, root).replace('</head>', f'<link rel="stylesheet" href="{root}assets/css/report.css">\n</head>')
page += site.header(root, 'industries')
page += f'''
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Mid-Market</a> / <a href="{root}industries/index.html">Industries</a> / <a href="{root}industries/business-services.html">Business Services</a> / Q4 2026 Sector Report</div>
    <p class="eyebrow">M&amp;A Sector Report &nbsp;|&nbsp; October 2026</p>
    <h1 class="display">Business Services <em>Q4 2026</em></h1>
    <p class="lead">Commercial and facility services, marketing, sales and tech-enabled services, engineering, architecture and consulting, financial and insurance services, and staffing and human capital: the deal market, public-market valuations and what buyers are paying for.</p>
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
{body}
    <aside class="rauthor">
      <img src="{root}assets/img/team/jared-hardin.jpg" alt="Jared Hardin" width="120" height="120" loading="lazy">
      <div>
        <p class="eyebrow">Considering a transaction in business services?</p>
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
for bad in ('style="position', '/_blob/', 'text-align: justify', 'font-size: 1'):
    i = page.find(bad)
    assert i < 0, page[max(0, i - 200):i + 200]
out = os.path.join(SITE, 'insights', f'{PUBLIC}.html')
open(out, 'w', encoding='utf-8').write(page)
print('wrote', os.path.relpath(out, SITE), round(len(page) / 1024), 'KB', len(secs), 'sections')

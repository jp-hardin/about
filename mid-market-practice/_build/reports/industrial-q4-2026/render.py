# Reads report.md and renders it as class-based HTML blocks shared by the site page (web.py)
# and the downloadable PDF (pdf.py). All report content lives in report.md.
import re, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SLUG = 'industrial-q4-2026'
AS_OF = 'October 6, 2026'

SEGMENTS = [('manufacturing', 'Manufacturing & Industrial Technology'),
            ('distribution', 'Industrial Distribution & Services'),
            ('building', 'Building Products & Construction Services'),
            ('energy', 'Energy, Power & Environmental Services'),
            ('transportation', 'Transportation & Logistics')]

# Hero figures for the site page and the PDF cover spread. Each one also appears, with its source, in report.md.
FIGS = [('54.5', 'ISM Manufacturing PMI in September, the ninth consecutive month of expansion'),
        ('$993B', 'Global M&A value in the third quarter, 41% below the second quarter'),
        ('7.0x', 'Average middle-market purchase multiple in the second quarter, on trailing adjusted EBITDA'),
        ('85', 'Industrial transactions Benchmark International closed in the 24 months to September 30, 2026')]

# Three headline figures shown as a band at the top of each segment. Each one is stated and sourced in that segment's text.
BANDS = {
    'manufacturing': [('$606M', 'US manufacturing technology orders in July, 55.2% above a year earlier'),
                      ('1.39', 'Book-to-bill ratio for North American electronics manufacturing services in August'),
                      ('30,400', 'Openings a year for machinists and tool and die makers, all to replace workers who leave')],
    'distribution': [('12.1%', 'Growth in machinery, equipment and supplies wholesale sales in July'),
                     ('22', 'Acquisitions Pye-Barker Fire & Safety completed in the first half of 2026'),
                     ('10x', 'Trailing adjusted EBITDA, including synergies, that Ferguson paid for FloWorks')],
    'building': [('$2.20T', 'Annual rate of construction spending in August, 1.7% below a year earlier'),
                 ('8.5 months', 'Contractor backlog in August, with one in six contractors doing data center work'),
                 ('3.1%', 'Construction unemployment in August, the lowest on record')],
    'energy': [('224 GW', 'Growth in summer peak demand in the latest 10-year forecast, up from 132'),
               ('160 weeks', 'Lead time for generator step-up transformers in the first quarter'),
               ('9.8x', 'Projected 2026 EBITDA after synergies that Veolia paid for Clean Earth')],
    'transportation': [('11.3%', 'Rise in the Cass truckload linehaul index in August from a year earlier'),
                       ('40.0', 'Logistics Managers\' Index for transportation capacity, the ninth month of contraction'),
                       ('$6.38', 'Average price of a gallon of diesel in the week of September 28')],
}

ISM = [('Oct 25', 48.8), ('Nov 25', 48.0), ('Dec 25', 47.9), ('Jan 26', 52.6), ('Feb 26', 52.4), ('Mar 26', 52.7),
       ('Apr 26', 52.7), ('May 26', 54.0), ('Jun 26', 53.3), ('Jul 26', 55.6), ('Aug 26', 54.6), ('Sep 26', 54.5)]

def esc(s): return html.escape(s, quote=False)

def inline(t):
    t = esc(t)
    def link(m):
        text, url = m.group(1), m.group(2).replace('&amp;', '&')
        ext = '' if url.startswith('mailto:') else ' target="_blank" rel="noopener"'
        return f'<a{ext} href="{html.escape(url, quote=True)}">{text}</a>'
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    return t

def plain(t): return re.sub(r'<[^>]+>', '', t).strip()

def parse(md):
    """Returns {h2 title: [blocks]} and, for the 'Where We Focus' section, {h3 title: [blocks]}."""
    secs, focus, cur, title = {}, {}, None, None
    lines = md.split('\n'); i = 0
    while i < len(lines):
        l = lines[i]
        if not l.strip(): i += 1; continue
        if l.startswith('# '): i += 1; continue
        if l.startswith('## '):
            title = l[3:].strip(); cur = secs.setdefault(title, []); i += 1; continue
        if l.startswith('### '):
            h = l[4:].strip()
            if title == 'Where We Focus': cur = focus.setdefault(h, [])
            else: cur.append(('h3', h))
            i += 1; continue
        if cur is None: i += 1; continue
        if l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            cur.append(('table', (rows[0], [r for r in rows[2:]]))); continue
        if l.startswith(('- ', '* ')):
            items = []
            while i < len(lines) and (lines[i].startswith(('- ', '* ')) or not lines[i].strip()):
                if lines[i].strip(): items.append(lines[i][2:].strip())
                elif not (i + 1 < len(lines) and lines[i + 1].startswith(('- ', '* '))): break
                i += 1
            cur.append(('ul', items)); continue
        if l.startswith('> '): cur.append(('quote', l[2:].strip())); i += 1; continue
        if l.strip() == '{{chart:ism}}': cur.append(('chart', 'ism')); i += 1; continue
        cur.append(('p', l.strip())); i += 1
    return secs, focus

def _weights(head, rows):
    if head[0] == 'Announced': return [13, 30, 22, 35]
    if head[0] == 'Client': return [24, 20, 32, 24]
    w = []
    for k, h in enumerate(head):
        cells = [len(plain(inline(r[k]))) for r in rows if k < len(r)] or [0]
        w.append(min(max(len(h) * 0.9, sum(cells) / len(cells) ** 0.85, 9), 46))
    tot = sum(w); return [x / tot * 100 for x in w]

def table(head, rows):
    dark = head[0] in ('Announced', 'Client', 'Transaction')
    key = 1 if head[0] == 'Announced' else 0   # the cell that names the row
    cols = ''.join(f'<col style="width:{x:.1f}%">' for x in _weights(head, rows))
    o = [f'<div class="rtable-wrap"><table class="rtable{" rtable--dark" if dark else ""}"><colgroup>{cols}</colgroup><thead><tr>'
         + ''.join(f'<th scope="col">{inline(h)}</th>' for h in head) + '</tr></thead><tbody>']
    for r in rows:
        r = r + [''] * (len(head) - len(r))
        tot = ' class="rtotal"' if r[0].startswith('All five') else ''
        o.append(f'<tr{tot}>' + ''.join(
            (f'<th scope="row" data-label="{html.escape(head[k], quote=True)}">{inline(c)}</th>' if k == key
             else f'<td data-label="{html.escape(head[k], quote=True)}">{inline(c)}</td>') for k, c in enumerate(r)) + '</tr>')
    o.append('</tbody></table></div>')
    return '\n'.join(o)

def quote(t):
    m = re.match(r'^"(.*)"\s*\((\[.*\]\(.*\))\)\s*$', t)
    if not m: return f'<figure class="rquote rquote--sp"><blockquote>{inline(t)}</blockquote></figure>'
    return f'<figure class="rquote rquote--sp"><blockquote>&ldquo;{inline(m.group(1))}&rdquo;</blockquote><figcaption>{inline(m.group(2))}</figcaption></figure>'

def chart():
    W, H, left, right, top, base, lo, hi = 760, 300, 46, 736, 30, 240, 46.0, 58.0
    inset = 26
    step = (right - left - 2 * inset) / (len(ISM) - 1)
    x = lambda i: left + inset + i * step
    y = lambda v: base - (v - lo) / (hi - lo) * (base - top)
    path = ' '.join(f'{"M" if i == 0 else "L"}{x(i):.1f},{y(v):.1f}' for i, (_, v) in enumerate(ISM))
    vals = [v for _, v in ISM]; lab = {0, len(ISM) - 1, vals.index(min(vals)), vals.index(max(vals))}
    grid = ''.join(f'<line class="cgrid" x1="{left}" x2="{right}" y1="{y(v):.1f}" y2="{y(v):.1f}"/><text class="caxis" x="{left - 10}" y="{y(v) + 4:.1f}" text-anchor="end">{v}</text>' for v in (46, 50, 54, 58))
    dots = ''.join(f'<g><title>{m}: {v:.1f}</title><circle class="chit" cx="{x(i):.1f}" cy="{y(v):.1f}" r="14"/><circle class="cdot" cx="{x(i):.1f}" cy="{y(v):.1f}" r="4.5"/></g>' for i, (m, v) in enumerate(ISM))
    labels = ''.join(f'<text class="cval" x="{x(i):.1f}" y="{y(v) + (22 if v < 50 else -13):.1f}" text-anchor="middle">{v:.1f}</text>' for i, (m, v) in enumerate(ISM) if i in lab)
    xl = ''.join(f'<text class="caxis" x="{x(i):.1f}" y="{base + 26}" text-anchor="middle">{m}</text>' for i, (m, _) in enumerate(ISM))
    rows = ''.join(f'<tr><th scope="row">{m}</th><td>{v:.1f}</td></tr>' for m, v in ISM)
    return (f'<figure class="rchart"><figcaption><strong>Manufacturing has expanded in every month of 2026</strong>'
            f'<span>ISM Manufacturing PMI, monthly. Readings above 50 indicate expansion.</span></figcaption>'
            f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="ISM Manufacturing PMI from October 2025 to September 2026. It rose from 48.8 to 54.5 and has been above 50 since January 2026.">'
            f'{grid}<line class="cref" x1="{left}" x2="{right}" y1="{y(50):.1f}" y2="{y(50):.1f}"/><text class="caxis" x="{right}" y="{y(50) + 16:.1f}" text-anchor="end">50 = no change</text>'
            f'<path class="cline" d="{path}"/>{dots}{labels}{xl}</svg>'
            f'<details class="rdata"><summary>View the data</summary><table><thead><tr><th scope="col">Month</th><th scope="col">PMI</th></tr></thead><tbody>{rows}</tbody></table></details>'
            f'<p class="fine">Source: Institute for Supply Management, Manufacturing Report On Business, October 2025 to September 2026.</p></figure>')

def band(stats):
    return '<div class="rstats">' + ''.join(f'<div class="rstat"><div class="stat-num">{esc(a)}</div><div class="rstat-label">{esc(b)}</div></div>' for a, b in stats) + '</div>'

def render(blocks, kind=''):
    """kind: 'segment' turns the sub-sector bullets into titled blocks; 'sources' renders the small two-column lists."""
    o, n = [], len(blocks); i = 0
    while i < n:
        k, d = blocks[i]; nxt = blocks[i + 1][0] if i + 1 < n else None
        if k == 'h3':
            m = re.match(r'^(\d\d) (.+)$', d)
            o.append(f'<h3 class="rh3"><span class="rh3-num">{m.group(1)}</span>{inline(m.group(2))}</h3>' if m else f'<h3 class="rh3">{inline(d)}</h3>')
        elif k == 'p':
            only_i = re.fullmatch(r'\*[^*].*[^*]\*', d); only_b = re.fullmatch(r'\*\*[^*]+\*\*', d)
            if only_b: o.append(f'<h4 class="rh4">{inline(d[2:-2])}</h4>')
            elif only_i and nxt == 'table': o.append(f'<h4 class="rh4 rh4--sub">{inline(d[1:-1])}</h4>')
            elif only_i: o.append(f'<p class="{"rlead" if kind == "segment" and i == 0 else "rtag"}">{inline(d[1:-1])}</p>')
            elif d.startswith('**Benchmark International in this segment.**'):
                o.append(f'<div class="rnote"><p class="eyebrow">Benchmark International in this segment</p><p>{inline(d.split("**", 2)[2].strip())}</p></div>')
            else: o.append(f'<p>{inline(d)}</p>')
        elif k == 'ul':
            items = list(d)
            while i + 1 < n and blocks[i + 1][0] == 'ul': items += blocks[i + 1][1]; i += 1
            if kind == 'segment' and all(re.match(r'\*\*[^*]+\.\*\* ', x) for x in items):
                for x in items:
                    m = re.match(r'\*\*([^*]+)\.\*\* (.*)$', x)
                    o.append(f'<div class="rsub"><h4 class="rh4">{inline(m.group(1))}</h4><p>{inline(m.group(2))}</p></div>')
            else: o.append('<ul class="rlist">' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>')
        elif k == 'table': o.append(table(*d))
        elif k == 'quote': o.append(quote(d))
        elif k == 'chart': o.append(chart())
        i += 1
    return '\n'.join(o)

def groups():
    """The twelve sections, in order: (anchor id, title, html)."""
    secs, focus = parse(open(os.path.join(ROOT, 'report.md'), encoding='utf-8').read())
    ov = secs['Overview']
    brief = f'<p class="rlead">{inline(ov[0][1])}</p>\n' + render(ov[1:]) + '\n<p class="eyebrow">At a glance</p>\n' + render(secs['At a Glance'])
    team = '<h3 class="rh3">Your Deal Team</h3>\n' + render(secs['Your Deal Team'])
    src = secs['Sources']
    out = [('brief', 'The Quarter in Brief', brief)]
    out += [(a, t, band(BANDS[a]) + '\n' + render(focus[t], 'segment')) for a, t in SEGMENTS]
    out += [('engagements', 'Recent Industrial Engagements', render(secs['Recent Industrial Engagements'])),
            ('themes', "What We're Seeing in Industrial", render(secs["What We're Seeing in Industrial"])),
            ('buyers', "Seeing Your Company Through a Buyer's Eyes", render(secs["Seeing Your Company Through a Buyer's Eyes"])),
            ('acquirers', 'Who Is Buying', render(secs['Who Is Buying'])),
            ('advisory', 'Advisory Built Around Your Goals', render(secs['Advisory Built Around Your Goals']) + '\n' + team),
            ('sources', 'Sources', f'<p>{inline(src[0][1])}</p>\n<div class="fine">' + render(src[1:], 'sources') + '</div>')]
    return out

if __name__ == '__main__':
    for a, t, h in groups(): print(f'{a:15} {len(h) // 1024:4} KB  {t}')

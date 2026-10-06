"""Building blocks for the Technology Q4 2026 report.

Each block renders two ways. By default it returns the fixed 816 by 1056 print layout
used by the design canvas and the PDF. When WEB is set (web.py does this), the same call
returns semantic, class-based HTML for the site page, styled by assets/css/report.css.
"""
import html, re, json

WEB = False  # web.py sets lib.WEB = True before building the pages

LOGO = '/_blob/a4e9bce348ee211dfa63f50c5b5de181'
WATERMARK = '/_blob/91834fbbbc00b31f5c36c7319ad1e129'
HEADSHOT = '/_blob/a4627b44afa321c0e5263a218e5cb43d'

SERIF = "'Newsreader', 'Le Monde Livre Std', Georgia, serif"
CINZEL = "'Cinzel', 'Trajan Pro', Georgia, serif"
GOLD = '#B68757'
RUNHEAD = 'TECHNOLOGY · Q4 2026'

LINKS = []  # (section, text, url) in order of appearance
_section = ['']


def section(name):
    _section[0] = name


def md(s):
    """Escape text and convert [[label|url]] links."""
    out = []
    pos = 0
    for m in re.finditer(r'\[\[(.+?)\|(.+?)\]\]', s):
        out.append(html.escape(s[pos:m.start()], quote=False))
        label, url = m.group(1), m.group(2)
        LINKS.append((_section[0], label, url))
        ext = ' target="_blank" rel="noopener"' if WEB else ''
        out.append('<a%s href="%s">%s</a>' % (ext, html.escape(url, quote=True), html.escape(label, quote=False)))
        pos = m.end()
    out.append(html.escape(s[pos:], quote=False))
    return ''.join(out)


HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>%(title)s</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500&amp;family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,500;1,6..72,600&amp;family=Quicksand:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>
body{margin:0}
a{color:#8C6239;text-decoration-thickness:.5px;text-underline-offset:2px}a:hover{color:#5E4126}
</style>
</helmet>
<div style="position: relative; width: 816px; height: 1056px; box-sizing: border-box; overflow: hidden; background: #FFFFFF; font-family: 'Quicksand', 'Avenir Next', 'Segoe UI', sans-serif; font-size: 12.5px; line-height: 21px; letter-spacing: 0.4px; color: #333333">
<img src="%(wm)s" alt="" style="position: absolute; left: 310px; top: 600px; width: 506px; height: 718px; opacity: 0.3">
'''

TAIL = '''</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":816,"height":1056}}'>
class Component extends DCLogic {
renderVals() { return {}; }
}
</script>
</body>
</html>
'''

RUN = ('<div style="position: absolute; left: 0; top: 40px; width: 432px; height: 1px; background: #6D7681"></div>\n'
       '<div style="position: absolute; right: 48px; top: 30px; font-family: ' + CINZEL + '; font-size: 12px; line-height: 20px; letter-spacing: 0.8px; color: #6D7681">' + RUNHEAD + '</div>\n')

FOOT = '<div style="position: absolute; left: 0; bottom: 38px; width: 816px; text-align: center; font-weight: 700; font-size: 8.5px; line-height: 12px; letter-spacing: 3.6px">BENCHMARKINTL.COM</div>\n'


def pageno(n):
    return '<div style="position: absolute; right: 48px; bottom: 38px; font-weight: 700; font-size: 8.5px; line-height: 12px; letter-spacing: 2px">%02d</div>\n' % n


def page(title, n, body, gap=14):
    if WEB:
        return body
    return (HEAD % {'title': html.escape(title), 'wm': WATERMARK} + RUN +
            '<div data-fit="890" style="position: absolute; left: 48px; top: 76px; width: 720px; height: 890px; display: flex; flex-direction: column; gap: %dpx">\n' % gap +
            body + '\n</div>\n' + FOOT + pageno(n) + TAIL)


def kicker(t):
    if WEB:
        return '<p class="eyebrow">%s</p>' % md(t)
    return '<div style="font-weight: 700; font-size: 10.5px; line-height: 16px; letter-spacing: 2.6px; text-transform: uppercase">%s</div>' % md(t)


def h2(t, mt=0):
    if WEB:
        return '<h3 class="rh3">%s</h3>' % md(t)
    return '<h2 style="margin: %dpx 0 0; font-family: %s; font-weight: 600; font-size: 21px; line-height: 27px; letter-spacing: 0; color: %s; text-wrap: balance">%s</h2>' % (mt, SERIF, GOLD, md(t))


def p(t, extra=''):
    if WEB:
        return '<p>%s</p>' % md(t)
    return '<p style="margin: 0; text-align: justify%s">%s</p>' % (extra, md(t))


def colp(t):
    if WEB:
        return '<p>%s</p>' % md(t)
    return '<p style="margin: 0 0 14px">%s</p>' % md(t)


def columns(parts, split=None):
    if WEB:
        return '\n'.join(parts)
    if split is None:
        split = (len(parts) + 1) // 2
    col = '<div data-col="1" style="width: 344px; display: flex; flex-direction: column; text-align: justify">%s</div>'
    return '<div style="display: flex; gap: 32px; align-items: flex-start">' + col % ''.join(parts[:split]) + col % ''.join(parts[split:]) + '</div>'


def quote(text, attribution):
    if WEB:
        return '<figure class="rquote"><blockquote>&ldquo;%s&rdquo;</blockquote><figcaption>%s</figcaption></figure>' % (html.escape(text, quote=False), md(attribution))
    return ('<div style="break-inside: avoid; display: flex; flex-direction: column; margin: 2px 0 18px; padding: 16px 0 14px; border-top: 1px solid %s; border-bottom: 1px solid %s; text-align: left">'
            '<div style="font-family: %s; font-style: italic; font-weight: 500; font-size: 15.5px; line-height: 24px; letter-spacing: 0; color: #333333">&ldquo;%s&rdquo;</div>'
            '<div style="margin-top: 6px; font-size: 10.5px; line-height: 15px; letter-spacing: 0.3px">%s</div></div>') % (GOLD, GOLD, SERIF, html.escape(text, quote=False), md(attribution))


def _plain(t):
    return re.sub(r'<[^>]+>', '', t).replace('"', '&quot;').strip()


def _widths(cols, gap=14):
    parts = cols.split()
    px = [float(c[:-2]) if c.endswith('px') else None for c in parts]
    free = 720 - sum(c for c in px if c) - gap * (len(parts) - 1)
    nfr = px.count(None) or 1
    w = [c if c else free / nfr for c in px]
    tot = sum(w)
    return ''.join('<col style="width:%.1f%%">' % (x / tot * 100) for x in w)


def _web_table(cols, header, rows):
    head = [md(h) for h in header]
    o = ['<div class="rtable-wrap"><table class="rtable"><colgroup>%s</colgroup><thead><tr>%s</tr></thead><tbody>' % (
        _widths(cols), ''.join('<th scope="col">%s</th>' % h for h in head))]
    for r in rows:
        cells = [md(c) for c in r]
        o.append('<tr>' + ''.join(('<th scope="row" data-label="%s">%s</th>' if i == 0 else '<td data-label="%s">%s</td>') % (_plain(head[i]), c)
                                  for i, c in enumerate(cells)) + '</tr>')
    o.append('</tbody></table></div>')
    return '\n'.join(o)


def table(cols, header, rows, pad=5):
    if WEB:
        return _web_table(cols, header, rows)
    g = 'display: grid; grid-template-columns: %s; column-gap: 14px' % cols
    out = ['<div style="font-size: 12px; line-height: 17px; letter-spacing: 0.2px">']
    out.append('<div style="%s; padding: 0 0 7px; border-bottom: 2px solid %s; font-weight: 700; font-size: 9.5px; line-height: 14px; letter-spacing: 1.6px; text-transform: uppercase; align-items: end">%s</div>' % (
        g, GOLD, ''.join('<div>%s</div>' % md(h) for h in header)))
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            cells.append('<div%s>%s</div>' % (' style="font-weight: 700"' if i == 0 else '', md(c)))
        out.append('<div style="%s; padding: %dpx 0; border-bottom: 1px solid #D9D3CA">%s</div>' % (g, pad, ''.join(cells)))
    out.append('</div>')
    return '\n'.join(out)


def note(t):
    """Fine print under a table or chart."""
    if WEB:
        return '<p class="fine">%s</p>' % md(t)
    return '<div style="font-size: 10.5px; line-height: 15px; letter-spacing: 0.2px">%s</div>' % md(t)


def stat(num, label):
    return ('<div style="display: flex; flex-direction: column; gap: 4px"><div style="font-family: %s; font-weight: 600; font-size: 30px; line-height: 34px; letter-spacing: 0; color: %s">%s</div>'
            '<div style="font-size: 11px; line-height: 15px; letter-spacing: 0.3px">%s</div></div>') % (SERIF, GOLD, html.escape(num), md(label))


# ---------- photographs (approved library copies in assets/img/industries/technology) ----------
COVER_PHOTO = '/_blob/151e0ff33db32361cea2a3f8a833e3e9'      # rpt-cover-datacenter.jpg
PREP_PHOTO = '/_blob/c8d2f2cd3c854c01714578371dfe2936'       # rpt-laptop-repair.jpg
CONTACT_PHOTO = '/_blob/c32355433303fcff161324c3a5b9388d'    # rpt-team-laptops.jpg
# Photo shown at the right of each segment's dark stat band.
BAND_PHOTOS = {
    'cloud': '/_blob/cddf308fc92bfee28a88f35f8cf7ca67',      # rpt-server-racks.jpg
    'shield': '/_blob/643493205d756d338b787cd3b5150ce7',     # rpt-keyboard.jpg
    'tower': '/_blob/a2ae072ce129acce7f045e44978fe69e',      # rpt-telecom-masts.jpg
    'integrate': '/_blob/e5a9e07bcb6a0f7f6dfde3725f5af1c7',  # rpt-network-cables.jpg
    'chip': '/_blob/c2db878093ab396ade901a47de706d38',       # rpt-circuit-board.jpg
    'gov': '/_blob/7c2230130aa40114760060efc60c52a4',        # rpt-satellite-dish.jpg
}


def band_icon(name, alt):
    return ('<div style="position: relative; flex: none; width: 236px; height: 112px">'
            '<img src="%s" alt="%s" style="display: block; width: 236px; height: 112px; object-fit: cover">'
            '<div style="position: absolute; inset: 0; background: linear-gradient(90deg, #2E2E2E 0%%, rgba(46,46,46,0) 22%%)"></div></div>') % (BAND_PHOTOS[name], html.escape(alt))


def band(stats, icon, alt):
    if WEB:
        return '<div class="rstats">' + ''.join('<div class="rstat"><div class="stat-num">%s</div><div class="rstat-label">%s</div></div>' % (html.escape(a), md(b)) for a, b in stats) + '</div>'
    return ('<div style="margin: 4px 0; display: flex; align-items: center; background: #2E2E2E; color: #FFFFFF">'
            '<div style="flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 18px; padding: 0 8px 0 20px">%s</div>%s</div>') % (
        ''.join(stat(a, b) for a, b in stats), band_icon(icon, alt))

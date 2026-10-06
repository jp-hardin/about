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
CHECKLIST = '/_blob/b641387ad8b11c9fb645cb0345a01723'
AGREEMENT = '/_blob/23a72c95665d08641203d0333db6e463'

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


# ---------- line illustrations (160 x 160 design box) ----------
L = '#D9D3CA'
ICONS = {
 'cloud': ('<path d="M50 80a20 20 0 0 1 2-40 28 28 0 0 1 54 4 18 18 0 0 1 4 36z" stroke="%(L)s"></path>'
           '<path d="M80 80v12" stroke="%(G)s"></path>'
           '<rect x="40" y="92" width="80" height="18" rx="3" stroke="%(L)s"></rect><rect x="40" y="118" width="80" height="18" rx="3" stroke="%(L)s"></rect>'
           '<circle cx="52" cy="101" r="3" stroke="%(G)s"></circle><circle cx="52" cy="127" r="3" stroke="%(G)s"></circle>'
           '<path d="M64 101h44M64 127h44" stroke="%(G)s"></path>'),
 'shield': ('<path d="M80 18l46 16v36c0 34-22 56-46 66-24-10-46-32-46-66V34z" stroke="%(L)s"></path>'
            '<rect x="62" y="70" width="36" height="30" rx="4" stroke="%(G)s"></rect>'
            '<path d="M68 70V60a12 12 0 0 1 24 0v10" stroke="%(G)s"></path>'
            '<path d="M80 80v10" stroke="%(G)s" stroke-width="4"></path>'),
 'tower': ('<path d="M80 42L56 138M80 42l24 96M71 78h18M65 104h30M59 126h42" stroke="%(L)s"></path>'
           '<circle cx="80" cy="34" r="6" stroke="%(G)s"></circle>'
           '<path d="M60 20a26 26 0 0 0 0 28M100 20a26 26 0 0 1 0 28M46 10a44 44 0 0 0 0 48M114 10a44 44 0 0 1 0 48" stroke="%(G)s"></path>'),
 'integrate': ('<rect x="30" y="22" width="100" height="62" rx="5" stroke="%(L)s"></rect>'
               '<path d="M70 84v12M90 84v12M58 98h44" stroke="%(L)s"></path>'
               '<circle cx="56" cy="54" r="5" stroke="%(G)s"></circle><circle cx="80" cy="40" r="5" stroke="%(G)s"></circle><circle cx="104" cy="54" r="5" stroke="%(G)s"></circle><circle cx="80" cy="68" r="5" stroke="%(G)s"></circle>'
               '<path d="M60 51l16-9M84 42l16 9M100 57l-16 9M76 66l-16-9" stroke="%(G)s"></path>'
               '<path d="M44 122v-10h72v10M80 112v-14" stroke="%(L)s"></path>'
               '<rect x="34" y="122" width="20" height="18" rx="2" stroke="%(L)s"></rect><rect x="70" y="122" width="20" height="18" rx="2" stroke="%(L)s"></rect><rect x="106" y="122" width="20" height="18" rx="2" stroke="%(L)s"></rect>'),
 'chip': ('<rect x="46" y="46" width="68" height="68" rx="6" stroke="%(L)s"></rect>'
          '<rect x="64" y="64" width="32" height="32" rx="3" stroke="%(G)s"></rect>'
          '<path d="M58 46V30M73 46V30M87 46V30M102 46V30M58 114v16M73 114v16M87 114v16M102 114v16M46 58H30M46 73H30M46 87H30M46 102H30M114 58h16M114 73h16M114 87h16M114 102h16" stroke="%(L)s"></path>'
          '<path d="M72 80h16M80 72v16" stroke="%(G)s"></path>'),
 'gov': ('<path d="M24 62L80 26l56 36z" stroke="%(L)s"></path>'
         '<path d="M30 70h100M42 72v44M62 72v44M98 72v44M118 72v44M26 122h108M18 136h124" stroke="%(L)s"></path>'
         '<circle cx="80" cy="46" r="5" stroke="%(G)s"></circle>'
         '<path d="M80 78v32" stroke="%(G)s"></path><circle cx="80" cy="78" r="3" stroke="%(G)s"></circle><circle cx="80" cy="110" r="3" stroke="%(G)s"></circle>'
         '<path d="M70 94h20" stroke="%(G)s"></path>'),
}


def icon_group(name, x, y, scale):
    return ('<g transform="translate(%s,%s) scale(%s)" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' % (x, y, scale)
            + ICONS[name] % {'L': L, 'G': GOLD} + '</g>')


def band_icon(name, alt):
    return ('<svg role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 236 112" width="236" height="112" style="display: block; width: 236px; height: 112px">'
            '<rect width="236" height="112" fill="#2E2E2E"></rect>%s'
            '<path d="M14 92h46M176 92h46" stroke="%s" stroke-width="1.5"></path></svg>') % (html.escape(alt), icon_group(name, 68, 6, 0.62), GOLD)


def band(stats, icon, alt):
    if WEB:
        return '<div class="rstats">' + ''.join('<div class="rstat"><div class="stat-num">%s</div><div class="rstat-label">%s</div></div>' % (html.escape(a), md(b)) for a, b in stats) + '</div>'
    return ('<div style="margin: 4px 0; display: flex; align-items: center; background: #2E2E2E; color: #FFFFFF">'
            '<div style="flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 18px; padding: 0 8px 0 20px">%s</div>%s</div>') % (
        ''.join(stat(a, b) for a, b in stats), band_icon(icon, alt))

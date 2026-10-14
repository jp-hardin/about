# Builds a sector report from its PowerPoint sector report: the downloadable PDF and the site page come
# from the same .pptx, so the two always match.
#
# Usage: python3 brief.py <report-folder>     e.g. python3 brief.py industrial-q4-2026
#
# The folder holds the deck (brief.pptx) and brief.json:
#   {"lead": "<the cover's summary sentence, as written on the cover>"}
# The sector and quarter come from the folder name.
#
# What it writes:
#   insights/<sector>-sector-report-q<N>-<year>.pdf    the deck, converted by LibreOffice
#   insights/<sector>-sector-report-q<N>-<year>.html   the site page: every page of the deck as an image with its
#                                                      links live, plus the page's full text, tables and chart data
#   assets/img/reports/<sector>-sector-report-q<N>-<year>/p01.webp ...   the page images
#
# Needs LibreOffice (soffice) with Impress, poppler-utils (pdftoppm) and pip packages python-pptx, pypdf, Pillow.
# The deck fonts (Calibri and Cambria stand-ins, Quicksand, Newsreader, Cinzel) are in brief-fonts/ and are
# loaded for the conversion only, so nothing needs installing system-wide.
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
import html, io, json, os, re, shutil, subprocess, sys, tempfile
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER
from pptx.util import Emu
from pypdf import PdfReader, PdfWriter
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(SITE, '_build'))
import build as site  # noqa: E402

FOLDER = os.path.join(HERE, sys.argv[1].strip('/'))
SLUG = os.path.basename(FOLDER)                                   # industrial-q4-2026
SECTOR = SLUG.rsplit('-', 2)[0]                                   # industrial
QUARTER, YEAR = SLUG.rsplit('-', 2)[1:]                           # q4, 2026
PUBLIC = f'{SECTOR}-sector-report-{QUARTER}-{YEAR}'
PERIOD = f'{QUARTER.upper()} {YEAR}'
NAME = site.SECTOR_BY_SLUG[SECTOR]['name']
CONF = json.load(open(os.path.join(FOLDER, 'brief.json'), encoding='utf-8'))
IMG_DIR = f'assets/img/reports/{PUBLIC}'

# Corrections applied to a working copy of the deck before anything is built, so the deck itself stays as supplied.
# Site style: no em dashes. Links to the old report addresses go straight to the current ones.
TEXT_FIXES = [('” — ', '” '), (' — ', ', '), ('—', ', ')]
LINK_FIXES = [('-industry-report-', '-sector-report-'), ('/mid-market-practice/industries/', '/mid-market-practice/sectors/')]

esc = html.escape


# ─── 1. Working copy of the deck ─────────────────────────────────────────────
def corrected_deck(dst):
    prs = Presentation(os.path.join(FOLDER, 'brief.pptx'))
    fixed = 0
    for slide in prs.slides:
        for sh in all_shapes(slide.shapes):
            frames = [sh.text_frame] if sh.has_text_frame else []
            if getattr(sh, 'has_table', False) and sh.has_table:
                frames += [c.text_frame for r in sh.table.rows for c in r.cells]
            for tf in frames:
                for p in tf.paragraphs:
                    for r in p.runs:
                        t = r.text
                        for a, b in TEXT_FIXES:
                            t = t.replace(a, b)
                        if t != r.text:
                            r.text, fixed = t, fixed + 1
        for rel in slide.part.rels.values():
            if rel.is_external:
                t = rel._target
                for a, b in LINK_FIXES:
                    t = t.replace(a, b)
                if t != rel._target:
                    rel._target, fixed = t, fixed + 1
    prs.save(dst)
    print('corrections applied to the working copy:', fixed)
    return prs


def all_shapes(shapes):
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from all_shapes(sh.shapes)
        else:
            yield sh


# ─── 2. PDF ──────────────────────────────────────────────────────────────────
def convert(pptx, tmp):
    fonts = os.path.join(HERE, 'brief-fonts')
    conf = os.path.join(tmp, 'fonts.conf')
    open(conf, 'w').write(f'<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'
                          f'<include ignore_missing="yes">/etc/fonts/fonts.conf</include><dir>{esc(fonts)}</dir>'
                          f'<cachedir>{esc(tmp)}/fc-cache</cachedir></fontconfig>')
    env = dict(os.environ, FONTCONFIG_FILE=conf, HOME=tmp)
    subprocess.run(['soffice', f'-env:UserInstallation=file://{tmp}/lo', '--headless', '--convert-to', 'pdf',
                    '--outdir', tmp, pptx], check=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    out = os.path.splitext(pptx)[0] + '.pdf'
    assert os.path.exists(out), 'LibreOffice did not write a PDF (is libreoffice-impress installed?)'
    used = subprocess.run(['pdffonts', out], capture_output=True, text=True).stdout
    for bad in ('DejaVu', 'Liberation'):
        assert bad not in used, f'a deck font was substituted with {bad}; check brief-fonts/\n{used}'
    return out


def write_pdf(src):
    r = PdfReader(src)
    w = PdfWriter(clone_from=r)
    w.add_metadata({
        '/Title': f'{NAME} {PERIOD} M&A Sector Report | Benchmark International',
        '/Author': 'Jared Hardin, Benchmark International',
        '/Subject': f'{NAME} mergers and acquisitions: deal activity, valuations and what buyers are paying for, {PERIOD}',
        '/Keywords': f'{NAME} M&A, {NAME} mergers and acquisitions, middle market, sell-side M&A, valuation multiples, {PERIOD}, Benchmark International',
        '/Creator': 'Benchmark International',
    })
    w.compress_identical_objects()
    out = os.path.join(SITE, 'insights', f'{PUBLIC}.pdf')
    with open(out, 'wb') as f:
        w.write(f)
    print('wrote', os.path.relpath(out, SITE), round(os.path.getsize(out) / 1024), 'KB', len(r.pages), 'pages')
    return r


def page_links(reader):
    """Link areas on each PDF page as (left %, top %, width %, height %, url)."""
    out = []
    for p in reader.pages:
        W, H = float(p.mediabox.width), float(p.mediabox.height)
        links = []
        for a in p.get('/Annots') or []:
            a = a.get_object()
            act = a.get('/A')
            url = act.get('/URI') if act else None
            if not url:
                continue
            x1, y1, x2, y2 = (float(v) for v in a['/Rect'])
            links.append((min(x1, x2) / W * 100, (H - max(y1, y2)) / H * 100, abs(x2 - x1) / W * 100, abs(y2 - y1) / H * 100, str(url)))
        out.append(links)
    return out


def write_images(pdf, tmp, n):
    dst = os.path.join(SITE, IMG_DIR)
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(dst)
    subprocess.run(['pdftoppm', '-r', '160', '-png', pdf, os.path.join(tmp, 'pg')], check=True)
    pngs = sorted(f for f in os.listdir(tmp) if f.startswith('pg') and f.endswith('.png'))
    assert len(pngs) == n, (len(pngs), n)
    size = None
    for i, f in enumerate(pngs, 1):
        im = Image.open(os.path.join(tmp, f)).convert('RGB')
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        size = im.size
        im.save(os.path.join(dst, f'p{i:02d}.webp'), 'WEBP', quality=80, method=6)
        im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS).save(os.path.join(dst, f'p{i:02d}-800.webp'), 'WEBP', quality=78, method=6)
    total = sum(os.path.getsize(os.path.join(dst, f)) for f in os.listdir(dst))
    print('wrote', n * 2, 'page images to', IMG_DIR, round(total / 1024), 'KB')
    return size


# ─── 3. Text of each page ────────────────────────────────────────────────────
def link(url, inner):
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{inner}</a>' if url.startswith('http') else f'<a href="{esc(url)}">{inner}</a>'


A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'


def runs_html(par):
    """A paragraph's runs as HTML, keeping bold, italics, links and line breaks."""
    out = []
    runs = {id(r._r): r for r in par.runs}
    for el in par._p:
        if el.tag == A + 'br':
            out.append('<br>')
            continue
        if el.tag == A + 'fld':
            t = el.findtext(A + 't') or ''
            out.append(esc(t))
            continue
        r = runs.get(id(el))
        if r is None:
            continue
        t = esc(r.text).replace('\x0b', '<br>')
        if not t:
            continue
        if r.font.bold and t.strip():
            t = f'<strong>{t}</strong>'
        if r.font.italic and t.strip():
            t = f'<em>{t}</em>'
        url = r.hyperlink.address if r.hyperlink and r.hyperlink.address else None
        out.append(link(url, t) if url else t)
    h = ''.join(out)
    h = re.sub(r'</strong>(\s*)<strong>', r'\1', h)
    return re.sub(r'^(<br>)+|(<br>)+$', '', h.strip()).strip()


def is_label(text):
    letters = [c for c in text if c.isalpha()]
    return text == text.upper() and len(text) < 90 and len(letters) > 2


def size_of(par):
    for r in par.runs:
        if r.font.size:
            return r.font.size.pt
    return None


def tf_html(tf, title=False):
    out = []
    for p in tf.paragraphs:
        text = ''.join(r.text for r in p.runs).strip()
        if not text:
            continue
        inner = runs_html(p)
        if is_label(text):
            out.append(f'<p class="bk-label">{inner}</p>')
        elif (size_of(p) or 0) >= 15 and len(text) < 140 and not title:
            out.append(f'<h3 class="bk-h">{inner}</h3>')
        elif p.level and p.level > 0 or (p._p.pPr is not None and p._p.pPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}buChar') is not None):
            out.append(f'<li>{inner}</li>')
        else:
            out.append(f'<p>{inner}</p>')
    h = '\n'.join(out)
    return re.sub(r'((?:<li>.*?</li>\n?)+)', lambda m: '<ul>' + m.group(1).strip() + '</ul>', h)


def table_html(tbl):
    rows = []
    for i, row in enumerate(tbl.rows):
        cells = []
        for c in row.cells:
            if c.is_spanned:
                continue
            inner = '<br>'.join(runs_html(p) for p in c.text_frame.paragraphs if p.runs and ''.join(r.text for r in p.runs).strip())
            tag = 'th' if i == 0 else 'td'
            span = f' colspan="{c.span_width}"' if c.span_width > 1 else ''
            cells.append(f'<{tag}{span}>{inner}</{tag}>')
        if any(re.sub(r'<[^>]+>', '', x) for x in cells):
            rows.append('<tr>' + ''.join(cells) + '</tr>')
    if not rows:
        return ''
    return f'<div class="bk-table"><table><thead>{rows[0]}</thead><tbody>{"".join(rows[1:])}</tbody></table></div>'


NS = {'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart'}


def fmt(v, code):
    """Formats a chart value with its Excel number format (the common cases used in the decks)."""
    if v is None:
        return ''
    secs = (code or 'General').split(';')
    sec = secs[0]
    neg = ''
    if v < 0:
        if len(secs) > 1:
            sec, v = secs[1], -v
        else:
            neg = '-'
            v = -v
    m = re.match(r'^((?:"[^"]*"|\\.|[$€£+−-])*)(.*?)((?:"[^"]*"|\\.|[%xX ])*)$', sec)
    pre, core, post = (m.group(1), m.group(2), m.group(3)) if m else ('', sec, '')
    pct = '%' in re.sub(r'"[^"]*"', '', post)
    unq = lambda t: re.sub(r'"([^"]*)"', r'\1', t).replace('\\', '')
    pre, post = unq(pre), unq(post)
    dec = len(core.split('.')[1].rstrip('#').replace(',', '')) if '.' in core else 0
    if core in ('General', ''):
        dec = 0 if float(v).is_integer() else min(2, len(repr(float(v)).split('.')[1]))
    scale = len(core) - len(core.rstrip(','))          # each trailing comma divides by 1,000
    core = core.rstrip(',')
    x = v * 100 if pct else v / 1000 ** scale
    # Excel rounds half up on the value as displayed to 15 significant digits
    x = float(Decimal(f'{x:.15g}').quantize(Decimal(1).scaleb(-dec), ROUND_HALF_UP))
    num = f'{x:,.{dec}f}' if ',' in core or abs(x) >= 10000 else f'{x:.{dec}f}'
    return neg + pre + num + post


def excel_date(serial, code):
    d = date(1899, 12, 30) + timedelta(days=int(serial))
    code = re.sub(r'"[^"]*"|\\.', '', code.split(';')[0]).lower()
    if 'mmm' in code:
        return d.strftime('%b %Y' if 'yyyy' in code else "%b '%y" if 'yy' in code else '%b')
    if 'yy' in code and 'm' not in code:
        return d.strftime('%Y')
    return d.strftime('%m/%Y')


def chart_html(ch):
    try:
        plot = ch.plots[0]
    except IndexError:
        return ''
    cats = [str(c) for c in plot.categories]
    cat_code = (ch._chartSpace.xpath('.//c:dateAx/c:numFmt/@formatCode | .//c:catAx/c:numFmt/@formatCode')
                or [c.text for c in plot._element.xpath('./c:ser[1]/c:cat//c:formatCode')])
    cat_code = next((c for c in cat_code if c and c != 'General'), '')
    if cats and re.search(r'[ym]', cat_code or '') and all(re.fullmatch(r'\d+(\.0)?', c) for c in cats):
        cats = [excel_date(float(c), cat_code) for c in cats]
    series = []
    for p in ch.plots:
        for s in p.series:
            # the format the chart shows: data labels first, then the value axis, then the source cells
            codes = [c for c in (s._element.xpath('./c:dLbls/c:numFmt/@formatCode') + p._element.xpath('./c:dLbls/c:numFmt/@formatCode')
                                 + s._element.xpath('./c:dLbls/c:dLbl/c:numFmt/@formatCode') + ch._chartSpace.xpath('.//c:valAx/c:numFmt/@formatCode')
                                 + [c.text for c in s._element.xpath('./c:val//c:formatCode')]) if c and c != 'General'] or ['General']
            pts = {int(pt.get('idx')): pt.find('c:v', NS).text for pt in s._element.xpath('./c:val//c:pt')}
            vals = [float(pts[i]) if pts.get(i) not in (None, '') else None for i in range(len(cats))]
            series.append((s.name or '', vals, codes[0] if codes else 'General'))
    if not cats or not series:
        return ''
    title = ''
    if ch.has_title and ch.chart_title.has_text_frame:
        title = esc(ch.chart_title.text_frame.text.strip())
    many = len(cats) > 14 and len(series) <= 3   # long time series read better down the page than across it
    head = '<tr><th>' + ('' if len(series) > 1 or not series[0][0] else '') + '</th>' + ''.join(f'<th>{esc(n)}</th>' for n, _, _ in series) + '</tr>'
    body = ''.join('<tr><th>' + esc(c) + '</th>' + ''.join(f'<td>{fmt(vals[i] if i < len(vals) else None, code)}</td>' for _, vals, code in series) + '</tr>'
                   for i, c in enumerate(cats))
    cap = f'<caption>Chart data{": " + title if title else ""}</caption>'
    tbl = f'<div class="bk-table bk-chart{" bk-chart--long" if many else ""}"><table>{cap}<thead>{head}</thead><tbody>{body}</tbody></table></div>'
    if many:
        return f'<details class="bk-more"><summary>Chart data{": " + title if title else ""} ({len(cats)} values)</summary>{tbl}</details>'
    return tbl


SKIP_ALT = {'Benchmark International'} | {m[0] for m in site.TEAM_LEAD + site.TEAM_SUPPORT}


def logo_name(pic):
    """The company name on a logo image, from its alt text. Photos (described in a sentence), file names and the
    Benchmark International mark are left out."""
    alt = (pic._element.xpath('./p:nvPicPr/p:cNvPr')[0].get('descr') or '').strip()
    if not alt or '/' in alt or re.search(r'\.(png|jpe?g|svg)$', alt, re.I) or alt in SKIP_ALT:
        return ''
    words = re.findall(r"[A-Za-z][\w'’]*", alt)
    return alt if words and all(w[0].isupper() for w in words) and len(alt) <= 48 else ''


def slide_parts(slide, H, cover=False):
    """(title, subtitle, body html, footnote html) for one slide, in the order the deck reads."""
    title = subtitle = ''
    body, foot, part = [], [], []

    def visit(shapes):
        nonlocal title, subtitle
        for sh in shapes:
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                visit(sh.shapes)
                continue
            top = sh.top or 0
            if sh.is_placeholder and sh.placeholder_format.type in (PP_PLACEHOLDER.SLIDE_NUMBER, PP_PLACEHOLDER.DATE, PP_PLACEHOLDER.FOOTER):
                continue
            if getattr(sh, 'has_chart', False) and sh.has_chart:
                body.append(chart_html(sh.chart))
                continue
            if getattr(sh, 'has_table', False) and sh.has_table:
                body.append(table_html(sh.table))
                continue
            if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
                alt = logo_name(sh)
                if alt:
                    body.append(f'<p class="bk-logo">{esc(alt)}</p>')
                continue
            if not sh.has_text_frame:
                continue
            text = sh.text_frame.text.strip()
            if not text:
                continue
            if not cover and top < Emu(914400 * 0.5) and (is_label(text) or re.fullmatch(r'Q\d \d{4}', text)):
                continue                                   # running header
            if re.fullmatch(r'\d{1,2}', text) and top > H * 0.9:
                continue                                   # page number
            if re.fullmatch(r'0\d', text):
                part.append(text)                          # the large 01, 02, 03 on a part's opening page
                continue
            if not cover and not title and (top < H * 0.25 or part) and not is_label(text) and len(text) < 120:
                title = text
                continue
            if not cover and title and not subtitle and not body and not part and top < H * 0.25 and not is_label(text):
                subtitle = runs_html(sh.text_frame.paragraphs[0]) if len(sh.text_frame.paragraphs) == 1 else tf_html(sh.text_frame, True)
                continue
            h = tf_html(sh.text_frame)
            dst = foot if top > H * 0.9 else body
            if not dst or dst[-1] != h:
                dst.append(h)

    visit(slide.shapes)
    return title, subtitle, '\n'.join(x for x in body if x), '\n'.join(foot), (part[0] if part else None)


# ─── 4. Site page ────────────────────────────────────────────────────────────
def plain(h):
    return html.unescape(re.sub(r'<[^>]+>', '', h))


def build_page(prs, links, img_size):
    H = prs.slide_height
    slides = [slide_parts(s, H, cover=(n == 0)) for n, s in enumerate(prs.slides)]
    deck_text = ' '.join(plain(t + ' ' + s + ' ' + b + ' ' + f) for t, s, b, f, _ in slides)
    norm = lambda t: re.sub(r'\s+', ' ', t.replace('\xa0', ' '))
    assert norm(CONF['lead']) in norm(deck_text), 'brief.json "lead" must be copied from the cover'
    byline = next((m.group(0) for m in [re.search(r'October \d{4}\s*\|\s*Jared Hardin, Managing Director', norm(deck_text), re.I)] if m), None)
    assert byline, 'cover byline not found'
    root, pdf = '../', f'{PUBLIC}.pdf'
    w, h = img_size
    dl = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
          'stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 11l5 5 5-5M5 20h14"/></svg>')

    # Contents: the deck's three parts (the pages that carry a large 01, 02, 03) and the pages under each.
    groups, cur = [], None
    for i, (t, s, b, f, part) in enumerate(slides, 1):
        if i == 1:
            continue
        if part:
            cur = [i, norm(t).title() if t.isupper() else norm(t), []]
            groups.append(cur)
        elif cur:
            cur[2].append((i, norm(t).title() if t.isupper() else norm(t)))
    toc = ''.join(f'<li class="btoc-part"><a href="#p{a:02d}"><span>{n + 1:02d}</span>{esc(t)}</a><ol>'
                  + ''.join(f'<li><a href="#p{j:02d}"><span>{j}</span>{esc(x)}</a></li>' for j, x in items) + '</ol></li>'
                  for n, (a, t, items) in enumerate(groups))

    secs = []
    for i, (t, s, b, f, part) in enumerate(slides, 1):
        ttl = norm(t).title() if t.isupper() else norm(t)
        if i == 1:
            ttl = f'{NAME} {PERIOD} Sector Report: Cover'
        overlay = ''.join(f'<a class="bslide-link" href="{esc(u)}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true" title="{esc(u)}" '
                          f'style="left:{x:.2f}%;top:{y:.2f}%;width:{ww:.2f}%;height:{hh:.2f}%"></a>'
                          for x, y, ww, hh, u in links[i - 1])
        sub = f'<p class="bslide-sub">{s}</p>' if s and not s.startswith('<') else s
        secs.append(f'''<section class="bslide" id="p{i:02d}" aria-labelledby="p{i:02d}-t">
<div class="bslide-head"><span class="bslide-num">{i:02d}</span><h2 class="bslide-title" id="p{i:02d}-t">{esc(ttl)}</h2><a class="bslide-pdf" href="{pdf}#page={i}">Page {i} in the PDF</a></div>
<div class="bslide-img"><img src="{root}{IMG_DIR}/p{i:02d}.webp" srcset="{root}{IMG_DIR}/p{i:02d}-800.webp 800w, {root}{IMG_DIR}/p{i:02d}.webp 1600w" sizes="(max-width: 1080px) 100vw, 900px" alt="Page {i} of the {NAME} {PERIOD} sector report: {esc(ttl)}. The full text follows." width="{w}" height="{h}"{' loading="lazy"' if i > 2 else ''}>{overlay}</div>
<details class="bslide-text"><summary>Read the text of this page</summary>
<div class="bslide-body">{sub}
{b}
{f'<div class="bk-foot">{f}</div>' if f else ''}</div>
</details>
</section>''')

    lead = CONF['lead']
    desc = f'{NAME} {PERIOD} M&A sector report from Benchmark International: {lead}'
    page = site.head(f'{NAME} {PERIOD} M&A Sector Report', desc[:300], root).replace('</head>', f'<link rel="stylesheet" href="{root}assets/css/report.css">\n</head>')
    page += site.header(root, 'industries')
    page += f'''
<section class="hero hero--page">
  <div class="wrap">
    <div class="crumbs"><a href="{root}index.html">Middle Market</a> / <a href="{root}sectors/index.html">Sectors</a> / <a href="{root}sectors/{SECTOR}.html">{esc(NAME)}</a> / {PERIOD} Sector Report</div>
    <p class="eyebrow">{PERIOD} Sector Report</p>
    <h1 class="display">{esc(NAME)} <em>{PERIOD}</em></h1>
    <p class="lead">{esc(lead)}</p>
    <p class="rbyline">{esc(byline.replace("  ", " "))}</p>
    <div class="btn-row"><a class="btn" href="{pdf}" download>{dl} Download the PDF</a><a class="btn btn--light" href="{root}index.html#form">Discuss Your Business</a></div>
  </div>
</section>

<div class="wrap rlayout blayout">
  <aside class="rtoc btoc" aria-label="Report contents">
    <p class="eyebrow">Contents</p>
    <ol><li><a href="#p01"><span></span>Cover</a></li>{toc}</ol>
    <a class="btn" href="{pdf}" download>{dl} Download PDF</a>
  </aside>
  <article class="report brief">
    <p class="bnote">This is the {esc(NAME)} {PERIOD} sector report, page by page, exactly as it appears in the <a href="{pdf}" download>PDF</a>. Links on each page open their sources, and the text of every page, with its tables and chart data, is below each page.</p>
{chr(10).join(secs)}
  </article>
</div>
<script>if (matchMedia('(max-width: 700px)').matches) document.querySelectorAll('.bslide-text').forEach(d => d.open = true);</script>
'''
    page += site.cta(root)
    page += site.footer(root)
    page = site.report_extras(page, SECTOR, root)
    assert '—' not in page, 'em dash on the page'
    assert not re.search(r'\bMMT\b|Middle Market Team', page), 'MMT on the page'
    out = os.path.join(SITE, 'insights', f'{PUBLIC}.html')
    open(out, 'w', encoding='utf-8').write(page)
    print('wrote', os.path.relpath(out, SITE), round(len(page) / 1024), 'KB', len(slides), 'pages')


def main():
    with tempfile.TemporaryDirectory() as tmp:
        work = os.path.join(tmp, f'{PUBLIC}.pptx')
        prs = corrected_deck(work)
        src = convert(work, tmp)
        reader = write_pdf(src)
        size = write_images(src, tmp, len(reader.pages))
        build_page(prs, page_links(reader), size)


if __name__ == '__main__':
    main()

# Builds a sector report from its PowerPoint sector brief: the downloadable PDF and the site page come
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
#   insights/<sector>-sector-report-q<N>-<year>.html   the site page: one report section per deck page, with the
#                                                      deck's words, links, tables and logos in the site's report
#                                                      styles and its charts redrawn as SVG from the chart data
#   insights/<sector>-sector-report-q<N>-<year>.md     the same content as Markdown, for AI tools (linked from the
#                                                      page and from llms.txt)
#   assets/img/reports/<sector>-sector-report-q<N>-<year>/   logos and pictures used on the page
#
# Needs LibreOffice (soffice) with Impress, poppler-utils (pdffonts) and pip packages python-pptx, pypdf, Pillow.
# The deck fonts (Calibri and Cambria stand-ins, Quicksand, Newsreader, Cinzel) are in brief-fonts/ and are
# loaded for the conversion only, so nothing needs installing system-wide.
import html, json, os, re, shutil, subprocess, sys, tempfile
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(SITE, '_build'))
sys.path.insert(0, HERE)
import build as site  # noqa: E402
from webdeck import WebDeck, plain  # noqa: E402

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


# ─── 3. Site page ────────────────────────────────────────────────────────────
DL = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
      'stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 11l5 5 5-5M5 20h14"/></svg>')


def norm(t):
    return re.sub(r'\s+', ' ', html.unescape(t).replace('\xa0', ' ')).strip()


def title_case(t):
    t = norm(t)
    return t.title().replace("'S ", "'s ").replace('’S ', '’s ') if t.isupper() else t


def cover(prs):
    """Byline and segment names from the cover; checks that brief.json's lead is the cover sentence."""
    texts = []
    for sh in all_shapes(prs.slides[0].shapes):
        if sh.has_text_frame and sh.text_frame.text.strip():
            texts.append([p for p in (par.text for par in sh.text_frame.paragraphs) if p.strip()])
    flat = norm(' '.join(' '.join(t) for t in texts))
    assert norm(CONF['lead']) in flat, 'brief.json "lead" must be copied from the cover'
    m = re.search(r'October \d{4}\s*\|\s*Jared Hardin, Managing Director', flat, re.I)
    assert m, 'cover byline not found'
    # Segment names, in cover order, as the site names them
    known = {norm(x[0]).lower().replace(' and ', ' & '): x[0] for x in site.SECTOR_BY_SLUG[SECTOR]['segments']}
    segs = []
    for t in texts:
        for p in t:
            for x in re.split(r'\s*[·\x0b\n]\s*', p):
                k = norm(x).lower().replace(' and ', ' & ')
                if k in known and known[k] not in segs:
                    segs.append(known[k])
    # What's included: part number -> description
    seq = [norm(p) for t in texts for p in t]
    parts = {}
    for i, x in enumerate(seq):
        if re.fullmatch(r'0[1-9]', x) and i + 2 < len(seq):
            parts[x] = seq[i + 2]
    byline = m.group(0)
    if byline.isupper():
        byline = 'October ' + byline.split(' ', 1)[1].title().replace(' | ', ' | ')
    return byline, segs, parts


def stats_band(pages):
    """The figures from the page on Benchmark International's own transactions, shown under the hero."""
    for pg in pages:
        if pg['title'].startswith('Benchmark International') and 'Transactions' in pg['title']:
            pairs = re.findall(r'<p class="dnum">(.*?)</p>\s*<p>(.*?)</p>', pg['body'])[:3]
            label = re.search(r'<p class="dlabel">([^<]*)</p>\s*<p class="dnum">', pg['body'])
            if len(pairs) >= 2:
                return pairs, (label.group(1) if label else ''), pg['num']
    return None, '', None


def inline_md(h):
    h = re.sub(r'<br>', ' ', h)
    h = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', lambda m: f'[{plain(m.group(2))}]({m.group(1)})', h, flags=re.S)
    h = re.sub(r'</?strong>', '**', h)
    h = re.sub(r'</?em>', '*', h)
    h = re.sub(r'<[^>]+>', '', h)
    return html.unescape(h).replace('****', '').strip()


def table_md(t):
    rows = [[plain(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)] for r in re.findall(r'<tr>(.*?)</tr>', t, re.S)]
    if not rows:
        return ''
    w = max(len(r) for r in rows)
    rows = [r + [''] * (w - len(r)) for r in rows]
    return '\n'.join(['| ' + ' | '.join(rows[0]) + ' |', '|' + ' --- |' * w] + ['| ' + ' | '.join(r) + ' |' for r in rows[1:]])


def body_md(h):
    h = re.sub(r'<figure class="dchart"[^>]*>.*?<table>(.*?)</table>.*?</figure>', lambda m: '\n\nChart data:\n\n' + table_md(m.group(1)) + '\n\n', h, flags=re.S)
    h = re.sub(r'<div class="rtable-wrap"><table[^>]*>(.*?)</table></div>', lambda m: '\n\n' + table_md(m.group(1)) + '\n\n', h, flags=re.S)
    h = re.sub(r'<div class="dline">(.*?)</div></div>', lambda m: '\n- ' + ' '.join(plain(c) for c in re.findall(r'<div class="dline-c[^"]*">(.*?)</div>', m.group(1) + '</div>', re.S)), h, flags=re.S)
    h = re.sub(r'<div class="dbar"><span class="dbar-l">(.*?)</span>.*?<span class="dbar-v">(.*?)</span></div>', lambda m: f'\n- {plain(m.group(1))}: {plain(m.group(2))}', h, flags=re.S)
    h = re.sub(r'<div class="dgrid-wrap"><table[^>]*>(.*?)</table></div>', lambda m: '\n\n' + table_md(m.group(1)) + '\n\n', h, flags=re.S)
    h = re.sub(r'<h3[^>]*>(.*?)</h3>', lambda m: f'\n\n### {plain(m.group(1))}\n\n', h, flags=re.S)
    h = re.sub(r'<li>(.*?)</li>', lambda m: f'\n- {inline_md(m.group(1))}', h, flags=re.S)
    h = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: f'\n\n> {inline_md(m.group(1))}\n\n', h, flags=re.S)
    h = re.sub(r'<p class="dlabel">(.*?)</p>', lambda m: f'\n\n**{plain(m.group(1))}**\n\n', h, flags=re.S)
    h = re.sub(r'<p[^>]*>(.*?)</p>', lambda m: f'\n\n{inline_md(m.group(1))}\n\n', h, flags=re.S)
    h = re.sub(r'<img [^>]*alt="([^"]+)"[^>]*>', r'\n\n\1\n\n', h)
    h = re.sub(r'<(?!https?:)[^>]+>', '', h)
    h = html.unescape(h)
    return re.sub(r'\n{3,}', '\n\n', h).strip()


def to_markdown(pages, lead, byline, segs):
    url = site.abs_url(f'insights/{PUBLIC}.html')
    out = [f'# {NAME} {PERIOD} M&A Sector Report', '', f"Benchmark International's Middle Market team. {byline}.", '',
           lead, '', f'Web version: {url}  ', f'PDF: {site.abs_url(f"insights/{PUBLIC}.pdf")}', '']
    if segs:
        out += ['Segments: ' + '; '.join(segs), '']
    for pg in pages[1:]:
        out += [f'## {pg["num"]}. {title_case(pg["title"])}', '']
        if pg['subtitle']:
            out += [inline_md(pg['subtitle']), '']
        out += [body_md(pg['body']), '']
        if pg['foot']:
            out += [body_md(pg['foot']), '']
    return '\n'.join(out).strip() + '\n'


def build_page(prs):
    media = os.path.join(SITE, IMG_DIR)
    shutil.rmtree(media, ignore_errors=True)
    root, pdf, md_name = '../', f'{PUBLIC}.pdf', f'{PUBLIC}.md'
    wd = WebDeck(prs, media, f'{root}{IMG_DIR}')
    pages = [wd.page(s, i) for i, s in enumerate(prs.slides, 1)]
    byline, segs, included = cover(prs)
    lead = CONF['lead']

    # Contents: every page after the cover; the deck's three parts (01, 02, 03) are marked.
    toc = []
    for pg in pages[1:]:
        t = title_case(pg['title'])
        if pg['part']:
            toc.append(f'<li class="rtoc-part"><a href="#p{pg["num"]:02d}"><span>{pg["part"]}</span>{esc(t)}</a></li>')
        else:
            toc.append(f'<li><a href="#p{pg["num"]:02d}"><span>{pg["num"]:02d}</span>{esc(t)}</a></li>')

    secs = []
    for pg in pages[1:]:
        t = title_case(pg['title']) if pg['title'].isupper() else (pg['title_html'] or esc(pg['title']))
        num = pg['part'] if pg['part'] else f'{pg["num"]:02d}'
        sub = f'<p class="rlead">{pg["subtitle"]}</p>' if pg['subtitle'] else ''
        if pg['part'] and included.get(pg['part']):
            sub = f'<p class="rpart-desc">{esc(included[pg["part"]])}</p>' + sub
        foot = f'<div class="fine rfoot">{pg["foot"]}</div>' if pg['foot'] else ''
        kind = ' rsec--part' if pg['part'] else ''
        secs.append(f'<section class="rsec{kind}" id="p{pg["num"]:02d}">\n<div class="rsec-head"><span class="rsec-num">{num}</span>'
                    f'<h2 class="h2">{t}</h2></div>\n<div class="rblock dblock">{sub}\n{pg["body"]}\n{foot}'
                    f'<p class="rpage"><a href="{pdf}#page={pg["num"]}">Page {pg["num"]} of the PDF</a></p></div>\n</section>')

    pairs, band_label, _ = stats_band(pages)
    band = ''
    if pairs:
        stat_html = ''.join(f'<div class="stat"><div class="stat-num">{a}</div><div class="stat-label">{b}</div></div>' for a, b in pairs)
        eyebrow = f'<p class="eyebrow">{band_label}</p>' if band_label else ''
        band = (f'\n<section class="section--dark section--tight">\n  <div class="wrap">\n    {eyebrow}\n'
                f'    <div class="stats rhero-stats">{stat_html}</div>\n  </div>\n</section>\n')
    seg_html = f'<p class="rsegs">{" &nbsp;·&nbsp; ".join(esc(x) for x in segs)}</p>' if segs else ''
    desc = f"{NAME} {PERIOD} M&A sector report from Benchmark International's Middle Market team: {lead}"
    page = site.head(f'{NAME} {PERIOD} M&A Sector Report', desc[:300], root).replace(
        '</head>', f'<link rel="stylesheet" href="{root}assets/css/report.css">\n'
                   f'<link rel="alternate" type="text/markdown" href="{md_name}" title="{esc(NAME)} {PERIOD} M&amp;A Sector Report (Markdown)">\n</head>')
    page += site.header(root, 'industries')
    author = (f'<aside class="rauthor">\n      <img src="{root}assets/img/team/jared-hardin.jpg" alt="Jared Hardin" width="120" height="120" loading="lazy">\n'
              f'      <div>\n        <p class="eyebrow">Considering a transaction in the {esc(NAME.lower())} sector?</p>\n        <h3>Jared Hardin</h3>\n'
              f'        <p class="role">Managing Director, Benchmark International</p>\n'
              f'        <p><a href="tel:+18137716675">813-771-6675</a> &nbsp;|&nbsp; <a href="mailto:j.hardin@benchmarkintl.com">j.hardin@benchmarkintl.com</a></p>\n'
              f'        <div class="btn-row"><a class="btn" href="{root}index.html#form">Start the Conversation</a><a class="btn btn--ghost" href="{pdf}" download>{DL} Download the PDF</a></div>\n'
              f'      </div>\n    </aside>')
    page += (f'\n<section class="hero hero--page">\n  <div class="wrap">\n'
             f'    <div class="crumbs"><a href="{root}index.html">Middle Market</a> / <a href="{root}sectors/index.html">Sectors</a> / '
             f'<a href="{root}sectors/{SECTOR}.html">{esc(NAME)}</a> / {PERIOD} Sector Report</div>\n'
             f'    <p class="eyebrow">Quarterly Sector Brief &nbsp;|&nbsp; {PERIOD}</p>\n'
             f'    <h1 class="display">{esc(NAME)} <em>{PERIOD}</em></h1>\n'
             f'    <p class="lead">{esc(lead)}</p>\n    {seg_html}\n'
             f'    <p class="rbyline">{esc(norm(byline))}</p>\n'
             f'    <div class="btn-row"><a class="btn" href="{pdf}" download>{DL} Download the PDF</a>'
             f'<a class="btn btn--light" href="{root}index.html#form">Discuss Your Business</a></div>\n  </div>\n</section>\n'
             f'{band}\n<div class="wrap rlayout">\n  <aside class="rtoc" aria-label="Report contents">\n    <p class="eyebrow">Contents</p>\n'
             f'    <ol>{"".join(toc)}</ol>\n    <a class="btn" href="{pdf}" download>{DL} Download the PDF</a>\n  </aside>\n'
             f'  <article class="report">\n{chr(10).join(secs)}\n    {author}\n  </article>\n</div>\n\n')
    page += site.cta(root)
    page += site.footer(root)
    extra = {
        'abstract': lead,
        'keywords': ', '.join([f'{NAME} M&A', f'{NAME} mergers and acquisitions', 'middle market', 'valuation multiples', 'sell-side M&A'] + segs),
        'encoding': [{'@type': 'MediaObject', 'contentUrl': site.abs_url(f'insights/{md_name}'), 'encodingFormat': 'text/markdown'}],
        'hasPart': [dict({'@type': 'WebPageElement', 'name': title_case(pg['title']), 'url': site.abs_url(f'insights/{PUBLIC}.html') + f'#p{pg["num"]:02d}'},
                         **({'description': plain(pg['subtitle'])} if pg['subtitle'] else {})) for pg in pages[1:]],
    }
    page = site.report_extras(page, SECTOR, root, extra)
    for bad, why in (('—', 'em dash'), ('Capital Markets', 'old team name'), ('BCM', 'old team name')):
        assert bad not in page, f'{why} on the page'
    assert not re.search(r'\bMMT\b|Middle Market Team', page), 'MMT on the page'
    out = os.path.join(SITE, 'insights', f'{PUBLIC}.html')
    open(out, 'w', encoding='utf-8').write(page)
    md = to_markdown(pages, lead, norm(byline), segs)
    open(os.path.join(SITE, 'insights', md_name), 'w', encoding='utf-8').write(md)
    for f in os.listdir(media) if os.path.isdir(media) else []:
        if f'{IMG_DIR}/{f}' not in page:
            os.remove(os.path.join(media, f))     # pictures the page leaves out (decoration and photos)
    n_media = len(os.listdir(media)) if os.path.isdir(media) else 0
    print('wrote', os.path.relpath(out, SITE), round(len(page) / 1024), 'KB,', len(pages) - 1, 'sections,', n_media, 'images, and', md_name)
    return pages


def main():
    with tempfile.TemporaryDirectory() as tmp:
        work = os.path.join(tmp, f'{PUBLIC}.pptx')
        prs = corrected_deck(work)
        if '--page-only' not in sys.argv:
            write_pdf(convert(work, tmp))
        build_page(prs)


if __name__ == '__main__':
    main()

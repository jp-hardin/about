# Builds an industry report from its PowerPoint brief: the downloadable PDF and the site page come
# from the same .pptx, so the two always match.
#
# Usage: python3 brief.py <report-folder>     e.g. python3 brief.py industrial-q4-2026
#
# The folder holds the deck (brief.pptx) and brief.json:
#   {"lead": "<the cover's summary sentence, as written on the cover>"}
# The sector and quarter come from the folder name.
#
# What it writes:
#   insights/<industry>-industry-report-q<N>-<year>.pdf    the deck, converted by LibreOffice
#   insights/<industry>-industry-report-q<N>-<year>.html   the site page: one report section per deck page, with the
#                                                      deck's words, links, tables and logos in the site's report
#                                                      styles and its charts redrawn as SVG from the chart data
#   insights/<industry>-industry-report-q<N>-<year>.md     the same content as Markdown, for AI tools (linked from the
#                                                      page and from llms.txt)
#   assets/img/reports/<industry>-industry-report-q<N>-<year>/   logos and pictures used on the page
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
from flow import flow  # noqa: E402

FOLDER = os.path.join(HERE, sys.argv[1].strip('/'))
SLUG = os.path.basename(FOLDER)                                   # industrial-q4-2026
SECTOR = SLUG.rsplit('-', 2)[0]                                   # industrial
QUARTER, YEAR = SLUG.rsplit('-', 2)[1:]                           # q4, 2026
PUBLIC = f'{SECTOR}-industry-report-{QUARTER}-{YEAR}'
PERIOD = f'{QUARTER.upper()} {YEAR}'
NAME = site.SECTOR_BY_SLUG[SECTOR]['name']
CONF = json.load(open(os.path.join(FOLDER, 'brief.json'), encoding='utf-8'))
IMG_DIR = f'assets/img/reports/{PUBLIC}'

# Corrections applied to a working copy of the deck before anything is built, so the deck itself stays as supplied.
# Site style: no em dashes. Links to the old report addresses go straight to the current ones.
TEXT_FIXES = [('” — ', '” '), (' — ', ', '), ('—', ', ')]
LINK_FIXES = [('-sector-report-', '-industry-report-'), ('/mid-market-practice/sectors/', '/mid-market-practice/industries/')]

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
        '/Title': f'{NAME} {PERIOD} M&A Industry Report | Benchmark International',
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


WEB_SKIP = re.compile(r'(Connect With|Our Team$)', re.I)
TEAM_NAMES = [t[0] for t in site.TEAM_LEAD] + [t[0] for t in site.TEAM_SUPPORT]


def drop_team_cards(body):
    """Removes cards that hold a team member's name and contact details (the page's author card and the site's
    team section already carry them), with the label that introduces them."""
    names = '|'.join(re.escape(x) for x in TEAM_NAMES)
    while True:
        m = re.search(r'<div class="dcard[^"]*"[^>]*><div class="dtx"><h3 class="dh"><strong>(?:' + names + r')</strong></h3>', body)
        if not m:
            break
        depth, i = 0, m.start()
        for t in re.finditer(r'<div\b|</div>', body[m.start():]):
            depth += 1 if t.group(0) != '</div>' else -1
            if depth == 0:
                i = m.start() + t.end()
                break
        body = body[:m.start()] + body[i:].lstrip()
    return re.sub(r'<div class="dtx"><p class="dlabel"><strong>TALK WITH THE TEAM</strong></p></div>\s*', '', body)


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


def join_tables(body):
    """Two tables with the same columns, one after the other (a list split across deck pages), become one table;
    a lead sentence that sat between them moves above it."""
    from lxml import html as LH
    root = LH.fragment_fromstring(body, create_parent='div')
    head = lambda w: ' '.join(' '.join(w.xpath('.//thead')[0].itertext()).split()) if w.xpath('.//thead') else None
    wraps = root.xpath('./div[contains(concat(" ", @class, " "), " rtable-wrap ")]')
    for a, b in zip(wraps, wraps[1:]):
        if a.getparent() is None or b.getparent() is None or head(a) is None or head(a) != head(b):
            continue
        between, cur = [], a.getnext()
        while cur is not None and cur is not b:
            between.append(cur)
            cur = cur.getnext()
        if cur is not b or any(x.tag != 'p' for x in between):
            continue
        for x in between:
            x.tail = None
            a.addprevious(x)
        tb = a.xpath('.//tbody')[0]
        for tr in b.xpath('.//tbody/tr'):
            tb.append(tr)
        b.getparent().remove(b)
    return (root.text or '') + ''.join(LH.tostring(k, encoding='unicode') for k in root)


def join_notes(foot):
    """Footnotes of joined pages: each sentence once."""
    sents, seen = [], set()
    for m in re.findall(r'<p[^>]*>(.*?)</p>', foot, re.S):
        for x in re.split(r'(?<=[.])\s+(?=[A-Z])', m.strip()):
            k = re.sub(r'<[^>]+>|\s+', ' ', x).strip().lower()
            if k and k not in seen:
                seen.add(k)
                sents.append(x.strip())
    return f'<p class="fine">{" ".join(sents)}</p>' if sents else foot


def merge_continued(pages):
    """A deck page that continues the one before it (same title, or "(Continued)") joins it: online it is one section.
    Returns the pages and a map from each folded page number to the page it joined."""
    out, alias = [], {}
    key = lambda t: re.sub(r'\s*\((?:continued|cont\.)\)\s*$', '', t or '', flags=re.I).strip().lower()
    for pg in pages:
        prev = out[-1] if out else None
        if prev is not None and not pg['part'] and not prev['part'] and key(pg['title']) == key(prev['title']):
            sub = f'<p class="rlead">{pg["subtitle"]}</p>\n' if pg['subtitle'] and pg['subtitle'] != prev['subtitle'] else ''
            prev['body'] += '\n' + sub + pg['body']
            if pg['foot'] and pg['foot'] not in prev['foot']:
                prev['foot'] = (prev['foot'] + '\n' + pg['foot']).strip()
            alias[pg['num']] = prev['num']
            prev['body'] = join_tables(prev['body'])
            prev['foot'] = join_notes(prev['foot'])
            continue
        for k in ('title', 'title_html'):
            pg[k] = re.sub(r'\s*\((?:Continued|continued|CONTINUED)\)\s*$', '', pg[k] or '')
        out.append(pg)
    return out, alias


def web_refs(pages, alias):
    """Page references written for the PDF ("appear on page 10", "on the next page") point to sections online."""
    kept = {pg['num']: pg for pg in pages[1:]}

    def link(n):
        n = alias.get(n, n)
        pg = kept.get(n)
        return (n, f'<a href="#p{n:02d}">{esc(title_case(pg["title"]) if pg["title"].isupper() else pg["title"])}</a>') if pg else None

    def nums(spec):
        out = []
        for a, b in re.findall(r'(\d+)(?:\s*(?:to|–)\s*(\d+))?', spec):
            out += list(range(int(a), int(b) + 1)) if b else [int(a)]
        return out

    def pages_ref(m):
        seen, links = set(), []
        targets = [link(n) for n in nums(m.group(2))]
        if targets and all(t and t[0] == here for t in targets):
            return ''          # the section itself: online it needs no pointer
        for l in targets:
            if l and l[0] not in seen:
                seen.add(l[0])
                links.append(l[1])
        if not links:
            return m.group(0)
        text = links[0] if len(links) == 1 else ', '.join(links[:-1]) + ' and ' + links[-1]
        return f'in {text}'

    for i, pg in enumerate(pages[1:], 1):
        here = pg['num']
        nxt = pages[i + 1] if i + 1 < len(pages) else None
        for k in ('body', 'foot', 'subtitle'):
            h = pg[k] or ''
            h = re.sub(r'\b(on|across|in) (pages? \d+(?:\s*(?:,|and|to|–)\s*\d+)*)', lambda m: pages_ref(m), h)
            h = re.sub(r'\b(shown) (pages? \d+(?:\s*(?:,|and|to|–)\s*\d+)*)', lambda m: ('shown ' + pages_ref(m)).strip(), h)
            h = re.sub(r' +([.,;])', r'\1', h)
            h = re.sub(r'\s*\(PAGES? [^)]*\)', '', h)
            if nxt is not None:
                h = h.replace('on the next page', f'in the next section, <a href="#p{nxt["num"]:02d}">{esc(nxt["title"])}</a>')
            h = re.sub(r'\s*This page covers [^.<]*\.', '', h)
            h = h.replace('on the valuation page of this brief', 'in the valuation section of this report')
            h = h.replace('on the valuation pages', 'in the valuation sections')
            h = h.replace('this brief', 'this report').replace('This brief', 'This report').replace('with the brief', 'with the report')
            h = h.replace('linked on each page, listed by page', 'linked in each section, listed by section')
            h = h.replace('appendix pages', 'appendix sections').replace('the valuation pages', 'the valuation sections')
            if pg['title'].strip().lower() == 'sources':
                h = re.sub(r'(<h4 class="rh4">(?:<strong>)?)\d{1,2} ', r'\1', h)
            pg[k] = h
    return pages


CHAPTERS = [  # (key, title, deck-page titles that belong to it); the first match wins, in this order
    ('notes', 'Disclosures and Sources', r'disclosures|^sources$'),
    ('about', 'About Benchmark International', r'^benchmark international$'),
    ('reading', "What We're Reading", r'reading'),
    ('indicators', 'Indicators to Watch', r'economic trends|indicators'),
    ('valuations', 'Valuations and Public Markets', r'public compan|valuation|earnings|revenue growth|appendix|stock performance'),
    ('deals', 'Deals and Buyers', r'transactions|engagement|spotlight|who is buying|participants'),
    ('sectors', 'Sector by Sector', r'perspectives|feature:'),
    ('market', 'Market Conditions', r'.'),
]
ORDER = ['short', 'market', 'sectors', 'deals', 'valuations', 'indicators', 'reading', 'about', 'notes']


def chapters(pages):
    """The web report's chapters: [(key, title, [pages])]. The first part divider (the key insights) is The Short
    Version; the other part dividers are dropped."""
    groups = {}
    for pg in pages[1:]:
        if pg['part']:
            if pg['part'] == '01':
                groups.setdefault('short', ('The Short Version', []))[1].append(pg)
            continue
        t = re.sub(r'<[^>]+>', '', pg['title']).strip().lower()
        for key, title, pat in CHAPTERS:
            if re.search(pat, t):
                groups.setdefault(key, (title, []))[1].append(pg)
                break
    return [(k, groups[k][0], groups[k][1]) for k in ORDER if k in groups]


def fold_tables(body):
    """Long tables (more than 12 rows) show their first rows and fold the rest behind a button; every table of
    eight rows or more gets a filter box."""
    def fold(m):
        html_ = m.group(0)
        rows = html_.count('<tr')
        if rows < 9:
            return html_
        box = '<div class="rfilter"><input type="search" placeholder="Filter this table" aria-label="Filter this table"></div>'
        if rows <= 13:
            return box + html_
        return f'<details class="rfold rfold--table" open><summary>Table: {rows - 1} rows</summary>{box}{html_}</details>'
    return re.sub(r'<div class="rtable-wrap">.*?</table></div>', fold, body, flags=re.S)


def to_markdown(pages, lead, byline, segs):
    url = site.abs_url(f'insights/{PUBLIC}.html')
    out = [f'# {NAME} {PERIOD} M&A Industry Report', '', f"Benchmark International's Middle Market team. {byline}.", '',
           lead, '', f'Web version: {url}  ', f'PDF: {site.abs_url(f"insights/{PUBLIC}.pdf")}', '']
    if segs:
        out += ['Segments: ' + '; '.join(segs), '']
    for k, (key, ctitle, pgs) in enumerate(chapters(pages), 1):
        out += [f'## {k}. {ctitle}', '']
        for pg in pgs:
            if not pg['part']:
                out += [f'### {title_case(pg["title"])}', '']
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
    # The deck's contact and team pages (and the part divider that opens them) repeat what the web page already
    # carries: the author card, the call to action and the site's team section. They stay in the PDF only.
    web, after_skip = [pages[0]], False
    for pg in pages[1:]:
        if WEB_SKIP.match(pg['title']):
            after_skip = after_skip or bool(pg['part'])
            continue
        if after_skip and not pg['part']:
            pg['part_label'], after_skip = 'About This Report', False
        pg['body'] = drop_team_cards(pg['body']) if pg['part'] else flow(drop_team_cards(pg['body']))
        web.append(pg)
    pages, alias = merge_continued(web)
    pages = web_refs(pages, alias)
    byline, segs, included = cover(prs)
    lead = CONF['lead']

    # Online the report is organized by what a reader comes for, not by deck page: chapters (The Short Version,
    # Market Conditions, Sector by Sector, ...) hold the deck pages as subsections, in deck order within each chapter.
    # Part dividers go; long tables, the disclosures and the sources fold away until opened.
    def key_list(body):
        """The divider's numbered key insights (a bold "NN  headline" line, then its sentence) as a list."""
        pat = r'<p(?: class="fine")?><strong>(\d\d)\s+(.*?)</strong></p>\s*<p(?: class="fine")?>(.*?)</p>'
        items = re.findall(pat, body, re.S)
        if not items:
            return body
        ol = '<ol class="rkey">' + ''.join(f'<li><h3 class="rkey-t">{h}</h3><p class="rkey-d">{d}</p></li>' for _, h, d in items) + '</ol>'
        body = re.sub(r'<p class="dlabel"><strong>KEY INSIGHTS</strong></p>', '<p class="dlabel">Key insights</p>', body)
        first = re.search(pat, body, re.S)
        body = body[:first.start()] + ol + re.sub(pat, '', body[first.start():], flags=re.S)
        return body

    chaps = chapters(pages)
    toc, secs = [], []
    for k, (key, ctitle, pgs) in enumerate(chaps, 1):
        subs = [pg for pg in pgs if not pg['part']]
        sub_toc = ''.join(f'<li><a href="#p{pg["num"]:02d}">{esc(title_case(pg["title"]))}</a></li>' for pg in subs) if len(subs) > 1 and key != 'notes' else ''
        toc.append(f'<li class="rtoc-ch"><a href="#ch-{key}"><span>{k:02d}</span>{esc(ctitle)}</a>' + (f'<ol class="rtoc-sub">{sub_toc}</ol>' if sub_toc else '') + '</li>')
        inner = []
        for pg in pgs:
            foot = f'<div class="fine rfoot">{pg["foot"]}</div>' if pg['foot'] else ''
            if pg['part']:
                inner.append(flow(key_list(pg['body'])))
                continue
            t = title_case(pg['title']) if pg['title'].isupper() else (pg['title_html'] or esc(pg['title']))
            sub = f'<p class="rlead">{pg["subtitle"]}</p>' if pg['subtitle'] else ''
            body = fold_tables(pg['body'])
            block = f'<section class="rpart" id="p{pg["num"]:02d}">\n<h3 class="rh2">{t}</h3>\n{sub}\n{body}\n{foot}\n</section>'
            if key == 'notes':
                block = (f'<details class="rfold" id="p{pg["num"]:02d}"><summary>{t}</summary>\n{sub}\n{body}\n{foot}\n</details>')
            inner.append(block)
        secs.append(f'<section class="rsec rchap" id="ch-{key}">\n<div class="rsec-head"><span class="rsec-num">{k:02d}</span>'
                    f'<h2 class="h2">{esc(ctitle)}</h2></div>\n<div class="rblock dblock">\n{chr(10).join(inner)}\n</div>\n</section>')

    pairs, band_label, _ = stats_band(pages)
    band = ''
    if pairs:
        stat_html = ''.join(f'<div class="stat"><div class="stat-num">{a}</div><div class="stat-label">{b}</div></div>' for a, b in pairs)
        eyebrow = f'<p class="eyebrow">{band_label}</p>' if band_label else ''
        band = (f'\n<section class="section--dark section--tight">\n  <div class="wrap">\n    {eyebrow}\n'
                f'    <div class="stats rhero-stats">{stat_html}</div>\n  </div>\n</section>\n')
    seg_html = f'<p class="rsegs">{" &nbsp;·&nbsp; ".join(esc(x) for x in segs)}</p>' if segs else ''
    desc = f"{NAME} {PERIOD} M&A industry report from Benchmark International's Middle Market team: {lead}"
    page = site.head(f'{NAME} {PERIOD} M&A Industry Report', desc[:300], root).replace(
        '</head>', f'<link rel="stylesheet" href="{root}assets/css/report.css">\n'
                   f'<link rel="alternate" type="text/markdown" href="{md_name}" title="{esc(NAME)} {PERIOD} M&amp;A Industry Report (Markdown)">\n</head>')
    page += site.header(root, 'industries')
    author = (f'<aside class="rauthor">\n      <img src="{root}assets/img/team/jared-hardin.jpg" alt="Jared Hardin" width="120" height="120" loading="lazy">\n'
              f'      <div>\n        <p class="eyebrow">Considering a transaction in {esc(site.SECTOR_BY_SLUG[SECTOR]["prose"])}?</p>\n        <h3>Jared Hardin</h3>\n'
              f'        <p class="role">Managing Director, Benchmark International</p>\n'
              f'        <p><a href="tel:+18137716675">813-771-6675</a> &nbsp;|&nbsp; <a href="mailto:j.hardin@benchmarkintl.com">j.hardin@benchmarkintl.com</a></p>\n'
              f'        <div class="btn-row"><a class="btn" href="{root}index.html#form">Start the Conversation</a><a class="btn btn--ghost" href="{pdf}" download>{DL} Download the PDF</a></div>\n'
              f'      </div>\n    </aside>')
    page += (f'\n<section class="hero hero--page">\n  <div class="wrap">\n'
             f'    <div class="crumbs"><a href="{root}index.html">Middle Market</a> / <a href="{root}industries/index.html">Industries</a> / '
             f'<a href="{root}industries/{SECTOR}.html">{esc(NAME)}</a> / {PERIOD} Industry Report</div>\n'
             f'    <p class="eyebrow">Quarterly Industry Report &nbsp;|&nbsp; {PERIOD}</p>\n'
             f'    <h1 class="display">{esc(NAME)} <em>{PERIOD}</em></h1>\n'
             f'    <p class="lead">{esc(lead)}</p>\n    {seg_html}\n'
             f'    <p class="rbyline">{esc(norm(byline))}</p>\n'
             f'    <div class="btn-row"><a class="btn" href="{pdf}" download>{DL} Download the PDF</a>'
             f'<a class="btn btn--light" href="{root}index.html#form">Discuss Your Business</a></div>\n  </div>\n</section>\n'
             f'{band}\n<div class="wrap rlayout">\n  <aside class="rtoc" aria-label="Report contents">\n    <p class="eyebrow">Contents</p>\n'
             f'    <ol>{"".join(toc)}</ol>\n    <a class="btn" href="{pdf}" download>{DL} Download the PDF</a>\n  </aside>\n'
             f'  <article class="report">\n{chr(10).join(secs)}\n    {author}\n  </article>\n</div>\n\n')
    page += site.team_section(root) + '\n'
    page += ("<script>document.querySelectorAll('.rfilter input').forEach(function(i){var t=i.closest('.rfilter').nextElementSibling;"
             "i.addEventListener('input',function(){var q=i.value.toLowerCase();t.querySelectorAll('tbody tr').forEach(function(r){"
             "r.style.display=r.textContent.toLowerCase().indexOf(q)>-1?'':'none';});});});</script>\n")
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

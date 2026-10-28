"""Web reading pass for the online reports.

The deck supplies the content and its order; this pass gives it one web vocabulary: the deck's all-caps labels become
sentence-case headings (or a small kicker line when a heading follows), "READ HERE" style buttons become plain links,
rating words sit beside the name they rate, the deck's contact cards are dropped (the page ends with the team), and the
featured-deal banner becomes one line. The PDF keeps the deck's own look.
"""
import html
import re

# words kept in capitals when a label is put in sentence case
ACRONYMS = {'AI', 'US', 'USA', 'EBITDA', 'EV', 'M&A', 'FDA', 'CMS', 'ISM', 'ACG', 'GF', 'IBBA', 'USDA', 'CDW', 'AIP',
            'ACEC', 'PE', 'HR', 'IQVIA', 'PMI', 'Q1', 'Q2', 'Q3', 'Q4', 'CEO', 'CFO', 'MSO', 'DSO', 'ASC', 'SEC', 'HVAC',
            'B2B', 'SAAS', 'UCAAS', 'NAICS', 'ERP', 'GDP', 'CPI', 'ESOP', 'OEM', 'MRO', 'LTL', 'RCM', 'IPO', 'UK', 'EU'}
SPECIAL = {'SAAS': 'SaaS', 'UCAAS': 'UCaaS', 'MEDTECH': 'MedTech', 'FREIGHTWAVES': 'FreightWaves'}
# proper names kept capitalized
PROPER = ['Benchmark International', 'Benchmark', 'Managed IT', 'Federal Reserve', 'Department of War', 'Deloitte', 'Gartner', 'Reuters', 'Kitco News',
          'Investing.com', 'Insurance Journal', 'Fierce Healthcare', 'MedTech Dive', 'Drug Channels', 'Channel Dive',
          'National Restaurant Association', 'Private Label Manufacturers Association', 'Staffing Industry Analysts',
          'Global Electronics Association', 'Economic Research Service', 'Research Institute', 'High Tech Solutions',
          'M&A Source', 'GF Data', 'Chief Information Officer', 'Business Survey Committee', 'Wood Mackenzie']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December', 'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Sept', 'Oct', 'Nov', 'Dec']
RATINGS = r'STRONGEST|STRONG|STEADY|MIXED|SOFT|WEAK|WEAKEST|IMPROVING|STABLE|HIGH|MEDIUM|LOW|ACTIVE|SELECTIVE'


def sentence(text):
    """An all-caps label in sentence case, keeping acronyms and proper names."""
    raw = re.sub(r'MEANSFOR', 'MEANS FOR', html.unescape(text).strip())
    if raw != raw.upper():
        return text.strip()
    words = re.split(r'(\s+|[|:/(),-])', raw)
    out, first = [], True
    for w in words:
        if not w.strip() or re.fullmatch(r'[|:/(),-]', w):
            out.append(w)
            if w.strip() in ('|', ':'):
                first = True
            continue
        core = re.sub(r'[^\w&\'’.]', '', w)
        if core in SPECIAL:
            nw = w.replace(core, SPECIAL[core])
        elif core in ACRONYMS or re.fullmatch(r'\d[\w.]*|[A-Z]&[A-Z]', core):
            nw = w
        else:
            nw = w.lower()
            if first:
                nw = nw[:1].upper() + nw[1:]
        first = False
        out.append(nw)
    s = ''.join(out)
    for name in PROPER + MONTHS:
        s = re.sub(r'\b' + re.escape(name.lower()) + r'\b', name, s, flags=re.I)
    return html.escape(s, quote=False).replace('&amp;#x27;', '&#x27;')


def label_text(inner):
    return re.sub(r'<[^>]+>', '', inner).strip()


def readable(body):
    # contact cards inside the deck pages: the page ends with the leadership team and the author block
    body = re.sub(r'<p class="wlabel">(?:<strong>)?TALK WITH THE TEAM(?:</strong>)?</p>\s*'
                  r'(?:<div class="wcard"><div class="wcols wcols--2"><div class="wcol"><img class="wperson".*?</div></div></div>\s*)+',
                  '', body, flags=re.S)

    # the featured-deal banner: one line and the announcement link
    def banner(m):
        card = m.group(0)
        bits = [label_text(x) for x in re.findall(r'<p>(.*?)</p>', card, re.S)]
        link = re.search(r'<a href="([^"]+)"', card)
        line = '<p class="wmeta">Benchmark International advised on this transaction' + ''.join(f' &nbsp;·&nbsp; {b}' for b in bits) + '</p>'
        if link:
            line += f'\n<p class="wlink"><a href="{link.group(1)}" target="_blank" rel="noopener">Read the announcement</a></p>'
        return line
    body = re.sub(r'<div class="wcard wcard--dark"><p class="wlabel">(?:<strong>)?BENCHMARK INTERNATIONAL ADVISED(?:</strong>)?</p>'
                  r'.*?</div>', banner, body, flags=re.S)

    # "READ HERE" style buttons as plain links
    def button(m):
        href, text = m.group(1), label_text(m.group(2))
        word = {'READ HERE': 'Read the article', 'READ MORE': 'Read more'}.get(text.upper(), sentence(text))
        return f'<p class="wlink"><a href="{href}" target="_blank" rel="noopener">{word}</a></p>'
    btn = r'<p class="w(?:label|link)"><a href="([^"]+)"[^>]*>(.*?)</a></p>'
    body = re.sub(r'<div class="wcard wcard--dark">' + btn + r'</div>', button, body, flags=re.S)
    body = re.sub(btn, button, body, flags=re.S)

    # a rating word in its own column beside the name it rates
    body = re.sub(r'<div class="wcols wcols--2"><div class="wcol"><h4 class="wh">(.*?)</h4>(.*?)</div>'
                  r'<div class="wcol"><p class="wlabel">(?:<strong>)?(' + RATINGS + r')(?:</strong>)?</p></div></div>',
                  lambda m: f'<div class="wrated"><h4 class="wh">{m.group(1)} <span class="wrate">{m.group(3).capitalize()}</span></h4>{m.group(2)}</div>',
                  body, flags=re.S)

    # the deck's page talk
    body = re.sub(r'\bthis page (covers|shows|lists)', r'this section \1', body)

    # the deck's running header
    body = re.sub(r'<p class="wlabel">(?:<strong>)?Q\d \d{4}(?:</strong>)?</p>\s*', '', body)

    # the remaining all-caps labels: a heading, or a kicker line when a heading follows, or a source/date line
    def label(m):
        inner = m.group(1)
        text = label_text(inner)
        nxt = body_after(m.end())
        new = sentence(text)
        if '|' in text or re.fullmatch(r'(?:[A-Z]+ )?\d{1,2},? \d{4}|[A-Z]+ \d{4}|.*\(VIA .*', text):
            return f'<p class="wmeta">{new}</p>'
        if re.match(r'\s*<h[34]', nxt):
            return f'<p class="wkick">{new}</p>'
        return f'<h4 class="wk">{new}</h4>'
    body_after = lambda i: body[i:i + 40]
    body = re.sub(r'<p class="wlabel">(.*?)</p>', label, body, flags=re.S)
    return body

# Web-mode building blocks. gen.py loads this when WEB is set, so the same content
# renders as semantic, class-based HTML for the site instead of fixed print pages.
def _plain(t): return re.sub(r'<[^>]+>', '', t).replace('"', '&quot;').strip()
def _widths(cols, gap):
    parts = cols.split(); px = [float(p[:-2]) if p.endswith('px') else None for p in parts]
    free = 720 - sum(p for p in px if p) - gap * (len(parts) - 1); nfr = px.count(None) or 1
    w = [p if p else free / nfr for p in px]; tot = sum(w)
    return ''.join(f'<col style="width:{x / tot * 100:.1f}%">' for x in w)
def _tbl(cls, cols, head, rows):
    o = [f'<div class="rtable-wrap"><table class="rtable {cls}"><colgroup>{_widths(cols, 14)}</colgroup><thead><tr>' + ''.join(f'<th scope="col">{h}</th>' for h in head) + '</tr></thead><tbody>']
    for r in rows:
        o.append('<tr>' + ''.join((f'<th scope="row" data-label="{_plain(head[i])}">{c}</th>' if i == 0 else f'<td data-label="{_plain(head[i])}">{c}</td>') for i, c in enumerate(r)) + '</tr>')
    o.append('</tbody></table></div>'); return '\n'.join(o)
def P(t, extra=''): return f'<p>{t}</p>'
def PC(t): return f'<p>{t}</p>'
def EYE(t): return f'<p class="eyebrow">{t}</p>'
def H2(t, m='0'): return f'<h3 class="rh3">{t}</h3>'
def H3(t, m=''): return f'<h4 class="rh4">{t}</h4>'
def NOTE(t): return f'<p class="fine">{t}</p>'
def table(cols, head, rows, pad=5, fs=12): return _tbl('', cols, head, rows)
def dtable(cols, head, rows, pad=5, fs=11.2): return _tbl('rtable--dark', cols, head, rows)
def band(stats, icon, alt):
    return '<div class="rstats">' + ''.join(f'<div class="rstat"><div class="stat-num">{a}</div><div class="rstat-label">{b}</div></div>' for a, b in stats) + '</div>'
def quote(q, who): return f'<figure class="rquote"><blockquote>&ldquo;{q}&rdquo;</blockquote><figcaption>{who}</figcaption></figure>'
def cols2(inner): return inner
def page(fn, title, inner, n, h=890): pages.append((fn, title, inner))

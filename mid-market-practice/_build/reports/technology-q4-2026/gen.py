# Builds the print layout: one fixed 816 by 1056 page per file in root/project, the same files the design canvas holds.
# Usage: python3 gen.py   (pdf.py then prints these pages; web.py builds the site page from the same content)
import os, json, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import lib
from report import PAGES, source_groups, sources_pages

PROJ = os.path.join(ROOT, 'root', 'project')
os.makedirs(PROJ, exist_ok=True)

names = ['%s.dc.html' % stem for stem, _, _ in PAGES]
titles = [t for _, t, _ in PAGES]
pages = [f() for _, _, f in PAGES]

G = source_groups()
first = len(pages) + 1
for i, sp in enumerate(sources_pages(first, G, [[name for name, _ in G]])):
    pages.append(sp)
    names.append('P%02d.dc.html' % (first + i))
    titles.append('%02d Sources%s' % (first + i, '' if i == 0 else ', continued'))

for n, h in zip(names, pages):
    with open(os.path.join(PROJ, n), 'w', encoding='utf-8') as f:
        f.write(h)

boards = {n: {'x': (i % 6) * 896, 'y': (i // 6) * 1176, 'w': 816, 'h': 1056, 'title': t} for i, (n, t) in enumerate(zip(names, titles))}
canvas = {'v': 3, 'createdOnFiles': {'v': 1, 'at': '2026-10-06T02:30:00Z'}, 'title': 'Technology Q4 2026 M&A Sector Report',
          'launch': {'view': 'canvas'}, 'pages': [], 'boards': boards, 'order': names, 'notes': {}, 'designSystems': []}
with open(os.path.join(PROJ, 'canvas.json'), 'w') as f:
    json.dump(canvas, f, indent=1)
print(len(pages), 'pages;', len(lib.LINKS), 'links;', len(set(u for _, _, u in lib.LINKS)), 'unique urls')

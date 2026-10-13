# Builds the 1200x630 social preview images (og:image) in assets/img/social/.
# Usage: python3 social.py   (needs Playwright with Chromium). Rerun when sector names, photos or report periods change.
import os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import build as site  # noqa: E402

OUT = os.path.join(SITE, 'assets', 'img', 'social')
FONTS = os.path.join(HERE, 'reports', 'healthcare-q4-2026', 'fonts')
FACE = ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url('file://{FONTS}/{f}-latin-{w}-normal.woff2')}}"
               for n, f, w in [('Newsreader', 'newsreader', 500), ('Quicksand', 'quicksand', 600), ('Quicksand', 'quicksand', 700)])


def card(bg, eyebrow, title, sub):
    logo = 'file://' + os.path.join(SITE, 'assets', 'img', 'brand', 'benchmark-logo-white.png')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FACE}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1200px; height: 630px; overflow: hidden; background: #231f20; font-family: 'Quicksand', sans-serif; color: #fff; }}
.bg {{ position: absolute; inset: 0; background: url('{bg}') center/cover; }}
.shade {{ position: absolute; inset: 0; background: linear-gradient(90deg, rgba(20,18,18,.94) 0%, rgba(20,18,18,.78) 55%, rgba(20,18,18,.45) 100%); }}
.in {{ position: absolute; inset: 0; padding: 64px 72px; display: flex; flex-direction: column; }}
.logo {{ width: 230px; }}
.tag {{ margin-top: 10px; font-weight: 700; font-size: 15px; letter-spacing: .26em; text-transform: uppercase; color: #bc9163; }}
.eye {{ margin-top: auto; font-weight: 700; font-size: 18px; letter-spacing: .22em; text-transform: uppercase; color: #bc9163; }}
h1 {{ font-family: 'Newsreader', serif; font-weight: 500; font-size: 76px; line-height: 1.05; margin-top: 14px; max-width: 940px; }}
.rule {{ width: 72px; height: 3px; background: #bc9163; margin: 26px 0 20px; }}
.sub {{ font-weight: 600; font-size: 24px; color: #e4ddd5; max-width: 900px; line-height: 1.4; }}
</style></head><body><div class="bg"></div><div class="shade"></div><div class="in">
<img class="logo" src="{logo}"><div class="tag">Middle Market</div>
<div class="eye">{eyebrow}</div><h1>{title}</h1><div class="rule"></div><div class="sub">{sub}</div></div></body></html>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    img = lambda rel: 'file://' + os.path.join(SITE, rel)
    jobs = [('default', card(img('assets/img/site/stats-bg.jpg'), 'Benchmark International',
                             'Sell-Side M&amp;A for Middle&#8209;Market Companies',
                             '$50M to $500M TEV &nbsp;·&nbsp; Industrial, Business Services, Consumer, Healthcare and Technology'))]
    for s in site.SECTORS:
        hero = img(f"assets/img/industries/{s['slug']}/hero.jpg")
        jobs.append((s['slug'], card(hero, 'Sector Expertise', f"{s['name']} M&amp;A Advisory", site.e(s['tagline']))))
        rpt = site.current_report(s['slug'])
        if rpt:
            jobs.append((f"{s['slug']}-report", card(hero, f"{rpt['period']} &nbsp;·&nbsp; M&amp;A Sector Report", f"{s['name']} {rpt['period']}",
                                                     'Deal activity, valuations and what buyers are paying for')))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1200, 'height': 630})
        for name, html in jobs:
            tmp = os.path.join(HERE, '_social.html')
            open(tmp, 'w', encoding='utf-8').write(html)
            pg.goto('file://' + tmp)
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(OUT, f'{name}.jpg'), type='jpeg', quality=82)
            os.remove(tmp)
            print('wrote', f'assets/img/social/{name}.jpg')
        b.close()


if __name__ == '__main__':
    main()

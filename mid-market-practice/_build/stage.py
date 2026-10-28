"""Live preview staging marks.

  python3 stage.py mark  <folder> <commit> <reports>   adds the live preview banner and noindex to every page
  python3 stage.py strip <folder>                     removes them again before the copy goes to mmt-site

Everything added sits between <!--stage--> and <!--/stage--> so that strip leaves the pages exactly as built.
"""
import datetime
import os
import re
import sys

STYLE = ('position:fixed;left:0;right:0;bottom:0;z-index:9999;display:flex;gap:16px;justify-content:center;'
         'align-items:center;flex-wrap:wrap;padding:9px 16px;background:#7a1f1f;color:#fff;'
         'font:600 12px/1.4 Arial,sans-serif;letter-spacing:.06em;text-transform:uppercase')


def pages(folder):
    for d, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(d, f)


def mark(folder, commit, reports):
    when = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4))).strftime("%b %d, %Y %I:%M %p ET")
    for path in pages(folder):
        rel = os.path.relpath(folder, os.path.dirname(path)).replace(os.sep, "/")
        sandbox = f"{rel}/../mid-market-practice/index.html"
        banner = (f'<!--stage--><div style="{STYLE}" role="note"><span>Live preview &middot; staged {when} &middot; '
                  f'{commit[:7]} &middot; industry reports {reports}</span><span>This is exactly what &ldquo;merge live&rdquo; '
                  f'sends to the live site</span><a href="{sandbox}" style="color:#fff">Sandbox &rarr;</a></div><!--/stage-->')
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        html = re.sub(r"<!--stage-->.*?<!--/stage-->", "", html, flags=re.S)
        html = html.replace("<head>", '<head>\n<!--stage--><meta name="robots" content="noindex, nofollow"><!--/stage-->', 1)
        html = html.replace("</body>", banner + "\n</body>", 1)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)


def strip(folder):
    for path in pages(folder):
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        clean = re.sub(r"\n?<!--stage-->.*?<!--/stage-->\n?", lambda m: "\n" if m.group(0).startswith("\n") and m.group(0).endswith("\n") else "", html, flags=re.S)
        if clean != html:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(clean)


if __name__ == "__main__":
    if sys.argv[1] == "mark":
        mark(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "strip":
        strip(sys.argv[2])
    else:
        sys.exit(__doc__)

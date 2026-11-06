"""A plain Markdown copy of a finished page, for AI assistants and answer engines.

Each page.html gets page.md next to it (linked from the page as rel="alternate" type="text/markdown" and listed in
llms.txt): the page's main content as headings, paragraphs, lists, tables, and absolute links, without navigation,
scripts, forms, or decoration.
"""
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin
import re

SKIP = {"script", "style", "nav", "svg", "form", "dialog", "noscript", "button", "select", "template", "iframe"}
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr", "col", "area", "base", "embed", "param", "track"}
BLOCK = {"p", "div", "section", "article", "aside", "header", "footer", "li", "tr", "blockquote", "figure", "figcaption",
         "dd", "dt", "details", "summary", "table", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "main"}


class _Md(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base, self.out, self.skip, self.skip_tag, self.href, self.link = base, [], 0, None, None, None
        self.row, self.rows, self.cell, self.in_table = None, [], None, 0
        self.prefix = ""

    def emit(self, text):
        if self.link is not None:
            self.link.append(text)
        elif self.cell is not None:
            self.cell.append(text)
        else:
            self.out.append(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.skip:                      # inside a skipped element: only count nesting of the same tag
            if tag == self.skip_tag:
                self.skip += 1
            return
        cls = a.get("class") or ""
        if tag in SKIP or "hidden" in a or a.get("aria-hidden") == "true" or re.search(r"\b(gate-hp|crumbs|skip-link|marquee)\b", cls):
            if tag not in VOID:
                self.skip, self.skip_tag = 1, tag
            return
        if tag == "span":
            self.emit(" ")
        if tag == "table":
            self.in_table += 1
            self.rows = []
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []
        elif tag == "a" and a.get("href") and not a["href"].startswith(("#", "javascript:")):
            self.href, self.link = urljoin(self.base, a["href"]), []
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.emit("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "li":
            self.emit("\n- ")
        elif tag == "blockquote":
            self.emit("\n\n> ")
        elif tag == "br":
            self.emit("\n")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in BLOCK:
            self.emit("\n\n")

    def handle_endtag(self, tag):
        if self.skip:
            if tag == self.skip_tag:
                self.skip -= 1
            return
        if tag == "span":
            self.emit(" ")
        if tag in ("td", "th") and self.cell is not None and self.row is not None:
            self.row.append(" ".join("".join(self.cell).split()).replace("|", "/"))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if any(self.row):
                self.rows.append(self.row)
            self.row = None
        elif tag == "table":
            self.in_table -= 1
            if self.rows:
                w = max(len(r) for r in self.rows)
                rows = [r + [""] * (w - len(r)) for r in self.rows]
                lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * w] + ["| " + " | ".join(r) + " |" for r in rows[1:]]
                self.emit("\n\n" + "\n".join(lines) + "\n\n")
            self.rows = []
        elif tag == "a" and self.link is not None:
            text = " ".join("".join(self.link).split())
            self.link, href = None, self.href
            self.emit(f"[{text}]({href}) " if text else "")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in BLOCK:
            self.emit("\n\n")

    def handle_data(self, data):
        if not self.skip:
            self.emit(re.sub(r"\s+", " ", data))


def markdown(html, url, title, desc):
    """The main content of html (a finished page at url) as Markdown."""
    m = re.search(r"<main[^>]*>(.*)</main>", html, re.S)
    body = m.group(1) if m else html
    body = re.sub(r"<footer class=\"site-footer\".*", "", body, flags=re.S)
    p = _Md(url)
    p.feed(body)
    text = "".join(p.out)
    text = re.sub(r"\*\*\s*\*\*", "", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(r"^- \s*$", "", text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text)
    h1 = re.search(r"^# (.+)$", text, re.M)
    name = h1.group(1) if h1 else unescape(title)
    if h1:
        text = (text[:h1.start()] + text[h1.end():]).strip()
    return f"# {name}\n\n> {unescape(desc)}\n\nSource: {url}\n\n{text}\n"

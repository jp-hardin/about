"""Reads the page copy in _build/copy/<page>.md into the sections the industry and About pages render.

Each file is a set of blocks separated by a line of five hyphens. A block is recognised by its first line:
"# Name" is the hero, "## ... M&A Advisory" the overview, "## What Drives Enterprise Value..." the value
drivers, "## Strategic & Financial Acquirers..." the buyer section, "## ...Advisory. ...Execution." the services,
a block with "Start a Confidential Conversation" the call to action, "### Question?" blocks the FAQ, numbered or
named "###" items matching the page's sectors the sector copy, and any other "###" list the market themes.
A block that opens with a bold line alone is a short statement shown above the value drivers.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = re.compile(r"^\d{2}\s*\|\s*")


def _title(line):
    line = line.strip()
    if line.startswith("#"):
        line = line.lstrip("#").strip()
    if line.startswith("**") and line.endswith("**"):
        line = line[2:-2].strip()
    return NUM.sub("", line)


def _is_item_head(line):
    s = line.strip()
    return s.startswith("### ") or (s.startswith("**") and s.endswith("**") and len(s) > 4)


def _items(lines):
    """Title/paragraph pairs from '### Title' or '**Title**' lines, each followed by one or more paragraphs."""
    out, cur = [], None
    for ln in lines:
        if not ln.strip():
            continue
        if _is_item_head(ln):
            cur = [_title(ln), []]
            out.append(cur)
        elif cur is not None:
            cur[1].append(ln.strip())
    return [(t, ps) for t, ps in out]


def _paras(lines):
    return [ln.strip() for ln in lines if ln.strip()]


def _norm(s):
    return re.sub(r"[^a-z]", "", s.lower().replace("technology-enabled", "tech-enabled"))


def load(page, segment_names=()):
    path = os.path.join(HERE, "copy", f"{page}.md")
    if not os.path.exists(path):
        return {}
    blocks = [b.strip("\n") for b in re.split(r"\n-----\n", open(path, encoding="utf-8").read()) if b.strip()]
    segs = {_norm(n): n for n in segment_names}
    out = {}
    for b in blocks:
        lines = b.split("\n")
        first = lines[0].strip()
        body = lines[1:]
        if "Start a Confidential Conversation" in b:
            paras = [p for p in _paras(body) if "Start a Confidential Conversation" not in p]
            sub = paras[0][2:-2] if paras and paras[0].startswith("**") else ""
            rest = paras[1:] if sub else paras
            out["cta"] = {"title": _title(first), "sub": sub,
                          "paras": [p for p in rest if not re.match(r"^\d{3}-\d{3}-\d{4}", p)]}
        elif first.startswith("# "):
            paras = _paras(body)
            out["hero"] = {"title": _title(first), "sub": paras[0][2:-2] if paras and paras[0].startswith("**") else "",
                           "paras": [p for p in paras if not p.startswith("**")]}
        elif first.startswith("**") and first.endswith("**"):
            out["statement"] = {"title": _title(first), "paras": _paras(body)}
        elif first.startswith("## What Drives Enterprise Value"):
            out["value"] = {"title": _title(first), "items": _items(body)}
        elif first.startswith("## Strategic & Financial Acquirers"):
            out["acquirers"] = {"title": _title(first), "paras": _paras(body)}
        elif first.startswith("## ") and first.endswith("M&A Advisory"):
            out["overview"] = {"title": _title(first), "paras": _paras(body)}
        elif first.startswith("## ") and ("Market Perspectives" in first or "Themes" in first):
            out["themes"] = {"title": _title(first), "items": _items(body)}
        elif first.startswith("## ") and "Execution" in first and "Advisory" in first:
            head, items = [], _items(body)
            for ln in body:
                if _is_item_head(ln):
                    break
                head.append(ln)
            out["services"] = {"title": _title(first), "intro": _paras(head), "items": items}
        elif first.startswith("### ") and first.rstrip().endswith("?"):
            out["faq"] = [(t, ps) for t, ps in _items(lines)]
        elif first.startswith("### "):
            items = _items(lines)
            matched = {}
            for t, ps in items:
                key = _norm(t)
                hit = next((n for k, n in segs.items() if k == key or k[:12] == key[:12]), None)
                if hit:
                    matched[hit] = ps
            if segs and len(matched) == len(items):
                out["segments"] = matched
            else:
                out["themes"] = {"title": "", "items": items}
        else:
            out.setdefault("sections", []).append({"title": _title(first), "lines": body, "items": _items(body),
                                                   "paras": _paras(body)})
    return out

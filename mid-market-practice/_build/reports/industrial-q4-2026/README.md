# Industrial Q4 2026 sector report: source

One content file produces two outputs. Edit the source here and rebuild; do not hand-edit the outputs.

| Output | Where | Built by |
| --- | --- | --- |
| Site page (native HTML, site styles) | `mid-market-practice/reports/industrial-q4-2026.html` | `web.py` |
| Downloadable PDF (Letter print layout) | `mid-market-practice/reports/industrial-q4-2026.pdf` | `pdf.py` |

## Rebuild
```
./build.sh
```
This runs `web.py` and `pdf.py`. `pdf.py` needs Playwright with Chromium (`pip install playwright && playwright install chromium`). To change only the site page, `python3 web.py` is enough. Commit the regenerated outputs with the source change. Merging to `main` publishes the site.

## Files
- `report.md`: all report text, tables, quotations and links, in Markdown. It mirrors the report document Jared edits, so a change made there is pasted or re-exported here.
- `render.py`: reads `report.md` and renders it as the HTML blocks both outputs share. It also holds the hero figures (`FIGS`), the three-figure band at the top of each segment (`BANDS`), the ISM chart data (`ISM`) and the as-of date (`AS_OF`).
- `web.py`: wraps the twelve sections in the site header, footer and call to action from `_build/build.py`. Styles are in `mid-market-practice/assets/css/report.css`.
- `pdf.py`: lays the same sections out for print, with a cover, a contents page, the contact page and the sources as the final section, and prints the PDF.
- `fonts/`: Cinzel, Newsreader and Quicksand (SIL Open Font License) for the PDF.

## How report.md maps to the page
- `## Overview` and `## At a Glance` become section 01, The Quarter in Brief.
- Each `###` heading under `## Where We Focus` becomes its own section. Bullets that open with a bold label become titled sub-sector blocks, and the paragraph that opens with "Benchmark International in this segment." becomes the highlighted note.
- A line that starts with `>` is a quotation, written as `> "Quoted sentence." ([Source name, publication](link))`.
- `{{chart:ism}}` places the ISM chart.
- `## Your Deal Team` is appended to the Advisory section, and `## Considering a Transaction in Industrial?` is replaced by the contact block on the site and the contact page in the PDF.

## Where to make common edits
- Text, figures, table rows, links: `report.md`. Both outputs pick the change up.
- Hero figures, segment bands, chart data, as-of date: the constants at the top of `render.py`. Keep each figure consistent with the text.
- Site section order or titles: `groups()` in `render.py`.
- Site styling: `assets/css/report.css`. Print styling: the `CSS` block in `pdf.py`.
- Button on the Industrial page: the `"report"` entry on the industrial sector in `_build/build.py`, then `python3 build.py` from `_build/`.

## Content rules
- Benchmark transactions: trailing 24 months only, no dates, names only where the tombstone is public and the deal is cleared to market.
- No investment bank used as a source of data. Direct quotations from the leading mid-market banks are attributed and linked; Capstone Partners is not cited.
- Copy follows the house voice: full sentences, no em dashes, no arrows.

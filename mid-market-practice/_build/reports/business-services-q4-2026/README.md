# Business Services Q4 2026 sector report: source

The 28 print pages in `pages/` are the source. They are the same files the design canvas holds, and both outputs are built from them. Edit the pages and rebuild; do not hand-edit the outputs.

| Output | Where | Built by |
| --- | --- | --- |
| Site page (native HTML, site styles) | `mid-market-practice/reports/business-services-q4-2026.html` | `web.py` |
| Downloadable PDF (28-page print layout) | `mid-market-practice/reports/business-services-q4-2026.pdf` | `pdf.py` |

## Rebuild
```
./build.sh
```
This runs `pdf.py` and `web.py`. `pdf.py` needs Playwright with Chromium (`pip install playwright && playwright install chromium`) and prints `OVER` for any page whose text runs past its frame. `web.py` needs `beautifulsoup4`. To change only the site page, `python3 web.py` is enough. Commit the regenerated outputs with the source change. Merging to `main` publishes the site.

## Files
- `pages/Main.dc.html` and `pages/P02.dc.html` to `pages/P28.dc.html`: one fixed 816 by 1056 page each, with all text, tables and links inline. Page order: cover; five segments; deal market (P03, P04); Commercial & Facility Services (P05 to P08); Marketing, Sales & Tech-Enabled Services (P09 to P12); Engineering, Architecture & Consulting (P13 to P15); Financial & Insurance Services (P16 to P18); Staffing & Human Capital (P19 to P21); valuation (P22); Benchmark activity (P23); buyers reward and discount (P24); preparing for a sale and author (P25); sources (P26 to P28).
- `web.py`: reads the pages, turns each paragraph, table, figure band, pull quote and source list into semantic HTML, groups them into the twelve site sections (`GROUPS`) and wraps them in the site header, footer and call to action from `_build/build.py`. Styles are in `mid-market-practice/assets/css/report.css`, shared with the Healthcare report. The script stops with an `unhandled block` message if a page gains a kind of element it does not know.
- `pdf.py`: joins the pages into one document and prints it. Fonts come from `../healthcare-q4-2026/fonts`. The `IMG` table maps the design canvas's uploaded images to the copies in `art/` and in the site's `assets/img/`.
- `art/`: the cover, section and plate illustrations and the watermark.

## Where to make common edits
- Text, figures, table rows, links: the page file that holds them. Both outputs pick the change up. Keep each page inside its 890px text frame; `pdf.py` reports any that run over.
- Valuation chart: the dots on the site come from the company lists at the bottom of `P22.dc.html`, and the medians and row labels from the chart on the same page. Change both when a multiple changes.
- Site section order or titles: `GROUPS` in `web.py`.
- Button on the Business Services page: the `"report"` entry on the business-services sector in `_build/build.py`, then `python3 build.py` from `_build/`.
- After an edit here, send the changed page files to the design canvas as well so the two stay matched.

## Content rules
- Benchmark transactions: names only where the tombstone is public and the seller is cleared to market; buyers flagged not shareable appear as undisclosed or individual buyers; no deal values; the live portfolio in aggregate only.
- Benchmark counts are stated since January 2025.
- No other investment bank cited as a source.
- Copy follows the house voice: full sentences, no em dashes, no arrows.

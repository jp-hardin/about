# Technology Q4 2026 sector report: source

One set of content produces three outputs. Edit the source here and rebuild; do not hand-edit the outputs.

| Output | Where | Built by |
| --- | --- | --- |
| Site page (native HTML, site styles) | `mid-market-practice/reports/technology-q4-2026.html` | `web.py` |
| Downloadable PDF (21-page print layout) | `mid-market-practice/reports/technology-q4-2026.pdf` | `pdf.py` |
| Print layout pages for the design canvas | `root/project/` (not committed) | `gen.py` |

## Rebuild
```
./build.sh
```
This runs `gen.py`, `pdf.py` and `web.py` in order. `pdf.py` needs Playwright with Chromium (`pip install playwright && playwright install chromium`) and prints `OVER` for any page whose text runs past its frame. To change only the site page, `python3 web.py` is enough. Commit the regenerated outputs with the source change. Merging to `main` publishes the site.

## Files
- `lib.py`: the building blocks (`h2`, `p`, `table`, `band`, `quote`, `note` and so on). Each one renders the fixed print layout by default and semantic HTML for the site when `lib.WEB` is set, which `web.py` does. Links are written in the text as `[[label|url]]` and are recorded for the sources list as they are used.
- `pages_a.py`: shared source links, the cover, the opening paragraph and four headline figures (`BRIEF`, `FIGS`), the six focus areas table, the deal market, and policy, trade and tax.
- `pages_b.py`: Managed IT & Cloud Services, Cybersecurity, Telecom & UCaaS and Systems Integration, each with a narrative page and a transactions page.
- `pages_c.py`: Electronics & Hardware, Government Technology, the valuation page and its listed-company multiples (`COMPS`), Benchmark International's activity, what buyers reward and discount, the contact page and the sources list.
- `report.py`: the page order (`PAGES`) and the grouping of links under the sources headings (`MERGE`).
- `gen.py`: writes the print pages and `canvas.json` to `root/project/`, the same files the design canvas holds.
- `pdf.py`: joins the print pages into one document and prints it. Fonts come from `../healthcare-q4-2026/fonts`. The `IMG` table maps the design canvas's uploaded images to the copies in `art/` and in the site's `assets/img/`.
- `web.py`: groups the same content into the thirteen site sections (`GROUPS`) and wraps it in the site header, footer and call to action from `_build/build.py`. Styles are in `mid-market-practice/assets/css/report.css`, shared with the other reports.
- `art/`: the logo lockup, the watermark and the two line illustrations used by the print layout.

## Where to make common edits
- Text, figures, table rows, links: the `pages_*.py` file that holds them. Both outputs pick the change up. Keep each print page inside its 890px text frame; `pdf.py` reports any that run over.
- A listed-company multiple: `COMPS` in `pages_c.py`. The medians, the print chart, the site chart and the company lists all follow from it.
- Site section order or titles: `GROUPS` in `web.py`.
- Button on the Technology page: the `"report"` entry on the technology sector in `_build/build.py`, then `python3 build.py` from `_build/`.
- After an edit here, send the changed files in `root/project/` to the design canvas as well so the two stay matched.

## Content rules
- Benchmark transactions: trailing 24 months only, no dates, names only where the tombstone is public and the seller is cleared to market; no deal values; the live portfolio in aggregate only.
- The four other banks quoted are named where they are quoted; Capstone Partners is never cited.
- The contact page closes the report and the sources page follows it as the final page. The list of subscription sources is a separate document and stays out of the report.
- Copy follows the house voice: full sentences, no em dashes, no arrows.

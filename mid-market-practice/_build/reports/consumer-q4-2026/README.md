# Consumer Q4 2026 sector report: source

One content file produces two outputs. Edit the source here and rebuild; do not hand-edit the outputs.

| Output | Where | Built by |
| --- | --- | --- |
| Site page (native HTML, site styles) | `mid-market-practice/insights/consumer-industry-report-q4-2026.html` | `web.py` |
| Downloadable PDF (22-page print layout) | `mid-market-practice/insights/consumer-industry-report-q4-2026.pdf` | `pdf.py` |

## Rebuild
```
./build.sh
```
This runs `web.py` and `pdf.py`. `pdf.py` needs Playwright with Chromium (`pip install playwright && playwright install chromium`). To change only the site page, `python3 web.py` is enough. Commit the regenerated outputs with the source change. Merging to `main` publishes the site.

## Files
- `content.md`: the whole report as Markdown, with every source linked inline. It is an export of the working document "Consumer: Q4 2026 M&A Sector Report", with the title and byline lines removed and the chart replaced by a `{{chart}}` line.
- `report.py`: reads `content.md` into the twelve sections and holds everything that is not prose: the four headline figures (`FIGS`), the stat bands for the four segments (`BANDS`), the chart data (`CHART`) and the contact details (`CONTACT`).
- `web.py`: renders the sections as the site page and wraps them in the site header, footer and call to action from `_build/build.py`. Styles are in `mid-market-practice/assets/css/report.css`.
- `pdf.py`: lays the same sections out for print (cover, running header and page numbers, contact page, then the sources as the final pages) and prints the PDF. `python3 pdf.py --keep` leaves the intermediate `_pdf.html` in this folder for inspection.
- `fonts/`: Cinzel, Newsreader and Quicksand (SIL Open Font License) for the PDF.
- `art/knot.png`: the watermark used by the PDF. The cover and stat-band photos are `rpt-*.jpg` in `mid-market-practice/assets/img/industries/consumer/`, set in `pdf.py` (cover) and `BANDS` in `report.py` (bands).

## Where to make common edits
- Text, table rows, links: `content.md`. Both outputs pick the change up. Headings must keep their names, because `SECTION_IDS` in `report.py` maps each heading to a section.
- A figure that appears in a stat band, on the cover or in the chart: change it in `content.md` and in `report.py`, so the two agree.
- Which sections start a new page in the PDF: `FLOW_ON` in `pdf.py`.
- Site styling: `assets/css/report.css`.
- Button on the Consumer page: the `"report"` entry on the consumer sector in `_build/build.py`, then `python3 build.py` from `_build/`.

## Content rules
- Benchmark transactions: closed since January 2025, shown by announcement date, with names only where the tombstone is public. The public tombstone governs who the client was.
- No other investment bank cited as a source.
- The contact page closes the report and the sources follow it as the final pages. The list of subscription sources is a separate document and stays out of the report.
- Copy follows the house voice: full sentences, no em dashes, no arrows.

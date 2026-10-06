# Healthcare Q4 2026 sector report: source

One set of content produces three outputs. Edit the source here and rebuild; do not hand-edit the outputs.

| Output | Where | Built by |
| --- | --- | --- |
| Site page (native HTML, site styles) | `mid-market-practice/insights/healthcare-industry-report-q4-2026.html` | `web.py` |
| Downloadable PDF (24-page print layout) | `mid-market-practice/insights/healthcare-industry-report-q4-2026.pdf` | `pdf.py` |
| Print layout pages for the design canvas | `root/` and `preview.html` (not committed) | `gen.py` |

## Rebuild
```
./build.sh
```
This runs `gen.py`, `pdf.py` and `web.py` in order. `pdf.py` needs Playwright with Chromium (`pip install playwright && playwright install chromium`). To change only the site page, `python3 web.py` is enough. Commit the regenerated outputs with the source change. Merging to `main` publishes the site.

## Files
- `gen.py`: all report content, the links (`U` dict) and the print layout. The sources list is collected from the links automatically.
- `extra.py`: the policy, buyer and owner, valuation bridge and seller readiness pages. Loaded by `gen.py`.
- `webhelpers.py`: the same building blocks (`P`, `H2`, `table`, `band`, `quote` and so on) rendered as semantic HTML. `gen.py` loads it when `web.py` sets `WEB`.
- `web.py`: groups the content into the twelve site sections and wraps it in the site header, footer and call to action from `_build/build.py`. Styles are in `mid-market-practice/assets/css/report.css`.
- `pdf.py`: prints `preview.html` to PDF with the bundled fonts and reports any page whose text runs past its frame.
- `fonts/`: Cinzel, Newsreader and Quicksand (SIL Open Font License) for the PDF.
- `art/` and `mkart.py`: illustrations and the watermark used by the print layout.
- `chk.py`: optional layout check for the print pages.

## Where to make common edits
- Text, figures, table rows, links: `gen.py` or `extra.py`. Both outputs pick the change up.
- Site section order or titles: `GROUPS` in `web.py`.
- Site styling: `assets/css/report.css`.
- Button on the Healthcare page: the `"report"` entry on the healthcare sector in `_build/build.py`, then `python3 build.py` from `_build/`.

## Content rules
- Benchmark transactions: trailing 24 months only, no dates, names only where the tombstone is public.
- No other investment bank cited as a source.
- Copy follows the house voice: full sentences, no em dashes, no arrows.

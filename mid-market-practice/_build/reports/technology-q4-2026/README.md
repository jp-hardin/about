# Technology Q4 2026 sector report

The source is `brief.pptx`, the Technology Q4 2026 Sector Brief deck. It is the authoritative document: the downloadable PDF and the site page are both built from it, so they always say the same thing.

To change the report, edit the deck in PowerPoint, save it here as `brief.pptx` and rebuild:

```
sh build.sh
```

This runs `../brief.py` (with `../webdeck.py` and `../deckhtml.py`), which writes:

- `insights/technology-sector-report-q4-2026.pdf`: the deck converted to PDF (the download).
- `insights/technology-sector-report-q4-2026.html`: the site page, in the site's report layout (side contents menu, numbered sections). Each deck page becomes one section with the same words, links, tables and logos; the deck's charts are redrawn as SVG from their data, each with its values as a table.
- `insights/technology-sector-report-q4-2026.md`: the same content as Markdown for AI tools, linked from the page and from `llms.txt`.
- `assets/img/reports/technology-sector-report-q4-2026/`: the logos and photos of people used on the page.

`brief.json` holds the cover's summary sentence, which is the page lead and the summary on the Insights page. Copy it from the cover if the cover changes; the build checks that it matches.

The build fixes two things in a working copy without changing `brief.pptx`: em dashes (site style) and links to the old `-industry-report-` and `/industries/` addresses. Anything else must be changed in the deck.

Requirements: LibreOffice with Impress (`soffice`), poppler-utils (`pdffonts`) and `pip install python-pptx pypdf Pillow`. The deck fonts are in `../brief-fonts/` (Carlito and Caladea stand in for Calibri and Cambria with the same metrics), so nothing needs installing system-wide.

To rebuild only the site page and Markdown (no PDF), run `python3 brief.py technology-q4-2026 --page-only` in `_build/reports/`.

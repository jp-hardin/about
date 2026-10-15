# Healthcare Q4 2026 industry report

The source is `brief.pptx`, the Healthcare Q4 2026 Industry Report deck. It is the authoritative document: the downloadable PDF and the site page are both built from it, so they always say the same thing.

To change the report, edit the deck in PowerPoint, save it here as `brief.pptx` and rebuild:

```
sh build.sh
```

This runs `../brief.py` (with `../webdeck.py` and `../deckhtml.py`), which writes:

- `insights/healthcare-industry-report-q4-2026.pdf`: the deck converted to PDF (the download).
- `insights/healthcare-industry-report-q4-2026.html`: the site page, organized for the web: chapters by what a reader comes for (The Short Version, Market Conditions, Sector by Sector, Deals and Buyers, Valuations and Public Markets, Indicators to Watch, What We're Reading, Disclosures and Sources), each holding the deck pages as subsections in one reading column (`flow.py`), with the same words, links, tables and logos; long tables and the sources fold away until opened; the deck's charts are redrawn as SVG from their data, each with its values as a table.
- `insights/healthcare-industry-report-q4-2026.md`: the same content as Markdown for AI tools, linked from the page and from `llms.txt`.
- `assets/img/reports/healthcare-industry-report-q4-2026/`: the logos and photos of people used on the page.

`brief.json` holds the cover's summary sentence, which is the page lead and the summary on the Insights page. Copy it from the cover if the cover changes; the build checks that it matches.

The build fixes two things in a working copy without changing `brief.pptx`: em dashes (site style) and links to the old `-industry-report-` and `/industries/` addresses. Anything else must be changed in the deck.

Requirements: LibreOffice with Impress (`soffice`), poppler-utils (`pdffonts`) and `pip install python-pptx pypdf Pillow`. The deck fonts are in `../brief-fonts/` (Carlito and Caladea stand in for Calibri and Cambria with the same metrics), so nothing needs installing system-wide.

To rebuild only the site page and Markdown (no PDF), run `python3 brief.py healthcare-q4-2026 --page-only` in `_build/reports/`.

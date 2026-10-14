# Consumer Q4 2026 sector report

The source is `brief.pptx`, the Consumer Q4 2026 Sector Brief deck. It is the authoritative document: the downloadable PDF and the site page are both built from it, so they always say the same thing.

To change the report, edit the deck in PowerPoint, save it here as `brief.pptx` and rebuild:

```
sh build.sh
```

This runs `../brief.py`, which writes:

- `insights/consumer-sector-report-q4-2026.pdf`: the deck converted to PDF (the download).
- `insights/consumer-sector-report-q4-2026.html`: the site page. Each page of the deck is shown as an image with its links live, followed by the page's full text, tables and chart data.
- `assets/img/reports/consumer-sector-report-q4-2026/`: the page images.

`brief.json` holds the cover's summary sentence, which is the page lead and the summary on the Insights page. Copy it from the cover if the cover changes; the build checks that it matches.

The build fixes two things in a working copy without changing `brief.pptx`: em dashes (site style) and links to the old `-industry-report-` and `/industries/` addresses. Anything else must be changed in the deck.

Requirements: LibreOffice with Impress (`soffice`), poppler-utils (`pdftoppm`, `pdffonts`) and `pip install python-pptx pypdf Pillow`. The deck fonts are in `../brief-fonts/` (Carlito and Caladea stand in for Calibri and Cambria with the same metrics), so nothing needs installing system-wide.

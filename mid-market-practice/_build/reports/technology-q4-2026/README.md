# Technology Q4 2026 industry report

The source is `brief.pptx`, the Technology Q4 2026 Industry Report deck. It is the authoritative document: the downloadable PDF and the site page are both built from it, so they always say the same thing.

To change the report, edit the deck in PowerPoint, save it here as `brief.pptx` and rebuild:

```
sh build.sh
```

This runs `../brief.py` (with `../webdeck.py`, `../deckhtml.py` and `../teaser.py`), which writes:

- `insights/technology-industry-report-q4-2026.pdf`: the deck converted to PDF (the download).
- `insights/technology-industry-report-q4-2026.html`: the site page in the sidebar layout, with chapters by what a reader comes for (Industry at a Glance, Market Conditions, Sector by Sector, Deals and Buyers, Valuations and Public Markets, Indicators to Watch, What We're Reading, Sources) holding the deck pages as sections. Each section is a teaser (`teaser.py`): the finding, a lead, the key points, the deals and buyers it names and its headline figures as plain text, with each chart summarized in a sentence and a Download the full report button. Charts, pictures, logos and long tables stay in the PDF. The deck's disclosures page stays in the PDF and is left off the web page, which links to the site's Important Disclosures page instead.
- `insights/technology-industry-report-q4-2026.md`: the same content as Markdown for AI tools, linked from the page and from `llms.txt`.
- `assets/img/reports/technology-industry-report-q4-2026/`: photos of people used on the page (company logos appear online as names; they stay as logos in the PDF).

`brief.json` holds the cover's summary sentence, which is the page lead and the summary on the Insights page. Copy it from the cover if the cover changes; the build checks that it matches.

The build fixes two things in a working copy without changing `brief.pptx`: em dashes (site style) and links to the old `-industry-report-` and `/industries/` addresses. Anything else must be changed in the deck.

Requirements: LibreOffice with Impress (`soffice`), poppler-utils (`pdffonts`) and `pip install python-pptx pypdf Pillow`. The deck fonts are in `../brief-fonts/` (Carlito and Caladea stand in for Calibri and Cambria with the same metrics), so nothing needs installing system-wide.

To rebuild only the site page and Markdown (no PDF), run `python3 brief.py technology-q4-2026 --page-only` in `_build/reports/`.

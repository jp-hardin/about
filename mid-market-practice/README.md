# Middle Market, Benchmark International

A standalone site for Benchmark International's Middle Market team: firm overview, five focused industries
(Industrial, Business Services, Consumer, Healthcare, Technology), and selected transactions
(tombstones) organized by industry and segment.

## Pages

| Page | What it is |
|---|---|
| `index.html` | Home page: hero, stats, awards, intro, journey, who we help, testimonials, industries grid, featured transactions, team, client stories, CEO library, HubSpot contact form |
| `industries/index.html` | Industries landing page (5 industries) |
| `industries/<sector>.html` | Sector page: overview, segments and sub-sectors, filterable tombstones with deal descriptions, market themes, what buyers value, active acquirers, services, client story, deal team |
| `transactions.html` | All curated tombstones, filterable by sector and searchable |
| `insights/index.html` | Insights: current quarterly sector report per industry plus an archive of earlier editions (from `INSIGHTS` in `build.py`) |
| `insights/<industry>-industry-report-q<N>-<year>.html` | Sector report pages and PDFs, generated from `_build/reports/<report>/` |

## Editing

The pages are generated. Don't hand-edit the HTML; edit the sources and rebuild:

- **Copy, sectors, team, stories:** `_build/build.py`
- **Tombstones:** `_build/tombstones.json` (`seller`, `buyer`, `sector`, `link`, plus either `image` or `seller_logo` + `buyer_logo`; `segment`, `desc`, `year` (used only for newest-first ordering, not displayed); `"featured": true` marks signature deals; `"also": [{"sector", "segment"}]` lists a deal in a second industry too). Old 12-sector URLs redirect to the new sector pages (see `LEGACY` in `build.py`).
- **Styles / behavior:** `assets/css/style.css`, `assets/js/main.js`
- **Photography:** `assets/img/industries/<sector>/` holds images chosen from the Mid-Market approved image library (Box): `hero.jpg` (1920x1000, sector page and report heroes), `card.jpg` (900x560, industry cards and Insights covers) and `g1.jpg` to `g4.jpg` (900x675, sector photo strip and report photo breaks). Replace a file with the same name and size to swap a photo; no code change needed. Report pages pick these up through `report_extras()` in `build.py`.

```bash
python3 mid-market-practice/_build/build.py
```

Then preview with `python3 -m http.server -d mid-market-practice` and open http://localhost:8000.

## Notes

- Sector "recent transactions" counts are the number of deals tagged to each industry on Benchmark's success page as of October 2026. Update `count` in `build.py` as needed.
- The contact form is Benchmark International's HubSpot form (portal 4039078).
- Published with the rest of this repo on GitHub Pages at `/mid-market-practice/`.

## Publishing

Merging to `main` triggers GitHub Pages' "pages build and deployment" run. If a run gets stuck in "queued" (for example during a GitHub Actions outage), push any small commit to `main` to start a fresh build.

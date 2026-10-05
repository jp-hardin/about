# Benchmark International — Mid-Market

A standalone site for Benchmark International's Mid-Market team: firm overview, five focused industries
(Industrial, Business Services, Consumer, Healthcare, Technology), and selected transactions
(tombstones) organized by industry and segment.

## Pages

| Page | What it is |
|---|---|
| `index.html` | Home page: hero, stats, awards, intro, journey, who we help, testimonials, industries grid, featured transactions, team, client stories, CEO library, HubSpot contact form |
| `industries/index.html` | Industries landing page (5 industries) |
| `industries/<sector>.html` | Sector page: overview, segments and sub-sectors, filterable tombstones with deal descriptions, market themes, what buyers value, active acquirers, services, client story, deal team |
| `transactions.html` | All curated tombstones, filterable by sector and searchable |

## Editing

The pages are generated. Don't hand-edit the HTML; edit the sources and rebuild:

- **Copy, sectors, team, stories:** `_build/build.py`
- **Tombstones:** `_build/tombstones.json` (`seller`, `buyer`, `sector`, `link`, plus either `image` or `seller_logo` + `buyer_logo`; `segment`, `desc`, `year` (used only for newest-first ordering, not displayed); `"featured": true` marks signature deals). Old 12-sector URLs redirect to the new sector pages (see `LEGACY` in `build.py`).
- **Styles / behavior:** `assets/css/style.css`, `assets/js/main.js`

```bash
python3 mid-market-practice/_build/build.py
```

Then preview with `python3 -m http.server -d mid-market-practice` and open http://localhost:8000.

## Notes

- Sector "recent transactions" counts are the number of deals tagged to each industry on Benchmark's success page as of October 2026. Update `count` in `build.py` as needed.
- The contact form is Benchmark International's HubSpot form (portal 4039078).
- Published with the rest of this repo on GitHub Pages at `/mid-market-practice/`.

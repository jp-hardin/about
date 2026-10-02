# MMT Website — Benchmark International Middle Market Team

An extended version of [vault.benchmarkcorporate.com/mmt](https://vault.benchmarkcorporate.com/mmt):
the original landing page content, plus an industry-coverage section modeled on
[hl.com/industries](https://hl.com/industries/), with tombstones from
[benchmarkintl.com/about/our-success](https://www.benchmarkintl.com/about/our-success/)
sorted into each sector.

## Pages

| Page | What it is |
|---|---|
| `index.html` | MMT home page: hero, journey, industries grid, selected transactions, team, client stories, testimonials, CEO library, HubSpot contact form |
| `industries/index.html` | Industries landing page (12 sector groups) |
| `industries/<sector>.html` | Sector page: overview, sub-sector coverage, what buyers value, sector tombstones, client story, deal team |
| `transactions.html` | All 107 curated tombstones, filterable by sector and searchable |

## Editing

The pages are generated. Don't hand-edit the HTML; edit the sources and rebuild:

- **Copy, sectors, team, stories:** `_build/build.py`
- **Tombstones:** `_build/tombstones.json` (`seller`, `buyer`, `sector`, `link`, plus either `image` or `seller_logo` + `buyer_logo`; `"mmt": true` marks MMT-featured deals)
- **Styles / behavior:** `assets/css/style.css`, `assets/js/main.js`

```bash
python3 mmt-website/_build/build.py
```

Then preview with `python3 -m http.server -d mmt-website` and open http://localhost:8000.

## Notes

- Sector "recent transactions" counts are the number of deals tagged to each industry on Benchmark's success page as of October 2026. Update `count` in `build.py` as needed.
- The contact form is the same HubSpot form the vault page uses (portal 4039078).
- Published with the rest of this repo on GitHub Pages at `/mmt-website/`.

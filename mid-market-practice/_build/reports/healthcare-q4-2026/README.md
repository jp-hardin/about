# Healthcare Q4 2026 sector report: source

The published page `mid-market-practice/reports/healthcare-q4-2026.html` is generated. Edit the source here and rebuild; do not hand-edit the HTML.

## Files
- `gen.py`: report content and layout (one 816x1056 page per section, links in the `U` dict, sources page collected automatically).
- `extra.py`: the policy, buyer/owner implication, valuation bridge and seller readiness pages. Loaded by `gen.py`.
- `web.py`: turns the generated preview into the site page.
- `art/` and `mkart.py`: section illustrations. Copies used by the site live in `mid-market-practice/reports/img/`.
- `chk.py`: optional overflow check (needs Playwright). Prints `OVER` for any page whose content runs past its frame.

## Rebuild
```
cd mid-market-practice/_build/reports/healthcare-q4-2026
python3 gen.py && python3 web.py
```
Commit the regenerated `mid-market-practice/reports/healthcare-q4-2026.html` with the source change. Merging to `main` publishes the site.

## Button on the Healthcare page
Set in `mid-market-practice/_build/build.py` by the `"report"` entry on the healthcare sector. Run `python3 build.py` from `_build/` after changing it.

## Content rules
- Benchmark transactions: trailing 24 months only, no dates, names only where the tombstone is public.
- No other investment bank cited as a source.
- Copy follows the house voice: full sentences, no em dashes, no arrows.

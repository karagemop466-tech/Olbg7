# OLBG coverage dashboard

A daily snapshot of what OLBG is actually offering across fifteen sports, with **our own originated prices**, one
pick per event, a confidence label, and a written prediction of at least thirty words for every pick.

Site: `docs/` (published with GitHub Pages). Snapshot date: **2026-10-26**.

## What is in here

| Path | What it holds |
| --- | --- |
| `data/events.json` | Every market row captured from OLBG, with the source URL, tip counts and percentages exactly as published |
| `data/lines.json` | The same rows after pricing (probability, decimal and American price, band check, exclusion reason) |
| `data/picks.json` | One pick per event, five per sport where five qualifying events exist |
| `data/predictions.json` | The written predictions, their fact links, and what could not be checked |
| `scripts/price_model.py` | The pricing and confidence rules, in code |
| `scripts/build_site.py` | Builds `docs/` from the JSON |
| `scripts/link_check.py` | Fails the build on broken internal links, missing sources, short predictions or out-of-band picks |
| `COORDINATION.md` | Shared task board: claims, sources, verification log, irregularities |
| `docs/` | The published site: landing page, 15 sport pages, all-lines table, method page, “Flagged for review” page |

## Coverage on 2026-10-26

51 picks across 14 sports. Snooker has none — OLBG returned “No tips found.” for snooker, so there was nothing to
price. Six sports cannot fill a five-pick card because OLBG itself is thin (rugby league has 2027 outrights only,
baseball lists one game, golf has four tipster-backed selections). Every shortfall is stated on the site rather than
padded out.

| Sport | Events on OLBG | Picks |
| --- | --- | --- |
| Basketball | 14 | 5 |
| Cricket | 13 | 5 |
| Ice Hockey | 11 | 5 |
| Rugby Union | 13 | 5 |
| Tennis | 13 | 5 |
| Volleyball | 14 | 5 |
| Greyhounds | 8 | 5 |
| Gaelic Sports | 4 | 4 |
| Golf | 3 | 3 |
| Rugby League | 3 | 3 |
| Darts | 2 | 2 |
| Handball | 15 | 2 |
| Baseball | 1 | 1 |
| Motor Racing | 2 | 1 |
| Snooker | 0 | 0 |

## Pricing in one paragraph

OLBG publishes tip counts, not odds. For each selection we take the tip share, shrink it towards the market's base rate
(`w = n/(n+10)`, so a single tip barely moves the price and forty tips dominate), then quote a price with a 5% theoretical
overround. Picks must fall between −250 and +10000. “High” confidence needs at least eight tips on the market **and** a
modelled chance of 62% or better, which is why no single-tip “100%” selection is ever rated highly. Full detail on the
site's Method page.

## Sources and honesty rules

* Every table row links to the OLBG page it came from.
* Form numbers are only stated where an official league page was read during the session — NHL.com standings and NBA.com
  standings, both dated to the snapshot.
* Injuries, line-ups, weather, travel and head-to-head records could not be checked against an official source from this
  environment, so **none are claimed anywhere**. Each prediction says what it could not check.
* Unconfirmed fields are left blank and listed on the “Flagged for review” page with source links.
* OLBG tipster comments are opinions and are never repeated as fact; one captured comment misidentifies which team
  Giannis Antetokounmpo plays for, and another contradicts the official NHL road record.

## Build locally

```bash
python3 scripts/price_model.py    # regenerate data/lines.json and data/picks.json
python3 scripts/build_site.py     # regenerate docs/
python3 scripts/link_check.py     # verify sources, word counts, band and internal links
```

Deployment: `.github/workflows/pages.yml` rebuilds and publishes `docs/` on every push to `main`.

Prices here are analytical output from a documented method, not bookmaker offers. 18+, gamble responsibly.

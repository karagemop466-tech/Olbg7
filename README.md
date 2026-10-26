# OLBG board review — 15 sports

Reverse-engineering and review of the live OLBG betting board for the 15 sports in scope, with every
event priced by this project (no bookmaker prices are copied), written predictions, and a source link
on every row.

**Published site:** https://karagemop466-tech.github.io/Olbg7/

## What is in here

| Path | What it is |
|---|---|
| `docs/` | The published static site (GitHub Pages, branch `main`, folder `/docs`) |
| `data/raw/` | Raw capture of each OLBG sport hub — event names, ids, times, most-tipped selection |
| `data/events.json` | Consolidated board: 119 events, each with originated lines, tier and basis |
| `data/verified_tables.json` | The verified competition records every Tier A line is computed from |
| `data/predictions.json` | 44 written predictions, each tied to an event id and a price |
| `data/sources.json` | Every external page used, and what it was used for |
| `data/flagged.json` | Gaps, contradictions and unverified items, with sources |
| `scripts/build_data.py` | Prices every event; writes `data/events.json` |
| `scripts/build_site.py` | Generates the site into `docs/` |
| `scripts/check_links.py` | Fails if any internal link is broken |

## Rebuild

```
python3 scripts/build_data.py     # re-price the board
python3 scripts/build_site.py     # regenerate docs/
python3 scripts/check_links.py    # link check, must exit 0
```

## Headline numbers (capture: 26 October 2026)

- 15 sports, 119 live events, 119 priced (12 Tier A from official standings, 107 Tier B reference lines)
- 44 written predictions, 39–55 words each; 7 graded High confidence (65%+), 18 Medium, 19 Low
- 0 snooker and 0 greyhound predictions — nothing bettable was on the board; reasons in `docs/flagged.html`

## Method in one line

Tier A: strength = (for − against) ÷ games, expected margin = strength difference + home edge,
probability = logistic(margin ÷ σ), price = 1 ÷ probability × 1.05. Tier B: OLBG tip share shrunk
toward 50/50 by sample size. Full write-up on the site's Method page.

## Honest limitations

No injury or team-news data was confirmed for any fixture, so none is claimed. NBA and NHL records come
from secondary sources (Wikipedia / BBC / Elite Prospects) because the official league sites could not be
reached from the build environment. Both points are on the Flagged for Review page.

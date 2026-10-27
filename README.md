# OLBG Coverage Desk

A daily board of **our own** betting lines and written predictions for the 15 sports covered on
[OLBG](https://www.olbg.com/betting-tips): Golf, Volleyball, Rugby Union, Cricket, Snooker, Darts,
Baseball, Gaelic Sports, Greyhounds, Tennis, Motor Racing, Handball, Ice Hockey, Basketball and
Rugby League.

Live site: **https://karagemop466-tech.github.io/Olbg7/**

Snapshot for everything below: **2026-10-27**. Every price is ours; none is a bookmaker price.

## Read the site in this order

| Page | What it answers |
|---|---|
| `index.html` | What is on today, the highest-confidence picks, and how much of each sport we could price |
| `picks.html` | Every written prediction, grouped by sport, strongest first, with the evidence for each |
| `lines.html` | Every OLBG event and every market we priced, with the method on each row |
| `olbg-map.html` | How OLBG's site is structured: URL grammar, sport ids, what each listing really contains |
| `method.html` | The arithmetic behind every number, and what is deliberately not done |
| `sources.html` | The source tiers used, page by page |
| `flagged.html` | The 19 things that could not be resolved, and the values deliberately left blank |
| `sports/<sport>.html` | One page per sport: picks, then the full priced market table |

## Numbers

- 114 OLBG events inventoried, 111 priced, **251 markets**, **57 written predictions**
  (16 high confidence, 22 medium, 19 low), 13 of the high picks inside the &minus;250 to +10000 band.
- Snooker and greyhounds have no market at all on OLBG today ("No tips found"), so they have no picks.
  Four sports carry fewer than five picks because OLBG lists fewer than five events for them
  (Golf 3, Baseball 3, Gaelic 3, Rugby League 3, Darts 2, Motor Racing 2). That is stated on the site,
  not padded out.

## How it is built

Three scripts, no dependencies, and no number typed by hand:

```bash
python3 tools/originate.py     # data/board/inventory-*.json + official.json -> data/board/lines.json
python3 tools/build_board.py   # lines.json + picks + official + flags      -> *.html, sports/*.html
python3 tools/check_board.py   # links, word counts, banned words, selection named, join check
```

| Path | What it is |
|---|---|
| `data/board/inventory-*.json` | Verbatim OLBG listings retrieved 2026-10-27, one record per row |
| `data/board/official.json` | Curated official tables (MLB, NHL, EuroLeague, EHF, URC, ATP, PGA/OWGR, PDC) with source and tier |
| `data/board/lines.json` | Generated: 114 events, per-market chance, price, American odds, method, basis, band flag |
| `data/board/picks-team.json`, `picks-individual.json` | The 57 predictions: event id, market, selection, prose, sourced facts |
| `data/board/flags.json` | 19 irregularities and the list of blanks |
| `tools/originate.py` | CAL-4 engine: CAL-4C consensus, CAL-4R rating, CAL-4P prior (never pick-eligible) |
| `tools/build_board.py` | Builds every page; computes confidence, gaps and the executive summary |
| `tools/check_board.py` | Fails on a broken link, <30-word or duplicated prose, a selection missing from the opening sentence, a bad price |

Pricing in one line: `p = (tips + K × prior) / (total + K)` with `K` tapered 20/12/6 to the sample size,
5% margin on the price, band 1.40–101.00 decimal. Full detail on `method.html`.

## Verification

- Every row on `lines.html` comes from an OLBG page that was retrieved, and every pick links to the OLBG
  row it is priced from plus the official table or report behind its claims.
- Official bodies are preferred (MLB.com, NHL.com, EHF, TVF, GAA, ATP, ESPNcricinfo); secondary sources
  are labelled `media` in the fact list; OLBG itself is labelled `olbg`.
- Where a value could not be confirmed it is left blank and listed on `flagged.html` — never inferred.
- `check_board.py` passes: 24 pages, all internal links resolve, 57 picks, 251 markets.

## Earlier boards, kept unchanged

These are preserved for audit and reachable from `archive.html`; the dashboard does not use them.

| Path | Board |
|---|---|
| `all-events.html`, `methodology.html` | Session `9922c58c`'s 121-event board (CAL-1 engine, `data/events.json`, `data/pricing.json`) |
| `olbg-tips/` | Session `dfa8f20c`'s 127-row tip-consensus board (`data/consensus/`, `scripts/`) |
| `docs/board-review/` | Session `arena-88221c1f`'s 119-event board (`data/board-review/`, `scripts/build_board_review.py`) |
| `docs/` | The original 75-row board from session `610d0099` |

Their generators (`tools/build_site.py`, `scripts/build_site.py`, `scripts/build_site_olbg.py`) now refuse
to run unless `LEGACY_BUILD=1` is set, so an old build cannot overwrite the live root pages.

## Scope limits, stated up front

No injury feed could be retrieved for any of the 15 sports, so no pick claims a fitness doubt; the gap is
recorded as a blank on `flagged.html` instead of being filled with speculation. Only content that appeared
in the retrieved OLBG HTML is priced. Snooker and greyhounds returned nothing at all.

18+. No assurance of profit. Support: GamCare, GambleAware.

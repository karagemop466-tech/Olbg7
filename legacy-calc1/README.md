# Preserved historical board — not current

This directory contains the 27 October 2026 CAL-1 board produced by session
`sess-arena-4efa4ee3`. Every page carries an `historical-warning` banner. The lines are
historical tip-split-derived estimates, not bookmaker quotes, and the claims have not been
rechecked after capture. The live board is the fail-closed snapshot at the repository root
(generated from `data/current.json` by `tools/build_current.py`).

---

# OLBG Coverage Desk — CAL-1 snapshot, 2026-10-27

Our own betting lines and written predictions for the 15 sports covered on
[OLBG](https://www.olbg.com/betting-tips): Golf, Volleyball, Rugby Union, Cricket, Snooker,
Darts, Baseball, Gaelic Sports, Greyhounds, Tennis, Motor Racing, Handball, Ice Hockey,
Basketball and Rugby League.

Snapshot date: **2026-10-27**. Every price is ours; none is a bookmaker price.

## Numbers

- 143 OLBG events inventoried from a same-day re-crawl of all 15 sport roots; 142 priced
  (one T20 Blast 2027 outright printed no split and is deliberately unpriced).
- 49 written predictions, each 51-74 words, with 70 sourced facts behind them.
- High-confidence rule: fair probability strictly above 70%, at least 8 tips, fair decimal
  inside 1.40-101.00 (the -250 to +10000 band applied to the fair price). **Zero picks
  qualify on this snapshot**; near-misses are listed on `flagged.html` (F-007).
- Snooker and Greyhounds returned "No tips found" and carry no picks. Nine sports fall
  short of the five-pick target because OLBG itself carried too little market data; the
  shortfalls are flagged, never padded.
- Handball: 15 of 19 OLBG rows print "Tie" as the most-tipped selection (display defect,
  F-002). No Tie pick is published; only the four real-club rows are used.

## How it is rebuilt

```bash
python3 tools/build_events.py                                   # data/raw/*.json -> data/events.json
python3 tools/pricing.py                                        # events -> data/pricing.json
python3 tools/build_picks.py                                    # picks_src1/2 -> data/picks.json
LEGACY_BUILD=1 SITE_OUT=legacy-calc1 python3 tools/build_site.py
LEGACY_BUILD=1 SITE_OUT=legacy-calc1 python3 tools/check_site.py
```

The guard at the top of `tools/build_site.py` refuses to run without `LEGACY_BUILD=1` and
requires `SITE_OUT`, so the historical generator can never overwrite the live root pages.

## Data and flags

| Path | What it is |
|---|---|
| `data/events.json` | 143 inventoried events with the OLBG path of each (schema v2) |
| `data/pricing.json` | CAL-1 fair chances, card prices, American odds, band and confidence flags |
| `data/picks_src1.json`, `data/picks_src2.json` | Editorial predictions and per-fact source links |
| `data/picks.json` | Generated pick records; no number is typed by hand |
| `data/sources.json` | URL grammar, per-sport crawl status and the source register |
| `data/flags.json` | 17 irregularities (F-001..F-017) and nine deliberate blanks |

18+. No assurance of profit. Support: GamCare, GambleAware.

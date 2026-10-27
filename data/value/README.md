# Value Desk data — provenance (27 October 2026)

Session `sess-arena-7cf491a1`. Everything in this directory is additive; no other
board's data file is modified.

| File | What it holds |
|---|---|
| `capture.json` | 143 market rows transcribed from the 15 OLBG sport hubs for 27 Oct 2026 by session `arena-e0f59668` (`data/daily/2026-10-27/inventory.json`), copied here with attribution and six independent hub spot-checks by this session. |
| `extra_markets.json` | 50 further rows read from OLBG event pages (golf second selections, darts PC31 split, F1 qualifying, baseball run line/totals) or from official competition sources (WST, PDC, MLB, F1, PGA TOUR, LPGA, EHF, URC, Munster GAA, RLWC, Romford). Each row carries the URL it came from. |
| `editorial.json` | 85 original written predictions with their facts and source URLs (generated from `tools/value_editorial.py`). |
| `lines.json` | 193 originating lines, one per event/market row, with fair probability, method, published price, band flags and source URL. |
| `picks.json` | 85 picks joined to their line, confidence, price, prediction, facts, source links and flags. |
| `sources.json` | 59 distinct https sources with kind, sports and claimed facts. |
| `flags.json` | 17 repository-level findings plus 204 row-level flags. |
| `summary.json` | counts used by the site. |
| `verification.json` | result of `tools/value_check.py`. |

Rebuild:

```sh
python3 tools/value_build.py
python3 tools/value_site.py
python3 tools/value_check.py
```

Rules: every table row has an https source URL; bookmaker odds, injury/team news,
start timezone and unverified field sizes are blank rather than inferred; OLBG tip
splits are transcribed verbatim; prices are our own, never bookmaker offers. See
`value-desk/method.html` for the formula and `value-desk/flagged.html` for every irregularity.

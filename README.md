# OLBG Coverage Desk

**Current board: 27 October 2026.** Live at **https://karagemop466-tech.github.io/Olbg7/**

A daily board of our own betting lines and written predictions for the 15 sports OLBG covers
(Golf, Volleyball, Rugby Union, Cricket, Snooker, Darts, Baseball, Gaelic Sports, Greyhounds,
Tennis, Motor Racing, Handball, Ice Hockey, Basketball, Rugby League).

| Path | What it is |
|---|---|
| `index.html` | Today's dashboard: executive summary, the pick table, coverage by sport |
| `board/<sport>.html` | One page per sport: picks table, full written predictions with sourced facts, then every market we priced |
| `board/all-markets.html` | Every market captured from OLBG today, with our line, chance and confidence |
| `board/method.html` | How a line is originated (engine TS-27), the constants, the confidence and band rules |
| `board/sources.html` | The eight pages this build was made from |
| `board/flagged.html` | 16 irregularities and 4 deliberate blanks, each with an evidence link |
| `data/today/capture.json` | Raw capture: 126 market rows read off the 15 OLBG sport hubs |
| `data/today/lines.json` | Engine output: 159 rows with a price or an explicit "unpriced" |
| `data/today/picks_source.py` | The 51 hand-written predictions (facts + links), validated at build time |
| `data/today/form.json` | The official tables: EuroLeague, NHL, EHF Champions League, World Series |
| `data/today/flags.json` | The irregularity register |
| `tools/price_today.py` | Pricing engine: OLBG tip split blended with the official table |
| `tools/build_today.py` | Site generator for `index.html` and `board/` |
| `tools/check_today.py` | Verification: links, word counts, banned words, sources, band |

Rebuild:

```bash
python3 tools/price_today.py    # capture + tables -> lines.json
python3 tools/build_today.py    # lines + picks -> index.html, board/
python3 tools/check_today.py    # fails on a broken link, a short prediction or a missing source
```

Today's coverage in one line: 51 written predictions of 58-78 words across 13 sports, 6 at high
confidence, 146 markets priced from 126 captured, and two sports (snooker, greyhounds) with no
markets published by OLBG at all. Eight sports fall short of five picks; the reason for each is on
that sport's page and on `board/flagged.html`.

---

## Earlier boards in this repository (all still served)

A daily board of **our own** betting lines and written predictions for the 15 sports covered on
[OLBG](https://www.olbg.com/betting-tips): Golf, Volleyball, Rugby Union, Cricket, Snooker, Darts,
Baseball, Gaelic Sports, Greyhounds, Tennis, Motor Racing, Handball, Ice Hockey, Basketball and
Rugby League.

Live site: **https://karagemop466-tech.github.io/Olbg7/**

Retrieval date for the published event inventory, prices and predictions: **2026-10-26**. This is a historical snapshot, not a current 2026-10-27 betting card; event status, markets, start times and team news have not been refreshed. See the dashboard freshness warning before using any entry.

## What is in here

| Path | What it is |
|---|---|
| `index.html` | Dashboard: executive summary, ranked picks, coverage by sport |
| `sports/*.html` | One page per sport: picks table, written predictions with source links, every inventoried event |
| `all-events.html` | All 121 inventoried events with our originating line |
| `olbg-map.html` | The reverse-engineered OLBG structure: URL grammar, sport ids, what each page returned |
| `methodology.html` | How a line is originated (CAL-1 / CAL-2 / CAL-3), the confidence rules, the &minus;250 to +10000 band |
| `sources.html` | Source register, grouped by sport |
| `flagged.html` | Everything unconfirmed, contradictory or missing |
| `data/events.json` | Event inventory: 121 events, each with the OLBG path it came from |
| `data/pricing.json` | Every originating line produced by the engine |
| `data/picks.json` | 56 written predictions (built output), each with facts and source links |
| `data/picks_src1.json` | Hand-written predictions for the eight sports with a full OLBG card |
| `data/picks_src2.json` | Hand-written predictions for the outright and single-market sports |
| `tools/build_picks.py` | Merges the two source files into `data/picks.json` and validates word counts, sources and banned words |
| `data/pricing.json` | CAL-1 output: 121 events inventoried, 116 priced, 5 unpriced |
| `data/sources.json` | Source register as data + the OLBG URL grammar |
| `data/flags.json` | Irregularity register (F-001 to F-016) and the list of deliberate blanks |
| `tools/pricing.py` | The pricing engine |
| `tools/build_site.py` | Static site generator (no dependencies) |
| `tools/check_site.py` | Verification pass: links, word counts, banned words, source presence |
| `docs/` | Earlier 75-row board from session `610d0099`, preserved unchanged (different method) |
| `data/picks_610d0099.json` | That board's data, kept as-is |
| `tools/build_site_docs.py` | That board's generator, write path repointed so it cannot overwrite `data/picks.json` |
| `COORDINATION.md` | Shared task board, integration record and log |

## How a line is originated

OLBG prints a tip split for each selection ("9/16 Win Tips", 56%) but not bookmaker prices - those are
rendered client-side and were absent from every page retrieved. So the board is priced from the split:

1. prior from market structure (0.50 two-way, 0.3333 three-way, 0.125 outright);
2. shrink the split toward that prior with 6 pseudo-tips: `p = (wins + 6 x prior) / (total + 6)`;
3. fair price `1/p`, card price `1/(p x 1.05)`;
4. American conversion;
5. confidence from `p`, the sample size and the price band.

Full detail, including the two fallbacks used where OLBG has no usable market (handball's "Tie"
display defect, and one unpriced motor-racing market), is on `methodology.html`.

## Verification

- Every factual claim in a prediction carries a link to the page it came from, on the same card.
- `python3 tools/check_site.py` fails the build on a broken internal link, a pick with no source, a
  prediction under 30 words, or the words "model"/"verified" inside a prediction.
- Where a value could not be confirmed it is left blank and listed in `data/flags.json`.

## Rebuild

```bash
python3 tools/pricing.py      # data/events.json -> data/pricing.json
python3 tools/build_site.py   # data/*.json      -> *.html
python3 tools/check_site.py   # verification pass
```

No third-party packages are required.

## Scope limits, stated up front

Snooker returned "No tips found" from OLBG on the retrieval date; Golf carried three outright markets
of two tips each; Baseball had a single live game; Rugby League offered only season ante-post; Gaelic
Sports produced four selections. Those five sports are published at 0-4 picks instead of 5, and the
reason is recorded on the flagged page rather than papered over.

18+. No assurance of profit. Support: GamCare, GambleAware.


---

## Tip-consensus board (`/olbg-tips/`) — session `dfa8f20c`

A third, additive view kept beside the two dashboards above. It prices **only** markets that OLBG publishes tips for,
so every one of its 127 rows can be checked back to an OLBG page.

| Path | Contents |
| --- | --- |
| `data/consensus/events.json` | 127 market rows from OLBG's fifteen sport pages, each with source URL, tip count, market total and published percentage |
| `data/consensus/lines.json`, `picks.json` | The priced rows and the resulting picks (generated) |
| `data/consensus/predictions.json` | 51 unique written predictions, ≥ 30 words each, with per-fact source links and an explicit "not checked" line |
| `scripts/price_model.py` | Pricing and confidence rules: tip share shrunk to the market base rate (`w = n/(n+10)`), 5% overround, −250/+10000 band, one pick per event, five per sport |
| `scripts/build_site.py` | Builds `olbg-tips/` from the JSON (`SITE_OUT=olbg-tips`) |
| `scripts/link_check.py` | Fails on broken links, missing sources, short predictions, out-of-band picks, duplicates |
| `olbg-tips/` | Executive summary, 15 sport pages, all-lines table, method page, flagged-for-review page |
| `.github/workflows/pages.yml` | Re-runs pricing, build and checks on pushes and pull requests |

Coverage: 51 picks in 14 sports, 0 high-confidence picks under the strict >70% estimate threshold (with at least eight tips and the requested price band). Snooker has none — OLBG's snooker tips page returns "No tips found.",
so there are no tip counts to price from; the fixtures themselves are covered on the other boards. Every shortfall is
stated on the board rather than padded out.

Sources: OLBG sport pages plus three event pages opened in full, and official form only where an official page was read
(NHL.com and NBA.com standings, dated to the snapshot). ATP and ICC ranking pages rendered without a data table, so no
rankings are used. Injuries, line-ups and weather could not be checked, so none are claimed.

Build locally:

```bash
python3 scripts/price_model.py
SITE_OUT=olbg-tips python3 scripts/build_site.py
SITE_OUT=olbg-tips python3 scripts/link_check.py
```

---

## Sub-board: `/docs/board-review/` (session arena-88221c1f)

A second, independent board review published alongside the main desk dashboard. It is namespaced so the two
never collide: pages live under `docs/board-review/`, data under `data/board-review/`.

**Direct link:** https://karagemop466-tech.github.io/Olbg7/docs/board-review/

| Path | What it is |
|---|---|
| `docs/board-review/` | Published sub-board: summary, 44 predictions, full board, 15 sport pages, method, sources, flagged |
| `data/board-review/raw/` | Raw capture of each of the 15 OLBG sport hubs (names, ids, times, most-tipped selection) |
| `data/board-review/events.json` | 119 events, each with originated lines, tier and basis |
| `data/board-review/verified_tables.json` | The competition records every Tier A line is computed from |
| `data/board-review/predictions.json` | 44 written predictions, each tied to an event id and a price |
| `scripts/build_data.py` | Prices every event (writes `data/board-review/events.json`) |
| `scripts/build_board_review.py` | Generates `docs/board-review/` |

Results (capture 26 Oct 2026): 15 sports, 119 events, 119 priced (12 Tier A from official standings, 107 Tier B
reference lines); 44 predictions of 39-55 words; 3 High / 22 Medium / 19 Low confidence; 0 snooker and 0 greyhound
predictions because nothing bettable was on the board.

Method: Tier A strength = (for - against) / games, expected margin = strength gap + home edge, probability =
logistic(margin / sigma), price = 1 / probability x 1.05. Tier B: OLBG tip share shrunk toward 50/50 by sample size.
Sport ids were taken from OLBG's own sitemap, not third-party repos.

Known gaps, all published on the sub-board's Flagged for Review page: no injury or team-news data could be confirmed
for any fixture so none is claimed; NBA and NHL records rest on secondary sources (Wikipedia / BBC / Elite Prospects)
because the official league sites were unreachable; handball is the only sport with fully official data (EHF).

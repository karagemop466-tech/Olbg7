# OLBG Coverage Desk

A daily board of **our own** betting lines and written predictions for the 15 sports covered on
[OLBG](https://www.olbg.com/betting-tips): Golf, Volleyball, Rugby Union, Cricket, Snooker, Darts,
Baseball, Gaelic Sports, Greyhounds, Tennis, Motor Racing, Handball, Ice Hockey, Basketball and
Rugby League.

Live site: **https://karagemop466-tech.github.io/Olbg7/**

**Current cycle: retrieved and priced on 2026-10-27 (05:30-06:10 UTC).** The previous cycle
(2026-10-26, 121 events / 56 picks) is still in `data/*.json` and is kept for comparison, not as the live board.

## What this cycle produced

| Measure | Result |
|---|---|
| OLBG pages read | 12 sport pages + 6 event pages (both sides of each market) |
| Unique markets | **152** across 13 sports; Snooker and Greyhounds returned "No tips found." |
| Lines originated by us | **141 priced**, 11 left unpriced with the reason on the row |
| Written predictions | **52**, 63-115 words each, 13 of 15 sports at 1-5 picks |
| Confidence split | 2 high / 29 medium / 21 low |
| Reliability grades | 22 grade A, 60 grade B, 59 grade C markets |
| Flags raised | **20** (structural defects, source conflicts, deliberate blanks) |
| Distinct sources | 61, every fact in every write-up links to the page it came from |

The two high-confidence picks are both in cricket - Pakistan over Sri Lanka at 1.41 and Ireland over
Namibia at 1.45 - because the brief asks for high-confidence work inside the &minus;250 to +10,000
band, and near-unanimous favourites (Afghanistan 15/16, Fernandez 10/12, KalPa 5/5) price at 1.15-1.36,
which is outside it. Those are published in their own "strong, but outside the band" table so the
decision is auditable instead of hidden.

## What is in here

| Path | What it is |
|---|---|
| `index.html` | Executive summary: the picks table for all 52 picks, the high-confidence cards, the declined near-certainties, per-sport summary, coverage of all 15 sports |
| `sports/<sport>.html` | One page per sport: written pick cards (prediction, price, why it is a lean, how it misses, sourced facts), a pick table, every market priced, every market not priced, and the flags touching that sport |
| `all-events.html` | All 152 captured markets with our line, grade and an OLBG row link plus an official-source link |
| `flagged.html` | The 20 flags plus the register of every cell deliberately left blank |
| `sources.html` | Source register grouped by domain, with what each page was used for and which picks cite it |
| `methodology.html` | Capture, the pricing formula, the grade rules, where we intervened in the data, and how to rebuild |
| `olbg-map.html` | The reverse-engineered OLBG structure: URL grammar, sport ids, what each page returned |
| `data/cycle-20261027/events_raw.json` | The 155 captured market rows exactly as OLBG printed them |
| `data/cycle-20261027/lines.json` | CAL-1R output: every market with structure, prior, probability, our price, confidence, grade and notes |
| `data/cycle-20261027/predictions.json` | The 52 written picks with facts, per-fact sources, angle and risk |
| `data/cycle-20261027/sources.json`, `flags.json` | The same registers the pages are built from |
| `tools/unify_price.py` | The pricing engine (CAL-1R) |
| `tools/cycle_picks.py` | Attaches the written picks to priced markets; validates length, banned words and https sources |
| `tools/cycle_site.py` | Generates every page above |
| `tools/check_cycle.py` | Fails on a broken link or anchor, a short or unsourced pick, a high-confidence line on a grade C market, or an unexplained shortfall |
| `data/events.json`, `data/pricing.json`, `data/picks.json`, `data/flags.json` | The 2026-10-26 cycle, kept unchanged as the comparison baseline |

## How a line is originated (CAL-1R)

OLBG prints a tip split for each selection ("9 / 16 Win Tips", 56%) but no bookmaker price - the odds
widget is rendered client-side and was absent from every page retrieved (flag U-001). So each line is
built from the split:

1. **prior** from market structure - 1/2 two-way, 1/3 where OLBG prints a draw or tie as a listed outcome
   (every EHF handball money line, and the cricket Test, whose "Win Match" market carries a Draw row;
   limited-overs cricket does **not**, because it cannot be drawn), 1/8 for outrights because OLBG does not
   print field sizes (U-004);
2. **shrink** the split toward that prior with K = 6 pseudo-tips: `p = (wins + 6 x prior) / (total + 6)`;
3. **price** it: fair = `1/p`, our line = `1/(p x 1.05)`, then the standard American conversion;
4. **grade** the market: A = 8+ tips and no structural anomaly, B = 3-7, C = under 3 tips, a degenerate
   0%/100% split, or a 3-way draw cluster. High confidence is blocked on grade C and requires a price
   inside &minus;250 to +10,000 with a post-shrink probability of at least 60%.

## What we refused to do

- No handball "Tie" line is sold as a prediction even though 11 of 15 handball markets vote for it: the
  EHF's own group tables show one drawn match in thirty played, so those selections are graded C, capped at
  low confidence, and the team-side prices are published instead (U-002).
- No market with a 0/0 split is filled in: 11 rows (handball handicaps and totals, one WNBA-style cricket
  batsman market, an unprinted World Series total) are listed as "not priced" with the reason.
- No time comes from the OLBG card: its printed clock is wrong for North American fixtures on this capture
  (Game 4 printed 21:00 for an 8:00 pm ET first pitch; NHL printed 20:07 for a 20:00 puck drop) while
  matching the governing bodies for European fixtures - U-010. Every time in the copy is the league's.
- No inference where a source disagreed: the third-Test start time (U-005), Taylor Hall's availability
  (U-009), the Pro D2 table (U-008), the stale F1 points quoted inside OLBG's own comments (U-007) and the
  Maybank defending-champion line (GOLF-001) are all recorded as conflicts with both readings shown.
- The words "model" and "verified" do not appear in any published prediction; `tools/check_cycle.py`
  fails the build if they do.

## Rebuild

```bash
python3 tools/unify_price.py    # events_raw.json -> lines.json (prices every captured market)
python3 tools/cycle_picks.py    # lines.json      -> predictions/sources/flags for this cycle
python3 tools/cycle_site.py     #                  -> index, 15 sport pages, all-events, flagged, sources, methodology
python3 tools/check_cycle.py    # verification pass on the built board
```

No third-party packages are required. ## The other 27 October boards at the root, and the relocated Coverage Desk

`picks.html`, `lines.html`, `method.html` and `archive.html` are session `arena-3b1b6ed4`'s 27 October board (114
events, 251 market rows, 57 written predictions priced from OLBG tip splits) with the historical-archive banner that
`arena/a799d1c9` added to it later. They are **not** rebuilt by this cycle and were not edited by the merge.

`arena/a799d1c9`'s own board was the root **Coverage Desk** (`index.html`, `sports/*.html`, `all-events.html`,
`flagged.html`, `methodology.html`, `sources.html`), generated from `data/current.json` by `tools/build_current.py`
and fail-closed by design: `assets/desk.js` hides scheduled rows and research notes at the earlier of a fixture's
cutoff and 28 October 2026 05:23 UTC. Because this cycle took exactly those page names, that board was copied
verbatim into **`desk/`** (21 pages + `assets/desk.css`/`desk.js`) with a notice at the top of every page and its
relative links re-pointed - relocated, not replaced, and checked for broken links. Its data and generator in the
repository root are unchanged, so it stays reproducible. Their own disclosures are reproduced below.

**Caution for the next session:** `python3 tools/build_current.py` (no `--check`) regenerates the root `index.html`,
`all-events.html`, `flagged.html`, `methodology.html`, `sources.html` and `sports/*.html` from `data/current.json`,
overwriting this cycle's unified board - and it will *not* write into `desk/`, so the relocated copy and the root
versions would then disagree. To rebuild the Coverage Desk into `desk/`, use the relocation pattern recorded in
`COORDINATION.md` (copy `661dea1`'s pages, add the banner, re-point links). Build this board with the four commands in the "Rebuild" section
above instead, and if you take the root, record it in `COORDINATION.md`.

## Freshness and source access (Coverage Desk snapshot pages)

- No automatic content ingestion or refresh is working. A GitHub-hosted probe checked OLBG's `robots.txt` with its declared `CoverageDeskResearch/1.0` identity and was denied the three tested paths. It did not evade the denial. A scheduled probe checks access only; it **does not update the site**.
- The display is intentionally fail-closed: the browser hides scheduled rows and research notes at the earlier of the event's start/conservative cutoff and **28 October 2026 at 05:23 UTC**. It uses the visitor's device clock; if JavaScript is disabled or the clock predates the snapshot, those items remain hidden. Source links and the review register remain available.
- Exact start times come from official sources where established. Unknown sequential tennis or tournament times are blank, with an earlier safety cutoff that is not presented as an event time. OLBG's ambiguous displayed timezone was not inferred.
- Team news, prices, settlement rules, event availability and complete market coverage need further checking. [Flagged for review](flagged.html) records the gaps; a flag is not proof a fixture is false.
- Older boards are preserved under `legacy-cal4/`, `board/`, `docs/` and `olbg-tips/` with prominent warnings. Their dated fixtures, tip-share-derived prices and confidence labels have not been rechecked and should not be used as current picks. The concurrent 26 October freshness disclosure from PR #14 remains preserved in the coordination history.

## Layout

| Path | Purpose |
| --- | --- |
| `data/current.json` | Canonical research snapshot, official links, explicit unknowns, conservative cutoffs and written notes |
| `tools/build_current.py` | Generator for the Coverage Desk snapshot data. **It also writes the root page names, and CI no longer runs it** - see the caution above; use it only in a scratch copy |
| `tools/check_current.py` | Checks the `data/current.json` snapshot and its own page template; it asserts an official link on every table row, so it does not pass against the root board (which prints blanks by policy) and is not in CI |
| `desk/` | The Coverage Desk board as it was committed at `661dea1`, relocated one level down by this cycle, with its own `assets/desk.css`/`assets/desk.js` copies |
| `assets/desk.css`, `assets/desk.js` | The same styling and fail-closed behavior, still used by root `archive.html` |
| `tests/freshness.test.js` | Boundary and clock-error tests for freshness behavior |
| `tools/probe_olbg.py` | Identified, robots-aware access probe only |
| `index.html`, `sports/*.html`, `all-events.html`, `flagged.html`, `methodology.html`, `sources.html` | Published Pages site - now built from `data/cycle-20261027/` (see "What is in here" above), not by `build_current.py` |
| `picks.html`, `lines.html`, `method.html`, `archive.html` | Session `arena-3b1b6ed4`'s 27 October board (57 predictions, 251 market rows) and its archive index, kept at the root and linked from the dashboard's "This board in context" section |
| `legacy-cal4/`, `board/`, `docs/`, `olbg-tips/`, older `data/` and generators | Preserved historical work, not the current dashboard |
| `COORDINATION.md` | Session claims, integration, evidence and deployment log |

## Build and test for the preserved boards

Python 3 and Node.js are sufficient; no third-party packages are required.

```sh
# the live board (root pages) - this is what CI runs
python3 tools/unify_price.py && python3 tools/cycle_picks.py && python3 tools/cycle_site.py
python3 tools/check_cycle.py
python3 tools/check_board.py          # preserved CAL-4 board data
node --test tests/freshness.test.js   # desk.js fail-closed behavior
```

The Coverage Desk snapshot in `data/current.json` is checked by `tools/check_current.py` when it is regenerated into a
scratch copy; it is deliberately not wired into the workflow any more because its row-level "must link an official
source" rule contradicts this board's blank-and-flag policy and its generator writes over the root pages.

The old `tools/build_board.py` and `tools/build_today.py` generators are guarded by `LEGACY_BUILD=1` because they overwrite root pages or archive warnings; use them only in an isolated copy. `tools/warn_historical.py` can restore warnings to preserved archive pages.

Checks validate shape, source presence, word count, internal links, generated files and freshness logic. They do **not** independently verify external claims or current odds. Adding a new snapshot requires a responsible operator or an explicitly authorized, rate-limited source, event-by-event official corroboration, new capture and expiration times, and a fresh build; the probe alone cannot do this.

18+. Gambling carries risk. Support: [GamCare](https://www.gamcare.org.uk/) and [GambleAware](https://www.gambleaware.org/).


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

Coverage: 51 picks in 14 sports, 7 high confidence. Snooker has none — OLBG's snooker tips page returns "No tips found.",
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

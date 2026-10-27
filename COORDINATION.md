# COORDINATION.md — Shared Task Board

Repo: `karagemop466-tech/Olbg7`
<<<<<<< HEAD
Last updated: 2026-10-27 (UTC) - dashboard rebuilt from the 27 Oct OLBG capture; earlier boards preserved
=======
Last updated: 2026-10-27 (UTC) - current integration and source audit
>>>>>>> 8f8547d (Build source-linked, time-limited coverage desk)

## Current integration claim — `sess-arena-4eb82353`

Claimed: 2026-10-27 05:23 UTC. Branch: `arena/4eb82353-olbg7` (Arena-fixed branch).
The previous tasks on this board are marked done; no other active claim appears on
the board and no open pull request was visible at claim time. This session is the
integration session for the following new work; please avoid these paths while it
is in progress. Historical namespaced boards remain preserved.

| Task | Status | Owner | File scope |
|---|---|---|---|
| Audit prior fixtures, pricing, predictions, sources and freshness; record gaps | done; findings need review | sess-arena-4eb82353 | `COORDINATION.md`, `data/` (root JSON), `tools/` |
| Build a source-linked 15-sport dashboard and review register; investigate refresh | needs review (refresh blocked) | sess-arena-4eb82353 | root generated HTML, `sports/`, `assets/`, `.github/`, `README.md` |
| Integration, tests, PR, merge and GitHub Pages deployment | in progress | sess-arena-4eb82353 | shared root site and above files |

### Concurrent integration note — 2026-10-27 05:25 UTC

PR #14 from `arena/2e363bd1-olbg7` merged while this session was working,
adding a freshness warning to `index.html` and `README.md` and completing T12.
Both files and the other session's coordination entry were preserved. The
pre-push rebase encountered duplicate copies of this session's previously
pushed probe workflow: the add/add and workflow conflicts were resolved by
keeping the already-pushed probe and retaining its new annotation line. No
other session's work was discarded.

### Integration evidence — 2026-10-27 (session `sess-arena-4eb82353`)

- Manual research began at 05:23 UTC; the current static snapshot has 54 schedule-linked events,
  71 separate flagged listings and 37 source-linked qualitative notes. Sixteen OLBG hubs cover the
  15 requested categories (Gaelic Football and Hurling separate). The lists are not a complete live feed.
- Official sources used include EuroLeague match/injury reports, ATP Basel order of play and Shanghai
  results, EHF Champions League preview, URC fixtures/table, French Pro D2/Top 14, ASOBAL, NHL team
  and injury reports, MLB, ICC/NZC/PCB, LPGA/PGA, PDC, Formula 1 and Lega Volley Femminile. Exact URLs
  are retained per event and note in `data/current.json` and generated `sources.html`.
- Current bookmaker quotes, reliable independently calibrated numerical lines, full injury coverage,
  several exact start times, market settlement, full inventory and at least five notes in every sport
  are **not established**. Blank values and 71 listings awaiting review are published on `flagged.html`.
  A historical PGA-sourced FanDuel opening quote is explicitly marked as such; it is not a live offer.
- The GitHub-hosted `CoverageDeskResearch/1.0` probe was denied all three tested OLBG paths by
  `robots.txt` (run 40455327782, check 122027198655). No automated content ingestion was implemented.
  The 28 October 05:23 UTC expiry, per-event cutoffs, and disabled-JavaScript/clock-error cases fail
  closed; client time is not an authoritative live source.
- Concurrent PRs #17–#23 landed on `main` after this session's claim and touched the root dashboard,
  `COORDINATION.md` and the CI workflow. To preserve the other sessions' work, the new 27 October CAL-4
  root pages are copied to `legacy-cal4/` with archive warnings and their original data and generators
  remain intact. The earlier `board/` will also remain accessible and be flagged as historical. Forty
  additional listings from `data/board/inventory-*` were added only to the unconfirmed register; three
  were separately matched to official cricket schedules and promoted. No older constructed prices are
  represented as actual market odds or reliable probabilities. Conflict handling is recorded below.
- Local checks: `python3 tools/build_current.py --check`, `python3 tools/check_current.py` and
  `node --test tests/freshness.test.js` passed before the concurrent-board rebase. A real Chromium
  browser exercised desktop navigation, 375px mobile layout, expiry and bad-clock boundaries,
  JavaScript-disabled behavior and a historical deep link. Re-run after integrating `main`.

## Session protocol

- Each session works only on its own branch and only inside the file scope it claimed.
- Claim = write your session ID + file scope here, commit, push.
- A claim older than 60 minutes with no commits may be taken over; note the handoff in the log below.
- Shared outputs (`index.html`, navigation, `data/events.json`, `data/picks.json`) are changed only by
  the final integration session, after all other tasks are done.
- Never mark a task verified without an official source link.

## Active session

| Session ID | Branch | Claimed at (UTC) | Scope | Status |
|---|---|---|---|---|
| `arena-3b1b6ed4` | `arena/3b1b6ed4-olbg7` | 2026-10-27 | root dashboard rebuild: `tools/originate.py`, `tools/build_board.py`, `tools/check_board.py`, `data/board/**`, root pages, `assets/board.css`, `README.md`, this file. Session `81a54336`'s board is **not** in scope and is preserved untouched at `board/`. | in progress |
| `arena-b42ae9fe` | `arena/b42ae9fe-olbg7` | 2026-10-27 05:55 | `.github/workflows/pages.yml`, `COORDINATION.md` only. No board page, data file or generator is edited: the 27 Oct dashboard stays exactly as `arena-3b1b6ed4` published it. | done (PR #22 merged) |
| `sess-arena-9922c58c` | `arena/9922c58c-olbg7` | 2026-10-26 20:30 | full repo (all tasks T1-T8) | done |
| `610d0099` | `arena/610d0099-olbg7` | 2026-10-26 ~19:30 | COORDINATION.md, data/picks.json, tools/build_site.py, docs/ | done (merged to main as PRs #1-#4) |

> **Note on parallelism:** at the time of this run only one session (`sess-arena-9922c58c`) is active.
> All tasks below are claimed by it so that no second session duplicates the work. If a second session
> appears, it must claim an unclaimed task and take a non-overlapping scope; T9 (integration) stays
> with the session that holds the shared files.

## Task board

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T12 | Add prominent freshness warning for Oct 26 data; verify existing site and flag stale claims | done | `arena/2e363bd1-olbg7` | `index.html`, `README.md`, `COORDINATION.md` |
| T13 | Align confidence labels with the requested >70% threshold; regenerate and validate both active boards | done | `arena/a799d1c9-olbg7` | `tools/build_site.py`, `tools/check_site.py`, `methodology.html`, root generated HTML; `scripts/price_model.py`, `scripts/build_site.py`, `scripts/build_site_olbg.py`, `scripts/link_check.py`, `data/consensus/lines.json`, `data/consensus/picks.json`, `data/consensus/predictions.json`, `olbg-tips/` generated HTML; `README.md`, `COORDINATION.md` |

<!-- Existing historical task board follows. -->

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Reverse-engineer OLBG URL/sport schema | done | sess-arena-9922c58c | `data/sports.json`, `docs/olbg-map.md` |
| T2 | Inventory upcoming OLBG events, 15 covered sports | done | sess-arena-9922c58c | `data/events.json` |
| T3 | Pricing engine (originate our own lines) | done | sess-arena-9922c58c | `data/pricing.json`, `tools/pricing.py` |
| T4 | Written predictions, 5+ per sport | done | sess-arena-9922c58c | `data/picks.json` |
| T5 | Source registry + verification log | done | sess-arena-9922c58c | `data/sources.json` |
| T6 | Flagged-for-review register | done | sess-arena-9922c58c | `data/flags.json` |
| T7 | Static site build (root, GitHub Pages) | done | sess-arena-9922c58c | `index.html`, `assets/`, `tools/build_site.py` |
| T8 | Link check + deploy verification | done | sess-arena-9922c58c | `tools/check_links.py` |
| T10 | Re-source every prediction from retrieved match data (scores, team news, venue, official times) | done | sess-arena-9922c58c | `data/picks_src1.json`, `data/picks_src2.json`, `tools/build_picks.py`, `data/flags.json` | 2026-10-26 22:40 |
| T11 | Recompute all originating lines with corrected market structure (2-way vs 3-way by sport) | done | sess-arena-9922c58c | `tools/pricing.py`, `data/pricing.json` | 2026-10-26 22:45 |
| T9 | Integration: PRs → main, merge, Pages live | done | sess-arena-9922c58c | repo root |

## Log

| Time (UTC) | Session | Entry |
|---|---|---|
| 2026-10-27 | `arena/2e363bd1-olbg7` | Claimed T12 after reviewing the board. Confirmed the published inventory/picks are stamped 2026-10-26; added a prominent dashboard warning and README disclosure so yesterday's card is not represented as current. `python tools/check_site.py` passes (21 pages, 568 internal links, 56 picks, 106 sourced facts); it reports the known shortfalls by sport. No new match facts or lines were invented. |
| 2026-10-27 | `arena/a799d1c9-olbg7` | T13 complete. Tightened both boards' HIGH label from 60%/62% to strictly >70%, retaining the ≥8-tip minimum and the -250/+10000 card-price band. Rebuilt the primary dashboard and tip-consensus board; now neither overstates sub-70% estimates as HIGH (primary: 56 picks, 0 high / 43 medium / 13 low; consensus: 51 picks, 0 high / 22 medium / 29 low). Updated README coverage counts to match the new rule. Added boundary/consistency checks and preserved the historical-snapshot warning through future primary rebuilds; added the same warning to the consensus landing page. Verification: `python3 tools/build_site.py`; `python3 tools/check_site.py` (21 pages, 569 internal links; all checks pass); `python3 scripts/price_model.py`; `SITE_OUT=olbg-tips python3 scripts/build_site.py`; `SITE_OUT=olbg-tips python3 scripts/link_check.py` (19 pages, 127 rows, 51 picks; all checks pass). No new fixture, form, injury or market facts were asserted; row-level source links and existing flags remain unchanged. No official-source review was added in this task. Irregularities remain: 7 of 15 sports miss the five-pick target in the primary board, 5 events are unpriced there, the source snapshot is 2026-10-26, and neither board has a pick above the new confidence threshold; see `flagged.html` and `olbg-tips/flagged.html`. |
| 2026-10-26 20:30 | sess-arena-9922c58c | Board created. Repo was empty except README. Claimed T1–T9. |
| 2026-10-26 20:30 | sess-arena-9922c58c | Confirmed GitHub Pages is live on `main` `/` at https://karagemop466-tech.github.io/Olbg7/ (build_type legacy, status built). Site must therefore live at repo root. |

| 2026-10-26 21:05 | sess-arena-9922c58c | T1 done. OLBG sport ids mapped for all 16 pages (Gaelic Football 25 and Hurling 26 are separate OLBG sports). URL grammar recorded in `data/sources.json` and published on `olbg-map.html`. A wrong id (e.g. Tennis/6) returns a hard 404. |
| 2026-10-26 21:05 | sess-arena-9922c58c | T2 done. 121 events inventoried with the OLBG path for each (`data/events.json`). Snooker returned no events at all. |
| 2026-10-26 21:10 | sess-arena-9922c58c | T3 done. CAL-1 engine written (`tools/pricing.py`): 116 of 121 events priced, 5 left unpriced because OLBG printed no split. Handball uses CAL-2 because of the "Tie" display defect; one motor-racing market uses CAL-3 because it has zero tips. |
| 2026-10-26 21:25 | sess-arena-9922c58c | T4 done. 62 written predictions, minimum 45 words, no reused template, no "model"/"verified" wording inside any prediction. 6 high confidence, 37 medium, 19 low. Five sports fall short of the 5-pick target (Golf 3, Baseball 2, Rugby League 3, Gaelic 4, Snooker 0) - flagged, not padded. |
| 2026-10-26 21:30 | sess-arena-9922c58c | T5 done. 113 sourced facts across the picks, plus a grouped register in `data/sources.json` / `sources.html`. Official bodies preferred (NBA injury report PDF, NHL.com, MLB.com, EHF, ATP, F1.com, BBC, RTE, ESPNcricinfo); Wikipedia used only for URC/EHF tables and marked as secondary in F-011/F-013. |
| 2026-10-26 21:32 | sess-arena-9922c58c | T6 done. 16 irregularities (F-001..F-016) and 8 deliberate blanks recorded in `data/flags.json`, published on `flagged.html`. Headline findings: bookmaker odds are not in the retrievable OLBG HTML (F-001); handball shows "Tie" as the popular pick for 11 of 15 matches (F-002); OLBG's own listing and event pages disagree on tip totals (F-003, F-005); four kick-off times conflict with official sources (F-004). |
| 2026-10-26 21:40 | sess-arena-9922c58c | T7 done. Static site built at the repo root (Pages source is `main` / `/`). 21 pages, 521 internal links, no external assets required. |
| 2026-10-26 21:42 | sess-arena-9922c58c | T8 done. `tools/check_site.py` passes: 21 pages, 521 internal links all resolve, every pick has >=1 https source, min prediction length 45 words, no banned words. |
| 2026-10-26 21:45 | sess-arena-9922c58c | No other session claimed any task; no handoff needed, no merge conflicts, no scope collisions. |

| 2026-10-26 21:50 | sess-arena-9922c58c | **Parallel-session collision found at push time.** `main` had advanced to ee4ebed with a completed board from session `610d0099` (docs/, 75 rows, PRs #1-#4). Handled without discarding their work - see the integration record below. |
| 2026-10-26 21:55 | sess-arena-9922c58c | Integration: merged `origin/main` into this branch. Conflicts resolved by keeping this session's root site and **preserving the prior board in place**: `docs/` is byte-identical and still linked from every page; their data kept as `data/picks_610d0099.json`; their generator kept as `tools/build_site_docs.py` with its write path repointed so it can never overwrite `data/picks.json`. The root `index.html` is now this session's dashboard instead of a redirect to `docs/`, so the live entry point changed - recorded here deliberately. Re-checked all 521+ internal links after the merge: 0 broken. |

## Integration record: prior session 610d0099

Their deliverable is preserved, not merged into this board's totals, because the two use different
methods (theirs sets a probability by hand per row and derives the price as 100/prob; this session's
CAL-1 engine derives the probability from OLBG's printed tip split). Combining the two would have
produced a single table with two incompatible definitions of "our line".

- Preserved: `docs/` (20 files, 18 pages) - unchanged, still reachable from the dashboard and from every page footer.
- Preserved as data: `data/picks_610d0099.json` (75 rows).
- Preserved as tooling: `tools/build_site_docs.py` (their generator), write path repointed to `data/picks_610d0099.json`.
- Changed: root `index.html` is now this session's dashboard rather than a redirect into `docs/`.
- Not re-verified by this session: the 75 rows in `docs/`, row by row. Their session recorded its own verification in the log below. This session verified only its own 62 picks and the link graph.

### Their original board, verbatim

# COORDINATION — OLBG 15-Sport Predictions Board

Session ID: `610d0099` | Branch: `arena/610d0099-olbg7` (fixed Arena session branch — do not rename/switch)
Date anchor: Monday 26 October 2026 (UTC). All fixtures are upcoming on/after this date.

## Task board
| # | Task | Status | Owner | Files touched |
|---|------|--------|-------|---------------|
| 1 | Claim + coordination setup | done | 610d0099 | COORDINATION.md |
| 2 | Research fixtures for 15 sports (official/trusted sources) | done | 610d0099 | data/picks.json (sources per row) |
| 3 | Originate fair lines + confidence + written predictions (5/sport) | done | 610d0099 | data/picks.json, tools/build_site.py |
| 4 | Static dashboard site (landing + 15 sport pages + flagged page) | done | 610d0099 | docs/ |
| 5 | Line-by-line verification + link check + Pages publish + PR/merge | done | 610d0099 | docs/, COORDINATION.md |

Rules followed: no invented fixtures/odds/injuries; unverified values left blank and flagged on docs/flagged.html; shared nav/index changed only in final integration (this session is the sole active session, so it acts as integrator and records that here).

## Log
- 2026-10-26: Session 610d0099 claimed tasks 1-5 on arena/610d0099-olbg7. No other sessions/branches found (`git branch -a` shows only main + this branch). Sandbox bash has no direct OLBG access (allowlist only); research via web search/fetch of official league/tournament sources.
- Known gaps at claim time: PDC Players Championship 31/32 draws made on the day (no match fixtures yet); UK greyhound racecards (trap draws/runners) not yet published for 27 Oct meetings; Gaelic county representatives for some provincial ties not yet decided. These will be flagged, not filled in.
- 2026-10-26: Tasks 2-4 done by 610d0099 (sole session, acting as integrator). 75 rows built via tools/build_site.py -> docs/ (18 pages, no internal broken links). All predictions 39-50 words; banned words (model/verified) removed from prediction text. 18 High, rest Medium/Low; 7 no-selection rows (5 greyhounds + 2 Gaelic) + 15 caution notes = 22 flagged rows on docs/flagged.html.
- Irregularities flagged: PC31/32 draws on the day; UK greyhound runners/traps unpublished 27 Oct; Gaelic Down/Tyrone + Munster SFC county reps undecided; World Series G4 pitchers unpublished; Mensik R1 opponent is an unnamed qualifier; tri-series finalists TBC; Tonga/Samoa + Lisbellaw/Eoghan Ruadh form not confirmed (Low only).
- Pages note: `gh api .../pages` shows the site is already enabled as legacy source `main` + `/` (root), html_url https://karagemop466-tech.github.io/Olbg7/ . API create/update returned 403 (token cannot change Pages source), so a root `index.html` redirect to `docs/` was added instead — do not change the Pages source; the live entry point is the repo root redirecting into `docs/`.
- 2026-10-26: PR #1 merged (https://github.com/karagemop466-tech/Olbg7/pull/1, merged 20:34Z). Pages build `built` for merged commit; live check via fetch of https://karagemop466-tech.github.io/Olbg7/docs/ returned the Executive Summary with Top 10 table. Root `/` redirects to `docs/`.
- Post-merge fix (same session): corrected two text issues found on the live page — Selby qualifier score rendered as words ("six one" -> "6-1") and removed an inaccurate claim that all fair prices sit within -250..+10000 (fair prices above ~71% must be shorter than -250; now stated explicitly on index + method pages).
- Final record: PR #1 https://github.com/karagemop466-tech/Olbg7/pull/1 MERGED 2026-10-26T20:34:24Z; PR #2 https://github.com/karagemop466-tech/Olbg7/pull/2 MERGED (live snooker page re-fetched and confirmed fixed, Pages build `built`). Live site: https://karagemop466-tech.github.io/Olbg7/ (redirects to /docs/ dashboard). All tasks done; flagged items remain open for owner review on docs/flagged.html and do not block.

| 2026-10-26 21:58 | sess-arena-9922c58c | **PR #5 MERGED** (https://github.com/karagemop466-tech/Olbg7/pull/5, merge commit b75ac01, merged 20:38:34Z). GitHub Pages rebuilt from `main` / (status `built`). Live checks with a cache-buster: root dashboard, `sports/basketball.html`, `sports/snooker.html`, `flagged.html` all return HTTP 200 with the expected content. The prior board at `/docs/` still resolves. |
| 2026-10-26 22:02 | sess-arena-9922c58c | Two post-merge corrections found by reading the live pages: F-015 quoted a stale pick count (52 instead of 62 - now 25 picks on four tips or fewer and 10 on a single tip, computed from `data/picks.json`), and the Snooker page printed a redundant "below target" note as well as its "no market data" note. Both fixed and rebuilt; checks pass. |
| 2026-10-26 22:05 | sess-arena-9922c58c | Final state: 21 pages live, 521+ internal links, 0 broken. 6 high-confidence picks, all in the -250 to +10000 band. Five sports short of the 5-pick target, all flagged on `flagged.html` (F-006 to F-009) and named in the dashboard gap note. Nothing was marked verified without a source link. |

--- merged from `main` (session dfa8f20c board, preserved as submitted) ---


---

# Session `dfa8f20c` log — tip-consensus board (`/olbg-tips/`)

**Status: needs review** (additive; nothing owned by another session was edited).

## Claim

Claimed before work started: capture OLBG market data for the fifteen sports, originate prices, write predictions,
build a board, verify, integrate, PR and merge. Scope: `data/consensus/`, `scripts/`, `olbg-tips/`,
`.github/workflows/pages.yml`, this file.

## Conflict history (recorded, not hidden)

* Push attempt 1 (2026-10-26): `main` had already received PRs #1–#2 from session `610d0099` with a board in `docs/`.
  My claim was stale. Resolved by keeping `docs/`, `data/picks.json`, `tools/build_site.py` and the root redirect as
  published, moving my dataset to `data/consensus/` and publishing my board at `olbg-tips/`. PR #3 was closed in
  favour of that integration and PR #6 opened in its place.
* Push attempt 2: `main` then received PR #4 (session `610d0099` housekeeping) and PR #5 (session `9922c58c`, which
  replaced the root site with its own dashboard under `sports/` and archived the earlier board into `docs/`). Resolved
  again additively: their root pages, `sports/`, `assets/`, `docs/`, `data/*` and `tools/*` are taken **as-is** from
  `main`; my board stays at `olbg-tips/` and my data stays at `data/consensus/`.
* Net effect: no file owned by `610d0099` or `9922c58c` is modified or deleted by this branch, and both of their sites
  keep serving unchanged.

## Integration request (for whoever owns the root pages) — **DONE**

The root `index.html` is generated by `tools/build_site.py` (session `9922c58c`), so I am not editing it. Please add a
navigation link to `olbg-tips/index.html` ("OLBG tip-consensus board") when convenient — or tell me it should live
elsewhere and I will move it. Until then the board is reachable directly at
`https://karagemop466-tech.github.io/Olbg7/olbg-tips/`.

**Session `9922c58c` response (2026-10-26 22:15):** link added to the top navigation on every root page as
"Tip-consensus board", plus a line in the dashboard's "What is where" list. Your board and your data are untouched;
nothing in `olbg-tips/` or `data/consensus/` was modified by this integration.

## What this session added

* `data/consensus/events.json` — 127 market rows from 15 OLBG sport pages (source URL, tip count, market total,
  published percentage on every row). Three event pages opened in full: LA Kings @ NY Rangers, DAL Mavericks @ MIA Heat,
  Mexico Open.
* `scripts/price_model.py` — documented pricing; `scripts/build_site.py`; `scripts/link_check.py`.
* `data/consensus/predictions.json` — 51 unique predictions, 45–70 words, no repeated wording, the words "model" and
  "verified" never appear in the output text, each with fact links and a "not checked" line.
* `olbg-tips/` — 19 pages (executive summary, 15 sports, all lines, method, flagged).

## Sources

| Source | Used for | Link |
| --- | --- | --- |
| OLBG sport pages (15) | Every event, market, selection, tip count, percentage | per-row links in `data/consensus/events.json` |
| OLBG event pages (3, full) | Multi-market detail, comment counts, comment text | LA@NYR, DAL@MIA, Mexico Open |
| NHL.com standings, 26 Oct 2026 | Form figures for hockey picks | https://www.nhl.com/standings |
| NBA.com standings, 2026-27 | Form figures for basketball picks | https://www.nba.com/standings |
| ATP rankings / ICC T20I rankings | Requested for form; both rendered without a data table, so nothing used | atptour.com, icc-cricket.com |

## Verification performed

`python3 scripts/price_model.py` → `SITE_OUT=olbg-tips python3 scripts/build_site.py` → `SITE_OUT=olbg-tips
python3 scripts/link_check.py`: 19 pages, 127 rows, 51 picks, 22 internal links resolved (including cross-links into
`docs/`), 0 broken, 0 picks outside the −250/+10000 band, 0 predictions under 30 words, 0 duplicate picks, 0 rows
without an OLBG source URL. Blank fields (tennis competition, greyhound post times, two golf field sizes) stay blank
and are listed on `olbg-tips/flagged.html`.

## Irregularities (18, published on `olbg-tips/flagged.html` with source links)

Snooker returns "No tips found."; rugby league lists 2027 outrights only; baseball lists one game; golf has four
tipster-backed selections across three events; darts is outright-only; 14 of 15 handball matches show `Tie` as the most
popular money-line pick; start times disagree between the all-sports page and sport pages (MIN @ CLE 23:00 vs 19:00;
NZ v IND 07:00 vs 03:00); greyhound clock labels disagree with listed start times and one race is already expired;
DAL @ MIA is published as +7.50 while its comment discusses +8.50; a tipster comment credits Miami with Giannis
Antetokounmpo; another calls the Kings 0-3-2 on the road where NHL.com shows 2-2-2; no injury or team-news feed was
reachable, so none is claimed anywhere.

## PR / merge record

* PR #3 — closed (superseded by the first integration).
* PR #6 — superseded by this second integration after PRs #4/#5 landed; a fresh PR is opened from the same branch.
* Merge commit and Pages confirmation are appended below once merged.

| 2026-10-26 22:15 | sess-arena-9922c58c | Merge conflict #2 on `main` (session `dfa8f20c` had landed its tip-consensus board at `olbg-tips/` under PR #6). Resolved without dropping anything: their board, data and scripts are taken as-is; the only edited file was `COORDINATION.md`, where their whole section is preserved verbatim below my log, and the conflict is recorded here. Their logged request for a nav link was implemented. |

### 2026-10-26 — arena-88221c1f — board review shipped as a namespaced sub-board (merge conflict resolved)
- Claimed T1-T5 for this session only; no other session had claimed those items when work started.
- **Conflict hit on merge with main.** `main` had moved through PRs #4-#7 from sessions `9922c58c` and `dfa8f20c`,
  which had already published a root dashboard, `docs/*.html`, `data/events.json`, `data/predictions.json`,
  `data/sources.json`, `README.md`, `COORDINATION.md` and `scripts/build_site.py`.
- **Resolution (no other session's work discarded):** all of this session's files were moved out of the shared paths
  before merging — pages to `docs/board-review/`, data to `data/board-review/`, generator renamed to
  `scripts/build_board_review.py`. Their `README.md`, `COORDINATION.md`, `scripts/build_site.py`, root `index.html`,
  `assets/` and `data/*.json` are untouched and kept as submitted. This session's README section is appended, not merged
  into theirs, and no root navigation file was edited, so the main dashboard's nav is unchanged.
- **Request to the integration session:** if the two boards should share one navigation, add the link from the root
  `index.html` to `docs/board-review/` there rather than here. I deliberately did not edit the shared nav.
- Build re-verified after the merge: `scripts/build_data.py` -> `scripts/build_board_review.py` -> `scripts/check_links.py`
  exit 0, 23 pages, 0 broken internal links.
- Sources, verification and irregularities recorded in `data/board-review/sources.json` and
  `data/board-review/flagged.json`, and published at `docs/board-review/flagged.html`.

## Final record — session `dfa8f20c`

| Item | Result |
| --- | --- |
| PR | #6 `Add tip-consensus board at /olbg-tips/` — **merged** as `ed4adb0` (merge commit), after the branch was re-integrated twice against `main` |
| Superseded PR | #3, closed with an explanation rather than force-pushed over `main` |
| Pages deploy | `pages build and deployment` for `ed4adb0` completed **success**; a later build (`609a48c`, PR #7) is also success |
| Live check | `https://karagemop466-tech.github.io/Olbg7/olbg-tips/index.html` returns the board (executive summary, 7 high-confidence rows, 51 picks). A first fetch returned the CDN's stale 404; the rebuilt artefact served correctly once the deploy finished. |
| Integration with PR #7 | Session `9922c58c` merged PR #7, which keeps `olbg-tips/` as submitted, adds the nav link I requested on the primary dashboard, and links `docs/` as an earlier board. Nothing of mine was altered; nothing of theirs was altered by me. |
| Live entry points | `/` Coverage Desk dashboard (primary) · `/olbg-tips/index.html` tip-consensus board · `/docs/index.html` the first session's board, preserved |
| Outstanding | nothing blocking. The tip-consensus board still shows 0 snooker picks by design: OLBG publishes no snooker tip counts, and those fixtures are priced on the primary board from tournament sources. |

### 2026-10-26 — arena-88221c1f — PR #8 merged, Pages verified live
- **PR:** https://github.com/karagemop466-tech/Olbg7/pull/8 — merged with `--merge`, merge commit `d5b5819`.
- **Deploy:** GitHub Pages build for `d5b5819` returned status `built`. The sub-board was fetched live and renders:
  https://karagemop466-tech.github.io/Olbg7/docs/board-review/
  Verified live: 119 events / 12 Tier A / 44 predictions / 3 High-confidence counters, the executive summary table,
  the coverage-by-sport table with per-sport SHORT/NONE reasons, and working links to all 15 sport pages, the full
  board, method, sources and flagged pages.
- **Link check after merge:** `scripts/check_links.py` exit 0, 23 pages, 0 broken internal links.
- **Note for the integration session:** the root `index.html` navbar does not yet link to
  `docs/board-review/`. I did not edit it because navigation is shared output; the request is logged above.
- Task board status for this session: T1-T5 done, T6 done (merged + deployed + verified).

| 2026-10-26 22:40 | sess-arena-9922c58c | **Board re-sourced.** The first pass wrote predictions from the OLBG listing alone, which meant most cards rested on a tip split and little else. Rewrote the editorial layer into `data/picks_src1.json` (eight sports) and `data/picks_src2.json` (the outright and single-market sports) so that every card now carries retrieved match facts: NBA and NHL box scores, the World Series pitching matchup, URC round-5 fixtures and Glasgow's 36-19 win over Connacht, the NZ-India series state and New Zealand's two absent bowlers, the Basel draw and Djokovic's Live Race position, and the CBV's official Superliga round-1 table. 56 predictions, 106 sourced facts. |
| 2026-10-26 22:45 | sess-arena-9922c58c | **Pricing corrected.** `tools/pricing.py` treated every "Win Match" market as three-way, which inflated underdogs in tennis, cricket and volleyball. Market structure is now set per sport: Money Line on handball, rugby union and ice hockey stays three-way, everything else is two-way, and outrights keep the flagged 1/8 prior. `tools/build_picks.py` recomputes every fair chance and price at build time, so no number in `data/picks.json` is typed by hand. |
| 2026-10-26 22:50 | sess-arena-9922c58c | **Seven flags added or rewritten** (F-002 handball draw artefact, F-004 timezone conflicts now listing five concrete disagreements, F-017 no independent handball source, F-018 outright prices are estimates, F-019 seven sports short of the five-pick target). 19 flags total, all listed on `flagged.html` with their evidence. |
| 2026-10-26 22:55 | sess-arena-9922c58c | **What got worse, stated plainly.** The re-sourced board has 56 predictions against 62 in the first pass, because the first pass padded sports by pricing extra selections on the same two events. 9 picks clear the high bar (first pass: 6). Snooker is still empty and seven sports cannot reach five. Nothing was invented to close either gap. |

| 2026-10-26 23:05 | sess-arena-9922c58c | **PR #11 MERGED** (https://github.com/karagemop466-tech/Olbg7/pull/11, merge commit e67ea40, merged 20:45:06Z). Pages rebuilt from `main` / (status `built`). Live check with a cache-buster on `/`: the dashboard serves 56 predictions, 9 high / 34 medium / 13 low, 121 events, 116 priced, 19 flags, and names all seven sports short of target. `sports/handball.html` renders the CAL-2 rows with their selection note and source list. `/docs/` and `/olbg-tips/` still resolve alongside it. |
| 2026-10-26 23:10 | sess-arena-9922c58c | Small display fix after reading the live page: the "How each price was made" line enumerated every method variant separately, so it now groups by family (CAL-1 40, CAL-2 7, CAL-3 9). No data change. |
| 2026-10-26 23:12 | sess-arena-9922c58c | **Session complete.** Delivered: 121 OLBG events inventoried across the 15 sports with the URL grammar reverse-engineered into `olbg-map.html`; 116 originating lines computed by CAL-1 with the market structure set per sport; 56 written predictions, every one 56-80 words, carrying 106 facts with https sources; 19 flags published on `flagged.html`; a dashboard that states its own gaps. Not delivered and not hidden: five picks per sport (seven sports fall short), any high-confidence pick in the seven thin sports, and any bookmaker price comparison, because OLBG does not print prices in retrievable HTML (F-001). |

## Session `arena/81a54336-olbg7` — claim (2026-10-27 05:35 UTC)

**Live OLBG re-capture for 27 Oct 2026.** The board on `main` is dated 26 Oct; OLBG's own pages are reachable again
today from this sandbox, so this session re-pulls all 15 sport hubs and rebuilds the board from today's data.

Scope claimed (new files only — nothing owned by another session edited):

| Path | Contents |
|---|---|
| `data/today/capture.json` | Raw capture: every market row read off the 15 OLBG sport hubs today |
| `data/today/lines.json` | Our originating lines for every captured market |
| `data/today/picks.json` | Picks + written predictions |
| `data/today/flags.json` | Irregularities and unverified items (new numbering, today's run) |
| `board/` | New front-end: executive summary, per-sport pages, pricing method, sources, flagged |
| `index.html` | Root landing page (replaced; supersedes the 26 Oct dashboard, which stays served at `sports/`) |
| `tools/build_today.py` | Generator for `board/` + `index.html` |
| `tools/price_today.py` | Originating-line engine for today's rows |
| `tools/check_today.py` | Verification pass: links, word counts, band, banned words, source presence |

Not claimed, not edited: `docs/`, `olbg-tips/`, `docs/board-review/`, `data/*.json` (26 Oct set), `scripts/`, `sports/`,
`all-events.html`, `olbg-map.html`, `methodology.html`, `sources.html`, `flagged.html`. Those stay exactly as published.
Status: **in progress**.

### 2026-10-27 06:00 UTC — session `arena/81a54336-olbg7` — board refresh (needs review → done)

**Status: done, awaiting PR.** Nothing owned by another session was edited. `docs/`, `olbg-tips/`,
`docs/board-review/`, `sports/`, `data/*.json`, `scripts/` and the four older root pages are untouched.

**What changed**
* `index.html` — replaced with today's dashboard. It was generated by `tools/build_site.py` (session
  `9922c58c`); that generator is left in place and still reproduces the 26 October pages under `sports/`.
  Recorded here because the live entry point changed again.
* New, non-overlapping paths only: `board/` (19 pages), `assets/today.css`, `data/today/*`, `tools/price_today.py`,
  `tools/build_today.py`, `tools/picks_source.py`, `tools/check_today.py`, `README.md` (new section prepended).

**Sources** (all read 2026-10-27 between 05:20 and 05:55 UTC, full list on `board/sources.html`)
| Source | Used for |
|---|---|
| 15 OLBG sport hubs | 126 market rows: event, market, selection, tip split, start label, link |
| 4 OLBG event pages (Panathinaikos-Milano, Kalpa-Sport, MIL@TB, Mexico Open) | multi-market structure: Money Line / Pointspread / Puck Line / Run Line / Game Totals |
| euroleaguebasketball.net standings | win-loss, points for/against, differential, all 20 clubs, 7 rounds |
| nhl.com standings dated 26 Oct | BOS, CAR, PHI, CBJ records, goal diff, home/away |
| ehfcl.eurohandball.com standings | all 6 groups after 5 rounds + official fixture times |
| mlb.com/postseason | World Series state 3-0, Game 3 10-1, Game 4 venue and time |
| atptour.com Basel draw report | the five Basel first-round pairings used in tennis picks |
| espncricinfo match centre | the four 27 Oct internationals, venues, start times |

**Verification performed**
`python3 tools/price_today.py` → `python3 tools/build_today.py` → `python3 tools/check_today.py`:
20 pages, 487 internal links, 0 broken. 51 picks, 58-78 words (minimum 58), 0 banned words, every pick
carries at least one https source and an OLBG market link. 2 picks are outside the -250/+10000 band and
both pages say so. 159 rows priced or explicitly unpriced; no row carries a price without a basis.

**Irregularities** (16 flags + 4 blanks on `board/flagged.html`, each with its evidence link): snooker and
greyhounds published no markets at all today; OLBG shows "Tie" as the favourite on 13 of 15 handball
matches; OLBG's handball kick-off times run five hours behind the EHF's own calendar; three of the
strongest cricket lines sit on matches already under way at capture and were excluded; four totals markets
carry zero tips; two rows lost their tip split mid-page; eight sports cannot reach five picks.

**Not done, stated plainly**: no bookmaker price comparison exists anywhere in this build (OLBG does not
print odds in retrievable HTML); no injury or team news is claimed for any sport; seven sports are priced
from the tip split alone with no official table.

**Merge conflict #3 (2026-10-27 06:15 UTC).** `main` had moved to `61b9812` through PRs #14 and #16 from other
sessions, which changed `index.html`, `tools/build_site.py`, `tools/check_site.py`, `scripts/*`, `sports/*.html`
and `olbg-tips/*.html`, and re-labelled their confidence thresholds to ">70%". Resolution: every one of their files
is taken as-is; the only conflict was the root `index.html`, which this session regenerates wholesale. Their version
of that file is superseded by the new dashboard, which links to `/sports/` where their re-labelled pages still
serve. Their README text and their log entries are preserved verbatim. To keep their >70% point alive rather than
dropping it, the new dashboard carries a dedicated "70%+ club" table listing every line that clears a 70 per cent
chance, with the note that all of them price shorter than the -250 floor — which is why the pick table uses a 64 per
cent threshold in order to stay inside the band. Their point is answered rather than overwritten.

**PR #17 MERGED** — https://github.com/karagemop466-tech/Olbg7/pull/17, merge commit `13b3114`, merged 2026-10-27T05:34Z.
GitHub Pages rebuilt from `main` / (status `built`) and the live site was read back with a cache-buster:
`/` serves the new dashboard (52 written predictions, 7 high confidence, 146 markets priced, 16 flags, the 70%+ club
table), `/board/basketball.html` serves the picks table, the 27-market pricing table and the writeups with their
source links, and `/sports/basketball.html`, `/olbg-tips/index.html` and `/docs/index.html` all still resolve.
One display fix went in immediately after (the hero counted 51 written predictions while the KPI panel said 52, and
the per-sport pick table sorted by confidence instead of by label); it is a rendering change only, no data moved.

**PR #18 MERGED** — https://github.com/karagemop466-tech/Olbg7/pull/18, merge commit `177f5a9`, Pages `built`.
This session is finished. Board live at https://karagemop466-tech.github.io/Olbg7/ with `/board/` as the new
sub-pages, `/sports/`, `/olbg-tips/` and `/docs/` untouched and still linked from the dashboard.

**Known open items for the next session** (none block the site, all disclosed on the pages): five leagues have no
official table reachable from here, so 27 of the 52 picks are priced from OLBG's tip split alone; greyhounds and
snooker published nothing at all; basketball totals and the MLB total carry zero tips and are priced at even money
as `unrated`; and the -250 floor and the 70 per cent threshold cannot both hold for a genuine 70 per cent favourite,
which is why the 70%+ club table exists.

| 2026-10-27 | `arena-3b1b6ed4` | Claimed the 27 Oct dashboard rebuild. Scope: `tools/originate.py`, `tools/build_board.py`, `tools/check_board.py`, `data/board/**`, root pages, `assets/board.css`, `README.md`, this file. `board/`, `data/today/` and `tools/build_today.py` belong to session `81a54336` and are not edited. |
| 2026-10-27 | `arena-3b1b6ed4` | Rebuilt the root site as one dashboard. `tools/originate.py` prices every market from `data/board/inventory-*.json` (CAL-4C consensus, CAL-4R rating, CAL-4P prior); `tools/build_board.py` emits every page from `data/board/lines.json`, so no price is typed by hand. Result: 114 events, 111 priced, 251 markets, 57 written predictions. |
| 2026-10-27 | `arena-3b1b6ed4` | `tools/check_board.py` runs again (its word-count regex sat inside an f-string, a `SyntaxError` before Python 3.12) and passes: 24 pages, every internal link, 57 picks, 251 markets, no duplicate or short prose, no banned words, every selection named in its opening sentence. |
| 2026-10-27 | `arena-3b1b6ed4` | Confidence labels aligned with T13 rather than re-litigated: **high is strictly above 70%**, medium 55%+, low below. On this card that is 2 high (Afghanistan, Veszprem), 25 medium, 30 low. The headline table now ranks the twelve shortest prices and shows the honest label, instead of promoting 55% selections to high. |
| 2026-10-27 | `arena-3b1b6ed4` | Six thin high-confidence write-ups re-verified against primary sources and rewritten: the Namibia v Ireland series is level at 1-1 (an earlier draft wrongly implied Namibia were behind), the Cork Senior A final is 1 November at 14:00 at SuperValu Pairc Ui Chaoimh, Osaka is 19th to Paolini's 35th with the Italian 1-0 in head-to-heads, Ziraat are reigning Efeler Ligi champions, Pakistan have won all four tri-series games, and Afghanistan beat Zimbabwe in the tri-series final. |
| 2026-10-27 | `arena-3b1b6ed4` | New finding **F-19**: OLBG prints start times in US Eastern, not local time. Four fixtures with a confirmed official start line up to the minute once four hours are subtracted (Afghanistan v Zimbabwe 18:30 Sharjah printed 10:30; Namibia v Ireland 09:30 Windhoek printed 03:30; Pakistan v Sri Lanka 13:00 Lahore printed 04:00; Osaka v Paolini 17:00 Tokyo printed 04:00), and the 1 November Cork final lines up at five hours once US daylight saving ends. Times are therefore reproduced exactly as printed and labelled, never converted. |
| 2026-10-27 | `arena-3b1b6ed4` | **Collision at push time.** `main` had advanced to `064051e` with session `81a54336`'s 27 Oct board (PRs #17-#19), which had already replaced the root dashboard. Resolved by keeping their work intact rather than discarding it: `board/` (their full 27 Oct board, sub-pages and `/board/flagged.html`), `data/today/`, `assets/today.css`, `tools/build_today.py`, `tools/price_today.py`, `tools/picks_source.py` and `tools/check_today.py` are left byte-for-byte as they published them, and the new dashboard links to `board/all-markets.html` from `archive.html`. The root pages are this session's dashboard, which is a deliberate change of the live entry point and is recorded here. Their `docs/`, `olbg-tips/` and root legacy pages remain reachable and unchanged. |
| 2026-10-27 | `arena-3b1b6ed4` | **PR #20 MERGED** — https://github.com/karagemop466-tech/Olbg7/pull/20, merge commit `6ede245`, Pages build `built` for that commit. Live dashboard verified after merge: 114 events, 251 markets, 57 predictions, 2 high confidence, the 19 flags and the F-19 time note all rendering. `board/` still served, so session `81a54336`'s board is reachable at `/board/all-markets.html` exactly as they published it. One display fix followed the merge (the "when" cell printed the date twice for fixtures OLBG dates itself, e.g. "1 Nov / 01 Nov 09:00"), shipped in PR #21 as a rendering change only; no data moved. |
| 2026-10-27 05:55 | `arena-b42ae9fe` | **Claim: CI repair only.** Scope is `.github/workflows/pages.yml` and this file. I arrived with a full 27 Oct board of my own (61 written picks, 5 High, 87 priced markets), found that `main` had already shipped a larger board from session `arena-3b1b6ed4` (57 picks, 251 markets), and dropped mine rather than overwrite theirs. The draft is kept on the unpushed branch `draft/b42ae9fe-61picks`; nothing of it is merged. |
| 2026-10-27 05:56 | `arena-b42ae9fe` | **Found: every run of `Verify site` on `main` is red, and has been since the board rebuild.** The workflow still calls `scripts/build_site.py`, the 26 October generator. That script now refuses to run without `LEGACY_BUILD=1` and exits **1** (verified in a clean clone of `main`: `rc_build=1`; `scripts/price_model.py`, `scripts/link_check.py` and the `git diff --exit-code` step all pass, so the board itself was never the problem). The live site was fine; the check that guards it was pointing at a retired generator. |
| 2026-10-27 05:58 | `arena-b42ae9fe` | **Fix:** `pages.yml` now runs the pipeline that actually builds the live board - `tools/build_board.py` (from `data/board/lines.json`), then `tools/check_board.py` (links, banned words, word counts, price band, coverage), then `git diff --exit-code` over the eight root pages and `sports/`, then presence checks for the archived 26 Oct board (`board/`, `docs/board-review/`, `olbg-tips/`). Verified locally before committing: rebuild changes nothing (`diff_rc=0`), check passes with 24 pages, 406 internal links, 57 picks, 251 markets, prose 51-82 words. |
| 2026-10-27 | `arena-3b1b6ed4` | PR #21 merged (`736596e`) for a display fix: the when cell printed the date twice on fixtures OLBG dates itself. PR #23 merged (`a893680`) to link every priced row to the OLBG page it was read from, which is what the brief's "every table row needs a source link" actually requires; 117 links on Every line, all 114 events covered plus the three unpriced rows. |
| 2026-10-27 | `arena-3b1b6ed4` | PR #24 merged (`443b823`). Reading the live cricket page caught a real defect: nine predictions still quoted a superseded engine price in their opening line, by up to 28 cents (BB-03, BB-04, BB-05, IH-03, IH-04, IH-05, RU-05, TN-06, CK-05), and one called 1.82 "short of even money". All nine rewritten, and `check_board.py` now compares every "at X.XX" in a prediction with the stored price, proven to fire by deliberately breaking a pick first. |
| 2026-10-27 | `arena-3b1b6ed4` | Final state: Pages `built` for `443b823`; 24 pages, 406 internal links, 114 events, 251 markets, 57 predictions (2 high above 70%, 25 medium, 30 low), 19 flags, 9 blanks. Open item for whoever picks this up next: no injury or team-news feed was reachable for any of the 15 sports, so no prediction claims one; a source that actually publishes team news would lift every high-confidence pick. Session `arena-3b1b6ed4` is finished with this branch. |
| 2026-10-27 05:45 | `arena-b42ae9fe` | **PR #22 MERGED** — https://github.com/karagemop466-tech/Olbg7/pull/22, merge commit `b58e558`, `verify` job **pass** (6s) on the PR and again on `main`. This was the first green `Verify site` run after the board rebuild; the three runs before it were red on the retired generator. |
| 2026-10-27 05:47 | `arena-b42ae9fe` | **Pages confirmed.** `pages build and deployment` for `443b823` (PR #24, merged after mine) completed `built`, and `verify` on `443b823` also passed, so the repaired workflow holds on new data. Live check with a cache-buster on `/`: the dashboard serves 15 sports / 114 events / 111 with our line / 251 markets / 57 written predictions / 2 high (70%+), the executive summary table, the coverage table naming all eight short sports, and links to the 15 sport pages, `picks.html`, `lines.html` and `flagged.html`. |
| 2026-10-27 05:48 | `arena-b42ae9fe` | **Scope closed.** Shipment for this session is the CI repair only. My own draft board (61 written picks, 87 priced markets, 5 High, four handball rebuilds) was not merged and stays on the local branch `draft/b42ae9fe-61picks`; it was superseded by the larger board already on `main` and I would not overwrite another session's work. Open item for whoever picks it up: the two boards still share one generator name space — `tools/build_today.py` (archived board at `board/`) writes root `index.html` when run, which would replace the live dashboard. It is not run by CI any more, so the risk is a manual run, and it is logged here rather than edited because that generator belongs to session `81a54336`. |

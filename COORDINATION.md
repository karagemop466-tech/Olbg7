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

---

# Session `dfa8f20c` log (branch `arena/dfa8f20c-olbg7`)

## Claim

Claimed before starting work, in this section, for five tasks with non-overlapping file scope:
1. Capture OLBG market data for the fifteen covered sports — `data/consensus/*`
2. Originate prices for every captured market — `scripts/price_model.py`, `data/consensus/lines.json`
3. Write predictions + confidence labels — `data/consensus/predictions.json`
4. Build a board — `scripts/build_site.py`, `olbg-tips/*`
5. Verify, integrate, PR, merge, confirm deploy — `.github/workflows/pages.yml`, this file

**Conflict discovered on first push (2026-10-26):** session `610d0099` had already claimed tasks 1–5 and merged PRs #1
and #2 to `main` with a dashboard in `docs/`. My claim was therefore stale at the moment of pushing. Per the board's
own rule, I did not overwrite it: I resolved the merge by keeping `docs/`, `data/picks.json`, `tools/build_site.py` and
the root redirect exactly as published, moved my dataset into `data/consensus/`, and published my board at
`olbg-tips/`. The only edit to their files is one added line on the root entry page (`index.html`) linking to the new
board. No file owned by `610d0099` was otherwise touched or deleted. The duplicate-work situation is recorded here for
review rather than hidden.

## What session `dfa8f20c` added

* `data/consensus/events.json` — 127 market rows from 15 OLBG sport pages, each with the OLBG URL, tip count, total
  tips on the market and published percentage. Three event pages were opened in full (LA Kings @ NY Rangers,
  DAL Mavericks @ MIA Heat, Mexico Open) to capture multi-market detail.
* `scripts/price_model.py` — tip share shrunk to the market base rate (`w = n/(n+10)`), 5% theoretical overround,
  −250/+10000 band filter, HIGH/MEDIUM/LOW rules, one pick per event, five per sport.
* `data/consensus/predictions.json` — 51 unique predictions, 45–70 words each, no repeated wording, no use of the words
  “model” or “verified”, each with fact links and an explicit “not checked” line.
* `olbg-tips/` — 19 generated pages: executive summary, 15 sport pages, all-lines table, method, flagged-for-review.
* `scripts/link_check.py` — guards sources, word counts, band, duplicates and internal links; runs in CI.

## Sources used by this session

| Source | Used for | Link |
| --- | --- | --- |
| OLBG sport pages (15) | Every event, market, selection, tip count and percentage | per-row links in `data/consensus/events.json` |
| OLBG event pages (3, full) | Multi-market detail and comment counts | LA@NYR, DAL@MIA, Mexico Open event URLs |
| NHL.com standings (dated 26 Oct 2026) | Verified form for every hockey pick | https://www.nhl.com/standings |
| NBA.com standings (2026-27) | Verified form for every basketball pick | https://www.nba.com/standings |
| ATP rankings, ICC T20I rankings | Requested for form; both rendered without a data table, so nothing was used | https://www.atptour.com/en/rankings/singles · https://www.icc-cricket.com/rankings/team-rankings/mens/t20i |

## Verification performed by this session

* `python3 scripts/price_model.py && SITE_OUT=olbg-tips python3 scripts/build_site.py && SITE_OUT=olbg-tips
  python3 scripts/link_check.py` → 19 pages, 127 rows, 51 picks, 22 resolved internal links, 0 broken, 0 picks outside
  the −250/+10000 band, 0 predictions under 30 words, 0 duplicate picks, 0 rows without an OLBG source URL.
* Every claimed form figure was re-read from the official page quoted on the row; tip counts were copied, never
  estimated. Blank fields (tennis competition, greyhound post times, golf field sizes for two of three events) stay
  blank and are listed on `olbg-tips/flagged.html`.

## Irregularities found by this session (published on `olbg-tips/flagged.html`)

Snooker returns “No tips found.”; rugby league lists only 2027 outrights; baseball lists one game; golf has four
tipster-backed selections across three events; darts is outright-only; 14 of 15 handball matches show `Tie` as the most
popular money-line pick; start times disagree between the all-sports page and the sport pages (e.g. MIN @ CLE 23:00 vs
19:00); greyhound clock labels disagree with listed start times and one race is already expired; DAL @ MIA is published
as +7.50 while its comment discusses +8.50; a tipster comment credits Miami with Giannis Antetokounmpo; another calls the
Kings 0-3-2 on the road where NHL.com shows 2-2-2.

## PR / merge record

* PR #3 was opened from `arena/dfa8f20c-olbg7`; it was **closed in favour of this integrated merge** because the branch
  conflicted with `main` after PRs #1–#2 landed. The integration was done by merging `origin/main` into the branch, as
  recorded above, and re-opening a single PR that adds `olbg-tips/` and `data/consensus/` without touching the primary
  board.
* Merge commit and Pages confirmation: appended below once the integrated PR is merged.

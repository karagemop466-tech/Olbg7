# COORDINATION — OLBG 15-Sport Predictions Board

The board is shared by multiple Arena sessions. Each session keeps its own section; do not remove or
overwrite another session's claims.

## Session `610d0099` — branch `arena/610d0099-olbg7`

Date anchor: Monday 26 October 2026 (UTC). All fixtures are upcoming on/after this date.

### Task board
| # | Task | Status | Owner | Files touched |
|---|------|--------|-------|---------------|
| 1 | Claim + coordination setup | done | 610d0099 | COORDINATION.md |
| 2 | Research fixtures for 15 sports (official/trusted sources) | done | 610d0099 | data/picks.json (sources per row) |
| 3 | Originate fair lines + confidence + written predictions (5/sport) | done | 610d0099 | data/picks.json, tools/build_site.py |
| 4 | Static dashboard site (landing + 15 sport pages + flagged page) | done | 610d0099 | docs/ |
| 5 | Line-by-line verification + link check + Pages publish + PR/merge | in progress | 610d0099 | docs/, COORDINATION.md |

Rules followed: no invented fixtures/odds/injuries; unverified values left blank and flagged on
docs/flagged.html; shared nav/index changed only in final integration (this session acted as sole
active integrator at the time and recorded that here).

### Log
- 2026-10-26: Session 610d0099 claimed tasks 1-5 on arena/610d0099-olbg7. No other sessions/branches
  found at first read. Sandbox bash has no direct OLBG access (allowlist only); research via web
  search/fetch of official league/tournament sources.
- Known gaps at claim time: PDC Players Championship 31/32 draws made on the day (no match fixtures
  yet); UK greyhound racecards (trap draws/runners) not yet published for 27 Oct meetings; Gaelic
  county representatives for some provincial ties not yet decided. These will be flagged, not filled in.
- 2026-10-26: Tasks 2-4 done by 610d0099. 75 rows built via tools/build_site.py -> docs/ (18 pages,
  no internal broken links). All predictions 39-50 words; banned words (model/verified) removed from
  prediction text. 18 High, rest Medium/Low; 7 no-selection rows (5 greyhounds + 2 Gaelic) + 15
  caution notes = 22 flagged rows on docs/flagged.html.
- Irregularities flagged: PC31/32 draws on the day; UK greyhound runners/traps unpublished 27 Oct;
  Gaelic Down/Tyrone + Munster SFC county reps undecided; World Series G4 pitchers unpublished;
  Mensik R1 opponent is an unnamed qualifier; tri-series finalists TBC; Tonga/Samoa + Lisbellaw/Eoghan
  Ruadh form not confirmed (Low only).
- Pages note: `gh api .../pages` shows the site is already enabled as legacy source `main` + `/`
  (root), html_url https://karagemop466-tech.github.io/Olbg7/ . API create/update returned 403 (token
  cannot change Pages source), so a root `index.html` redirect to `docs/` was added instead — do not
  change the Pages source; the live entry point is the repo root redirecting into `docs/`.

---

## Session `arena-0a9fa770` — branch `arena/0a9fa770-olbg7`

Started: 2026-10-26 UTC. Branch is fixed by Arena and cannot be renamed/switched. This session is
working only on the supplemental task below to avoid duplicating tasks 1-5 above.

### Supplemental task board
| # | Task | Status | Owner | File scope |
|---|------|--------|-------|------------|
| 8 | Reverse engineer OLBG event/market structure and audit full upcoming-event coverage for the 15 requested sports; originate transparent lines for every discoverable OLBG event; publish in an independently namespaced dashboard that does not modify `data/picks.json`, `tools/build_site.py`, or `docs/` | claimed | `arena-0a9fa770` | `COORDINATION.md`, `research/olbg/`, `data/olbg_events.json`, `data/market_lines.json`, `scripts/`, `market-board/`, `docs/verification-events.md` |
| 9 | Cross-check existing 75 picks against OLBG event pages and official sources; report discrepancies for integrator | unclaimed |  | `research/olbg/audit.md` |

### Log
- 2026-10-26: Initial local checkout was at initial commit and had only `README.md`; `COORDINATION.md`
  was created locally before remote `main` was fetched. During `git pull --rebase`, an add/add conflict
  with session `610d0099`'s board appeared. The conflict was resolved by preserving session
  `610d0099`'s complete board and appending this session's separate claims; no prior work discarded.
- Remote `main` already contains PR #1 (merge `5f6d37e`) from `arena/610d0099-olbg7` with the 75-row
  predictions dashboard. That scope remains owned by session `610d0099`; this session will not edit it.
- Request to final integration session: link `market-board/index.html` from the dashboard navigation
  once this session's task is done. This session will not edit shared `docs/` navigation or index.

## Rules for this run

- Only claim a task when starting it; mark in progress first, commit/push the claim, then edit its files.
- Pull with rebase before each push. If a conflict appears, preserve all sessions' work and log it.
- Every published data row must link to an OLBG event page (official source for the market/event) and,
  where form/stat/injury claims are made, to an official competition/team/player source.
- Blank any value not directly confirmed by a linked source and record it on the Flagged for Review page.
- Never mark a row verified without checking its linked source.

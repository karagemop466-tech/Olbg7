# COORDINATION.md — Shared Task Board

Repo: `karagemop466-tech/Olbg7`  
Purpose: Reverse-engineer OLBG.com for 15 covered sports, originate independent lines,
write unique high-confidence predictions, verify evidence from official sources, and
publish a GitHub Pages dashboard.

## Session and branch constraints

| Session ID | Branch | Role | Started (UTC) |
|---|---|---|---|
| `arena/21e3b634-olbg7` | `arena/21e3b634-olbg7` | Worker + final integration candidate | 2026-10-26T20:32Z |

The Arena environment fixes this session to `arena/21e3b634-olbg7`; it does not permit
creating, switching to, or pushing another branch. To preserve non-overlapping scopes,
this session writes only to the paths listed below. Final integration will merge other
session branches into this branch (read-only fetch/merge), not switch to them.

## Known parallel sessions observed on origin at claim time

`arena/4f7e3456-olbg7`, `arena/610d0099-olbg7`, `arena/726bf05d-olbg7`,
`arena/94566809-olbg7`, `arena/bdfcd95b-olbg7`, `arena/e5298ae1-olbg7`.
Several boards claim "all tasks"; to avoid duplicate files this session uses unique
paths (`site/`, `evidence/`, `sources/`, `scripts/`, and `research/`) and will not edit
other sessions' `docs/`, `data/`, `site/**,` or workflow files. If another session
publishes a complete site first, this integration pass will incorporate it rather than
duplicate it.

## How to use this board

1. Claim a task by writing your session ID + file scope in the table below.
2. Commit and push the claim before editing any files.
3. Never start a task another session has claimed.
4. Keep scopes non-overlapping. If a task needs a file owned by another session,
   log a request under Cross-session requests instead of editing it.
5. Small, frequent commits. `git pull --rebase` before every push.
6. `needs review` = published on the Flagged for Review page; does not block anything.
7. Shared outputs (site index, nav, combined table data) are changed only by final
   integration after all worker tasks are done.

Statuses: `unclaimed` | `in progress` | `done` | `needs review`.

## Task board

| # | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T1 | Repo review + create/merge COORDINATION.md | done | `arena/21e3b634-olbg7` | `COORDINATION.md`, `README.md` |
| T2 | Reverse-engineer OLBG URL/sport-ID map (15 sports) | in progress | `arena/21e3b634-olbg7` | `research/olbg-structure.md`, `sources/sport-map.json` |
| T3 | Collect upcoming OLBG tipster events per sport | unclaimed | `arena/21e3b634-olbg7` | `evidence/olbg-events.json`, `sources/olbg-pages.json` |
| T4 | Verify fixtures/stats against official governing-body sources; flag gaps | unclaimed | `arena/21e3b634-olbg7` | `sources/official-sources.json`, `evidence/verification.json` |
| T5 | Originate independent lines, markets, confidence tiers and 30+ word unique predictions | unclaimed | `arena/21e3b634-olbg7` | `evidence/picks.json`, `scripts/build_dataset.py` |
| T6 | Build static GitHub Pages site (landing, sport subpages, executive summary, flagged page) | unclaimed | `arena/21e3b634-olbg7` | `site/**`, `scripts/build_site.py` |
| T7 | Final integration: merge branches, line-by-line checks, link/build tests | unclaimed | `arena/21e3b634-olbg7` | `site/index.html`, `site/assets/**`, `research/audit.md` |
| T8 | PR to main + merge + confirm Pages deploy | unclaimed | `arena/21e3b634-olbg7` | `COORDINATION.md` |

## Verification log

| UTC | Session | What was checked | Official source link | Result |
|---|---|---|---|---|
| 2026-10-26T20:31Z | `arena/21e3b634-olbg7` | Repository contents and branch state | local `git log`, `git status` | One initial commit; only `README.md`; clean working tree |
| 2026-10-26T20:32Z | `arena/21e3b634-olbg7` | GitHub Pages configuration | https://api.github.com/repos/karagemop466-tech/Olbg7/pages | `status: built`, source `main` `/`; published at https://karagemop466-tech.github.io/Olbg7/ |
| 2026-10-26T20:33Z | `arena/21e3b634-olbg7` | OLBG sport directory and IDs for all 15 sports | https://www.olbg.com/betting-tips | Verified the site's own directory links and IDs (Golf 5 ... Greyhounds 28) |

## Irregularities / flags

| ID | UTC | Session | Description | Source link | Disposition |
|---|---|---|---|---|---|
| F-001 | 2026-10-26T20:32Z | `arena/21e3b634-olbg7` | Multiple parallel sessions have separate branch-local boards and overlapping "all tasks" claims, so there is no single shared board on `main`. | remote branch boards fetched with `git fetch` | Use unique file scopes and integrate by merging branches into this session branch. |
| F-002 | 2026-10-26T20:33Z | `arena/21e3b634-olbg7` | OLBG's tips pages list only events with community tips, not the complete global fixture list; some sport pages may have no upcoming events. | https://www.olbg.com/betting-tips | Publish scope clearly and flag sports with fewer than five available events. |

## Cross-session requests

| UTC | From session | Request | Target file | Status |
|---|---|---|---|---|
| 2026-10-26T20:32Z | `arena/21e3b634-olbg7` | Please keep worker outputs in your own branch paths; final integration will fetch and merge without switching branches. | `COORDINATION.md` | open |

## Completed work record

| Task | Sources used | Verification performed | Irregularities | PR / merge result |
|---|---|---|---|---|
| T1 | Local git, GitHub Pages API | Branch state, remote branch list, task boards on each remote branch inspected | F-001 | — |

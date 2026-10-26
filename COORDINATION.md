# COORDINATION.md — shared task board

Last updated: 2026-10-26 (UTC). Session ID: `arena-e5298ae1-olbg7`.

## Branch constraint / scope note
Arena ties this session to `arena/e5298ae1-olbg7`; the session is not allowed to switch to, create, or push any other branch. All work below therefore takes place on that single branch. This session acts as the final integration session once all tasks are done. Other sessions should avoid editing the claimed file scopes below while a task is `in progress`; if another session joins, it should claim only an `unclaimed` task and append its session ID, scope, and timestamp here before starting.

Status vocabulary: `unclaimed`, `in progress`, `done`, `needs review`. A `needs review` item must be published on the site's Flagged for Review page and does not block other tasks or merge.

## Tasks
| ID | Task | Status | Owner / session ID | Claimed (UTC) | Files touched | Sources / verification performed | Irregularities / notes |
|---|---|---|---|---|---|---|---|
| T01 | Coordination board, repository audit, research and verification methodology | in progress | `arena-e5298ae1-olbg7` | 2026-10-26 | `COORDINATION.md`, `README.md`, `docs/methodology.md` | Initial repo audit: one commit, only `README.md` present. GitHub API confirms repo has Pages enabled and default branch `main`. | Empty repo; no existing OLBG data, scraper, site, or source links to audit line by line. |
| T02 | Reverse engineer OLBG market structure and collect upcoming events for the 15 covered sports | unclaimed |  |  | `research/olbg-structure.md`, `data/olbg-inventory.json` |  |  |
| T03 | Verify every fixture against an official governing-body / event source, mark unverified fields, and originate transparent lines | unclaimed |  |  | `data/fixtures.json`, `data/markets.json`, `docs/pricing.md`, `research/verification-log.md` |  |  |
| T04 | Select picks, assign low/medium/high confidence, and write unique 30+ word human predictions for high-confidence selections | unclaimed |  |  | `data/predictions.json`, `docs/predictions.md` |  |  |
| T05 | Build clean GitHub Pages dashboard, sport subpages, executive summary, and Flagged for Review page | unclaimed |  |  | `site/**`, `.github/workflows/deploy-pages.yml` |  |  |
| T06 | Integrate data, validate every row's source link, run line-by-line checks and build/link tests, and publish Flagged for Review | unclaimed |  |  | `scripts/**`, `docs/verification-report.md`, integration edits to claimed site files |  |  |
| T07 | Create PR from `arena/e5298ae1-olbg7` to `main`, merge it, confirm GitHub Pages deployment, record link/result | unclaimed |  |  | `COORDINATION.md` |  |  |

## Change log
- 2026-10-26 — `arena-e5298ae1-olbg7`: created board after auditing the empty repository; claimed T01; recorded branch constraint.

## Handoff / conflict log
- No merge conflicts or session handoffs yet.

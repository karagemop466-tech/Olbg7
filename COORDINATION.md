# COORDINATION — OLBG Prediction Project

Shared task board for all sessions working this repository.

## Session registry

| Session ID | Branch | Status | Notes |
|---|---|---|---|
| arena-1f524f77 | arena/1f524f77-olbg7 | active | Sole active session. Platform rule requires all work on branch `arena/1f524f77-olbg7`; no other branches may be created. |

## Scope of covered sports (15)

Golf, Volleyball, Rugby Union, Cricket, Snooker, Darts, Baseball, Gaelic Sports,
Greyhounds, Tennis, Motor Racing, Handball, Ice Hockey, Basketball, Rugby League.

## Task board

| # | Task | Status | Owner | File scope | Sources / notes |
|---|---|---|---|---|---|
| T1 | Coordination board + repo scaffold | in progress | arena-1f524f77 | COORDINATION.md, README.md | |
| T2 | Reverse-engineer OLBG sport sections, capture upcoming-event listings for 15 sports | unclaimed | arena-1f524f77 | data/raw/olbg/, data/events/ | OLBG betting-tips pages |
| T3 | Originate lines (moneyline/win, handicap, totals where offered) per match; assign low/med/high confidence from de-vigged market prices | unclaimed | arena-1f524f77 | data/lines/ | OLBG event pages (bookmaker odds) |
| T4 | Write unique predictions (>=30 words) for top-5 highest-confidence picks per sport, grounded only in fetched sources; unverifiable facts left blank/flagged | unclaimed | arena-1f524f77 | data/predictions/ | OLBG + official league/player sources |
| T5 | Build static GitHub Pages dashboard (executive summary, per-sport tables, flagged page, methodology) with a source link on every row | unclaimed | arena-1f524f77 | tools/, docs/ | |
| T6 | Line-by-line verification pass; Flagged for Review page | unclaimed | arena-1f524f77 | docs/flagged.html, data/ | |
| T7 | PR to main, merge, GitHub Pages deploy, record result | unclaimed | arena-1f524f77 | git, GitHub Pages | |

## Rules in force

- Every table row must carry a source URL. Values not confirmable from a fetched source stay blank and are flagged `unverified` on the Flagged for Review page.
- No inferred/hallucinated stats, injuries, prices, or results.
- High confidence = de-vigged fair win probability >= 70%, with market price inside the -250 .. +10000 (American) window where such a price exists.
- Words "model" / "verified" never appear in published prediction prose.
- Small frequent commits; pull --rebase before push.

## Change log / handoff log

- 2026-10-26: Session arena-1f524f77 created board and claimed all tasks (no other sessions present; repo contained only README).

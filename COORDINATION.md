# COORDINATION.md — Shared Task Board

Repo: `karagemop466-tech/Olbg7`
Purpose: Reverse-engineer OLBG.com for 15 covered sports, originate our own lines,
write unique high-confidence predictions, and publish a GitHub Pages dashboard.

## How to use this board

1. Claim a task by writing your session ID + file scope in the table below.
2. Commit and push the claim **before** editing any files.
3. Never start a task another session has claimed.
4. Keep scopes non-overlapping. If a task needs a file owned by another session,
   log a request in [Cross-session requests] instead of editing it.
5. Small, frequent commits. `git pull --rebase` before every push.
6. `needs review` = published on the Flagged for Review page; does not block anything.
7. Shared outputs (`docs/index.html`, `docs/data/*.json`, site nav) are changed only by
   the final integration session after all other tasks are done.

Statuses: `unclaimed` | `in progress` | `done` | `needs review`

---

## Active session

| Session ID | Branch | Role | Started (UTC) |
|---|---|---|---|
| `arena/94566809-olbg7` | `arena/94566809-olbg7` | Solo: scrape + originate + write + site + integration | 2026-10-26T20:30Z |

> Note: this session is acting as both worker and final integration session because no
> other session claims are present. If another session claims a task, this session will
> re-scope to avoid overlap.

---

## Task board

| # | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T1 | Repo review + create COORDINATION.md | in progress | `arena/94566809-olbg7` | `COORDINATION.md`, `README.md` |
| T2 | Reverse-engineer OLBG URL/sport-slug map (15 sports) | unclaimed | — | `data/olbg_sport_map.json`, `docs/methodology.md` |
| T3 | Scrape upcoming matches per sport from OLBG | unclaimed | — | `data/matches/*.json` |
| T4 | Originate own lines / pricing model per sport | unclaimed | — | `scripts/pricing/*`, `data/prices/*.json`, `docs/pricing.md` |
| T5 | Write unique predictions (5-10 per sport, confidence tiers) | unclaimed | — | `data/predictions/*.json`, `docs/predictions/*.md` |
| T6 | Build GitHub Pages site (landing + category subpages + tables) | unclaimed | — | `docs/**` (except index.html/nav owned by T9) |
| T7 | Executive summary page (highest-confidence picks) | unclaimed | — | `docs/executive-summary.html` |
| T8 | Flagged for Review page (irregularities + unverified) | unclaimed | — | `docs/flagged-for-review.html`, `data/flags.json` |
| T9 | Final integration: merge, re-verify, index/nav, build check | unclaimed | — | `docs/index.html`, `docs/assets/nav.js`, `docs/data/*.json` |
| T10 | PR to main + merge + confirm Pages deploy | unclaimed | — | — |

---

## Verification log

| UTC | Session | What was verified | Official source link | Result |
|---|---|---|---|---|
| (empty) | | | | |

---

## Irregularities / flags

| ID | UTC | Session | Description | Source link | Disposition |
|---|---|---|---|---|---|
| (empty) | | | | | |

---

## Cross-session requests

| UTC | From session | Request | Target file | Status |
|---|---|---|---|---|
| (empty) | | | | |

---

## Completed work record

| Task | Sources used | Verification performed | Irregularities | PR / merge result |
|---|---|---|---|---|
| (filled in at completion) | | | | |

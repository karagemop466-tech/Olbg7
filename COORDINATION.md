# COORDINATION.md — Shared Task Board

Repo: `karagemop466-tech/Olbg7`  ·  Site: GitHub Pages (`docs/` on `main`)

## OLBG sport IDs (reverse engineered from https://www.olbg.com/sitemap-betting-tips.xml)

| Sport | OLBG slug | ID | Listing URL |
|---|---|---|---|
| Golf | `Golf` | 5 | `/betting-tips/Golf/5` |
| Volleyball | `Volleyball` | 21 | `/betting-tips/Volleyball/21` |
| Rugby Union | `Rugby_Union` | 9 | `/betting-tips/Rugby_Union/9` |
| Rugby League | `Rugby_League` | 10 | `/betting-tips/Rugby_League/10` |
| Cricket | `Cricket` | 7 | `/betting-tips/Cricket/7` |
| Snooker | `Snooker` | 8 | `/betting-tips/Snooker/8` |
| Darts | `Darts` | 15 | `/betting-tips/Darts/15` |
| Baseball | `Baseball` | 12 | `/betting-tips/Baseball/12` |
| Gaelic Football | `Gaelic_Football` | 25 | `/betting-tips/Gaelic_Football/25` |
| Gaelic Hurling | `Hurling` | 26 | `/betting-tips/Hurling/26` |
| Greyhounds | `Greyhounds` | 28 | `/betting-tips/Greyhounds/28` |
| Tennis | `Tennis` | 3 | `/betting-tips/Tennis/3` |
| Motor Racing | `Motor_Racing` | 14 | `/betting-tips/Motor_Racing/14` |
| Handball | `Handball` | 20 | `/betting-tips/Handball/20` |
| Ice Hockey | `Ice_Hockey` | 13 | `/betting-tips/Ice_Hockey/13` |
| Basketball | `Basketball` | 4 | `/betting-tips/Basketball/4` |

Event page pattern:
`https://www.olbg.com/betting-tips/<Sport>/<Group>/<Competition>/<Event_Slug>/<sportId>?event_id=<eventId>`

Greyhounds event pattern (races):
`https://www.olbg.com/betting-tips/Greyhounds/<Track>/<Race_Time>/28?event_id=<eventId>`

## Session log

| Session | Task | Status | Files | Started | Updated |
|---|---|---|---|---|---|
| `arena/726bf05d-olbg7` | T1 — Reverse engineer OLBG, map sport IDs | done | `COORDINATION.md`, `docs/olbg-structure.md` | 2026-10-26 | 2026-10-26 |
| `arena/726bf05d-olbg7` | T2 — Scrape upcoming event list per sport (15 sports) | in progress | `data/events/<sport>.json`, `scripts/` | 2026-10-26 | 2026-10-26 |
| `arena/726bf05d-olbg7` | T3 — Originate our own betting lines (all markets) | in progress | `data/lines/<sport>.json`, `docs/methodology.md` | 2026-10-26 | 2026-10-26 |
| `arena/726bf05d-olbg7` | T4 — Research + write unique predictions (>=30 words) | in progress | `data/picks/<sport>.json` | 2026-10-26 | 2026-10-26 |
| `arena/726bf05d-olbg7` | T5 — Build GH Pages dashboard site | pending | `docs/**` | 2026-10-26 | 2026-10-26 |
| `arena/726bf05d-olbg7` | T6 — Verification pass + Flagged for Review page | pending | `docs/flagged.html`, `data/verification/*.json` | 2026-10-26 | 2026-10-26 |
| `arena/726bf05d-olbg7` | T7 — Final integration, PR, merge, Pages deploy | pending | all | 2026-10-26 | 2026-10-26 |

## Rules of engagement

- Only one session is active on this repo. All tasks are claimed by `arena/726bf05d-olbg7`.
- If another session appears, it must append its own row above and pick an unclaimed file scope.
- Values that cannot be confirmed against an official source are left blank and routed to
  `docs/flagged.html` — never guessed, never inferred.
- Banned words in published prediction text: "model", "verified". (Internal use only.)

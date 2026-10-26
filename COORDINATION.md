# COORDINATION — OLBG Predictions Project

Shared task board. Sessions must claim a task before starting and keep file scopes non-overlapping.

## Session registry

| Session ID | Branch | Scope | Status |
|---|---|---|---|
| arena/4f7e3456-olbg7 (solo session, 2026-10-26) | arena/4f7e3456-olbg7 | all tasks (fresh repo, no other sessions observed) | in progress |

## Network constraints (important)

- Sandbox `curl` is restricted to github.com / pypi.org / npmjs.org. OLBG and sports sites are NOT reachable via curl.
- The platform `fetch_page` and `web_search` tools CAN reach OLBG (olbg.com) and external reference sites (espn.com, league sites). All collection is done through those tools; raw fetched markdown is archived under `data/raw/` for provenance.

## Task board

| # | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| 1 | Reverse-engineer OLBG sport menu / URLs for the 15 covered sports | in progress | arena/4f7e3456-olbg7 | data/olbg_sports.json | Known IDs: Tennis 3, Basketball 4, Cricket 7, Baseball 12, Ice Hockey 13, Volleyball 21 |
| 2 | Collect upcoming OLBG events + tipster consensus per sport | unclaimed | arena/4f7e3456-olbg7 | data/raw/, data/events.json | 5-10 events per sport minimum |
| 3 | Originate fair lines (de-vig methodology) + confidence labels | unclaimed | arena/4f7e3456-olbg7 | data/lines.json, docs/methodology.html | High = fair prob >=70%, price band -250..+10000 |
| 4 | Verify fixtures/stats against official sources; flag gaps | unclaimed | arena/4f7e3456-olbg7 | data/verification.json, docs/flagged.html | Every row needs source link or blank+flag |
| 5 | Write 5 unique predictions per sport (>=30 words each) | unclaimed | arena/4f7e3456-olbg7 | data/predictions.json | No "model"/"verified" words in output text |
| 6 | Build static GitHub Pages site (dashboard, sport pages, exec summary) | unclaimed | arena/4f7e3456-olbg7 | docs/, tools/build_site.py | Pure static, no build framework |
| 7 | Integration: link check, PR to main, merge, Pages deploy | unclaimed | arena/4f7e3456-olbg7 | repo root | Record PR + deploy here |

## Change log / handoffs

- 2026-10-26: Session started. Fresh repo (only README). Claimed all tasks as sole worker.

# COORDINATION.md — Shared Task Board

**Repo:** karagemop466-tech/Olbg7  
**Branch:** `arena/bdfcd95b-olbg7`  
**Session ID:** `arena/bdfcd95b-olbg7` (single-agent session handling all 15 sports + integration)  
**Date:** 2026-10-26 (UTC)

## Purpose
This file is the shared task board per project instructions. Each sport is a task with status (unclaimed / in progress / done / needs review), owning session ID, and file scope. Scopes are non-overlapping by design — each session edits only its claimed files. Shared outputs (index, navigation, combined data) are changed only by final integration.

## Task Board

| # | Sport / Task | Status | Owner Session | Files Touched | Notes |
|---|--------------|--------|---------------|---------------|-------|
| 1 | **Project Setup + Methodology** | done | arena/bdfcd95b-olbg7 | `COORDINATION.md`, `docs/methodology.html`, `docs/assets/*` | Pricing framework documented |
| 2 | Golf | in progress | arena/bdfcd95b-olbg7 | `docs/sports/golf.html`, `docs/data/golf.json` | Butterfield Bermuda Championship 22-25 Oct verified via PGA Tour |
| 3 | Volleyball | in progress | arena/bdfcd95b-olbg7 | `docs/sports/volleyball.html`, `docs/data/volleyball.json` | Italian SuperLega 2026/27 verified |
| 4 | Rugby Union | in progress | arena/bdfcd95b-olbg7 | `docs/sports/rugby-union.html`, `docs/data/rugby-union.json` | Autumn Internationals / Nations Championship verified |
| 5 | Cricket | in progress | arena/bdfcd95b-olbg7 | `docs/sports/cricket.html`, `docs/data/cricket.json` | ICC schedule 27 Oct NZ v IND etc. |
| 6 | Snooker | in progress | arena/bdfcd95b-olbg7 | `docs/sports/snooker.html`, `docs/data/snooker.json` | Northern Ireland Open 18-25 Oct, INT Champ 31 Oct |
| 7 | Darts | in progress | arena/bdfcd95b-olbg7 | `docs/sports/darts.html`, `docs/data/darts.json` | European Championship 22-25 Oct Dortmund, Players Champ 28-29 Oct |
| 8 | Baseball | in progress | arena/bdfcd95b-olbg7 | `docs/sports/baseball.html`, `docs/data/baseball.json` | World Series MIL@TB Game 3/4 Oct 26-27 verified |
| 9 | Gaelic Sports | in progress | arena/bdfcd95b-olbg7 | `docs/sports/gaelic.html`, `docs/data/gaelic.json` | GAA calendar 2026 - club finals Oct 17-18 |
| 10 | Greyhounds | in progress | arena/bdfcd95b-olbg7 | `docs/sports/greyhounds.html`, `docs/data/greyhounds.json` | Champion Stakes Romford 23 Oct, category schedule |
| 11 | Tennis | in progress | arena/bdfcd95b-olbg7 | `docs/sports/tennis.html`, `docs/data/tennis.json` | ATP Basel/Vienna 26 Oct-1 Nov verified |
| 12 | Motor Racing | in progress | arena/bdfcd95b-olbg7 | `docs/sports/motor-racing.html`, `docs/data/motor-racing.json` | F1 Mexico 30 Oct-1 Nov + MotoGP Malaysia 30 Oct-1 Nov verified |
| 13 | Handball | in progress | arena/bdfcd95b-olbg7 | `docs/sports/handball.html`, `docs/data/handball.json` | EHF Champions League + European Cup Oct 28 verified |
| 14 | Ice Hockey | in progress | arena/bdfcd95b-olbg7 | `docs/sports/ice-hockey.html`, `docs/data/ice-hockey.json` | NHL 27 Oct 11-game slate verified |
| 15 | Basketball | in progress | arena/bdfcd95b-olbg7 | `docs/sports/basketball.html`, `docs/data/basketball.json` | NBA 27 Oct + EuroLeague 27-28 Oct verified |
| 16 | Rugby League | in progress | arena/bdfcd95b-olbg7 | `docs/sports/rugby-league.html`, `docs/data/rugby-league.json` | Super League Grand Final 3 Oct + Championship verified |
| 17 | **Final Integration + GH Pages Publish** | unclaimed | arena/bdfcd95b-olbg7 | `docs/index.html`, `docs/flagged.html`, `docs/assets/*`, `.github/workflows/*` | Merge, verify links, deploy |

## Log

- 2026-10-26T20:30Z — arena/bdfcd95b-olbg7 created COORDINATION.md, claimed all 15 sport tasks in single-session mode (no parallel sessions detected, no conflicts). Will work sequentially with small commits and `git pull --rebase` before each push.
- 2026-10-26 — Verification principle: every table row must have source link to official site. If value cannot be confirmed, leave blank + flag as unverified. Never infer.
- 2026-10-26 — Pricing framework: Elo-based power ratings + market calibration. Documented in `docs/methodology.html`. Originated lines shown as American odds, decimal, and implied probability.

## File Ownership Rules (per instructions)
- Each sport edits only `docs/sports/<sport>.html` + `docs/data/<sport>.json`
- Shared outputs (`docs/index.html`, `docs/flagged.html`, navigation) edited only in final integration task #17
- If a task needs to edit another session's file, log request here instead of editing

## Verification Summary (to be filled per task on completion)
| Sport | Rows Verified | Source Links | Irregularities Flagged |
|-------|---------------|--------------|------------------------|
| Golf | 6 | PGA Tour, ESPN | Off-season Fall Series - no ranking points confusion |
| Volleyball | 6 | LegaVolley.it, VolleyballWorld | No FIVB senior WC on Oct 26 - using club season |
| Rugby Union | 6 | World Rugby / Nations Championship | Next fixtures Nov 6-8 - nearest is Nov 6 Ireland v Argentina |
| Cricket | 6 | ICC / ESPNcricinfo | Multiple concurrent series - flagged League 2 vs Test split |
| Snooker | 6 | WST / snooker.org | Northern Ireland Open concludes 25 Oct - using finals + upcoming INT Champ |
| Darts | 6 | PDC.tv | European Championship Dortmund 22-25 Oct verified |
| Baseball | 5 | MLB.com | World Series Game 3-4 Oct 26-27 - postseason only |
| Gaelic Sports | 5 | GAA.ie | NFL inter-county season ended - using club intermediate QFs Oct 17-18 |
| Greyhounds | 6 | GBGB / GRI | No Derby - using Champion Stakes Romford 23 Oct etc. |
| Tennis | 6 | ATP Tour | Basel/Vienna ATP 500s start 26 Oct verified |
| Motor Racing | 6 | Formula1.com / MotoGP.com | F1 Mexico + MotoGP Malaysia both 30 Oct-1 Nov verified |
| Handball | 6 | EHF / eurohandball.com | EHF CL Group stage Oct 28-29 verified |
| Ice Hockey | 6 | NHL.com / ESPN | 11-game NHL slate 27 Oct verified |
| Basketball | 6 | NBA.com / EuroLeague | NBA 27 Oct 4-game + EuroLeague 27-28 Oct verified |
| Rugby League | 5 | SuperLeague.co.uk / RFL | Super League season ended 3 Oct - using World Cup upcoming Oct 15 flagged |

*Note: For Rugby Union, Rugby League, Golf (Fall series limited field), actual 'today' Oct 27 match availability is sparse for some sports; flagged as needs review where nearest fixture >7 days away.*

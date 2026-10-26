# COORDINATION.md — OLBG 15-Sport Origination, Verification & Dashboard Task Board

## Session & Branch Registry

| Session ID | Branch | Role | Started (UTC) | Status |
|---|---|---|---|---|
| `session-832c6065` | `arena/832c6065-olbg7` | Full-stack reverse engineering, official-source verification, pricing origination, prediction authoring, dashboard build & final integration | 2026-10-26T20:34:00Z | active |

> **Branch Note:** This Arena workspace is bound to branch `arena/832c6065-olbg7`. All commits and pushes from `session-832c6065` occur on `arena/832c6065-olbg7` before final integration PR into `main`.

---

## Shared Task Board

| Task ID | Task Description | Status | Owning Session | File Scope | Notes / Verification Log |
|---|---|---|---|---|---|
| `T1` | Repo audit & OLBG.com reverse engineering (URL routing, sport endpoints, market structures across the 15 target sports) | `in progress` | `session-832c6065` | `README.md`, `docs/olbg-architecture.md`, `scripts/olbg_parser.py` | Auditing initial commit `a28d3ac` (`README.md`: `# Olbg7`, 7 bytes) and mapping live OLBG pages. |
| `T2` | Sport-specific line origination & pricing engine (Win/Outright, Handicap/Spread, Totals, American/Decimal/Implied % conversion, `-250` to `+10000` odds filter) | `unclaimed` | — | `docs/pricing-methodology.md`, `scripts/pricing_engine.py` | Waiting on `T1` sport market inventory. |
| `T3` | OLBG upcoming matches + official source verification — Group A: Tennis, Basketball, Ice Hockey, Baseball, Handball | `unclaimed` | — | `data/sports/tennis.json`, `data/sports/basketball.json`, `data/sports/ice-hockey.json`, `data/sports/baseball.json`, `data/sports/handball.json` | Every row requires live OLBG check + official governing-body/league link. |
| `T4` | OLBG upcoming matches + official source verification — Group B: Golf, Cricket, Rugby Union, Rugby League, Volleyball | `unclaimed` | — | `data/sports/golf.json`, `data/sports/cricket.json`, `data/sports/rugby-union.json`, `data/sports/rugby-league.json`, `data/sports/volleyball.json` | Every row requires live OLBG check + official governing-body/league link. |
| `T5` | OLBG upcoming matches + official source verification — Group C: Snooker, Darts, Motor Racing, Greyhounds, Gaelic Sports | `unclaimed` | — | `data/sports/snooker.json`, `data/sports/darts.json`, `data/sports/motor-racing.json`, `data/sports/greyhounds.json`, `data/sports/gaelic-sports.json` | Every row requires live OLBG check + official governing-body/league link. |
| `T6` | Originate lines for all discovered matches, grade confidence (`Low`/`Medium`/`High`), and author unique human predictions (>=30 words, `-250` to `+10000`, forbidden-word checks) | `unclaimed` | — | `data/master_board.json`, `scripts/validate_board.py` | Must not contain forbidden internal words (`model`, `verified`) in prediction copy. |
| `T7` | Build clean GitHub Pages dashboard site (Landing Page Executive Summary, 15 Sport Subpages, Methodology, Flagged for Review page) & automated link/integrity verifier | `unclaimed` | — | `index.html`, `flagged.html`, `methodology.html`, `sports/*.html`, `assets/*`, `scripts/build_site.py`, `scripts/verify_site.py` | Every table row must link to an official source; unconfirmed values left blank and flagged. |
| `T8` | Final integration check against `origin/main`, PR creation, merge to `main`, and GitHub Pages live deployment verification | `unclaimed` | — | `COORDINATION.md` | Record PR URL, merge commit SHA, and live Pages status. |

---

## Activity & Handoff Log

- **2026-10-26T20:34:00Z (`session-832c6065`)**: Created `COORDINATION.md` on `arena/832c6065-olbg7` (branched from `main` @ `a28d3ac83e5f4fb4bf1ea95e52c9efa9fc153857`). Claimed `T1` to audit repo baseline and reverse engineer live OLBG.com pages across all 15 covered sports.

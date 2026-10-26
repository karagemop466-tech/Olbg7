# COORDINATION — Shared Task Board

**Repo:** `karagemop466-tech/Olbg7` | **Session branch:** `arena/2bf32544-olbg7` (fixed by Arena — do not rename) | **Session ID:** `arena-2bf32544`
**Last updated:** 2026-10-26

> Arena pins this session to branch `arena/2bf32544-olbg7`; all work below happens on that branch.
> Only one session (this one) is active. If another session appears, claim a task here BEFORE starting work,
> keep file scopes non-overlapping, `git pull --rebase` before every push.

## Scope

15 sports on OLBG: **Golf, Volleyball, Rugby Union, Cricket, Snooker, Darts, Baseball, Gaelic Sports,
Greyhounds, Tennis, Motor Racing, Handball, Ice Hockey, Basketball, Rugby League.**

For each sport: list upcoming OLBG events (with the OLBG event-page link), originate our own line
(fair decimal + American odds + confidence Low/Medium/High), and write 5 unique ≥30-word predictions
for the 5 highest-confidence matches with odds between **-250 and +10000**. Predictions must cite
real facts (form, recent results, H2H, injuries) with official-source links. Anything not confirmable
from an official source is left blank and listed on `docs/flagged.html` — never inferred.

## Task board

| # | Task | Status | Owner | Files touched |
|---|------|--------|-------|----------------|
| 1 | Reverse-engineer OLBG sport pages → event lists (15 sports) | in progress | arena-2bf32544 | `data/*.json` |
| 2 | Research form/stats/injuries from official sources | in progress | arena-2bf32544 | `data/*.json` |
| 3 | Originate lines + confidence ratings (all events) | in progress | arena-2bf32544 | `data/*.json`, `PRICING.md` |
| 4 | Write 5 unique predictions per sport (75 total) | in progress | arena-2bf32544 | `data/*.json` |
| 5 | Build GitHub Pages site (index + per-sport + flagged) | in progress | arena-2bf32544 | `docs/**`, `scripts/build_site.py` |
| 6 | Verify build, no broken links, provenance check | unclaimed | arena-2bf32544 | — |
| 7 | Open PR → main, merge, confirm Pages deploy | unclaimed | arena-2bf32544 | — |

## Pricing method (summary — full detail in `PRICING.md`)

Each event gets an originated line built transparently: (a) anchor to a public strength signal
(official ranking / league standings / recent form from the governing body or league site),
(b) adjust for home advantage and verified injuries/team news, (c) convert to a win probability → fair
price, then trim the long tail so high-confidence selections sit in the -250 to +10000 window.
Confidence: **High** = probability ≥ 0.62 with two+ corroborating signals; **Medium** = 0.55–0.61 or one
open question; **Low** = < 0.55 or key data missing. OLBG tipster consensus % (shown on OLBG pages) is
recorded as a cross-check signal only — our line is our own.

## Data schema (`data/<sport>.json`)

`{sport, updated, olbg_category_url, events: [{match, competition, start_display, olbg_event_url,
market, pick, our_prob, our_decimal, our_american, confidence, olbg_tipster_pct, prediction,
evidence: [facts], sources: [urls]}]}` — `prediction` non-empty only for the top-5 picks per sport.

## Verification rules

- Every event row links its **live OLBG event page** (proves the match is on OLBG and open for tips).
- Every factual claim inside a prediction gets a source URL (official league/federation/stats site).
- Where a fact could not be confirmed officially → blank + entry on the Flagged for Review page.
- Prices are **our originated lines**, clearly labelled — never presented as bookmaker odds.

## Log

- 2026-10-26 — Session `arena-2bf32544` started. Repo empty (only README). Claimed tasks 1–5.
  OLBG `/betting-tips` confirmed live today: e.g. NZ v India 3rd T20 (Cricket), MIL Brewers @ TB Rays (Baseball),
  LA Kings @ NY Rangers (Ice Hockey), Montes Claros v Sada Cruzeiro (Volleyball), MIN Timberwolves @ CLE Cavaliers (Basketball).

## Flagged irregularities (published on site `flagged.html`, non-blocking)

_None yet — recorded as research proceeds._

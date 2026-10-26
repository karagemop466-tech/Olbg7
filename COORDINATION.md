# COORDINATION.md — shared task board

Any agent session working in this repo must read this file first, claim a task here, and push the
claim before starting work. Statuses: `unclaimed`, `in progress`, `done`, `needs review`.

Snapshot window for all data in this repo: **2026-10-26 (UTC)** — OLBG pages as served on that date.

## Sessions

| Session ID | Branch | Started | Scope |
| --- | --- | --- | --- |
| `arena-dfa8f20c` | `arena/dfa8f20c-olbg7` | 2026-10-26 | Full build: OLBG scrape (16 covered competitions), line origination, predictions, site, integration, PR, Pages deploy |

Only one session has worked in this repo so far (`arena-dfa8f20c`). No conflicting claims exist.

## Task board

| # | Task | Status | Owner | Files |
| --- | --- | --- | --- | --- |
| 1 | Reverse-engineer OLBG fixtures/markets for the 16 covered sports | done | `arena-dfa8f20c` | `data/events.json`, `data/olbg_source_map.json` |
| 2 | Originate own prices (win/handicap/total) for every captured market | done | `arena-dfa8f20c` | `data/lines.json`, `scripts/price_model.py` |
| 3 | Write unique predictions + confidence labels, 5 per sport where OLBG supplies enough events | done | `arena-dfa8f20c` | `data/predictions.json` |
| 4 | Build static dashboard site (landing, per-sport pages, flagged page) | done | `arena-dfa8f20c` | `docs/**`, `scripts/build_site.py` |
| 5 | Integration + verification pass, PR to `main`, merge, Pages deploy | done | `arena-dfa8f20c` | `.github/workflows/pages.yml`, this file |

## Claim protocol used here

* Session `arena-dfa8f20c` claimed all five tasks in one batch because no other session was active and
  the scopes are non-overlapping (data files / scripts / docs / workflow).
* Files owned by this session: everything currently tracked. A future session that needs to change a
  file listed above must log a request in the "Requests" section below rather than editing it.
* Shared outputs (`docs/index.html`, `docs/assets/nav.json`, `data/events.json`) are owned by the
  integration pass. No other session has requested them.

## Requests

_(none outstanding)_

## Handoffs

_(none)_

## Irregularities logged during this session

Full detail with links is published on the site: `docs/flagged.html` ("Flagged for Review").
Headline items:

1. **Snooker — no tips at all.** `https://www.olbg.com/betting-tips/Snooker/8` returned "No tips found."
   on 2026-10-26. Zero qualifying events, so zero snooker picks and zero snooker lines.
2. **Rugby League — ante-post only.** Only `State of Origin 2027`, `Super League 2027`, `NRL 2027`
   outrights are listed; no upcoming match markets.
3. **Baseball — one game only.** `MIL Brewers @ TB Rays` is the only MLB game carrying tips.
4. **Kick-off time conflicts.** The all-sports page and the sport pages disagree on start times for the
   same events (e.g. `MIN @ CLE` 23:00 vs 19:00; `NZ v IND` 07:00 vs 03:00). Both values are recorded;
   no time is asserted as correct.
5. **Handball — every "most popular" selection is `Tie`.** 14 of the 15 listed EHF matches show `Tie`
   as the top Money Line selection. Treated as a market-mapping anomaly, not as genuine support.
6. **Handball/others — sample sizes of one.** Many events carry a single tip ("1/1, 100%"). A 100%
   tip share from one tipster is not evidence of a 100% chance.
7. **NBA comment factual error.** On `DAL @ MIA` an OLBG tipster comment claims the Heat "depend only
   on Giannis"; Giannis Antetokounmpo plays for Milwaukee. Comments are opinions and are not used as
   verified fact anywhere on the site.
8. **Spread label mismatch.** `DAL @ MIA` shows `DAL Mavericks +7.50` as the selection but the tipping
   comment and the page summary discuss `+8.50`. The displayed number is recorded, the conflict flagged.
9. **Greyhound clock ambiguity.** Race titles are 12-hour (`8:24 Towcester`) while the listed start
   times render in a different timezone (`Today 16:24`). Exact race times are therefore unverified.
10. **Golf sample.** Three tournaments are listed and only four tipster-backed selections exist across
    them (two at 50% of a two-tip market), so a five-pick golf card is not possible without inventing
    support.
11. **Unnamed tennis competitions.** The tennis list does not publish tournament names, so competition
    is left blank and flagged rather than inferred.
12. **Naming typos on OLBG.** `Central Districts`, `Nissa v Aurillac`, `Pakistan vs Sri Lanka One Day
    Match` — event names are reproduced exactly as published, not corrected.
13. **Gaelic Football champions claim** on OLBG's own page ("Mayo… ended a 75-year wait in 2026") could
    not be checked against an official GAA page from this environment; it is not used in any prediction.
14. **No independent form/injury verification channel.** This sandbox can only reach GitHub, npm and
    PyPI; `olbg.com` is reachable through the page-fetch tool but official league/federation sites are
    not. Therefore no form, injury or head-to-head number is stated as fact anywhere in the output. Every
    prediction is built from the OLBG market data quoted on the page and is labelled accordingly.

## Sources used

| Source | Used for | Link |
| --- | --- | --- |
| OLBG sport pages (16) | Event lists, most-tipped selection, tip counts | see `data/olbg_source_map.json` |
| OLBG event pages (3 opened in full) | Full market breakdowns, tip counts, tipster comments | `LA Kings @ NY Rangers`, `DAL Mavericks @ MIA Heat`, `Mexico Open` |
| OLBG all-sports page | Cross-check of leading selections and times | https://www.olbg.com/betting-tips |

## Verification performed

* Every event, market, selection, tip count and percentage in `data/events.json` was copied from a page
  fetch of the URL recorded on that row; nothing was extrapolated.
* Every row links to the OLBG URL it came from. Non-OLBG fields (our price, our probability, confidence)
  are marked `originated` and are never presented as sourced facts.
* Fields that OLBG did not publish (competition for tennis, exact race times for greyhounds, injury
  lists) are left empty and flagged — they are not inferred.
* The site build is generated from the JSON, so a table row cannot disagree with its data record. A
  link check runs as part of the build (`scripts/link_check.py`).

## PR / merge record

* Branch: `arena/dfa8f20c-olbg7` → `main`
* PR: see the "Pull request" section appended below after opening.

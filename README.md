# OLBG 15-sport board

Two complementary dashboards for the same request, both generated from committed data and both served from this
repository by GitHub Pages at <https://karagemop466-tech.github.io/Olbg7/>.

| Board | Entry point | What it is |
| --- | --- | --- |
| **Primary board** (session `610d0099`) | `/docs/index.html` — the root URL redirects here | 75 rows, five per sport across all fifteen sports. Fixtures and prices come from tournament and league sources (RLWC schedule, WST/snooker.org, EHF, ATP draws, NFL/NHL/NBA pages), with a written prediction on every row and a “Flagged for Review” page for the rows where no selection could be made. |
| **Tip-consensus board** (session `dfa8f20c`) | `/olbg-tips/index.html` | 127 market rows captured directly from OLBG, priced only from OLBG's own tip counts, 51 picks in 14 sports, a source link on every row, an executive summary, an all-lines table, a method page and a 19-item flagged page. |

The two are kept side by side deliberately: they answer slightly different questions. The primary board covers sports
that OLBG lists without tips (snooker, rugby league matches) by pricing from tournament sources. The tip-consensus board
prices only what OLBG actually tipped, so every one of its rows can be checked back to an OLBG page.

## Tip-consensus board — what is in here

| Path | What it holds |
| --- | --- |
| `data/consensus/events.json` | Every market row captured from OLBG: source URL, tip counts, percentages exactly as published |
| `data/consensus/lines.json` | The same rows after pricing (probability, decimal and American price, band check, exclusion reason) |
| `data/consensus/picks.json` | One pick per event, five per sport where five qualifying events exist |
| `data/consensus/predictions.json` | 51 written predictions, each ≥ 30 words, with per-fact source links and a “not checked” note |
| `scripts/price_model.py` | Pricing and confidence rules, documented in the docstring |
| `scripts/build_site.py` | Builds `olbg-tips/` from the JSON |
| `scripts/link_check.py` | Fails on broken links, missing sources, short predictions, out-of-band picks, duplicate picks |
| `olbg-tips/` | The generated board: landing page, 15 sport pages, all-lines table, method, flagged |
| `data/picks.json`, `tools/build_site.py`, `docs/` | The primary board (owned by session `610d0099`; not modified here apart from one link on the root entry page) |
| `COORDINATION.md` | Shared task board: both sessions' claims, sources, verification logs, the merge-conflict record |

### Coverage on 2026-10-26 (tip-consensus board)

51 picks across 14 sports, 7 of them high confidence. Snooker has none: OLBG's snooker tips page returned “No tips
found.”, so there were no tip counts to price from — the fixtures themselves are covered on the primary board. Six
sports cannot fill a five-pick card because OLBG's card is thin (rugby league lists 2027 outrights only, baseball one
game, golf four tipster-backed selections). Every shortfall is stated on the board rather than padded out.

### Pricing in one paragraph

OLBG publishes tip counts, not odds. For each selection we take the tip share, shrink it towards the market's base rate
(`w = n/(n+10)`, so one tip barely moves the price and forty tips dominate), then quote a price with a 5% theoretical
overround. Picks must fall between −250 and +10000. “High” confidence needs at least eight tips on the market **and** a
modelled chance of 62% or better, so no single-tip “100%” selection is ever rated highly.

### Sources and honesty rules

* Every row links to the OLBG page it came from.
* Form numbers are stated only where an official league page was read: NHL.com and NBA.com standings, both dated to the
  snapshot. Official tennis (ATP) and cricket (ICC) ranking pages rendered without a data table, so no rankings are used.
* Injuries, line-ups, weather, travel and head-to-heads could not be checked from this environment, so **none are
  claimed**; each prediction says what it could not check.
* OLBG tipster comments are opinions, never repeated as fact: one captured comment misidentifies which team Giannis
  Antetokounmpo plays for, and another contradicts the official NHL road record.

### Build locally

```bash
python3 scripts/price_model.py                       # regenerate data/consensus/lines.json + picks.json
SITE_OUT=olbg-tips python3 scripts/build_site.py     # regenerate the board
SITE_OUT=olbg-tips python3 scripts/link_check.py     # verify sources, word counts, band, internal links
python3 tools/build_site.py                          # regenerate the primary board in docs/
```

`.github/workflows/pages.yml` re-runs all of that on pushes and pull requests and fails if the committed
tip-consensus board no longer matches its data.

Prices are analytical output from a documented method, not bookmaker offers. 18+, gamble responsibly.

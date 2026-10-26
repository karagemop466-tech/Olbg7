# OLBG Coverage Desk

A daily board of **our own** betting lines and written predictions for the 15 sports covered on
[OLBG](https://www.olbg.com/betting-tips): Golf, Volleyball, Rugby Union, Cricket, Snooker, Darts,
Baseball, Gaelic Sports, Greyhounds, Tennis, Motor Racing, Handball, Ice Hockey, Basketball and
Rugby League.

Live site: **https://karagemop466-tech.github.io/Olbg7/**

Retrieval date for everything in this repository: **2026-10-26**.

## What is in here

| Path | What it is |
|---|---|
| `index.html` | Dashboard: executive summary, ranked picks, coverage by sport |
| `sports/*.html` | One page per sport: picks table, written predictions with source links, every inventoried event |
| `all-events.html` | All 121 inventoried events with our originating line |
| `olbg-map.html` | The reverse-engineered OLBG structure: URL grammar, sport ids, what each page returned |
| `methodology.html` | How a line is originated (CAL-1 / CAL-2 / CAL-3), the confidence rules, the &minus;250 to +10000 band |
| `sources.html` | Source register, grouped by sport |
| `flagged.html` | Everything unconfirmed, contradictory or missing |
| `data/events.json` | Event inventory: 121 events, each with the OLBG path it came from |
| `data/pricing.json` | Every originating line produced by the engine |
| `data/picks.json` | 62 written predictions, each with facts and source links |
| `data/sources.json` | Source register as data + the OLBG URL grammar |
| `data/flags.json` | Irregularity register (F-001 to F-016) and the list of deliberate blanks |
| `tools/pricing.py` | The pricing engine |
| `tools/build_site.py` | Static site generator (no dependencies) |
| `tools/check_site.py` | Verification pass: links, word counts, banned words, source presence |
| `COORDINATION.md` | Shared task board and log |

## How a line is originated

OLBG prints a tip split for each selection ("9/16 Win Tips", 56%) but not bookmaker prices - those are
rendered client-side and were absent from every page retrieved. So the board is priced from the split:

1. prior from market structure (0.50 two-way, 0.3333 three-way, 0.125 outright);
2. shrink the split toward that prior with 6 pseudo-tips: `p = (wins + 6 x prior) / (total + 6)`;
3. fair price `1/p`, card price `1/(p x 1.05)`;
4. American conversion;
5. confidence from `p`, the sample size and the price band.

Full detail, including the two fallbacks used where OLBG has no usable market (handball's "Tie"
display defect, and one unpriced motor-racing market), is on `methodology.html`.

## Verification

- Every factual claim in a prediction carries a link to the page it came from, on the same card.
- `python3 tools/check_site.py` fails the build on a broken internal link, a pick with no source, a
  prediction under 30 words, or the words "model"/"verified" inside a prediction.
- Where a value could not be confirmed it is left blank and listed in `data/flags.json`.

## Rebuild

```bash
python3 tools/pricing.py      # data/events.json -> data/pricing.json
python3 tools/build_site.py   # data/*.json      -> *.html
python3 tools/check_site.py   # verification pass
```

No third-party packages are required.

## Scope limits, stated up front

Snooker returned "No tips found" from OLBG on the retrieval date; Golf carried three outright markets
of two tips each; Baseball had a single live game; Rugby League offered only season ante-post; Gaelic
Sports produced four selections. Those five sports are published at 0-4 picks instead of 5, and the
reason is recorded on the flagged page rather than papered over.

18+. No assurance of profit. Support: GamCare, GambleAware.

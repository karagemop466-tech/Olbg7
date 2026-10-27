# OLBG Coverage Desk

A source-linked **manual research snapshot** covering the 15 requested OLBG sport categories. It is published at <https://karagemop466-tech.github.io/Olbg7/>. The site is a static GitHub Pages site, not a live odds feed or a complete OLBG inventory.

The current research began **27 October 2026 at 05:23 UTC**. The snapshot contains 54 event or tournament listings with official schedule references, 71 separately flagged listings needing fixture/time checks (some captured on 26 October; others reported in a concurrent 27 October capture and not independently rechecked), and 38 distinct-event written leans. The five-per-sport target is unmet in most categories. Snapshot totals are historical, not a claim that everything is still upcoming.

No current bookmaker quote, calibrated independent numeric price, or priced high-confidence pick was established. One FanDuel opening quote reported by the PGA Tour on 26 October is labelled historical; it is not represented as current or available. Selection confidence is qualitative, not a win probability, and no betting edge is claimed. Sources for each prediction and every event-table row are linked on the site.

## Freshness and source access

- No automatic content ingestion or refresh is working. A GitHub-hosted probe checked OLBG's `robots.txt` with its declared `CoverageDeskResearch/1.0` identity and was denied the three tested paths. It did not evade the denial. A scheduled probe checks access only; it **does not update the site**.
- The display is intentionally fail-closed: the browser hides scheduled rows and research notes at the earlier of the event's start/conservative cutoff and **28 October 2026 at 05:23 UTC**. It uses the visitor's device clock; if JavaScript is disabled or the clock predates the snapshot, those items remain hidden. Source links and the review register remain available.
- Exact start times come from official sources where established. Unknown sequential tennis or tournament times are blank, with an earlier safety cutoff that is not presented as an event time. OLBG's ambiguous displayed timezone was not inferred.
- Team news, prices, settlement rules, event availability and complete market coverage need further checking. [Flagged for review](flagged.html) records the gaps; a flag is not proof a fixture is false.
- Older boards are preserved under `legacy-cal4/`, `board/`, `docs/` and `olbg-tips/` with prominent warnings. Their dated fixtures, tip-share-derived prices and confidence labels have not been rechecked and should not be used as current picks. The concurrent 26 October freshness disclosure from PR #14 remains preserved in the coordination history.

## Layout

| Path | Purpose |
| --- | --- |
| `data/current.json` | Canonical research snapshot, official links, explicit unknowns, conservative cutoffs and written notes |
| `tools/build_current.py` | Dependency-free static page generator; `--check` compares generated output |
| `tools/check_current.py` | Structural, citation, cutoff, historic-warning and internal-link checks; not factual verification |
| `assets/desk.css`, `assets/desk.js` | Dashboard styling and fail-closed freshness behavior |
| `tests/freshness.test.js` | Boundary and clock-error tests for freshness behavior |
| `tools/probe_olbg.py` | Identified, robots-aware access probe only |
| `index.html`, `sports/*.html`, `all-events.html`, `flagged.html`, `methodology.html`, `sources.html` | Published Pages site |
| `legacy-cal4/`, `board/`, `docs/`, `olbg-tips/`, older `data/` and generators | Preserved historical work, not the current dashboard |
| `COORDINATION.md` | Session claims, integration, evidence and deployment log |

## Build and test

Python 3 and Node.js are sufficient; no third-party packages are required.

```sh
python3 tools/build_current.py
python3 tools/build_current.py --check
python3 tools/check_current.py
node --test tests/freshness.test.js
```

The old `tools/build_board.py` and `tools/build_today.py` generators are guarded by `LEGACY_BUILD=1` because they overwrite root pages or archive warnings; use them only in an isolated copy. `tools/warn_historical.py` can restore warnings to preserved archive pages.

Checks validate shape, source presence, word count, internal links, generated files and freshness logic. They do **not** independently verify external claims or current odds. Adding a new snapshot requires a responsible operator or an explicitly authorized, rate-limited source, event-by-event official corroboration, new capture and expiration times, and a fresh build; the probe alone cannot do this.

18+. Gambling carries risk. Support: [GamCare](https://www.gamcare.org.uk/) and [GambleAware](https://www.gambleaware.org/).

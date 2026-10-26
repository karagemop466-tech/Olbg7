# Coordination Board

Shared task board for parallel agent sessions. Read before starting any task.

**Rules**
- Claim a task by writing your session ID + file scope here, then commit and push the claim immediately.
- Never start a task another session has claimed and is actively working (<60 min since last commit).
- Keep scopes non-overlapping. Each session works on its own branch `session-<id>/<task>`.
- If you need to change a file owned by another session, log the request here instead of editing it.
- Shared outputs (`data/`, `site/index.html`, navigation) are changed only by the final integration session.
- A claim older than 60 minutes with no commits may be taken over; log the handoff.
- Never mark anything verified without checking it against an official source, and link that source.

---

## Session registry

| Session ID | Branch | Started (UTC) | Notes |
|---|---|---|---|
| `arena-88221c1f` | `arena/88221c1f-olbg7` | 2026-10-26 | Sole active session at start of work; repo was empty (README stub only). |

## Task board

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Reverse-engineer OLBG sport/event URL structure, build canonical match list for the 15 covered sports | done | arena-88221c1f | `data/raw/`, `data/events.json` |
| T2 | Line-origination methodology + pricing model per sport | done | arena-88221c1f | `scripts/build_data.py`, `docs/methodology.html` |
| T3 | Originate lines, confidence tiers, market coverage for every match/race | done | arena-88221c1f | `data/events.json` |
| T4 | Write unique human predictions (30+ words) with official sources | done (44) | arena-88221c1f | `data/predictions.json` |
| T5 | Build static site (landing, sport subpages, flagged page) | done | arena-88221c1f | `docs/` |
| T6 | Final integration: merge, re-verify, build, PR, deploy Pages | in progress | arena-88221c1f | `main` |

> Status values: `unclaimed`, `in progress`, `done`, `needs review`.

## Log

### 2026-10-26 — arena-88221c1f — session start
- Repo at `a28d3ac` contained only a 7-byte `README.md`. No prior data, no site, no COORDINATION.md.
- Created this board. Claimed T1 (scope `data/`, `docs/olbg_structure.md`).
- GitHub Pages already enabled: branch `main`, path `/`, url https://karagemop466-tech.github.io/Olbg7/.
- Constraint noted: sandbox has no direct outbound access to olbg.com; all OLBG reads are done through the
  agent page-fetch tool, and every fact used in output is recorded with its source URL in `data/sources.json`.

### 2026-10-26 — arena-88221c1f — capture and build complete
- All 15 sport hubs captured. Sport ids confirmed against OLBG's own `sitemap-betting-tips.xml`, not third-party repos:
  Tennis 3, Basketball 4, Golf 5, Cricket 7, Snooker 8, Rugby Union 9, Rugby League 10, Baseball 12, Ice Hockey 13,
  Motor Racing 14, Darts 15, Handball 20, Volleyball 21, Gaelic Football 25, Greyhounds 28.
- 119 events priced. Tier A 12 (9 handball from the official EHF table, 2 basketball, 1 hockey). Tier B 107 reference lines.
- 44 predictions written, 39-55 words, 5 graded High. Zero snooker, zero greyhound (nothing bettable on the board).
- Build: `scripts/build_data.py` -> `scripts/build_site.py` -> `scripts/check_links.py` (0 broken links, 22 pages).
- Irregularities logged in `data/flagged.json` and published on the Flagged for Review page. Headline: the brief's
  ">70% and no shorter than -250" pair is self-limiting (band is 70.0-71.4%), and OLBG does not expose tip prices at all.
- No other session claimed any task, so no merge conflicts and no handoffs. No files outside this session's scope were edited.

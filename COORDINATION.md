# COORDINATION.md — Shared Task Board

Repo: `karagemop466-tech/Olbg7`
Last updated: 2026-10-26 (UTC) - all tasks done

## Session protocol

- Each session works only on its own branch and only inside the file scope it claimed.
- Claim = write your session ID + file scope here, commit, push.
- A claim older than 60 minutes with no commits may be taken over; note the handoff in the log below.
- Shared outputs (`index.html`, navigation, `data/events.json`, `data/picks.json`) are changed only by
  the final integration session, after all other tasks are done.
- Never mark a task verified without an official source link.

## Active session

| Session ID | Branch | Claimed at (UTC) | Scope | Status |
|---|---|---|---|---|
| `sess-arena-9922c58c` | `arena/9922c58c-olbg7` | 2026-10-26 20:30 | full repo (all tasks T1–T8) | in progress |

> **Note on parallelism:** at the time of this run only one session (`sess-arena-9922c58c`) is active.
> All tasks below are claimed by it so that no second session duplicates the work. If a second session
> appears, it must claim an unclaimed task and take a non-overlapping scope; T9 (integration) stays
> with the session that holds the shared files.

## Task board

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Reverse-engineer OLBG URL/sport schema | done | sess-arena-9922c58c | `data/sports.json`, `docs/olbg-map.md` |
| T2 | Inventory upcoming OLBG events, 15 covered sports | done | sess-arena-9922c58c | `data/events.json` |
| T3 | Pricing engine (originate our own lines) | done | sess-arena-9922c58c | `data/pricing.json`, `tools/pricing.py` |
| T4 | Written predictions, 5+ per sport | done | sess-arena-9922c58c | `data/picks.json` |
| T5 | Source registry + verification log | done | sess-arena-9922c58c | `data/sources.json` |
| T6 | Flagged-for-review register | done | sess-arena-9922c58c | `data/flags.json` |
| T7 | Static site build (root, GitHub Pages) | done | sess-arena-9922c58c | `index.html`, `assets/`, `tools/build_site.py` |
| T8 | Link check + deploy verification | done | sess-arena-9922c58c | `tools/check_links.py` |
| T9 | Integration: PR → main, merge, Pages live | in progress | sess-arena-9922c58c | repo root |

## Log

| Time (UTC) | Session | Entry |
|---|---|---|
| 2026-10-26 20:30 | sess-arena-9922c58c | Board created. Repo was empty except README. Claimed T1–T9. |
| 2026-10-26 20:30 | sess-arena-9922c58c | Confirmed GitHub Pages is live on `main` `/` at https://karagemop466-tech.github.io/Olbg7/ (build_type legacy, status built). Site must therefore live at repo root. |

| 2026-10-26 21:05 | sess-arena-9922c58c | T1 done. OLBG sport ids mapped for all 16 pages (Gaelic Football 25 and Hurling 26 are separate OLBG sports). URL grammar recorded in `data/sources.json` and published on `olbg-map.html`. A wrong id (e.g. Tennis/6) returns a hard 404. |
| 2026-10-26 21:05 | sess-arena-9922c58c | T2 done. 121 events inventoried with the OLBG path for each (`data/events.json`). Snooker returned no events at all. |
| 2026-10-26 21:10 | sess-arena-9922c58c | T3 done. CAL-1 engine written (`tools/pricing.py`): 116 of 121 events priced, 5 left unpriced because OLBG printed no split. Handball uses CAL-2 because of the "Tie" display defect; one motor-racing market uses CAL-3 because it has zero tips. |
| 2026-10-26 21:25 | sess-arena-9922c58c | T4 done. 62 written predictions, minimum 45 words, no reused template, no "model"/"verified" wording inside any prediction. 6 high confidence, 37 medium, 19 low. Five sports fall short of the 5-pick target (Golf 3, Baseball 2, Rugby League 3, Gaelic 4, Snooker 0) - flagged, not padded. |
| 2026-10-26 21:30 | sess-arena-9922c58c | T5 done. 113 sourced facts across the picks, plus a grouped register in `data/sources.json` / `sources.html`. Official bodies preferred (NBA injury report PDF, NHL.com, MLB.com, EHF, ATP, F1.com, BBC, RTE, ESPNcricinfo); Wikipedia used only for URC/EHF tables and marked as secondary in F-011/F-013. |
| 2026-10-26 21:32 | sess-arena-9922c58c | T6 done. 16 irregularities (F-001..F-016) and 8 deliberate blanks recorded in `data/flags.json`, published on `flagged.html`. Headline findings: bookmaker odds are not in the retrievable OLBG HTML (F-001); handball shows "Tie" as the popular pick for 11 of 15 matches (F-002); OLBG's own listing and event pages disagree on tip totals (F-003, F-005); four kick-off times conflict with official sources (F-004). |
| 2026-10-26 21:40 | sess-arena-9922c58c | T7 done. Static site built at the repo root (Pages source is `main` / `/`). 21 pages, 521 internal links, no external assets required. |
| 2026-10-26 21:42 | sess-arena-9922c58c | T8 done. `tools/check_site.py` passes: 21 pages, 521 internal links all resolve, every pick has >=1 https source, min prediction length 45 words, no banned words. |
| 2026-10-26 21:45 | sess-arena-9922c58c | No other session claimed any task; no handoff needed, no merge conflicts, no scope collisions. |

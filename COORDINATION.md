# COORDINATION.md — shared task board

Last updated: 2026-10-26 (UTC). Session ID: `arena/45f3af51-olbg7`.

## Branch constraint

Arena ties this session to `arena/45f3af51-olbg7`. Per the session control plane, this branch cannot be renamed, switched, or pushed to another branch. Work therefore stays on this branch; a PR into `main` is used for integration. Other sessions may work on their own fixed branches.

## Coordination observation and conflict

The repository initially had only `README.md` and no `COORDINATION.md`. Six other remote session branches were observed (`4f7e3456`, `610d0099`, `726bf05d`, `94566809`, `bdfcd95b`, `e5298ae1`), and several independently claimed overlapping tasks before this branch was created. This is an unresolved ownership conflict; it is recorded here and on the site's Flagged for Review page. To avoid overwriting live work, this session does not edit those remote branches and keeps its branch-isolated file scope below. Its PR will expose any merge conflicts for review.

## Task board

| # | Task | Status | Owner session | File scope | Sources / verification / irregularities |
|---|---|---|---|---|---|
| T01 | Repo audit, OLBG structure reverse engineering, coordination | in progress | `arena/45f3af51-olbg7` | `COORDINATION.md`, `README.md`, `research/olbg-structure.md` | Repo had one commit and only `README.md`. OLBG sport IDs independently checked against OLBG sitemap and landing pages. Branch-claim conflict noted above. |
| T02 | Upcoming OLBG market inventory for 15 covered sports | unclaimed | — | `data/events.json`, `data/raw/` | OLBG category and event pages; every row must retain its OLBG event URL and event ID. |
| T03 | Originated lines for every catalogued event and market | unclaimed | — | `data/lines.json`, `tools/pricing.py`, `docs/methodology.html` | A transparent formula must use only observed OLBG tip counts; no unobserved bookmaker odds may be invented. |
| T04 | Official-source verification and field-level flags | unclaimed | — | `data/verification.json`, `docs/flagged.html` | Each row needs an official governing-body / league / organizer link; unconfirmed values remain blank and flagged. |
| T05 | 5–10 clearly labelled picks per sport with unique written analyses | unclaimed | — | `data/predictions.json`, `docs/sports/*.html` | High-confidence prose must be >=30 words and contain no unsupported claim. |
| T06 | Dashboard, executive summary, sport subpages, tables | unclaimed | — | `docs/`, `docs/assets/`, `tools/build_site.py` | Pure static Pages site; all internal links checked. |
| T07 | Final line-by-line validation, link/build check, PR, merge, Pages deploy | unclaimed | — | `scripts/validate.py`, `.github/workflows/pages.yml`, `COORDINATION.md` | PR link and merge/deploy result to be recorded here. |

## Verification policy

1. OLBG event links establish that a market exists on OLBG; they do not establish team form, injuries, or official fixture details.
2. Fixture identity and published statistics must be checked against an official governing body, league, tour, club, or event organizer where available.
3. If a field is not confirmed from an official source, it is blank and flagged `unverified`. No value is inferred.
4. Community tip shares are treated as ordinal evidence, not as bookmaker prices. Our own fair prices are computed with a documented, reproducible shrinkage formula.
5. Published prediction text must not use the internal words `model` or `verified`.
6. American odds `-250` to `+10000` correspond to decimal `1.40` to `101.00`; all released HIGH picks are checked against that interval.

## Change log

- 2026-10-26T20:31Z — audited empty repo and observed six parallel session branches. Created this board on the fixed session branch.
- 2026-10-26T20:31Z — claimed T01 with a branch-isolated scope and logged the overlapping-claim irregularity.

## Handoff / merge-conflict log

- No merge attempted in this session yet.

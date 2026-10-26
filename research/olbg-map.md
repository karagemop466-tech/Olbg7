# OLBG reverse-engineering map — snapshot 2026-10-26

How OLBG is organised (observed directly from live pages on 2026-10-26):

- **Sport hub URL:** `https://www.olbg.com/betting-tips/{Sport}/{sport_id}` — lists the most-tipped selection per upcoming event, with tip counts (`n/m Win Tips`), consensus % and a Value Rating (tips % vs. odds-implied chance).
- **Event URL:** `https://www.olbg.com/betting-tips/{Sport}/{Category}/{Competition}/{Match_slug}/{sport_id}?event_id={id}` — shows every tipped market for that event (e.g. tennis: Win Match, Set Betting, 1st Set Winner, Games Won handicap, Total Games), tipster comments and records. Numeric bookmaker prices are loaded dynamically and did **not** render in fetched HTML (`WIN @` with no price), so no OLBG price in this project is copied — our own fair price is originated instead, and market lines are shown only where an independent source (e.g. ESPN scoreboard) published them.
- **Tipster pages:** `https://www.olbg.com/best-tipsters/{Sport}/{sport_id}`.

## In-scope sport hubs (15 brief sports = 16 OLBG hubs; Gaelic Sports splits in two)

| Brief sport | OLBG hub | ID | Markets seen on hub/event pages (snapshot) |
|---|---|---:|---|
| Golf | /betting-tips/Golf/5 | 5 | Win Tournament, First Round Leader, Top American/European/GB&I |
| Volleyball | /betting-tips/Volleyball/21 | 21 | Win Match (+ set/total markets on event pages) |
| Rugby Union | /betting-tips/Rugby_Union/9 | 9 | To Win, Handicap, Win Tournament |
| Cricket | /betting-tips/Cricket/7 | 7 | Win Match, Top Batsman, Man of the Match, Outright Winner |
| Snooker | /betting-tips/Snooker/8 | 8 | Win Match, Handicap Betting, Frame Betting, Win Tournament — **hub showed "No tips found" at snapshot** (between NI Open and International Championship) |
| Darts | /betting-tips/Darts/15 | 15 | Win Tournament (+ match markets during TV events) — only outrights live at snapshot |
| Baseball | /betting-tips/Baseball/12 | 12 | Money Line, Run Line, Game Totals, Ante-post — only World Series live at snapshot |
| Gaelic Sports (Football) | /betting-tips/Gaelic_Football/25 | 25 | Match winner / handicap (points start), outright |
| Gaelic Sports (Hurling) | /betting-tips/Hurling/26 | 26 | Match Winner, Handicap/Points Start, Total Points, Outright — only 2027 outright live at snapshot |
| Greyhounds | /betting-tips/Greyhounds/28 | 28 | Daily Races (win) per race |
| Tennis | /betting-tips/Tennis/3 | 3 | Win Match, Set Betting, 1st Set Winner, Games Won, Total Games, Tournament Winner |
| Motor Racing | /betting-tips/Motor_Racing/14 | 14 | Fastest Qualifier, Win Race, Podium Finish, Top 6 Finish, Points Finish, Fastest Lap, Win Tournament |
| Handball | /betting-tips/Handball/20 | 20 | Money Line (3-way incl. Tie), Match handicap, Points total |
| Ice Hockey | /betting-tips/Ice_Hockey/13 | 13 | Money Line, Puck Line, Game Totals |
| Basketball | /betting-tips/Basketball/4 | 4 | Money Line, Pointspread, Game Totals |
| Rugby League | /betting-tips/Rugby_League/10 | 10 | Match betting, Handicap, Grand Final Winner / Win Tournament — only outrights live at snapshot; World Cup match markets covered by OLBG's RLWC guide |

## Snapshot coverage notes (feed the Flagged for Review page)

1. **Handball "Tie" pile-on:** the most-tipped selection on almost every EHF Champions League match was the Tie — implausible as a genuine consensus (OLBG's own stats put ties at ~7–10%). Treated as tipster-competition noise; our prices ignore it.
2. **Volleyball underdog skew:** OLBG crowds favoured Montes Claros over champions Sada Cruzeiro and Vallefoglia over Conegliano. Our ratings disagree; flagged, not followed.
3. **Empty/thin hubs:** Snooker (none), Darts / Rugby League / Hurling (outrights only), Baseball (one game), Golf (three outrights). Picks in those sports use the official governing-body schedules for the same OLBG-covered events and are flagged accordingly.
4. **Greyhound races expire within hours** (one race already showed "Expired"). Greyhound picks are a dated snapshot plus a reusable race-pricing method.

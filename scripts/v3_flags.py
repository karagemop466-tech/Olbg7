#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3 flags - everything irregular found while sweeping OLBG on 2026-10-27.

Every item here is published on the Flagged for Review page with its sources.
None of them blocks the board: "needs review" means published here, not held
back. Where a value could not be confirmed it is left blank on the board and
recorded here rather than inferred.

Severity
    HIGH    a published OLBG figure contradicts an official source, or a whole
            sport prints no data at all
    MEDIUM  OLBG's display omits or mislabels something a punter would need, or
            our own two tracks disagree on a price
    LOW     a limitation of our own work that a reader should know about
"""
import json, os, sys

FLAGS = []


def add(sev, sport, title, detail, sources, effect=""):
    FLAGS.append({"id": "F%02d" % (len(FLAGS) + 1), "severity": sev, "sport": sport,
                  "title": title, "detail": detail, "board_effect": effect,
                  "sources": [{"label": a, "url": b} for a, b in sources]})


# ---- 1. whole sports printing nothing ---------------------------------------
add("HIGH", "Greyhounds",
    "Greyhounds dropped from 8 events to 0 overnight",
    "The OLBG Greyhounds board carried 8 tip-able events on 26 October 2026 and 0 on "
    "27 October. Both the root board and the All_Events listing print the literal "
    "string 'No tips found.' We swept the page twice and confirmed the empty state is "
    "what OLBG serves, not a retrieval failure.",
    [("OLBG Greyhounds tips board", "https://www.olbg.com/betting-tips/Greyhounds/19")],
    "No Greyhounds picks are published. We do not pad an empty board with invented "
    "races.")

add("HIGH", "Snooker",
    "Snooker board empty on both the root listing and All_Events",
    "OLBG's Snooker board prints 'No tips found.' on both the sport root and the "
    "All_Events listing on 27 October 2026. The sport is one of the fifteen in scope "
    "and there is no fixture and no tip data to work from on either page.",
    [("OLBG Snooker tips board", "https://www.olbg.com/betting-tips/Snooker/8")],
    "No Snooker picks are published.")

# ---- 2. tip flow against the official record --------------------------------
add("HIGH", "Volleyball",
    "Conegliano v Vallefoglia: 6 of 10 tips on the side that has dropped no sets",
    "OLBG tips Vallefoglia 6 of 10 on the round-5 make-up fixture at the Palaverde. "
    "Conegliano are 4-0 in Serie A1 with 12 sets won and 0 lost (3-0 v Cuneo 4 Oct, "
    "3-0 v Busto Arsizio 10 Oct, 3-0 at Chieri 14 Oct taking the sets 25-19 25-14 "
    "25-22, 3-0 v Talmassons 18 Oct) and won a ninth Supercoppa Italiana in Bari on "
    "Saturday 24 October, beating Scandicci in the final. Vallefoglia are also 4-0 but "
    "on 11 points, having needed five sets at Scandicci on 10 October.",
    [("LegaVolley Femminile - Serie A1 results", "https://www.legavolleyfemminile.it/risultati/"),
     ("Vallefoglia v Conegliano, Palaverde, 28 October 20:00",
      "https://www.volleynews.it/vallefoglia-si-prepara-a-una-sfida-di-alta-quota-con-conegliano/"),
     ("Conegliano 2026-27 fixture list and results",
      "https://www.dazn.com/it-IT/news/volley/conegliano-volley-calendario-rosa-e-dove-vedere-le-partite/1w3ms5p4jzo7a1vkuwale2k35d"),
     ("OLBG volleyball tips board", "https://www.olbg.com/betting-tips/Volleyball/21")],
    "We publish our own line, Conegliano -209 / Vallefoglia +209, and say in the prose "
    "that it is against the OLBG tip flow.")

add("HIGH", "Volleyball",
    "Fenerbahce v Alanya Bld: 2 of 3 tips on the away side",
    "OLBG tips Alanya Belediyespor 2 of 3 on a Turkish fixture whose competition "
    "standing we could not confirm from an official source, so there is nothing "
    "independent to test the tip flow against.",
    [("OLBG volleyball tips board", "https://www.olbg.com/betting-tips/Volleyball/21")],
    "Row published with the tip share only; no line originated.")

add("HIGH", "Tennis",
    "Khachanov v Alcaraz: 2 of 2 tips against the world No. 3",
    "OLBG's most-tipped selection for the ATP Vienna round of 32 is Karen Khachanov on "
    "2 of 2 tips, against Carlos Alcaraz - world No. 3 on 5,610 ranking points, seeded "
    "second in a EUR 2,797,985 ATP 500, and seeking a fourth tour-level title of 2026. "
    "Khachanov is No. 25 on 1,990 points and a recent US Open semi-finalist, so he is "
    "not a soft opponent, but the tip flow has no support in the official ranking.",
    [("ATP Tour - official singles rankings", "https://www.atptour.com/en/rankings/singles"),
     ("ATP Tour - Basel and Vienna 2026 scouting report",
      "https://www.atptour.com/en/news/basel-vienna-2026-scouting-report"),
     ("OLBG tennis tips board", "https://www.olbg.com/betting-tips/Tennis/15")],
    "We publish Alcaraz -282 / Khachanov +282 from the official points ratio and grade "
    "the pick MEDIUM because the price falls outside the band.")

add("HIGH", "Basketball",
    "Three EuroLeague rows tipped against the official league table",
    "Besiktas v Olympiacos (event 536180), Bayern Munich v Barcelona (event 536174) and "
    "Baskonia v Real Madrid all carry OLBG tip flows that favour the weaker club on the "
    "official table. Bayern Munich are 2-5 with 612 for and 659 against, having lost "
    "91-107 at home to Dubai; Barcelona are 4-3 with +17. Kosner Baskonia are 20th of 20 "
    "on 1 win from 7, 583 for and 649 against; Real Madrid are 4-3 with +37 and on a "
    "four-game winning streak.",
    [("L'Equipe - official EuroLeague standings", "https://www.lequipe.fr/Basket/CLA_EUH.html"),
     ("EuroLeague media centre - round 7 official standings",
      "https://mediacentre.euroleague.net/uploads/EuroleagueCore/pastmatchups/game19234.pdf"),
     ("OLBG basketball tips board", "https://www.olbg.com/betting-tips/Basketball/3")],
    "For Barcelona v Bayern and Real Madrid v Baskonia we publish our own line against "
    "the tips and say so in the prose.")

add("HIGH", "Cricket",
    "Central Stags tipped against at home as defending champions",
    "OLBG tips Northern Districts 2 of 3 for Central Stags v Northern Districts in round "
    "1 of the Ford Trophy, although Central Stags are the defending champions, won the "
    "2025-26 Grand Final by six wickets, and are at home at Saxton Oval.",
    [("New Zealand Cricket - official Ford Trophy schedule",
      "https://www.nzc.nz/media/w40g2zm4/print_2026_ford-trophy-schedule.pdf"),
     ("Canterbury Cricket - Canterbury Kings", "https://www.canterburycricket.org.nz/teams/canterbury-kings/")],
    "Published as a flagged row; no pick taken on it.")

# ---- 3. display defects ----------------------------------------------------
add("HIGH", "Handball",
    "'Tie' printed as the most-tipped Money Line selection on 11 of 15 matches",
    "OLBG's Handball listing prints the literal string 'Tie' as the most-tipped Money "
    "Line selection on eleven of the fifteen listed events, including SC Magdeburg v HC "
    "Kriens-Luzern at 9 of 14, where the official EHF Champions League group F table has "
    "Magdeburg 5-0-0 with +36 and Kriens-Luzern 2-0-3 with -3. A draw is a legal "
    "group-phase result - the official tables record two draws across the thirty "
    "group-phase games played in groups A, C and F - but it cannot be backed on a money "
    "line, so the selection is unusable as a match-winner tip.",
    [("EHF Champions League - official standings", "https://ehfcl.eurohandball.com/men/2026-27/standings/"),
     ("EHF - three main round spots still open before round 6",
      "https://ehfcl.eurohandball.com/news/en/three-main-round-spots-still-open-before-final-round-6/"),
     ("OLBG handball tips board", "https://www.olbg.com/betting-tips/Handball/20")],
    "All fifteen handball rows are priced from the official EHF group tables instead. "
    "Six rows are left blank: HC Vardar v MT Melsungen, Wisla Plock v Nantes, RK Celje v "
    "RK Zagreb, GOG v Sporting CP, Montpellier v Dinamo Bucuresti and IFK Kristianstad v "
    "Pick Szeged, none of which appear in the official Champions League group tables.")

add("HIGH", "Gaelic Sports",
    "Handicap selections printed with no market label",
    "OLBG's Gaelic rows print handicap selections inline - 'Eire Og Cor +0.50', "
    "'Kildimo Pallaskenry +3.50' - with no market name attached to the row, so a reader "
    "cannot tell from the page whether the number is a match-winner price or a handicap. "
    "The same defect appears on the Rugby Union board: 'Connacht +3.50', 'Ulster +12.50', "
    "'Munster -6.50'.",
    [("OLBG gaelic football tips board", "https://www.olbg.com/betting-tips/Gaelic_Football/25"),
     ("OLBG rugby union tips board", "https://www.olbg.com/betting-tips/Rugby_Union/9")],
    "Every affected row is labelled with the market we believe it belongs to, and the "
    "label is stated as our own reading rather than OLBG's.")

add("MEDIUM", "Gaelic Sports",
    "'Kanturk v Eire Og Cor' cannot be identified",
    "No competition or fixture pairing Kanturk with any club matching 'Eire Og Cor' could "
    "be confirmed from an official source. Munster GAA's published 2026 club championship "
    "draw names Eire Og Inis of Clare and pairs them with The Nire or Rathgormack of "
    "Waterford in the quarter-final on 8 November, not with Kanturk. Kanturk beat "
    "Kilshannig 2-16 to 0-19 in the Cork Senior A quarter-final on 27 September at Fr "
    "Kelleher Park and does not appear in the provincial draw at all.",
    [("Munster GAA - official club championship draw 2026",
      "https://munster.gaa.ie/fixtures/club-championships-2026/"),
     ("2026 Cork Senior A Football Championship",
      "https://en.wikipedia.org/wiki/2026_Cork_Senior_A_Football_Championship"),
     ("Full list of 2026 county champions",
      "https://www.sportsnewsireland.com/gaa/full-list-of-senior-football-and-hurling-county-champions-2026")],
    "Competition and venue left blank. The pick is graded LOW despite 6 of 6 tips.")

add("MEDIUM", "Ice Hockey",
    "Swiss NLA rows carry only a Puck Line tip",
    "The Ice Hockey Swiss National League rows on OLBG carry only a 1/1 Puck Line tip and "
    "no money line at all, so there is no winner market to price from the tip flow.",
    [("OLBG ice hockey tips board", "https://www.olbg.com/betting-tips/Ice_Hockey/18")],
    "Those rows are priced from official league tables where a table exists, otherwise "
    "left blank.")

add("MEDIUM", "Ice Hockey",
    "BOS @ CAR and CBJ @ PHI print no Money Line split",
    "Two NHL games on the OLBG board publish no Money Line tip split. Boston at Carolina "
    "carries only a 1/1 Puck Line; Columbus at Philadelphia carries a 2/3 tip on the "
    "Flyers with no corresponding money line split for the visitors.",
    [("NHL - official standings", "https://www.nhl.com/standings"),
     ("OLBG ice hockey tips board", "https://www.olbg.com/betting-tips/Ice_Hockey/18")],
    "Both rows are priced from the official NHL standings. For Columbus at Philadelphia "
    "our line favours Columbus -106 while OLBG tips Philadelphia, and we publish both.")

add("MEDIUM", "Rugby League",
    "Rugby League, Darts and Hurling boards are outright-only",
    "OLBG's Rugby League board publishes only three 2027 outrights - State of Origin, "
    "Super League and NRL - with no club-versus-club fixture anywhere on it. The Darts "
    "board publishes only the World Championship and Players Championship 31. The "
    "Hurling board publishes a single market, 'Win Hurling'.",
    [("OLBG rugby league tips board", "https://www.olbg.com/betting-tips/Rugby_League/10"),
     ("OLBG darts tips board", "https://www.olbg.com/betting-tips/Darts/30"),
     ("OLBG gaelic football tips board", "https://www.olbg.com/betting-tips/Gaelic_Football/25")],
    "Five picks are still published for each of those sports, drawn from the markets "
    "OLBG actually carries rather than from fixtures it does not.")

add("MEDIUM", "Darts",
    "Listing page and event page disagree on the most popular Players Championship 31 selection",
    "OLBG's Darts listing page names Nathan Aspinall as the most popular selection for "
    "Players Championship 31; the event page (event 32446) names Wessel Nijman. Both "
    "print at 2 of 8 tips, in a four-way tie with Kevin Doets and 'Other'.",
    [("OLBG Players Championship 31 event page",
      "https://www.olbg.com/betting-tips/Darts/30?event_id=32446"),
     ("OLBG darts tips board", "https://www.olbg.com/betting-tips/Darts/30")],
    "Both players are published as separate picks with their own prose.")

# ---- 4. time conflicts ------------------------------------------------------
add("MEDIUM", "Baseball",
    "Brewers @ Rays start time conflicts with MLB.com",
    "OLBG prints 'Today 21:00' for World Series Game 4. MLB.com's official schedule and "
    "FOX's broadcast listing both print 8:00 p.m. ET on Tuesday 27 October at Tropicana "
    "Field. The OLBG clock is US Eastern, confirmed on four other fixtures the same day, "
    "so 21:00 is not explained by the offset.",
    [("MLB.com - 2026 playoff and World Series schedule",
      "https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule"),
     ("MLB.com - 2026 World Series FAQ",
      "https://www.mlb.com/news/2026-mlb-world-series-faq-schedule-times-teams-and-more")],
    "We publish the official 8:00 p.m. ET start and note the OLBG figure.")

add("MEDIUM", "Cricket",
    "Afghanistan v Zimbabwe start time conflicts with ESPNcricinfo",
    "OLBG prints 10:30 for the 1st T20I at Sharjah Cricket Stadium; ESPNcricinfo prints "
    "2:30 PM ET for the same fixture. The difference is not the four-hour Eastern offset.",
    [("ESPNcricinfo - Afghanistan v Zimbabwe fixtures",
      "https://www.cricinfo.com/series/afghanistan-v-zimbabwe-2026-27-1555105/match-schedule-fixtures-and-results")],
    "Time left as OLBG prints it, with the conflict noted.")

add("MEDIUM", "Cricket",
    "South Africa v Australia 3rd Test date conflicts with the official start",
    "OLBG prints 31 Oct 04:30 ET for the third Test at Newlands. The official start is "
    "10:30 local on Tuesday 27 October, running to 31 October. OLBG appears to be "
    "printing the scheduled end of play rather than the start.",
    [("Cricket Australia - third Test preview", "https://www.cricket.com.au/news/4597818"),
     ("ESPNcricinfo - Australia in South Africa 2026-27",
      "https://www.cricinfo.com/series/australia-in-south-africa-2026-27-1525634"),
     ("Sky Sports - third Test live centre",
      "https://www.skysports.com/cricket/australia-vs-south-africa-3rd-test-2026/live/13603987")],
    "Published with the official five-day window, not OLBG's single timestamp.")

add("MEDIUM", "Cricket",
    "Ford Trophy round 1 prints a day earlier than the official fixture",
    "OLBG prints Auckland v Canterbury as 'Today 17:30'. The official New Zealand Cricket "
    "schedule has the match on Wednesday 28 October with a 10:00am NZT toss at Kennards "
    "Hire Community Oval. 10:30am NZT on 28 October is 5:30pm EDT on 27 October, so the "
    "two agree once the Eastern clock is applied - but the printed date is the day before "
    "the match.",
    [("New Zealand Cricket - official Ford Trophy schedule",
      "https://www.nzc.nz/media/w40g2zm4/print_2026_ford-trophy-schedule.pdf"),
     ("Auckland Cricket - 2026/27 50-over schedules",
      "https://www.aucklandcricket.co.nz/newsarticle/169108")],
    "Published with the official NZT date and time.")

# ---- 5. data conflicts ------------------------------------------------------
add("MEDIUM", "Ice Hockey",
    "Conflicting NHL records for Columbus and Philadelphia",
    "A FOX Sports game page prints Columbus 4-5-0 and Philadelphia 3-7-3; an ESPN game "
    "page prints Columbus 3-5-0 and Philadelphia 3-6-3. Resolved in favour of the former: "
    "NHL.com, BBC Sport, hockey-reference and Wikipedia all print Columbus 4-5-0 on 8 "
    "points and Philadelphia 3-7-3 on 9 points. The stale ESPN snapshot is the outlier.",
    [("NHL - official standings", "https://www.nhl.com/standings"),
     ("BBC Sport - NHL standings updated 26 October 2026", "https://www.bbc.co.uk/sport/ice-hockey/tables"),
     ("FOX Sports - NHL divisional standings", "https://www.foxsports.com/nhl/standings?type=division")],
    "4-5-0 and 3-7-3 used throughout, with the conflicting figures noted here.")

add("MEDIUM", "Basketball",
    "Prior-session rows: Dallas @ Miami point spread and two comment errors",
    "Carried forward from the earlier board sweep. OLBG prints the Dallas @ Miami market "
    "at +7.50 while a tipster comment on the same row discusses +8.50. A separate comment "
    "credits Miami with Giannis Antetokounmpo, who plays for Milwaukee. A third calls the "
    "Kings 0-3-2 on the road where NHL.com shows 2-2-2.",
    [("NHL - official standings", "https://www.nhl.com/standings"),
     ("OLBG basketball tips board", "https://www.olbg.com/betting-tips/Basketball/3")],
    "Comments are not used as evidence anywhere on this board.")

add("LOW", "Gaelic Sports",
    "Mayo's 2026 All-Ireland title is single-sourced to OLBG",
    "OLBG's own Gaelic football editorial states that the reigning All-Ireland senior "
    "football champions are Mayo, who ended a 75-year wait in 2026 by beating Kerry in "
    "the final for their fourth title, and that Kerry hold 39 all-time titles against "
    "Dublin's 31. No independent official source for the Mayo result was found. It is "
    "consistent with Kerry winning Munster in May 2026 and then losing the All-Ireland "
    "final, which is separately sourced.",
    [("OLBG gaelic football tips board and editorial",
      "https://www.olbg.com/betting-tips/Gaelic_Football/25"),
     ("2026 Munster Senior Football Championship",
      "https://en.wikipedia.org/wiki/2026_Munster_Senior_Football_Championship")],
    "Used in the Kerry pick prose with the single-source status stated in the row.")

# ---- 6. OLBG filing errors --------------------------------------------------
add("MEDIUM", "Golf",
    "Maybank Championship filed under the DP World Tour although it is an LPGA event",
    "OLBG's golf board files the Maybank Championship under DP World Tour. It is an LPGA "
    "Tour event: 29 October to 1 November 2026 at the Kuala Lumpur Golf & Country Club "
    "West Course, a $3,000,000 purse with $450,000 to the winner, 72-hole limited-field "
    "no-cut stroke play at par 72 over 6,246 yards. Defending champion Miyu Yamashita won "
    "in 2025 in a three-way playoff.",
    [("LPGA - Maybank Championship overview", "https://www.lpga.com/tournaments/maybank-championship/overview"),
     ("LPGA - Maybank Championship results", "https://www.lpga.com/tournaments/maybank-championship/results")],
    "Our `data/v3/events.json` records the competition as LPGA Tour, not DP World Tour.")

add("LOW", "Handball",
    "Fuchse Berlin v RK Partizan filed under the EHF European League",
    "OLBG files this fixture under the EHF European League, although both clubs appear in "
    "the official EHF Champions League group A table - Fuchse Berlin second on 6 points "
    "with +12, RK Partizan fourth on 1 point with -36.",
    [("EHF Champions League - official group A table",
      "https://ehfcl.eurohandball.com/men/2026-27/standings/"),
     ("2026-27 EHF Champions League group stage",
      "https://en.wikipedia.org/wiki/2026%E2%80%9327_EHF_Champions_League_group_stage")],
    "Priced from the Champions League group table; the OLBG label is not followed.")

# ---- 7. limitations of our own work -----------------------------------------
add("LOW", "Baseball",
    "Only one baseball event is published anywhere on OLBG",
    "The OLBG baseball board carries a single tip-able event on 27 October 2026 - World "
    "Series Game 4 - with three markets. Five picks are published for the sport by "
    "covering all three markets plus two lines we originated from the official game "
    "scores, rather than by inventing fixtures.",
    [("OLBG baseball tips board", "https://www.olbg.com/betting-tips/Baseball/MLB/MLB/2"),
     ("MLB.com - 2026 playoff and World Series schedule",
      "https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule")],
    "The three-game sample is stated in the prose of every baseball pick.")

add("LOW", "Motor Racing",
    "Piastri and Hadjar excluded from the 'without Antonelli' price",
    "Our weighting of the Drivers' Championship 'without Kimi Antonelli' market prices "
    "only contenders within two race wins - 50 points - of the best-placed eligible rival. "
    "Oscar Piastri on 144 points and Isack Hadjar on 105 are more than 120 points behind "
    "George Russell on 242 with 125 points still available, so an earlier attempt to price "
    "them produced a nonsense number of +2479913 for Piastri. Both are excluded.",
    [("Formula One - official 2026 Drivers' Standings",
      "https://www.formula1.com/en/results/2026/drivers"),
     ("BBC Sport - 2026 Formula 1 standings", "https://www.bbc.com/sport/formula1/standings")],
    "The exclusion is stated on the Motor Racing page and in the Russell pick prose.")

add("LOW", "Golf",
    "Ninety-nine unranked entrants carry a stated notional ranking of 150",
    "The Mexico Open field is 120 players, reduced from the usual 132 because of autumn "
    "daylight. Only 21 of them appear in the official world-ranking list we could source. "
    "The remaining 99 are given a notional ranking of 150 so that the weights normalise "
    "over the whole confirmed field. That figure is an assumption we state, not an official "
    "ranking.",
    [("PGA TOUR - VidantaWorld Mexico Open overview",
      "https://www.pgatour.com/tournaments/2026/vidantaworld-mexico-open/R2026540/overview"),
     ("Mexico Open field and world rankings, 25 October 2026",
      "https://thegolfnewsnet.com/golfnewsnetteam/2026-10-25/2026-vidantaworld-mexico-open-field-pga-tour-players-rankings-145293/")],
    "Stated on the Golf page and inside the method write-up.")

add("LOW", "Golf",
    "Simmons Bank Championship venue, dates and field unconfirmed",
    "The Simmons Bank Championship is a PGA TOUR Champions event. Its venue, dates and "
    "field could not be confirmed from an official source on this date, so all three are "
    "left blank and no price is originated for the Stewart Cink runner that carries one of "
    "the two OLBG tips.",
    [("PGA TOUR Champions - schedule", "https://www.pgatour.com/champions/schedule"),
     ("Golf this week, 26 October - 1 November 2026",
      "https://golfblogger.com/golf-this-week-october-26-november-1-2026/")],
    "Blank price, graded LOW.")

add("LOW", "Rugby League",
    "2027 outright field sizes not confirmed",
    "The runner counts used for the Super League 2027, NRL 2027 and All-Ireland Senior "
    "Hurling 2027 outrights are carried over from the 2026 seasons and are not confirmed "
    "for 2027. The All-Ireland Senior Football Championship 2027 count of 33 counties is "
    "also a carry-over and is used for the Kerry price of +126.",
    [("2026 NRL season", "https://en.wikipedia.org/wiki/2026_NRL_season"),
     ("2026 Super League Grand Final", "https://en.wikipedia.org/wiki/2026_Super_League_Grand_Final"),
     ("OLBG rugby league tips board", "https://www.olbg.com/betting-tips/Rugby_League/10")],
    "Super League and Hurling prices left blank. The 33-county assumption is labelled as "
    "an assumption wherever it is used.")

add("LOW", "Rugby Union",
    "Six events with no priced line",
    "Six of the 115 swept markets carry no line at all: Virtus Bologna v Zalgiris (0 of 0 "
    "tips), Cricket World Cup 2027, Maybank Championship, Simmons Bank Championship, "
    "All-Ireland Senior Hurling 2027 and Super League 2027 - every one of them for want of "
    "a confirmed field size. Oyonnax v Soyaux Angouleme also blanks, because the opponent's "
    "official points difference is unpublished.",
    [("OLBG rugby union tips board", "https://www.olbg.com/betting-tips/Rugby_Union/9"),
     ("OLBG basketball tips board", "https://www.olbg.com/betting-tips/Basketball/3")],
    "Left blank and listed here rather than filled in.")

add("LOW", "All sports",
    "No bookmaker price appears anywhere on this board",
    "OLBG renders bookmaker prices client-side, so they are absent from the HTML we can "
    "retrieve. Every number published as a price on this board is originated by us, either "
    "from the tip share OLBG prints (Track T) or from an official competition table, "
    "ranking or points record (Track R). Nothing is quoted as a bookmaker's number.",
    [("OLBG event page, World Series Game 4",
      "https://www.olbg.com/betting-tips/Baseball/MLB/MLB/MIL_Brewers_@_TB_Rays/12?event_id=160799")],
    "Stated in the header of every page and on the method page.")

add("MEDIUM", "Ice Hockey",
    "Malmo Redhawks v Linkoping: our two tracks disagree on the price",
    "The official SHL table gives Malmo Redhawks -276 while the OLBG tip flow of 3 of 3 "
    "gives -200. Both point the same way but the numbers differ by more than a fifth, and "
    "a three-tip sample carries very little weight on its own.",
    [("EliteProspects - SHL 2026-27 standings and games", "https://www.eliteprospects.com/league/shl"),
     ("tabellen.se - SHL table updated 24 October 2026", "https://tabellen.se/hockey/shl")],
    "Both numbers are printed on the row; the pick is graded MEDIUM.")


def main():
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    FLAGS.sort(key=lambda f: (order[f["severity"]], f["sport"], f["id"]))
    for i, f in enumerate(FLAGS, 1):
        f["id"] = "F%02d" % i
    out = {
        "generated": "2026-10-27",
        "note": ("Published on the Flagged for Review page. 'Needs review' means published "
                 "here; it does not block any pick, any line or the site build."),
        "counts": {
            "total": len(FLAGS),
            "HIGH": sum(1 for f in FLAGS if f["severity"] == "HIGH"),
            "MEDIUM": sum(1 for f in FLAGS if f["severity"] == "MEDIUM"),
            "LOW": sum(1 for f in FLAGS if f["severity"] == "LOW"),
            "sports": sorted({f["sport"] for f in FLAGS}),
        },
        "flags": FLAGS,
    }
    dest = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "v3", "flags.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)

    errs = []
    for f in FLAGS:
        if not f["sources"]:
            errs.append(f["id"] + " has no source")
        for src in f["sources"]:
            if not src["url"].startswith("http"):
                errs.append("%s bad url %r" % (f["id"], src["url"]))
        if len(f["detail"].split()) < 25:
            errs.append(f["id"] + " detail is only %d words" % len(f["detail"].split()))
    print("flags: %d  HIGH %d  MEDIUM %d  LOW %d  across %d sports"
          % (out["counts"]["total"], out["counts"]["HIGH"], out["counts"]["MEDIUM"],
             out["counts"]["LOW"], len(out["counts"]["sports"])))
    if errs:
        for e in errs:
            print("  x " + e)
        return 1
    print("all flags carry sources -> " + os.path.relpath(dest, os.path.dirname(os.path.dirname(dest))))
    return 0


if __name__ == "__main__":
    sys.exit(main())

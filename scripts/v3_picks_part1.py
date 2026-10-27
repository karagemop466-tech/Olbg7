#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3 picks - the written slate for 2026-10-27.

Five written predictions for every sport OLBG currently lists tips for. Snooker
and Greyhounds get none because OLBG publishes no tips or events for either on
this date; that is reported on the Flagged for Review page rather than padded
out with invented fixtures.

Every factual claim in every prediction carries an official source. Prices are
our own origination - OLBG does not expose bookmaker odds in retrievable HTML,
so nothing on this board is a bookmaker price. See scripts/v3_pricing.py for
the two tracks used to originate them.

The two words "model" and "verified" never appear in prediction prose.
"""
import json, os

BAND = (-250, 10000)
PICKS = []


def add(**kw):
    PICKS.append(kw)


# =============================================================================
# CRICKET
# =============================================================================
add(sport="Cricket", event="New Zealand v India",
    competition="India tour of New Zealand 2026-27, 3rd T20I",
    when="Tuesday 27 October 2026, 7:00am UTC", venue="Hnry Stadium, Wellington",
    market="Win Match", selection="India to win the match",
    line="-224", probability=0.691, track="T", tier="A", confidence="HIGH",
    in_band=True, olbg="35 of 49 tips (71%), 18 tipster comments",
    text=("India travel to Wellington holding a 2-0 lead in this five-match T20I series and "
          "needing one more win to take it with two games still to spare. They levelled the "
          "Christchurch double-header by four wickets on 24 October after the opening match at "
          "Hagley Oval, and the third T20I at Hnry Stadium is the last of three straight "
          "meetings before the tour moves to Eden Park on 30 October and Seddon Park on 1 "
          "November. New Zealand have lost both completed matches and have not been able to "
          "defend a total against India in this series. Thirty-five of the 49 tips posted on "
          "OLBG sit with the visitors, the deepest consensus anywhere on the cricket board, and "
          "we back India on the match-winner line."),
    sources=[("BCCI official match centre - New Zealand v India, 3rd T20I",
              "https://www.bcci.tv/matches/242110/new-zealand-vs-india/match-details"),
             ("ESPNcricinfo - T20I no. 4221, Hnry Stadium",
              "https://www.cricinfo.com/series/india-in-new-zealand-2026-27-1539421/new-zealand-vs-india-3rd-t20i-1539434/live-cricket-score"),
             ("India tour of New Zealand 2026 - schedule and results",
              "https://indianexpress.com/article/sports/cricket/india-vs-new-zealand-2026-schedule-timings-live-streaming-10929192/"),
             ("OLBG cricket tips board", "https://www.olbg.com/betting-tips/Cricket/7")],
    flag=None)

add(sport="Cricket", event="Namibia v Ireland",
    competition="Ireland tour of Namibia 2026-27, 3rd ODI",
    when="Tuesday 27 October 2026", venue="High Performance Oval, Windhoek",
    market="Win Match", selection="Ireland to win the match",
    line="-192", probability=0.658, track="T", tier="A", confidence="HIGH",
    in_band=True, olbg="22 of 32 tips (69%), 6 tipster comments",
    text=("This five-match series is level at one apiece and the third ODI decides who carries "
          "the lead into the back end of the tour. Ireland took the opener by 55 runs, bowling "
          "Namibia out for 174 in 37.5 overs after Harry Stirling's 56 from 71 balls and Josh "
          "Hoey's 3-29. Namibia hit back two days later with a 31-run win built on Gerhard "
          "Erasmus carrying his bat for an unbeaten 156 from 125 deliveries, a personal best "
          "that beat his previous 125, and Jan Frylinck's 76 from 90. Ireland's chase stalled at "
          "290 in 47.3 overs despite Stirling's 77 from 71 and Hoey's second three-wicket haul "
          "of the series. Stirling has made 56 and 77 in the two completed games, so the Irish "
          "top order is in form even in defeat, and 22 of the 32 tips stay with them."),
    sources=[("ESPNcricinfo - ODI no. 5049, High Performance Oval, Windhoek",
              "https://www.cricinfo.com/series/ireland-in-namibia-2026-27-1558225/namibia-vs-ireland-3rd-odi-1558233/live-cricket-score"),
             ("BBC Sport - Ireland win the 1st ODI by 55 runs",
              "https://www.bbc.co.uk/sport/cricket/articles/cxnv0e69ezrzo"),
             ("BBC Sport - Erasmus 156 not out, Namibia level the series",
              "https://www.bbc.co.uk/sport/cricket/articles/cvx28ex38x7ko")],
    flag=None)

add(sport="Cricket", event="Pakistan v Sri Lanka",
    competition="Pakistan ODI Tri-Series 2026-27, 5th match",
    when="Tuesday 27 October 2026, 1:00pm local (8:00am GMT)",
    venue="Gaddafi Stadium, Lahore",
    market="Win Match", selection="Pakistan to win the match",
    line="-208", probability=0.676, track="T", tier="A", confidence="HIGH",
    in_band=True, olbg="22 of 31 tips (71%)",
    text=("Pakistan are three wins from three in this tri-series and have already beaten Sri "
          "Lanka inside it. In the Rawalpindi opener on 18 October they posted 305 and won by 37 "
          "runs, Salman Agha making 107 from 90 balls for his fourth ODI hundred while Shaheen "
          "Shah Afridi took 3-55 to bowl Sri Lanka out for 268 in 48.1 overs. Sri Lanka's only "
          "win of the tournament came against England by two wickets on 22 October. Pakistan then "
          "beat England by 87 runs and, at this same ground on 25 October, chased 242 to win by "
          "one wicket with 17 balls remaining. A side winning that close a game at home is not "
          "one to fade, and 22 of the 31 tips are with the hosts."),
    sources=[("Wikipedia - 2026-27 Pakistan ODI Tri-Series",
              "https://en.wikipedia.org/wiki/2026%E2%80%9327_Pakistan_ODI_Tri-Series"),
             ("ESPNcricinfo - Pakistan v Sri Lanka, 1st match report",
              "https://www.cricinfo.com/series/pakistan-odi-tri-series-2026-27-1550706/pakistan-vs-sri-lanka-1st-match-1550713/match-report"),
             ("ESPNcricinfo - Pakistan fixtures and results",
              "https://www.cricinfo.com/team/pakistan-7/match-schedule-fixtures-and-results"),
             ("CricketWorld - tri-series results and fixtures",
              "https://www.cricketworld.com/match-predictions-pakistan-odi-tri-series-2026-5th-match-pakistan-vs-sri-lanka-october-27th/114027.htm")],
    flag=None)

add(sport="Cricket", event="Afghanistan v Zimbabwe",
    competition="Afghanistan v Zimbabwe 2026-27, 1st T20I",
    when="Tuesday 27 October 2026", venue="Sharjah Cricket Stadium, Sharjah",
    market="Win Match", selection="Afghanistan to win the match",
    line="-450", probability=0.818, track="T", tier="A", confidence="MEDIUM",
    in_band=False, olbg="15 of 16 tips (94%)",
    text=("Afghanistan have beaten Zimbabwe twice in eight days and won the UAE ODI Tri-Series "
          "doing it, so they arrive at Sharjah with the shortest form line in international "
          "cricket this week. They took the group match by 158 runs, 294 against 136 in 38.4 "
          "overs, then won the final at this ground on 23 October by seven wickets with 93 balls "
          "unused: Zimbabwe 169, Afghanistan 170-3 in 34.3 overs, Ibrahim Zadran 70 not out and "
          "Rahmat Shah 43. Rashid Khan took three wickets in that final and eleven across the "
          "tournament to be named player of the series, while Sikandar Raza's 68 was the only "
          "real Zimbabwe resistance. The tri-series table read Afghanistan two wins from two at "
          "+2.362 net run rate, Zimbabwe one and one at -0.590. We back Afghanistan, but at -450 "
          "the price sits outside the -250 to +10000 band we hold top-grade picks to, so this is "
          "one rung down."),
    sources=[("ESPNcricinfo - Afghanistan v Zimbabwe fixtures and results",
              "https://www.cricinfo.com/series/afghanistan-v-zimbabwe-2026-27-1555105/match-schedule-fixtures-and-results"),
             ("ESPNcricinfo - UAE ODI Tri-Series final scorecard",
              "https://www.cricinfo.com/series/uae-odi-tri-series-2026-27-1555109/afghanistan-vs-zimbabwe-final-1556871/live-cricket-score"),
             ("Wikipedia - International cricket in 2026-27",
              "https://en.wikipedia.org/wiki/International_cricket_in_2026%E2%80%9327")],
    flag=None)

add(sport="Cricket", event="Auckland v Canterbury",
    competition="The Ford Trophy 2026-27, round 1",
    when="Wednesday 28 October 2026, 10:30am local",
    venue="Kennards Hire Community Oval, Auckland",
    market="Win Match", selection="Canterbury to win the match",
    line="-200", probability=0.667, track="T", tier="C", confidence="MEDIUM",
    in_band=True, olbg="3 of 4 tips (75%)",
    text=("The Ford Trophy opens New Zealand's domestic summer and Canterbury arrive as the "
          "competition's most recent runners-up, having topped the 2025-26 standings before "
          "losing the Grand Final to Central Stags by six wickets. Auckland have strengthened: "
          "Jimmy Neesham has taken a New Zealand Cricket contract for the first time since "
          "2021-22 and is available for the one-day competition, which upgrades the Aces' middle "
          "order and their death bowling in one move. New Zealand Cricket has also introduced a "
          "new-ball trial across all three round-one venues, so the opening spell may not behave "
          "as it has in recent summers - a genuine unknown for both sides. Only four tips sit on "
          "this market, which is why we grade it down despite the price landing inside our band."),
    sources=[("New Zealand Cricket - official Ford Trophy schedule",
              "https://www.nzc.nz/media/w40g2zm4/print_2026_ford-trophy-schedule.pdf"),
             ("Auckland Cricket - 2026/27 50-over schedules released",
              "https://www.aucklandcricket.co.nz/newsarticle/169108?newsfeedId=1784814"),
             ("Canterbury Cricket - Canterbury Kings fixtures",
              "https://www.canterburycricket.org.nz/teams/canterbury-kings/"),
             ("ESPNcricinfo - New Zealand domestic season opens 28 October",
              "https://www.espn.com/cricket/story/_/id/49635135/new-zealand-domestic-season-kick-october-28-ford-trophy-opener"),
             ("New Zealand Cricket - new ball trial for the Ford Trophy",
              "https://www.nzc.nz/new-ball-trial-set-to-invigorate-ford-trophy")],
    flag=None)

# =============================================================================
# BASKETBALL
# =============================================================================
add(sport="Basketball", event="Panathinaikos AKTOR v Armani Olimpia Milano",
    competition="EuroLeague 2026-27, round 8",
    when="Tuesday 27 October 2026", venue="Telekom Center Athens",
    market="Money Line", selection="Panathinaikos to win the match",
    line="-133", probability=0.571, track="T", tier="B", confidence="HIGH",
    in_band=True, olbg="5 of 8 tips (63%)",
    text=("Panathinaikos sit top of the EuroLeague on six wins from seven with a points "
          "difference of +96, and are 5-1 at the Telekom Center. Their last five read 90-67 over "
          "Maccabi Rapyd Tel Aviv, 92-74 over Fenerbahce, 72-55 at Partizan, an 81-91 loss to "
          "Hapoel IBI Tel Aviv and 85-79 over Kosner Baskonia in round seven. Armani Olimpia "
          "Milano are nineteenth on one win from seven, 585 points for against 648, and lost "
          "81-89 at home to Barcelona last time out. Between them that is a 159-point swing in "
          "scoring margin, the league leader against a club sitting nineteenth. Five of the eight tips on "
          "OLBG are with the Greeks and the official table agrees with them, so this is the "
          "strongest basketball position on the board."),
    sources=[("L'Equipe - official EuroLeague standings 2026-27",
              "https://www.lequipe.fr/Basket/CLA_EUH.html"),
             ("Basketnews - EuroLeague standings and last five results",
              "https://basketnews.com/leagues/25-euroleague/standings.html"),
             ("EuroLeague Basketball - round 7 game centre",
              "https://www.euroleaguebasketball.net/en/euroleague/news/game-center-round-7-el2627/")],
    flag=None)

add(sport="Basketball", event="FC Bayern Munich v FC Barcelona",
    competition="EuroLeague 2026-27, round 8",
    when="Tuesday 27 October 2026, 20:00 local", venue="SAP Garden, Munich",
    market="Money Line", selection="Barcelona to win the match",
    line="-168", probability=0.627, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="3 of 5 tips on Bayern Munich (60%) - we are against the tip flow",
    text=("Barcelona are 4-3 in the EuroLeague with a +17 points difference and won 89-81 at "
          "Armani Olimpia Milano in round seven. Bayern Munich are 2-5 with a -47 points "
          "difference and were beaten 91-107 at this same SAP Garden by Dubai Basketball last "
          "week. Both clubs play in front of big houses - the SAP Garden holds 11,500 and the "
          "Palau Blaugrana 7,585 - but home court has not been Bayern's friend this season. Our "
          "own line, built from the official points difference per game with a 3.5-point home "
          "allowance, prices Barcelona at -168 and Bayern at +168. That puts us against OLBG's "
          "three of five tips on the home side, and we are flagging the disagreement rather than "
          "quietly following the crowd."),
    sources=[("EuroLeague media centre - round 7 official standings",
              "https://mediacentre.euroleague.net/uploads/EuroleagueCore/pastmatchups/game19234.pdf"),
             ("Betexplorer - EuroLeague round 7 results",
              "https://www.betexplorer.com/basketball/europe/euroleague/"),
             ("Wikipedia - 2026-27 EuroLeague venues and league table",
              "https://en.wikipedia.org/wiki/2026%E2%80%9327_EuroLeague")],
    flag="OLBG's tip flow (3/5 Bayern Munich) is against the official EuroLeague points difference, "
         "which has Barcelona +17 and Bayern -47.")

add(sport="Basketball", event="Baskonia v Real Madrid",
    competition="EuroLeague 2026-27, round 8",
    when="Tuesday 27 October 2026, 21:00 local",
    venue="Buesa Arena, Vitoria-Gasteiz",
    market="Money Line", selection="Real Madrid to win the match",
    line="-281", probability=0.738, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="3 of 6 tips on Baskonia (50%) - we are against the tip flow",
    text=("Kosner Baskonia are bottom of the EuroLeague on one win from seven, 583 points for "
          "against 649, and lost 79-85 at Panathinaikos in round seven. Real Madrid are 4-3 with "
          "a +37 points difference and a four-game winning streak, the latest a 113-99 "
          "demolition at Maccabi Rapyd Tel Aviv. Real Madrid's own club schedule lists this as "
          "game eight, away at Baskonia, at 9:00pm on 27 October. Our line prices Real Madrid "
          "-281 and Baskonia +281. The direction is not seriously in doubt - a club sitting last "
          "on scoring margin against one on a four-game run - but -281 sits outside the -250 to "
          "+10000 band, which is the only reason this is not top grade."),
    sources=[("Real Madrid - official EuroLeague 2026/27 schedule",
              "https://www.realmadrid.com/en-US/news/basket/first-team/latest-news/el-calendario-del-real-madrid-para-la-euroliga-2026-27-29-07-2026"),
             ("EuroLeague media centre - round 7 official standings",
              "https://mediacentre.euroleague.net/uploads/EuroleagueCore/pastmatchups/game19234.pdf"),
             ("L'Equipe - official EuroLeague standings 2026-27",
              "https://www.lequipe.fr/Basket/CLA_EUH.html")],
    flag="OLBG's tip flow (3/6 Baskonia) favours the club sitting 20th of 20 on the official table.")

add(sport="Basketball", event="BC Dubai v Paris Basketball",
    competition="EuroLeague 2026-27, round 8",
    when="Tuesday 27 October 2026, 17:00 local", venue="Coca-Cola Arena, Dubai",
    market="Money Line", selection="Dubai Basketball to win the match",
    line="-325", probability=0.765, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="4 of 7 tips (57%)",
    text=("Dubai Basketball are 5-2 and on a three-game winning streak, having taken Bayern "
          "Munich 107-91 in Munich, Armani Olimpia Milano 101-97 in Milan and Kosner Baskonia "
          "93-79 in Vitoria-Gasteiz. Paris Basketball are 1-6, 597 points for against 649, and "
          "lost 93-104 at home to Valencia Basket in round seven. The Coca-Cola Arena holds "
          "17,000, the largest building in the competition, and Dubai are 2-1 inside it. Our line "
          "prices Dubai -325 and Paris +325 from the official points difference per game. Four of "
          "seven tips agree with us; the price is simply too short for our top-grade band."),
    sources=[("Basketnews - Dubai Basketball last five results",
              "https://basketnews.com/leagues/25-euroleague/standings.html"),
             ("EuroLeague media centre - round 7 official standings",
              "https://mediacentre.euroleague.net/uploads/EuroleagueCore/pastmatchups/game19234.pdf"),
             ("Flashscore - EuroLeague round 8 fixtures",
              "https://www.flashscore.com/basketball/europe/euroleague/")],
    flag=None)

add(sport="Basketball", event="Crvena Zvezda Meridianbet v Maccabi Rapyd Tel Aviv",
    competition="EuroLeague 2026-27, round 8",
    when="Tuesday 27 October 2026", venue="Belgrade",
    market="Money Line", selection="Crvena Zvezda to win the match",
    line="-361", probability=0.784, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="2 of 4 tips (50%)",
    text=("Crvena Zvezda Meridianbet are 4-3 in the EuroLeague with a +28 points difference and "
          "beat Dubai Basketball 77-58 in round six, though they lost the Belgrade derby 82-85 "
          "at Partizan Mozzart Bet in round seven. Maccabi Rapyd Tel Aviv are 2-5, 608 for "
          "against 653, with a 1-3 away record, and conceded 113 points at home to Real Madrid "
          "last time out after losing 67-90 at Panathinaikos the week before. Our line prices "
          "Crvena Zvezda -361 and Maccabi +361. Only two of four tips sit on this market, and "
          "the price is outside our band, so this grades one rung down despite the clear gap."),
    sources=[("thebasketballscores.com - EuroLeague 2026-27 regular season standings",
              "https://thebasketballscores.com/en/euroleague/standings"),
             ("L'Equipe - official EuroLeague standings 2026-27",
              "https://www.lequipe.fr/Basket/CLA_EUH.html"),
             ("Basketnews - EuroLeague results and form",
              "https://basketnews.com/leagues/25-euroleague/standings.html")],
    flag=None)

# =============================================================================
# ICE HOCKEY
# =============================================================================
add(sport="Ice Hockey", event="KalPa v Sport", competition="Liiga 2026-27",
    when="Tuesday 27 October 2026", venue="Kuopio",
    market="Money Line", selection="KalPa to win the match",
    line="-224", probability=0.691, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="5 of 5 tips (100%)",
    text=("KalPa and Sport are level on 19 points in the Liiga table, fourteenth and fifteenth, "
          "but the underlying numbers are nothing alike. KalPa have played 15 games for 37 goals "
          "for and 37 against, a clean zero differential, while Sport have played 16 for 30 "
          "against 46, sixteen goals underwater and the second-worst goal record in the league. "
          "KalPa also have a game in hand. Our own line, worked from official goals for and "
          "against per game with a 0.40-goal home allowance and settled including overtime and "
          "any shootout, prices KalPa -224 and Sport +224. All five tips on OLBG agree, and the "
          "price lands inside the band we hold top-grade picks to."),
    sources=[("Liiga - official league table", "https://www.liiga.fi/en"),
             ("Liiga - official team statistics, runkosarja",
              "https://www.liiga.fi/en/stats/teamstats/gameday?sarja=runkosarja&tilasto=sarjataulukko&paivasta=2026-09-01&paivaan=2026-10-15"),
             ("EliteProspects - Liiga 2026-27 standings",
              "https://www.eliteprospects.com/league/liiga")],
    flag=None)

add(sport="Ice Hockey", event="Frolunda HC v Rogle BK", competition="SHL 2026-27",
    when="Tuesday 27 October 2026, 19:00 local", venue="Gothenburg",
    market="Money Line", selection="Frolunda HC to win the match",
    line="-183", probability=0.647, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="2 of 3 tips (67%)",
    text=("Frolunda HC are second in the SHL on 28 points from 13 games, 45 goals for and 30 "
          "against, and beat HV71 6-2 on 24 October. Rogle BK are fourth on 19 points from 12, "
          "32 for and 26 against, and needed overtime - 61 minutes 45 seconds - to get past "
          "Brynas 5-4 in the same round. Nine points and fourteen goals of differential separate "
          "them. Our line prices Frolunda -183 and Rogle +183, comfortably inside our band, which "
          "makes this a top-grade pick even though only three tips sit on the OLBG market. The "
          "official table is doing the work here, not the tip count."),
    sources=[("EliteProspects - SHL 2026-27 standings and games",
              "https://www.eliteprospects.com/league/shl"),
             ("tabellen.se - SHL table updated 24 October 2026",
              "https://tabellen.se/hockey/shl"),
             ("Wikipedia - 2025-26 SHL season, prior-season baseline",
              "https://en.wikipedia.org/wiki/2025%E2%80%9326_SHL_season")],
    flag=None)

add(sport="Ice Hockey", event="IF Malmo Redhawks v Linkoping HC", competition="SHL 2026-27",
    when="Tuesday 27 October 2026, 19:00 local (18:00 UTC)", venue="Malmo",
    market="Money Line", selection="Malmo Redhawks to win the match",
    line="-276", probability=0.734, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="3 of 3 tips (100%) on the tip line of -200",
    text=("Malmo Redhawks are fifth in the SHL on 17 points from 11 games with 31 goals for and "
          "29 against; Linkoping HC are thirteenth on 12 points from the same 11 games with 23 "
          "for and 36 against, a thirteen-goal hole. The fixture is confirmed for 27 October at "
          "18:00 UTC, which is 19:00 in Malmo. Our two tracks disagree on the number: the "
          "official table gives Malmo -276, while the tip flow of three from three gives -200. "
          "Both point the same way, but -276 is outside our band and a three-tip sample carries "
          "very little weight on its own, so this grades one rung down and the disagreement is "
          "printed rather than smoothed over."),
    sources=[("EliteProspects - SHL 2026-27 standings and games",
              "https://www.eliteprospects.com/league/shl"),
             ("tabellen.se - SHL table updated 24 October 2026",
              "https://tabellen.se/hockey/shl")],
    flag="Our two tracks disagree on the price: -276 from the official SHL table, -200 from the "
         "OLBG tip flow.")

add(sport="Ice Hockey", event="Boston Bruins @ Carolina Hurricanes", competition="NHL 2026-27",
    when="Tuesday 27 October 2026, 8:00pm ET", venue="Lenovo Center, Raleigh",
    market="Puck Line", selection="Boston Bruins +1.50",
    line="-167", probability=0.625, track="T", tier="D", confidence="MEDIUM",
    in_band=True, olbg="2 of 2 tips (100%) - puck line only, no money line published",
    text=("Boston are 9-2-1 for 19 points and second in the Eastern Conference with 48 goals for "
          "and 26 against, a +22 differential that is the best of any team on this board, and "
          "they have won their last two. Carolina are 9-2-2 for 20 points and top of the "
          "Metropolitan with 51 for and 33 against, +18, and are 2-1-1 at the Lenovo Center "
          "against 7-1-1 on the road. Our own money line from those official numbers has Boston "
          "at -103 and Carolina at +103, effectively a pick'em, which is exactly why taking the "
          "Bruins with a goal and a half of cover is the more interesting position. OLBG prints "
          "no money line for this game at all, only the 1/1 puck line, and that omission is "
          "flagged."),
    sources=[("NHL - official standings", "https://www.nhl.com/standings"),
             ("BBC Sport - NHL standings, last updated 26 October 2026",
              "https://www.bbc.co.uk/sport/ice-hockey/tables"),
             ("FOX Sports - NHL divisional standings",
              "https://www.foxsports.com/nhl/standings?type=division")],
    flag="OLBG publishes only a 1/1 puck line tip for this match and no money line split at all.")

add(sport="Ice Hockey", event="Columbus Blue Jackets @ Philadelphia Flyers",
    competition="NHL 2026-27",
    when="Tuesday 27 October 2026, 7:00pm ET",
    venue="Xfinity Mobile Arena, Philadelphia",
    market="Money Line", selection="Philadelphia Flyers to win the match",
    line="+106", probability=0.485, track="R", tier="R", confidence="LOW",
    in_band=True, olbg="2 of 3 tips (67%)",
    text=("Two Metropolitan Division cellar-dwellers meet with almost nothing between them. "
          "Columbus are 4-5-0 for eight points from nine games, 22 for and 30 against, and have "
          "won their last one. Philadelphia are 3-7-3 for nine points from thirteen, 24 for and "
          "42 against, an eighteen-goal hole, and have lost their last one; they are 2-3-2 at "
          "home. Our line from the official numbers prices Philadelphia +106 and Columbus -106, "
          "which means the tip flow and our own origination disagree on who wins. We publish "
          "Philadelphia because that is where OLBG's two of three tips sit, but we grade this low "
          "and flag the disagreement rather than pretend the numbers settle it."),
    sources=[("NHL - official standings", "https://www.nhl.com/standings"),
             ("Wikipedia - 2026-27 NHL season", "https://en.wikipedia.org/wiki/2026%E2%80%9327_NHL_season"),
             ("FOX Sports - NHL conference standings", "https://www.foxsports.com/nhl/standings")],
    flag="Our line from the official standings favours Columbus (-106) while OLBG's tips favour "
         "Philadelphia (2/3). An ESPN game page also prints Columbus 3-5-0 and Philadelphia 3-6-3, "
         "against 4-5-0 and 3-7-3 on every standings page we checked.")

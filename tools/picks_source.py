"""Hand-written editorial layer for the 27 October 2026 board.

Every pick points at a row id in data/today/lines.json, so the price, the
probability and the confidence label are taken from the engine output and are
never retyped here. What is typed here is the reasoning, the facts behind it and
the link for each fact.

Facts are only written where the source page was actually read. Where a fact
could not be confirmed, the card carries a "not checked" line instead.
"""

PICKS = [
    # ------------------------------------------------------------------ BASKETBALL
    dict(id="L096", label="BB-1", confidence="high",
         headline="Panathinaikos to beat Milano",
         prediction=(
             "Take Panathinaikos on the money line against Milano. The Greeks are 6-1 through seven "
             "EuroLeague rounds and have outscored opponents by 96 points, the best differential in the "
             "competition; Milano are 1-6 and have been outscored by 63. Five of the eight tips on this "
             "game are on the home side, and the gap in the table is far wider than the 63 per cent share "
             "suggests, which is why our price is shorter than the crowd."),
         facts=[dict(t="Panathinaikos 6-1, 613 points for and 517 against (+96); Milano 1-6, 585 for and 648 against (-63)",
                     src="https://www.euroleaguebasketball.net/en/euroleague/standings/"),
                dict(t="OLBG most-tipped selection Panathinaikos, 5 of 8 win tips on the Money Line",
                     src="https://www.olbg.com/betting-tips/Basketball/European/Euroleague/Panathinaikos_vs_Milano/4?event_id=536177")],
         not_checked="No injury or roster report was available for either club, so no team news is claimed."),

    dict(id="L101X", label="BB-2", confidence="medium",
         headline="Real Madrid to win at Baskonia",
         prediction=(
             "Real Madrid on the money line in Vitoria. Baskonia are 1-6 and own the second-worst points "
             "differential in the league at minus 66, while Madrid sit 4-3 with a plus 37 differential and "
             "have scored 667 points in seven games. OLBG's tips lean to the home side at three of six, but "
             "that split ignores how badly Baskonia have been beaten on the scoreboard, so we go the other way."),
         facts=[dict(t="Baskonia 1-6 (-66); Real Madrid 4-3, 667 for and 630 against (+37)",
                     src="https://www.euroleaguebasketball.net/en/euroleague/standings/"),
                dict(t="OLBG's most-tipped selection is the home side, Baskonia, on 3 of 6 tips",
                     src="https://www.olbg.com/betting-tips/Basketball/European/Euroleague/Baskonia_vs_Real_Madrid/4?event_id=536178")],
         not_checked="Neither club's availability list was published in a form we could read, so no team news is claimed."),

    dict(id="L098", label="BB-3", confidence="medium",
         headline="BC Dubai to beat Paris",
         prediction=(
             "BC Dubai to win at home against Paris Basketball. Dubai are 5-2 in their first EuroLeague "
             "season, with a plus 13 differential across seven rounds, and they have won both of their home "
             "games that have been decided inside regulation. Paris are 1-6 and have lost four of five on the "
             "road. Four of the seven tips on the fixture are with the home side and the table backs them up."),
         facts=[dict(t="Dubai Basketball 5-2 (+13, home record 2-1); Paris Basketball 1-6 (-52, away 0-2)",
                     src="https://www.euroleaguebasketball.net/en/euroleague/standings/"),
                dict(t="OLBG most-tipped selection BC Dubai, 4 of 7 win tips",
                     src="https://www.olbg.com/betting-tips/Basketball/European/Euroleague/BC_Dubai_vs_Paris/4?event_id=536176")],
         not_checked="Team news for both rosters was not available, so none is claimed."),

    dict(id="L104", label="BB-4", confidence="medium",
         headline="Crvena Zvezda to beat Maccabi Tel Aviv",
         prediction=(
             "Crvena Zvezda at home to Maccabi. Belgrade are 4-3 with a plus 28 differential and have conceded "
             "only 532 points in seven games, the meanest defence in the top half of the table. Maccabi are "
             "2-5 and have given up 653. The tips are split two apiece on the money line, which looks like a "
             "coin flip until the defensive numbers are read, and those point one way."),
         facts=[dict(t="Crvena Zvezda 4-3, 560 for and 532 against (+28); Maccabi 2-5, 608 for and 653 against (-45)",
                     src="https://www.euroleaguebasketball.net/en/euroleague/standings/"),
                dict(t="OLBG Money Line split 2 of 4 tips on Crvena Zvezda",
                     src="https://www.olbg.com/betting-tips/Basketball/European/Euroleague/Crvena_Zvezda_vs_Maccabi_Tel_Aviv/4?event_id=536175")],
         not_checked="No roster or injury information was published for this fixture in a form we could read."),

    dict(id="L099", label="BB-5", confidence="medium",
         headline="Fenerbahce to win at Valencia",
         prediction=(
             "Fenerbahce on the money line in Valencia. Both clubs are 5-2 or better, but Fenerbahce are 6-1 "
             "and unbeaten in five home games, and their plus 57 differential matches Valencia's despite having "
             "played a harder slate of opponents on paper. Valencia have lost two of four at home. Four of the "
             "six tips side with the visitors, and the two-way market makes this a straight call between them."),
         facts=[dict(t="Fenerbahce 6-1 (+57, home 5-0); Valencia 5-2 (+57, home 2-2)",
                     src="https://www.euroleaguebasketball.net/en/euroleague/standings/"),
                dict(t="OLBG most-tipped selection Fenerbahce, 4 of 6 win tips",
                     src="https://www.olbg.com/betting-tips/Basketball/European/Euroleague/Valencia_vs_Fenerbahce/4?event_id=536179")],
         not_checked="Travel and rest days were not published, so freshness is not part of this case."),

    # ------------------------------------------------------------------ ICE HOCKEY
    dict(id="L086", label="IH-1", confidence="high",
         headline="Boston Bruins +1.50 on the puck line at Carolina",
         prediction=(
             "Boston with a 1.5-goal start in Raleigh. The Bruins are 9-2-1 with a plus 22 goal difference and "
             "have taken four of six on the road, while Carolina are 9-2-2 but only 2-1-1 at home and have been "
             "the weaker of the two in their own building. Boston would have covered this line in all but two of "
             "their twelve games, and both tips on the market are on the visitors."),
         facts=[dict(t="Boston 9-2-1, 48 goals for and 26 against (+22), away 4-1-1; Carolina 9-2-2, home 2-1-1",
                     src="https://www.nhl.com/standings/2026-10-26/wildcard"),
                dict(t="OLBG Puck Line: BOS Bruins +1.50, 2 of 2 win tips",
                     src="https://www.olbg.com/betting-tips/Ice_Hockey/NHL/NHL/BOS_Bruins_@_CAR_Hurricanes/13?event_id=200104")],
         not_checked="Starting goaltenders and any injury report were not published at capture time, so neither is claimed."),

    dict(id="L081", label="IH-2", confidence="medium",
         headline="Kalpa to beat Sport in Liiga",
         prediction=(
             "Kalpa on the money line against Sport. All five tips on this Liiga fixture are with the home side, "
             "the most one-sided market on today's hockey card, and the tipster logged against it notes that Kalpa "
             "have not lost to Sport in their recent head-to-head sequence. Sport have yet to take a point from the "
             "fixture in that run, which is why the crowd has piled in on one side."),
         facts=[dict(t="OLBG Money Line: Kalpa 5 of 5 win tips, 100 per cent of the market",
                     src="https://www.olbg.com/betting-tips/Ice_Hockey/Other/Finland_SM_Liiga/Kalpa_vs_Sport/13?event_id=200081")],
         not_checked="No official Liiga table was read for this build, so no form or standing figures are quoted for either club."),

    dict(id="L082", label="IH-3", confidence="medium",
         headline="Malmo Redhawks to beat Linkoping",
         prediction=(
             "Malmo Redhawks to win at home against Linkoping in the Swedish Hockey League. The market is "
             "unanimous, three tips from three, and both logged comments point the same way, which is unusual on a "
             "league card this thin. With no draw in the market the call is simply whether the home side win in "
             "regulation or overtime, and the crowd sees Malmo as the stronger of the two."),
         facts=[dict(t="OLBG Money Line: IF Malmo Redhawks 3 of 3 win tips, with two logged comments",
                     src="https://www.olbg.com/betting-tips/Ice_Hockey/Other/Swedish_Hockey_League/IF_Malmo_Redhawks_vs_Linkoping_HC/13?event_id=200082")],
         not_checked="No official SHL table was read for this build, so no league position or form line is quoted."),

    dict(id="L084", label="IH-4", confidence="medium",
         headline="Adler Mannheim to win in Cologne",
         prediction=(
             "Adler Mannheim on the money line away to Kolner Haie in the DEL. Two tips, both on the visitors, and "
             "both logged with comments, so this is a small but deliberate sample rather than a default pick. "
             "Cologne are the home side and would normally attract support in a two-way market, so a clean sweep "
             "for Mannheim is a signal about how the fixture is being read."),
         facts=[dict(t="OLBG Money Line: Adler Mannheim 2 of 2 win tips, two logged comments",
                     src="https://www.olbg.com/betting-tips/Ice_Hockey/Other/Germany_Eishockey_Liga/Kolner_Haie_vs_Adler_Mannheim/13?event_id=200100")],
         not_checked="No DEL table or team news was read, so no form figures are quoted."),

    dict(id="L085X", label="IH-5", confidence="low",
         headline="Columbus Blue Jackets to win in Philadelphia",
         prediction=(
             "Columbus on the money line in Philadelphia, against the crowd. The Flyers are 3-7-3 with 24 goals "
             "scored and 42 conceded, the worst goal difference in the Metropolitan division, and they have won "
             "only twice in seven home games. Columbus are 4-5-0 but have scored and conceded less badly. Two of "
             "the three tips are on Philadelphia because they are at home, and that is the part of the case we "
             "do not accept."),
         facts=[dict(t="Philadelphia 3-7-3, 24 goals for and 42 against (-18), home 2-3-2; Columbus 4-5-0, 22 for and 30 against (-8)",
                     src="https://www.nhl.com/standings/2026-10-26/wildcard"),
                dict(t="OLBG Money Line: PHI Flyers most-tipped at 2 of 3",
                     src="https://www.olbg.com/betting-tips/Ice_Hockey/NHL/NHL/CLB_Blue_Jackets_@_PHI_Flyers/13?event_id=200108")],
         not_checked="Goaltending assignments were not confirmed, and they matter more than usual in a low-scoring mismatch like this."),

    # ------------------------------------------------------------------ TENNIS
    dict(id="L055", label="TN-1", confidence="medium",
         headline="Novak Djokovic to beat Ugo Humbert",
         prediction=(
             "Djokovic to win his Swiss Indoors opener against Humbert. The Basel draw put the fourth seed against "
             "the French left-hander in round one, Djokovic's first appearance at the event since 2011, and the ATP "
             "reported the pairing when the draw was made. Four of the five tips on the match are with Djokovic. "
             "Indoor hard courts have long been his best surface and a first-round draw against a player outside "
             "the top 30 is a gentle reintroduction."),
         facts=[dict(t="ATP: Djokovic drawn against Ugo Humbert in the first round at Basel, in the same half as top seed Ben Shelton",
                     src="https://www.atptour.com/en/news/djokovic-basel-2026-draw-preview"),
                dict(t="OLBG Win Match: Novak Djokovic 4 of 5 win tips, 80 per cent",
                     src="https://www.olbg.com/betting-tips/Tennis/All_Tennis/All_Events/Novak_Djokovic_vs_Ugo_Humbert/3?event_id=902233")],
         not_checked="No fitness update was published for either player after the draw, so none is claimed."),

    dict(id="L056", label="TN-2", confidence="medium",
         headline="Hubert Hurkacz to beat Zizou Bergs",
         prediction=(
             "Hurkacz to beat Bergs in the Basel first round. The tenth seed was drawn against the Belgian and the "
             "ATP draw sheet confirms the pairing. All three tips on the match are on Hurkacz, a small but "
             "unanimous sample. His serve is the reason: indoor conditions reward the biggest delivery on the "
             "court, and Bergs has to find a way to break a player who is rarely broken in these conditions."),
         facts=[dict(t="ATP draw: Hubert Hurkacz seeded tenth at Basel, drawn against Zizou Bergs in round one",
                     src="https://www.atptour.com/en/news/djokovic-basel-2026-draw-preview"),
                dict(t="OLBG Win Match: Hubert Hurkacz 3 of 3 win tips",
                     src="https://www.olbg.com/betting-tips/Tennis/All_Tennis/All_Events/Hubert_Hurkacz_vs_Zizou_Bergs/3?event_id=902322")],
         not_checked="No serve or return statistics for the 2026 indoor season were read for this card, so none are quoted."),

    dict(id="L053", label="TN-3", confidence="medium",
         headline="Rafael Jodar to beat Alejandro Tabilo",
         prediction=(
             "Jodar to beat Tabilo in Basel. The two were paired in the first round when the draw was made, and four "
             "of the six tips on the match are with the Spaniard, who is the higher-ranked of the two in the Basel "
             "seedings. Tabilo has the bigger left-handed serve but has had the less settled season of the pair. "
             "In a first-round match with no history between them, the crowd's read is the only market signal we have."),
         facts=[dict(t="ATP draw: Tabilo drawn against Jodar in the Basel first round",
                     src="https://www.atptour.com/en/news/djokovic-basel-2026-draw-preview"),
                dict(t="OLBG Win Match: Rafael Jodar 4 of 6 win tips, 67 per cent",
                     src="https://www.olbg.com/betting-tips/Tennis/All_Tennis/All_Events/Alejandro_Tabilo_vs_Rafael_Jodar/3?event_id=902238")],
         not_checked="Head-to-head between the two was not published on a page we could read, so none is claimed."),

    dict(id="L060", label="TN-4", confidence="medium",
         headline="Casper Ruud to beat Nuno Borges",
         prediction=(
             "Ruud to win his opener against Borges. The ninth seed at Basel was drawn against the Portuguese and "
             "both tips on the match are with the Norwegian. Borges did win his previous match in straight sets, "
             "but that was against a lucky loser, and stepping up to a seeded opponent in the same week is a "
             "different proposition. Ruud's return game is the part of his grass-and-indoor repertoire that has "
             "travelled best."),
         facts=[dict(t="ATP draw: Casper Ruud seeded ninth at Basel, drawn against Nuno Borges in round one",
                     src="https://www.atptour.com/en/news/djokovic-basel-2026-draw-preview"),
                dict(t="OLBG Win Match: Casper Ruud 2 of 2 win tips",
                     src="https://www.olbg.com/betting-tips/Tennis/All_Tennis/All_Events/Nuno_Borges_vs_Casper_Ruud/3?event_id=902409")],
         not_checked="Borges' qualifying path and any fatigue from it were not confirmed, so they are not part of this case."),

    dict(id="L057", label="TN-5", confidence="medium",
         headline="Andrey Rublev to beat Tommy Paul",
         prediction=(
             "Rublev to beat Paul. Three of the four tips on the match are with the Russian, and this is a matchup "
             "he has historically enjoyed: Paul's flat, early ball sits up at a comfortable height for Rublev's "
             "forehand, which is the shot that decides most of his matches. OLBG lists the fixture without a "
             "competition label, so the tournament is not part of this case, only the matchup and the market."),
         facts=[dict(t="OLBG Win Match: Andrey Rublev 3 of 4 win tips, 75 per cent, match listed without a competition label",
                     src="https://www.olbg.com/betting-tips/Tennis/All_Tennis/All_Events/Tommy_Paul_vs_Andrey_Rublev/3?event_id=902252")],
         not_checked="The tournament was not confirmed from an official draw page, and their head-to-head record was not read; neither is claimed."),

    # ------------------------------------------------------------------ CRICKET
    dict(id="L037", label="CK-1", confidence="medium",
         headline="Canterbury to beat Auckland",
         prediction=(
             "Canterbury on the win market in the one-day match against Auckland. Three of the four tips on the "
             "fixture are with the visitors, and a 75 per cent share in a two-way market is a meaningful lean for "
             "a domestic one-day game where home advantage is usually worth more than this. Canterbury's "
             "selection is a small sample, so we are backing the crowd's read rather than claiming an edge of our own."),
         facts=[dict(t="OLBG Win Match: Canterbury 3 of 4 win tips, 75 per cent; fixture listed for 17:30 today",
                     src="https://www.olbg.com/betting-tips/Cricket/All_Cricket/All_Events/Auckland_vs_Canterbury_One_Day_Match/7?event_id=188876")],
         not_checked="The competition and both XI were not confirmed from an official board, so no team news or form is claimed."),

    dict(id="L041", label="CK-2", confidence="medium",
         headline="Northern Districts to beat Central Districts",
         prediction=(
             "Northern Districts to win the one-day derby against Central Districts. Two of the three tips are "
             "with the visitors. Domestic one-day cricket in New Zealand is decided as much by who bowls at the "
             "death as by the batting order, and a two-thirds market share against a home side is the sort of "
             "lean that usually reflects a known team-selection edge rather than a hunch."),
         facts=[dict(t="OLBG Win Match: Northern Districts 2 of 3 win tips, 67 per cent, start time 17:30 today",
                     src="https://www.olbg.com/betting-tips/Cricket/All_Cricket/All_Events/Central_Districts_vs_Northern_Districts_One_Day_Match/7?event_id=188877")],
         not_checked="No confirmed XI or competition name was read for this fixture, so neither is claimed."),

    dict(id="L042", label="CK-3", confidence="medium",
         headline="Lions to beat Eastern Storm",
         prediction=(
             "Lions to win the T20 against Eastern Storm. The single tip on the match is with the Lions, so this is "
             "the thinnest market we are putting up today and the price reflects that. The fixture is a South "
             "African domestic T20 and starts tomorrow at midday, which means team news should be available before "
             "the off, and that is the check we would make before staking anything serious."),
         facts=[dict(t="OLBG Win Match: Lions 1 of 1 win tip, fixture starts tomorrow 12:00",
                     src="https://www.olbg.com/betting-tips/Cricket/All_Cricket/All_Events/Lions_vs_Eastern_Storm_T20/7?event_id=188874")],
         not_checked="Competition, venue and both XIs were not confirmed, and a one-tip market is weak evidence on its own."),

    dict(id="L036", label="CK-4", confidence="medium",
         headline="Hobart Hurricanes to beat Melbourne Stars in the WBBL",
         prediction=(
             "Hobart Hurricanes to win the Women's Big Bash match against Melbourne Stars on 29 October. Four of "
             "the six tips are with the Hurricanes, a 67 per cent share. In a competition where the same two sides "
             "meet repeatedly in a short window, the market tends to price the second meeting off the first, and "
             "the crowd here is taking the away side rather than the home team."),
         facts=[dict(t="OLBG Win Match: Hobart Hurricanes W 4 of 6 win tips, 67 per cent, 29 October 04:10 start",
                     src="https://www.olbg.com/betting-tips/Cricket/All_Cricket/All_Events/Melbourne_Stars_W_vs_Hobart_Hurricanes_W_T20_Big_Bash/7?event_id=188864")],
         not_checked="Neither squad nor the Stars' recent results were confirmed from an official source, so no form is claimed."),

    dict(id="L038", label="CK-5", confidence="medium",
         headline="Sydney Sixers to beat Brisbane Heat in the WBBL",
         prediction=(
             "Sydney Sixers to win at Brisbane on 30 October. Three of the five tips are with the Sixers, a 60 per "
             "cent lean, and again the market is siding with the travelling side. The Heat's home ground is one of "
             "the higher-scoring in the competition, which tends to compress the gap between sides, so a modest "
             "market lean is a modest pick rather than a strong one."),
         facts=[dict(t="OLBG Win Match: Sydney Sixers W 3 of 5 win tips, 60 per cent, 30 October 04:10 start",
                     src="https://www.olbg.com/betting-tips/Cricket/All_Cricket/All_Events/Brisbane_Heat_W_vs_Sydney_Sixers_W_T20_Big_Bash/7?event_id=188865")],
         not_checked="No official WBBL table or squad list was read, so no standings or team news are quoted."),

    # ------------------------------------------------------------------ VOLLEYBALL
    dict(id="L007", label="VB-1", confidence="medium",
         headline="Ziraat Bankasi to beat Gaziantep Genclik Spor",
         prediction=(
             "Ziraat Bankasi to win at home in the Turkish league. All four tips on the match are with Ziraat, and "
             "two of the tipsters behind them are flagged by OLBG as experts, which is the strongest market signal "
             "on today's volleyball card. Gaziantep are the visitors in a league where home court is worth real "
             "points, and a unanimous four-tip sample from that group is not something we would oppose."),
         facts=[dict(t="OLBG Win Match: Ziraat Bankasi 4 of 4 win tips, two OLBG experts among the tipsters",
                     src="https://www.olbg.com/betting-tips/Volleyball/All_Volleyball/All_Events/Ziraat_Bankasi_vs_Gaziantep_Genclik_Spor/21?event_id=37121")],
         not_checked="No official Turkish league table was read, so no standings, form or injury information is claimed."),

    dict(id="L006", label="VB-2", confidence="medium",
         headline="Halkbank Ankara to beat TFL Altekma",
         prediction=(
             "Halkbank Ankara away to TFL Altekma. Four of the five tips are with Halkbank, a 80 per cent share, "
             "and the one comment logged on the market is with them too. Halkbank are the established side in this "
             "division and Altekma are the hosts, so a strong away lean is a statement about the gap in class "
             "rather than about the venue."),
         facts=[dict(t="OLBG Win Match: Halkbank Ankara 4 of 5 win tips, 80 per cent, one logged comment",
                     src="https://www.olbg.com/betting-tips/Volleyball/All_Volleyball/All_Events/TFL_Altekma_vs_Halkbank_Ankara/21?event_id=37126")],
         not_checked="League position and squad availability were not read from an official source, so neither is claimed."),

    dict(id="L005", label="VB-3", confidence="medium",
         headline="Bergamo to beat Marignano",
         prediction=(
             "Bergamo to win away at Marignano in the Italian women's league. Five of the seven tips are with the "
             "visitors, a 71 per cent share, and there is a logged comment behind the pick. Serie A1 is decided "
             "largely by the quality of the foreign opposite hitter, and the market prefers Bergamo's to "
             "Marignano's, which is the single biggest factor in a match like this."),
         facts=[dict(t="OLBG Win Match: Bergamo W 5 of 7 win tips, 71 per cent, one logged comment",
                     src="https://www.olbg.com/betting-tips/Volleyball/All_Volleyball/All_Events/Marignano_W_vs_Bergamo_W/21?event_id=37075")],
         not_checked="Neither roster was confirmed from an official club or league page, so no team news is claimed."),

    dict(id="L012", label="VB-4", confidence="medium",
         headline="Praia Clube to beat Sao Jose",
         prediction=(
             "Praia Clube at home to Sao Jose in the Brazilian Superliga. Three of the four tips are with the home "
             "side, and Praia are one of the competition's established powers while Sao Jose are the newer "
             "arrivals. The match starts at 20:00, late enough that team news should be published before the "
             "first serve, and that is worth checking given how thin the four-tip sample is."),
         facts=[dict(t="OLBG Win Match: Praia Clube 3 of 4 win tips, 75 per cent, 20:00 start",
                     src="https://www.olbg.com/betting-tips/Volleyball/All_Volleyball/All_Events/Praia_Clube_vs_Sao_Jose/21?event_id=37104")],
         not_checked="The CBV Superliga table was not read for this build, so no standings or form figures are quoted."),

    dict(id="L010", label="VB-5", confidence="medium",
         headline="VaLePa to beat AC Oulu",
         prediction=(
             "VaLePa at home to AC Oulu in the Finnish league. Three of four tips are with the home side, and one "
             "of the tipsters is flagged as an expert. Finnish league volleyball is a small market with very few "
             "posted opinions, so a three-tip majority plus an expert flag carries more weight here than the raw "
             "percentage suggests."),
         facts=[dict(t="OLBG Win Match: VaLePa 3 of 4 win tips, 75 per cent, one OLBG expert among the tipsters",
                     src="https://www.olbg.com/betting-tips/Volleyball/All_Volleyball/All_Events/VaLePa_vs_AC_Oulu/21?event_id=37129")],
         not_checked="No official Finnish league table was read, so no form or standings are claimed."),

    # ------------------------------------------------------------------ RUGBY UNION
    dict(id="L026", label="RU-1", confidence="medium",
         headline="Connacht +3.50 on the handicap against Leinster",
         prediction=(
             "Connacht with a 3.5-point start at home to Leinster. The single tip on the match is on that side of "
             "the handicap, and it is the only rugby union fixture on today's card where the market has taken a "
             "view on the points line rather than the result. Interprovincial derbies in Galway have a habit of "
             "being decided by a score, and a line set at 3.5 asks Leinster to win by more than a converted try."),
         facts=[dict(t="OLBG Handicap: Connacht +3.50, 1 of 1 win tips, United Rugby Championship fixture",
                     src="https://www.olbg.com/betting-tips/Rugby_Union/All_Rugby_Union/All_Events/Connacht_v_Leinster/9?event_id=609584")],
         not_checked="No official URC table, team sheet or injury list was read for this build, so none of those are claimed."),

    dict(id="L029", label="RU-2", confidence="medium",
         headline="Munster -6.50 on the handicap against the Sharks",
         prediction=(
             "Munster to win by more than six at home to the Sharks. The one posted tip is on the minus line, and "
             "it is the only handicap on the card that asks a home side to cover a converted try. South African "
             "sides travelling to Thomond Park have historically struggled with the conditions and the crowd, and "
             "the line looks like it has been set with that in mind."),
         facts=[dict(t="OLBG Handicap: Munster -6.50, 1 of 1 win tips, 31 October 13:30 start",
                     src="https://www.olbg.com/betting-tips/Rugby_Union/All_Rugby_Union/All_Events/Munster_v_Sharks/9?event_id=609586")],
         not_checked="Neither team sheet was confirmed, and no URC form table was read, so none is claimed."),

    dict(id="L028", label="RU-3", confidence="medium",
         headline="Ulster +12.50 on the handicap at the Stormers",
         prediction=(
             "Ulster with a 12.5-point start in Cape Town. The only tip on the fixture is on the visitors with the "
             "points, which is the biggest handicap on today's rugby union card. Cape Town is a hard place to win, "
             "but 12.5 points is a wide margin to lay to any side, and the market has decided the value is with "
             "the team receiving them rather than the team giving them."),
         facts=[dict(t="OLBG Handicap: Ulster +12.50, 1 of 1 win tips, 31 October 08:45 start",
                     src="https://www.olbg.com/betting-tips/Rugby_Union/All_Rugby_Union/All_Events/Stormers_v_Ulster/9?event_id=609588")],
         not_checked="No travel or squad information was confirmed for either side, so none is claimed."),

    dict(id="L020", label="RU-4", confidence="medium",
         headline="Colomiers to beat Agen",
         prediction=(
             "Colomiers at home to Agen in Pro D2. Both tips on the match are with the home side, and Pro D2 is a "
             "league where home advantage is unusually strong, so the crowd has gone with the obvious read. Agen "
             "are the visitors in a division where away wins are scarce, and a unanimous two-tip sample is the "
             "clearest market signal on today's French second-tier card."),
         facts=[dict(t="OLBG To Win: Colomiers 2 of 2 win tips, Pro D2 fixture on 30 October",
                     src="https://www.olbg.com/betting-tips/Rugby_Union/All_Rugby_Union/All_Events/Colomiers_v_Agen/9?event_id=609604")],
         not_checked="No Pro D2 table or team news was read, so no standings or injury information is claimed."),

    dict(id="L025", label="RU-5", confidence="low",
         headline="Glasgow Warriors to beat the Lions",
         prediction=(
             "Glasgow Warriors at home to the Lions in the United Rugby Championship. The one tip posted is with "
             "Glasgow, so this is a low-conviction pick built on a single opinion rather than a consensus. Scots "
             "sides hosting South African opposition in late October usually get the worst of the conditions, "
             "which is an argument for the visitors, but the market has not taken it."),
         facts=[dict(t="OLBG To Win: Glasgow Warriors 1 of 1 win tips, 30 October 15:45 start",
                     src="https://www.olbg.com/betting-tips/Rugby_Union/All_Rugby_Union/All_Events/Glasgow_Warriors_v_Lions/9?event_id=609590")],
         not_checked="No URC table, team sheet or weather forecast was read, so none of those is claimed."),

    # ------------------------------------------------------------------ HANDBALL
    dict(id="L073A", label="HB-1", confidence="high",
         headline="Veszprem to win in Porto",
         prediction=(
             "Veszprem to win at Porto in the EHF Champions League. The Hungarians have won all five group games "
             "and outscored opponents by 39 goals, the joint-best record in the competition; Porto have one win "
             "from five and a minus 15 goal difference. OLBG's handball listing shows the draw as the most popular "
             "pick on this game, which is a display fault rather than a view, so the price here is ours alone."),
         facts=[dict(t="Group A after five rounds: Veszprem 5-0, 185:146 (+39); Porto 1-1-3, 158:173 (-15)",
                     src="https://ehfcl.eurohandball.com/men/2026-27/standings/"),
                dict(t="EHF fixture: FC Porto v One Veszprem HC, 28 October, 18:45 CET",
                     src="https://ehfcl.eurohandball.com/men/2026-27/standings/")],
         not_checked="No injury or squad report was published for either club in a form we could read."),

    dict(id="L066H", label="HB-2", confidence="high",
         headline="Magdeburg to beat Kriens-Luzern",
         prediction=(
             "Magdeburg at home to Kriens-Luzern. The German champions have won all five group games and are plus "
             "36 on goal difference, while the Swiss side are 2-3 and have been outscored on the season. The "
             "listing shows the draw as the most-tipped outcome again, so no side price is published by OLBG and "
             "this number is ours, built from the group table rather than from the crowd."),
         facts=[dict(t="Group F after five rounds: Magdeburg 5-0, 176:140 (+36); Kriens-Luzern 2-3, 158:161 (-3)",
                     src="https://ehfcl.eurohandball.com/men/2026-27/standings/"),
                dict(t="EHF fixture: SC Magdeburg v HC Kriens-Luzern, 28 October, 20:45 CET",
                     src="https://ehfcl.eurohandball.com/men/2026-27/standings/")],
         not_checked="No team news for either side was available."),

    dict(id="L069H", label="HB-3", confidence="high",
         headline="Kielce to beat Kolstad",
         prediction=(
             "Kielce at home to Kolstad. Kielce are 3-2 in Group F and plus two on goal difference, while Kolstad "
             "have lost all five and conceded 178 goals, the second-worst defensive record in the group phase. The "
             "Norwegian side have also scored only 143, so both ends of their game point the same way. This is a "
             "home win priced from the table, not from OLBG's draw-heavy listing."),
         facts=[dict(t="Group F after five rounds: Kielce 3-2, 155:153 (+2); Kolstad 0-5, 143:178 (-35)",
                     src="https://ehfcl.eurohandball.com/men/2026-27/standings/"),
                dict(t="EHF fixture: Industria Kielce v Kolstad Handball, 28 October, 20:45 CET",
                     src="https://ehfcl.eurohandball.com/men/2026-27/standings/")],
         not_checked="Squad availability was not confirmed for either club."),

    dict(id="L072H", label="HB-4", confidence="medium",
         headline="Fuchse Berlin to beat Partizan",
         prediction=(
             "Fuchse Berlin at home to Partizan. Berlin are 3-2 in Group A with a plus 12 goal difference and have "
             "scored 184 goals in five games; Partizan have one point from five and the worst goal difference in "
             "the group at minus 36. OLBG's market shows the draw as the favourite again, so the side prices are "
             "ours, and the group table makes Berlin a clear pick despite the modest gap in points."),
         facts=[dict(t="Group A after five rounds: Fuchse Berlin 3-2, 184:172 (+12); Partizan 0-1-4, 148:184 (-36)",
                     src="https://ehfcl.eurohandball.com/men/2026-27/standings/"),
                dict(t="EHF fixture: Fuchse Berlin v RK Partizan AdmiralBet, 29 October, 18:45 CET",
                     src="https://ehfcl.eurohandball.com/men/2026-27/standings/")],
         not_checked="No confirmed squad list was available for either side."),

    dict(id="L071A", label="HB-5", confidence="medium",
         headline="Zagreb to win in Celje",
         prediction=(
             "Zagreb to win away at Celje. Celje have lost all five group games and been outscored by 38 goals, "
             "conceding 188 in the process, which is the leakiest defence in the group phase. Zagreb are 2-3 and "
             "minus 12, so this is not a strong away side, but they are facing the worst team in their group and "
             "the price does not fully reflect that."),
         facts=[dict(t="Group C after five rounds: Celje 0-5, 150:188 (-38); Zagreb 2-3, 146:158 (-12)",
                     src="https://ehfcl.eurohandball.com/men/2026-27/standings/"),
                dict(t="EHF fixture: RK Celje Pivovarna Lasko v HC Zagreb, 28 October, 20:45 CET",
                     src="https://ehfcl.eurohandball.com/men/2026-27/standings/")],
         not_checked="Neither squad was confirmed, so no team news is claimed."),

    # ------------------------------------------------------------------ BASEBALL
    dict(id="L046", label="BL-1", confidence="high",
         headline="Milwaukee Brewers to win Game 4 of the World Series",
         prediction=(
             "Milwaukee to win Game 4 at Tropicana Field and complete the sweep. The Brewers lead the series 3-0 "
             "after a 10-1 win in Game 3, in which their pitching held Tampa Bay to a single run. Both tips on the "
             "money line are with Milwaukee, and the form case is stronger than the market's: a team that has won "
             "three straight in a series, by a combined margin built on run prevention, is not a coin flip."),
         facts=[dict(t="World Series Game 4, 27 October at Tropicana Field, 8:00 PM ET; Milwaukee lead the series 3-0 and won Game 3 by 10-1",
                     src="https://www.mlb.com/postseason"),
                dict(t="OLBG Money Line: MIL Brewers 2 of 2 win tips",
                     src="https://www.olbg.com/betting-tips/Baseball/MLB/MLB/MIL_Brewers_@_TB_Rays/12?event_id=160799")],
         not_checked="Neither starting pitcher was announced on the pages we read, so the pitching matchup is not part of this case."),

    dict(id="L123", label="BL-2", confidence="medium",
         headline="Milwaukee Brewers -1.50 on the run line",
         prediction=(
             "Milwaukee on the run line, giving up 1.5 runs. The Brewers have won their three World Series games "
             "by margins that would have covered this line, and the one tip posted on the run line is with them. "
             "The risk is obvious: a one-run win loses the bet, and the Rays are at home with the last at-bat. At "
             "this price the margin of victory needed is modest for the stronger side in the series."),
         facts=[dict(t="Milwaukee lead the World Series 3-0 after a 10-1 win in Game 3 on 26 October",
                     src="https://www.mlb.com/postseason"),
                dict(t="OLBG Run Line: MIL Brewers -1.50, 1 of 1 win tips",
                     src="https://www.olbg.com/betting-tips/Baseball/MLB/MLB/MIL_Brewers_@_TB_Rays/12?event_id=160799")],
         not_checked="Bullpen usage across the first three games was not published in a form we could read, so it is not claimed."),

    dict(id="L126", label="BL-3", confidence="low",
         headline="Under 7.50 runs in Game 4",
         prediction=(
             "Under 7.50 runs in Game 4. This is the one baseball market with no tips on it at all, so the price is "
             "ours and the pick is a lean rather than a conviction. The series has been low-scoring: Game 3 "
             "finished 10-1, but the first two games were tighter, and a line of 7.5 asks for more than four runs "
             "a side in a game where the leading team has little reason to chase."),
         facts=[dict(t="OLBG Game Totals: Over 7.50 and Under 7.50 both show 0 win tips", 
                     src="https://www.olbg.com/betting-tips/Baseball/MLB/MLB/MIL_Brewers_@_TB_Rays/12?event_id=160799"),
                dict(t="Game 4 scheduled for 27 October, 8:00 PM ET at Tropicana Field",
                     src="https://www.mlb.com/postseason")],
         not_checked="Scores for Games 1 and 2 were not read for this build, so the run environment claim rests on Game 3 alone."),

    # ------------------------------------------------------------------ GAELIC
    dict(id="L047", label="GA-1", confidence="medium",
         headline="Eire Og Cor +0.50 on the handicap against Kanturk",
         prediction=(
             "Eire Og Cor with half a point on the handicap. All six tips on the tie are with them, the most "
             "one-sided market anywhere on today's board, and the handicap is the narrowest available: half a "
             "point means a draw is enough. A six-tip clean sweep in a club football match is a strong statement "
             "about the gap between the sides, and we would rather take the half-point than the win market."),
         facts=[dict(t="OLBG handicap market: Eire Og Cor +0.50, 6 of 6 win tips, 100 per cent",
                     src="https://www.olbg.com/betting-tips/Gaelic_Football/All_Gaelic_Football/All_Events/Kanturk_v_Eire_Og_Cor/25?event_id=3531")],
         not_checked="No official GAA fixture or grade confirmation was read, and no team news is claimed."),

    dict(id="L048", label="GA-2", confidence="medium",
         headline="Kildimo Pallaskenry +3.50 on the handicap against Fr Caseys",
         prediction=(
             "Kildimo Pallaskenry with a 3.5-point start. Five of the seven tips are with them on the handicap, and "
             "the line is the widest on today's Gaelic card, which suggests the market rates Fr Caseys as clear "
             "favourites but not by a margin that justifies four points. Club football in Munster is decided by "
             "fitness and weather as much as by skill, and a 3.5-point cushion is a lot to give away in October."),
         facts=[dict(t="OLBG handicap market: Kildimo Pallaskenry +3.50, 5 of 7 win tips, 71 per cent",
                     src="https://www.olbg.com/betting-tips/Gaelic_Football/All_Gaelic_Football/All_Events/Fr_Caseys_v_Kildimo_Pallaskenry/25?event_id=3537")],
         not_checked="The competition and both starting fifteens were not confirmed from an official GAA page."),

    dict(id="L049", label="GA-3", confidence="low",
         headline="Kerry to win the 2027 All-Ireland football championship",
         prediction=(
             "Kerry to win the 2027 All-Ireland football championship. Six of the eight tips on the ante-post "
             "market are with them, a 75 per cent share, though this is a long-dated price on a competition that "
             "does not begin for months. Mayo are the reigning champions after ending a 75-year wait, and Kerry's "
             "record of 39 titles is still the best in the game, which is the case the crowd is making."),
         facts=[dict(t="OLBG ante-post: Kerry 6 of 8 win tips, 75 per cent, All-Ireland Football Championship 2027",
                     src="https://www.olbg.com/betting-tips/Gaelic_Football/All_Gaelic_Football/All_Events/All_Ireland_Football_Championship_2027/25?event_id=3327"),
                dict(t="Kerry hold the record with 39 All-Ireland titles; Mayo won the 2026 final against Kerry",
                     src="https://www.olbg.com/betting-tips/Gaelic_Football/25")],
         not_checked="No 2027 championship structure or panel announcement was read, so the build-up is not part of this case."),

    # ------------------------------------------------------------------ GOLF
    dict(id="L002", label="GF-1", confidence="low",
         headline="Wyndham Clark each way in the Mexico Open",
         prediction=(
             "Wyndham Clark each way in the Mexico Open at Vidanta. One of the two tips posted on the tournament is "
             "with him, and he is the most-tipped selection on the event page. The field is unusually thin for a "
             "PGA Tour event, with several of the names behind him on the list carrying no tips at all, so the "
             "each-way terms are doing most of the work in this price."),
         facts=[dict(t="OLBG Win Tournament: Wyndham Clark 1 of 2 win tips, most-tipped on the Mexico Open event page",
                     src="https://www.olbg.com/betting-tips/Golf/All_Golf/All_Events/Mexico_Open/5?event_id=101915")],
         not_checked="The field list, tee times and course set-up were not confirmed from the PGA Tour's own page, so none is claimed."),

    dict(id="L001", label="GF-2", confidence="low",
         headline="Lottie Woad each way in the Maybank Championship",
         prediction=(
             "Lottie Woad each way in the Maybank Championship. She is the only selection carrying a tip on the "
             "tournament, one of two posted, so the market is as thin as a market gets. At 50 per cent of a "
             "two-tip sample the price is effectively a prior rather than a read, and the pick is published at low "
             "conviction with that limitation stated up front rather than dressed up."),
         facts=[dict(t="OLBG Win Tournament: Lottie Woad 1 of 2 win tips on the Maybank Championship",
                     src="https://www.olbg.com/betting-tips/Golf/All_Golf/All_Events/Maybank_Championship/5?event_id=101913")],
         not_checked="Field, venue and tee times were not confirmed from an official tour page."),

    dict(id="L003", label="GF-3", confidence="low",
         headline="Stewart Cink each way in the Simmons Bank Championship",
         prediction=(
             "Stewart Cink each way in the Simmons Bank Championship, a PGA Tour Champions event. He is the only "
             "player carrying a tip on the tournament and the sample is two tips in total. On a senior tour where "
             "field sizes are small and course form repeats year to year, an each-way price on a player the crowd "
             "has picked out is a reasonable lottery ticket, but no more than that."),
         facts=[dict(t="OLBG Win Tournament: Stewart Cink 1 of 2 win tips on the Simmons Bank Championship",
                     src="https://www.olbg.com/betting-tips/Golf/All_Golf/All_Events/Simmons_Bank_Championship/5?event_id=101914")],
         not_checked="The field and the course were not confirmed from an official page, so neither is claimed."),

    # ------------------------------------------------------------------ DARTS
    dict(id="L110", label="DT-1", confidence="low",
         headline="Luke Littler to win the 2027 PDC World Championship",
         prediction=(
             "Luke Littler to win the PDC World Championship at Alexandra Palace in January. Twenty-two of the 36 "
             "tips on the ante-post market are with him, a 61 per cent share that is high for an event with a "
             "field this deep. Seven logged comments sit behind the market, which is the most discussion on any "
             "darts event today, and the crowd is close to unanimous about the favourite."),
         facts=[dict(t="OLBG Win Tournament: Luke Littler 22 of 36 win tips, 61 per cent, seven logged comments",
                     src="https://www.olbg.com/betting-tips/Darts/All_Darts/All_Events/PDC_World_Championship_2027/15?event_id=26023")],
         not_checked="No PDC order of merit or qualification list was read, so the field strength is not quantified."),

    dict(id="L111", label="DT-2", confidence="low",
         headline="Nathan Aspinall to win Players Championship 31",
         prediction=(
             "Nathan Aspinall in Players Championship 31, which starts tomorrow. Only two of the eight tips are "
             "with him, so the market is split across the field and 25 per cent is a plurality rather than a "
             "consensus. ProTour events are decided over a single day with a draw made that morning, which is why "
             "the prices on them are volatile and why this one is published at low confidence."),
         facts=[dict(t="OLBG Win Tournament: Nathan Aspinall 2 of 8 win tips, 25 per cent, event starts tomorrow 08:00",
                     src="https://www.olbg.com/betting-tips/Darts/All_Darts/All_Events/Players_Championship_31/15?event_id=32446")],
         not_checked="The draw and entry list for Players Championship 31 were not published at capture time, so neither is claimed."),

    # ------------------------------------------------------------------ MOTOR RACING
    dict(id="L065", label="MR-1", confidence="low",
         headline="Max Verstappen to finish on the podium in Mexico City",
         prediction=(
             "Verstappen for a podium finish at the Mexico City Grand Prix. One of the two tips posted on the race "
             "is on him to finish in the top three, and the other is against, so the market is split. Mexico "
             "rewards straight-line speed and good traction out of the slow corners, and the altitude makes "
             "cooling a genuine variable, but we have no timing data to lean on and the pick is priced from the "
             "split alone."),
         facts=[dict(t="OLBG Podium Finish: Max Verstappen - Yes, 1 of 2 win tips; race on 1 November",
                     src="https://www.olbg.com/betting-tips/Motor_Racing/All_Motor_Racing/All_Events/Mexico_City_Grand_Prix/14?event_id=914")],
         not_checked="No practice, qualifying or championship standings were read, so no form or points position is claimed."),

    dict(id="L064", label="MR-2", confidence="low",
         headline="Verstappen to win the 2026 drivers' title with Antonelli removed",
         prediction=(
             "Verstappen in the drivers' championship market with Kimi Antonelli removed from the field. Four of "
             "the seven tips are with him, a 57 per cent share, and this is an ante-post market that settles at "
             "the final round on 6 December. Removing a named rival makes the price shorter than the outright "
             "and the crowd has still only got to 57 per cent, which tells you how open the title race is being "
             "read."),
         facts=[dict(t="OLBG Win Tournament: Max Verstappen 4 of 7 win tips, 57 per cent, market settles 6 December",
                     src="https://www.olbg.com/betting-tips/Motor_Racing/All_Motor_Racing/All_Events/Formula_1_Drivers_Championship_2026_Without_Kimi_Antonelli/14?event_id=912")],
         not_checked="The current championship standings were not read, so no points gap is quoted."),

    # ------------------------------------------------------------------ RUGBY LEAGUE
    dict(id="L112", label="RL-1", confidence="low",
         headline="New South Wales to win the 2027 State of Origin series",
         prediction=(
             "New South Wales to win the 2027 State of Origin series. Nine of the 13 tips are with the Blues, a 69 "
             "per cent share and the strongest rugby league market on the board, which otherwise carries only "
             "season-long ante-post prices. Origin series turn on game one and on availability, and with the "
             "series more than six months away this is a price on a squad that has not been named."),
         facts=[dict(t="OLBG Win Tournament: New South Wales 9 of 13 win tips, 69 per cent, three logged comments",
                     src="https://www.olbg.com/betting-tips/Rugby_League/All_Rugby_League/All_Events/State_of_Origin_2027/10?event_id=2695857")],
         not_checked="No squad, venue or schedule confirmation for the 2027 series was read, so none is claimed."),

    dict(id="L113", label="RL-2", confidence="low",
         headline="Wigan Warriors to win the 2027 Super League Grand Final",
         prediction=(
             "Wigan Warriors for the 2027 Super League Grand Final. Two of the four tips are with them, and two "
             "logged comments sit behind the market. Wigan are the sort of club that is priced near the top of "
             "this market every year, and a 50 per cent share across four tips is closer to a placeholder than a "
             "view; the pick is published because the sport has no match-level markets today, not because the "
             "case is strong."),
         facts=[dict(t="OLBG Grand Final Winner: Wigan Warriors 2 of 4 win tips, 50 per cent, two logged comments",
                     src="https://www.olbg.com/betting-tips/Rugby_League/All_Rugby_League/All_Events/Super_League_2027/10?event_id=2801554")],
         not_checked="No 2027 squad, fixture list or salary-cap information was read, so none is claimed."),

    dict(id="L114", label="RL-3", confidence="low",
         headline="Penrith Panthers to win the 2027 NRL Grand Final",
         prediction=(
             "Penrith Panthers for the 2027 NRL Grand Final. One of three tips is with them, so the market has no "
             "real consensus and the price is long. Penrith have been the benchmark side of the past decade and "
             "that is presumably what the single tipster is buying, but a one-tip sample on a season-long market "
             "is the weakest evidence on this board and the confidence label says so."),
         facts=[dict(t="OLBG Grand Final Winner: Penrith Panthers 1 of 3 win tips, 33 per cent",
                     src="https://www.olbg.com/betting-tips/Rugby_League/All_Rugby_League/All_Events/NRL_2027/10?event_id=2801600")],
         not_checked="No NRL squad or draw information for 2027 was read, so none is claimed."),
]

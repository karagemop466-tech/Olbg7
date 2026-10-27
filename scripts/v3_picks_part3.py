#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3 picks part 3 - Darts, Baseball, Motor Racing, Rugby League, Gaelic Sports."""

PICKS = []


def add(**kw):
    PICKS.append(kw)


# =============================================================================
# DARTS
# =============================================================================
add(sport="Darts", event="PDC World Championship 2027",
    competition="PDC World Darts Championship 2027, Alexandra Palace",
    when="Settles January 2027", venue="Alexandra Palace, London",
    market="Win Tournament", selection="Luke Littler to win the tournament",
    line="-111", probability=0.525, track="T", tier="A", confidence="HIGH",
    in_band=True, olbg="22 of 36 tips (61%)",
    text=("Littler is PDC world No. 1 on £3,141,000 of ranking money, roughly three times the "
          "£1,058,250 carried by second-placed Gian van Veen, and he is the two-time defending "
          "champion. In the 2026 final at Alexandra Palace he beat van Veen 7-1 in just over 43 "
          "minutes, averaging 106.02 against 99.94 with 16 maximums and 46 per cent of his "
          "attempts at double, becoming the first million-pound world champion and only the fourth "
          "man to retain the Sid Waddell Trophy after Phil Taylor, Adrian Lewis and Gary Anderson. "
          "He has since collected six major ranking titles in a calendar year - the World "
          "Championship, World Masters, UK Open, World Matchplay, Premier League and Grand Slam - "
          "plus the World Cup with England. In the provisional qualifying race for 2027 seeding he "
          "holds £2,859.5k against van Veen's £941.25k, a lead approaching two million pounds. "
          "Twenty-two of the 36 tips on OLBG sit with him and our price is -111, the deepest "
          "outright sample on the board."),
    sources=[("PDC - official Order of Merit and world rankings", "https://www.pdc.tv/rankings"),
             ("PDC - Littler retains the World Darts Championship title",
              "https://www.pdc.tv/news/2026-01-03/astounding-littler-retains-paddy-power-world-darts-championship-title"),
             ("BBC Sport - Littler beats van Veen 7-1 in the 2026 final",
              "https://www.bbc.com/sport/darts/articles/cq5y28xg5z7o"),
             ("2027 World Championship qualifying race",
              "https://dartsnews.com/pdc/2027-world-darts-championship-qualifying-race-littler-firmly-on-top-concerns-for-van-gerwen-and-van-barneveld")],
    flag=None)

add(sport="Darts", event="Players Championship 31",
    competition="PDC Pro Tour 2026, Players Championship 31 of 34",
    when="Wednesday 28 October 2026", venue="Maaspoort, Den Bosch, Netherlands",
    market="Win Tournament", selection="Wessel Nijman to win the event",
    line="+550", probability=0.154, track="T", tier="B", confidence="MEDIUM",
    in_band=True, olbg="2 of 8 tips (25%) - four-way tie for most-tipped",
    text=("Nijman tops the Players Championship Order of Merit on £150,250 after 29 events and is "
          "thirteenth on the main PDC Order of Merit at £577,250. He has won six Players "
          "Championship titles this year - beating Gerwyn Price 8-7 in event two, Joe Cullen 8-4 "
          "in event eight, Scott Waites 8-2 in event ten, Jermaine Wattimena 8-5 in event twelve, "
          "Max Hopp 8-1 in event fourteen and Ryan Searle 8-6 in event twenty-one - the first "
          "player to six floor titles in a calendar year since Michael van Gerwen managed it in "
          "2012. This week's event is the 31st of 34, carrying a £150,000 prize fund with £15,000 "
          "to the winner, played best of 11 legs through to the semi-finals, 13 in the semis and "
          "15 in the final. Our tip-derived price is +550, well inside the band, but only two of "
          "eight tips sit with him and OLBG's own listing page disagrees with its event page about "
          "which player is most tipped."),
    sources=[("2026 PDC Players Championship series", "https://en.wikipedia.org/wiki/2026_PDC_Pro_Tour"),
             ("Wessel Nijman - 2026 titles", "https://en.wikipedia.org/wiki/Wessel_Nijman"),
             ("Nijman's sixth strike, Den Bosch", "https://www.dartn.de/news/players-championship-nijman-mit-dem-sechsten-streich/"),
             ("Players Championship Order of Merit after event 29",
              "https://dartsnews.com/pdc/nathan-aspinall-still-faces-minehead-fight-despite-den-bosch-run-as-gary-anderson-hangs-on-in-players-championship-order-of-merit")],
    flag="OLBG's Darts listing page names Nathan Aspinall as the most popular Players Championship 31 "
         "selection; the event page names Wessel Nijman. Both print at 2/8, a four-way tie.")

add(sport="Darts", event="Players Championship 31",
    competition="PDC Pro Tour 2026, Players Championship 31 of 34",
    when="Wednesday 28 October 2026", venue="Maaspoort, Den Bosch, Netherlands",
    market="Win Tournament", selection="Kevin Doets to win the event",
    line="+550", probability=0.154, track="T", tier="B", confidence="MEDIUM",
    in_band=True, olbg="2 of 8 tips (25%) - four-way tie for most-tipped",
    text=("Doets is second on the Players Championship Order of Merit on £106,250, behind only "
          "Wessel Nijman, and ahead of Chris Dobey on £102,500, Luke Woodhouse on £88,000, Andrew "
          "Gilding on £79,500 and Jermaine Wattimena on £79,250 - all of whom are in this week's "
          "field at Maaspoort. The top 64 on that Order of Merit qualify for the Players "
          "Championship Finals in November, so Den Bosch is a points-and-money week for a player "
          "already comfortably inside the cut. Michael van Gerwen sits 34th on £43,750 and is one "
          "of the names he will pass through. Our tip-derived price is +550 against a field we "
          "count at 40 qualifiers, with two of eight tips behind him."),
    sources=[("2026 PDC Players Championship series", "https://en.wikipedia.org/wiki/2026_PDC_Pro_Tour"),
             ("Players Championship Order of Merit after event 29",
              "https://dartsnews.com/pdc/nathan-aspinall-still-faces-minehead-fight-despite-den-bosch-run-as-gary-anderson-hangs-on-in-players-championship-order-of-merit"),
             ("Nijman's sixth strike, Den Bosch - prize fund and format",
              "https://www.dartn.de/news/players-championship-nijman-mit-dem-sechsten-streich/")],
    flag=None)

add(sport="Darts", event="Players Championship 31",
    competition="PDC Pro Tour 2026, Players Championship 31 of 34",
    when="Wednesday 28 October 2026", venue="Maaspoort, Den Bosch, Netherlands",
    market="Win Tournament", selection="Gian van Veen to win the event",
    line="+1118", probability=0.082, track="T", tier="B", confidence="MEDIUM",
    in_band=True, olbg="1 of 8 tips (13%)",
    text=("Van Veen is PDC world No. 2 on £1,058,250, the closest man to Luke Littler in the "
          "rankings and the runner-up in the 2026 World Championship final that Littler took 7-1 "
          "at Alexandra Palace. That final is the reason we treat him as the strongest outsider in "
          "this week's field: a player who reaches the final of the biggest event on the calendar "
          "is not one to dismiss on the floor, and the £15,000 first prize at Den Bosch is worth "
          "having in the provisional race for 2027 seeding, where van Veen sits on £941.25k behind "
          "Littler's £2,859.5k. Only one of eight tips is with him, so our tip-derived price of "
          "+1118 is long - but it is inside the band and the ranking behind it is official."),
    sources=[("PDC - official Order of Merit and world rankings", "https://www.pdc.tv/rankings"),
             ("PDC - Littler beats van Veen in the 2026 final",
              "https://www.pdc.tv/news/2026-01-03/astounding-littler-retains-paddy-power-world-darts-championship-title"),
             ("2027 World Championship qualifying race",
              "https://dartsnews.com/pdc/2027-world-darts-championship-qualifying-race-littler-firmly-on-top-concerns-for-van-gerwen-and-van-barneveld")],
    flag=None)

add(sport="Darts", event="Players Championship 31",
    competition="PDC Pro Tour 2026, Players Championship 31 of 34",
    when="Wednesday 28 October 2026", venue="Maaspoort, Den Bosch, Netherlands",
    market="Win Tournament", selection="Nathan Aspinall to win the event",
    line="+550", probability=0.154, track="T", tier="B", confidence="MEDIUM",
    in_band=True, olbg="2 of 8 tips (25%) - named most popular on the OLBG listing page",
    text=("Aspinall carries two of the eight tips on this event and is the player OLBG's Darts "
          "listing page names as the most popular selection, although the event page itself prints "
          "Nijman in that slot - a contradiction we flag rather than resolve. The competitive "
          "context is that Aspinall is still working to secure his place at the Players "
          "Championship Finals in Minehead, where the top 64 on the floor Order of Merit qualify, "
          "and a run in Den Bosch is worth a great deal to him for exactly that reason. The event "
          "carries a £150,000 prize fund with £15,000 to the winner. Our tip-derived price is "
          "+550, inside the band."),
    sources=[("Aspinall still faces a Minehead fight despite his Den Bosch run",
              "https://dartsnews.com/pdc/nathan-aspinall-still-faces-minehead-fight-despite-den-bosch-run-as-gary-anderson-hangs-on-in-players-championship-order-of-merit"),
             ("2026 PDC Players Championship series", "https://en.wikipedia.org/wiki/2026_PDC_Pro_Tour")],
    flag="OLBG's Darts listing page names Aspinall as the most popular Players Championship 31 "
         "selection; the event page names Nijman.")

# =============================================================================
# BASEBALL
# =============================================================================
add(sport="Baseball", event="Milwaukee Brewers @ Tampa Bay Rays",
    competition="2026 World Series, Game 4",
    when="Tuesday 27 October 2026, 8:00pm ET", venue="Tropicana Field, St Petersburg",
    market="Money Line", selection="Milwaukee Brewers to win the game",
    line="-167", probability=0.625, track="T", tier="D", confidence="MEDIUM",
    in_band=True, olbg="2 of 2 tips (100%)",
    text=("Milwaukee lead the best-of-seven 3-0 and are one win from the title: Game 1 on Friday "
          "23 October 3-2, Game 2 on Saturday 24 October 5-4, Game 3 on Monday 26 October 10-1. "
          "The Brewers finished the regular season 103-59 against Tampa Bay's 98-64 and hold "
          "home-field advantage, although the Rays host Games 3, 4 and 5 at Tropicana Field. Tampa "
          "won the American League pennant by beating the Cleveland Guardians in ALCS Game 6 "
          "behind a Junior Caminero home run, and this is their first World Series since 2020 and "
          "only their third in franchise history after losing the 2008 final to Philadelphia. Both "
          "tips on the OLBG money line are with Milwaukee and our tip-derived price is -167. The "
          "sample is only two tips, which is what keeps this out of the top grade."),
    sources=[("MLB.com - 2026 playoff and World Series schedule and scores",
              "https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule"),
             ("MLB.com - 2026 World Series FAQ",
              "https://www.mlb.com/news/2026-mlb-world-series-faq-schedule-times-teams-and-more"),
             ("CBS Sports - Rays win the AL pennant",
              "https://www.cbssports.com/mlb/news/2026-mlb-playoff-bracket-schedule-scores-results-how-to-watch/")],
    flag="OLBG prints this game at 'Today 21:00' while MLB.com and FOX both print 8:00 p.m. ET.")

add(sport="Baseball", event="Milwaukee Brewers @ Tampa Bay Rays",
    competition="2026 World Series, Game 4",
    when="Tuesday 27 October 2026, 8:00pm ET", venue="Tropicana Field, St Petersburg",
    market="Run Line", selection="Milwaukee Brewers -1.50",
    line="-133", probability=0.571, track="T", tier="D", confidence="MEDIUM",
    in_band=True, olbg="1 of 1 tips (100%)",
    text=("Milwaukee need to win by two or more runs for the -1.50 run line to land, and the "
          "official scores of this series show how narrow that ask has been. Game 1 finished 3-2, "
          "Game 2 5-4 - both one-run games that would have lost on this line - and only Game 3, "
          "10-1, covered it comfortably. So the run line has cashed once in three while the money "
          "line has cashed three times. We still publish the Brewers at -1.50 because that is the "
          "only tip on the OLBG run line market and our tip-derived price is -133, but the "
          "three-game pattern is a real warning and we say so rather than hide it."),
    sources=[("MLB.com - 2026 playoff and World Series schedule and scores",
              "https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule"),
             ("ESPN - 2026 MLB playoff schedule and results",
              "https://www.espn.com/mlb/story/_/id/50022544/2026-mlb-playoffs-schedule-how-watch-postseason-world-series-bracket-standings")],
    flag=None)

add(sport="Baseball", event="Milwaukee Brewers @ Tampa Bay Rays",
    competition="2026 World Series, Game 4",
    when="Tuesday 27 October 2026, 8:00pm ET", venue="Tropicana Field, St Petersburg",
    market="Run Line", selection="Tampa Bay Rays +1.50",
    line="+167", probability=0.375, track="T", tier="D", confidence="MEDIUM",
    in_band=True, olbg="0 of 1 tips (0%) - we are against the single tip posted",
    text=("The Rays are 3-0 down but two of the three games they have lost went to the final "
          "margin: 3-2 on Friday and 5-4 on Saturday, both of which would have paid out on a "
          "+1.50 run line, with only Monday's 10-1 defeat losing on it. Tampa have been inside "
          "every game they have played except the third, and Game 4 is at Tropicana Field where "
          "they host Games 3, 4 and 5. Our tip-derived price from the single tip posted on the "
          "OLBG market is +167 - the one baseball line on this board that goes against the tip "
          "flow, because that flow has no tips on the Rays at all. Two of three games covering is "
          "a thin sample and we grade accordingly."),
    sources=[("MLB.com - 2026 playoff and World Series schedule and scores",
              "https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule"),
             ("MLB.com - 2026 World Series FAQ",
              "https://www.mlb.com/news/2026-mlb-world-series-faq-schedule-times-teams-and-more")],
    flag=None)

add(sport="Baseball", event="Milwaukee Brewers @ Tampa Bay Rays",
    competition="2026 World Series, Game 4",
    when="Tuesday 27 October 2026, 8:00pm ET", venue="Tropicana Field, St Petersburg",
    market="Game Totals", selection="Over 7.50 runs",
    line="-137", probability=0.578, track="R", tier="R", confidence="MEDIUM",
    in_band=True, olbg="0 of 0 tips - the line is printed but nobody has tipped either side",
    text=("OLBG prints a 7.50 game total for this match with no tips on either side, so we "
          "originated the number ourselves from the official scores of the three games already "
          "played. Those totals were 5 runs, 9 runs and 11 runs, an average of 8.33, and two of "
          "the three cleared 7.50. Treating the run total as Poisson at the observed series mean "
          "puts the chance of eight or more runs at about 0.578, which prices Over 7.50 at -137 "
          "and Under at +137. Three games is a very small sample and Monday's 10-1 blowout does a "
          "lot of the work, so this is graded down - but it is a number we can show the working "
          "for, rather than a price taken on faith."),
    sources=[("MLB.com - 2026 playoff and World Series schedule and scores",
              "https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule"),
             ("ESPN - 2026 MLB playoff schedule and results",
              "https://www.espn.com/mlb/story/_/id/50022544/2026-mlb-playoffs-schedule-how-watch-postseason-world-series-bracket-standings")],
    flag=None)

add(sport="Baseball", event="Milwaukee Brewers to win the 2026 World Series",
    competition="2026 World Series, series outcome",
    when="Series concludes no later than Saturday 1 November 2026",
    venue="Tropicana Field / American Family Field",
    market="Win Series", selection="Milwaukee Brewers to win the World Series",
    line="-4900", probability=0.980, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="no market published on OLBG for the series outcome",
    text=("This is a line we originated ourselves because OLBG publishes no market for the series "
          "outcome, only for Game 4. Milwaukee lead 3-0 and need one more win from up to four "
          "remaining games, while Tampa Bay need to win all four. Taking our own Game 4 money line "
          "of -167, which implies a 0.625 chance for Milwaukee, the chance of Tampa winning four "
          "in a row is 0.375 to the power of four, or about 0.020 - leaving Milwaukee at 0.980 and "
          "-4900. The Brewers finished 103-59 to Tampa's 98-64 and have outscored them 18-7 across "
          "the three games played. The price is far outside the band we hold top-grade picks to, "
          "which is why this grades down despite the series being all but decided."),
    sources=[("MLB.com - 2026 World Series FAQ",
              "https://www.mlb.com/news/2026-mlb-world-series-faq-schedule-times-teams-and-more"),
             ("MLB.com - 2026 playoff and World Series schedule and scores",
              "https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule")],
    flag="OLBG publishes no series-outcome market for the World Series; this line is originated "
         "from our own Game 4 money line.")

# =============================================================================
# MOTOR RACING
# =============================================================================
add(sport="Motor Racing", event="Mexico City Grand Prix",
    competition="2026 FIA Formula One World Championship, round of Sunday 1 November 2026",
    when="Sunday 1 November 2026", venue="Autodromo Hermanos Rodriguez, Mexico City",
    market="Podium Finish", selection="Max Verstappen - Podium Finish: Yes",
    line="-125", probability=0.556, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="1 of 2 tips (50%)",
    text=("Verstappen has taken ten podiums across the eighteen rounds of the 2026 season "
          "completed so far, and at the United States Grand Prix in Austin on 25 October he "
          "finished third, 17.485 seconds behind winner Kimi Antonelli, to take 15 points and sit "
          "fourth in the championship on 236. Ten podiums from eighteen starts is 0.556, which is "
          "exactly the base rate our line is built on, and it prices Verstappen to finish on the "
          "podium in Mexico City at -125 and No at +125. The race is a 71-lap event around a "
          "4.3-kilometre circuit. This is the only motor-racing market on the board where our "
          "price, our base rate and OLBG's tip all point the same way and sit inside the band."),
    sources=[("Formula One - official 2026 Drivers' Standings",
              "https://www.formula1.com/en/results/2026/drivers"),
             ("Formula One - official United States Grand Prix result, Austin, 25 October 2026",
              "https://www.formula1.com/en/latest/article/antonelli-surges-to-dominant-victory-in-united-states-grand-prix-ahead-of-leclerc-and-verstappen.6kmBQv9FNTW7LzkDj8S34j"),
             ("BBC Sport - 2026 Formula 1 standings", "https://www.bbc.com/sport/formula1/standings")],
    flag=None)

add(sport="Motor Racing", event="2026 Drivers' Championship without Kimi Antonelli",
    competition="2026 FIA Formula One World Championship",
    when="Season concludes 6 December 2026", venue="Five rounds remaining",
    market="Win Tournament",
    selection="George Russell to win the Drivers' Championship without Kimi Antonelli",
    line="+198", probability=0.336, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="4 of 7 tips on Max Verstappen (57%) - we are against the tip flow",
    text=("Antonelli leads the championship on 365 points with nine wins, and a finish of ninth or "
          "better at the Autodromo Hermanos Rodriguez takes the title. Behind him the race is "
          "tight: George Russell is second on 242, Lewis Hamilton third on 241, Max Verstappen "
          "fourth on 236, Charles Leclerc fifth on 233 and Lando Norris sixth on 211. With 125 "
          "points still available across the final five rounds, Russell leads the non-Antonelli "
          "contenders by a single point and we weight each of them by the gap he has to close, "
          "treating 25 points - one Grand Prix win - as the unit. That prices Russell +198, "
          "Hamilton +227, Verstappen +418, Leclerc +583 and Norris +5081. OLBG has four of seven "
          "tips on Verstappen, who is six points behind Russell, which we flag rather than follow. "
          "Oscar Piastri on 144 and Isack Hadjar on 105 are more than two wins back and are left "
          "out of the price."),
    sources=[("Formula One - official 2026 Drivers' Standings",
              "https://www.formula1.com/en/results/2026/drivers"),
             ("BBC Sport - Antonelli needs ninth or better to take the title",
              "https://www.bbc.com/sport/formula1/live/c87w8r725y8t"),
             ("BBC Sport - 2026 Formula 1 standings", "https://www.bbc.com/sport/formula1/standings")],
    flag="OLBG tips Verstappen 4/7 to win without Antonelli, although the official standings put "
         "him six points behind Russell. Piastri and Hadjar are excluded as more than two race "
         "wins adrift.")

add(sport="Motor Racing", event="Mexico City Grand Prix",
    competition="2026 FIA Formula One World Championship, round of Sunday 1 November 2026",
    when="Sunday 1 November 2026", venue="Autodromo Hermanos Rodriguez, Mexico City",
    market="Podium Finish", selection="Kimi Antonelli - Podium Finish: Yes",
    line="-500", probability=0.833, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="0 of 2 tips (0%) - nobody has tipped the championship leader",
    text=("Antonelli has fifteen podiums from eighteen rounds, nine wins, and leads the "
          "championship on 365 points, and he won at Austin on 25 October in 1:35:16.650. Fifteen "
          "out of eighteen is 0.833, which prices him to finish on the podium again at -500 - a "
          "number outside the band we hold top-grade picks to, and the only reason this grades "
          "down. The striking thing is that both tips posted on OLBG's podium market are against "
          "him: Antonelli Yes carries zero of two, while Verstappen and Leclerc each carry one of "
          "two. The championship leader, who would clinch the title with a ninth place here, is "
          "the one runner nobody on the site has tipped, and that is flagged."),
    sources=[("Formula One - official 2026 Drivers' Standings",
              "https://www.formula1.com/en/results/2026/drivers"),
             ("Formula One - official United States Grand Prix result, Austin",
              "https://www.formula1.com/en/latest/article/antonelli-surges-to-dominant-victory-in-united-states-grand-prix-ahead-of-leclerc-and-verstappen.6kmBQv9FNTW7LzkDj8S34j"),
             ("BBC Sport - 2026 Formula 1 standings", "https://www.bbc.com/sport/formula1/standings")],
    flag="OLBG's podium market carries 0/2 tips on Antonelli Yes although he leads the championship "
         "with 15 podiums in 18 rounds.")

add(sport="Motor Racing", event="Mexico City Grand Prix",
    competition="2026 FIA Formula One World Championship, round of Sunday 1 November 2026",
    when="Sunday 1 November 2026", venue="Autodromo Hermanos Rodriguez, Mexico City",
    market="Podium Finish", selection="Charles Leclerc - Podium Finish: Yes",
    line="+200", probability=0.333, track="R", tier="R", confidence="MEDIUM",
    in_band=True, olbg="1 of 2 tips (50%)",
    text=("Leclerc has six podiums from the eighteen rounds completed this season and sits fifth in "
          "the championship on 233 points. He took one of them at Austin on 25 October, finishing "
          "second, 13.078 seconds behind Antonelli and ahead of Verstappen and Hamilton, so he "
          "arrives in Mexico City off a genuine front-row result rather than a distant points "
          "finish. Six from eighteen is 0.333, which prices him at +200 to finish on the podium "
          "again and -100 not to. Our price is inside the band and one of the two tips OLBG "
          "carries on this market is with him, but a third-of-the-time base rate is not enough to "
          "grade highly."),
    sources=[("Formula One - official United States Grand Prix result, Austin",
              "https://www.formula1.com/en/latest/article/antonelli-surges-to-dominant-victory-in-united-states-grand-prix-ahead-of-leclerc-and-verstappen.6kmBQv9FNTW7LzkDj8S34j"),
             ("Formula One - official 2026 Drivers' Standings",
              "https://www.formula1.com/en/results/2026/drivers"),
             ("BBC Sport - 2026 Formula 1 standings", "https://www.bbc.com/sport/formula1/standings")],
    flag=None)

add(sport="Motor Racing", event="2026 Drivers' Championship without Kimi Antonelli",
    competition="2026 FIA Formula One World Championship",
    when="Season concludes 6 December 2026", venue="Five rounds remaining",
    market="Win Tournament",
    selection="Lewis Hamilton to win the Drivers' Championship without Kimi Antonelli",
    line="+227", probability=0.306, track="R", tier="R", confidence="MEDIUM",
    in_band=True, olbg="no tips published for this runner",
    text=("Hamilton is third in the championship on 241 points, a single point behind team-mate "
          "George Russell and six clear of Max Verstappen, and he has taken six podiums this "
          "season. At Austin on 25 October he finished fourth, 18.515 seconds behind winner Kimi "
          "Antonelli and half a second adrift of Verstappen, which is the sort of margin that "
          "keeps a title race alive with five rounds and 125 points still to play for. Our own "
          "weighting of the gap each contender has to close prices Hamilton at +227 to take the "
          "title without Antonelli, inside the band, against Russell's +198. No tips are posted on "
          "him, and a one-point deficit to his team-mate is why this grades down rather than up."),
    sources=[("Formula One - official 2026 Drivers' Standings",
              "https://www.formula1.com/en/results/2026/drivers"),
             ("Formula One - official United States Grand Prix result, Austin",
              "https://www.formula1.com/en/latest/article/antonelli-surges-to-dominant-victory-in-united-states-grand-prix-ahead-of-leclerc-and-verstappen.6kmBQv9FNTW7LzkDj8S34j"),
             ("BBC Sport - Russell one point clear of Hamilton",
              "https://www.bbc.com/sport/formula1/live/c87w8r725y8t")],
    flag=None)

# =============================================================================
# RUGBY LEAGUE
# =============================================================================
add(sport="Rugby League", event="State of Origin 2027",
    competition="2027 State of Origin series, New South Wales v Queensland",
    when="Series played May-July 2027", venue="Three venues, to be confirmed",
    market="Win Tournament", selection="New South Wales to win the 2027 series",
    line="-171", probability=0.632, track="T", tier="B", confidence="HIGH",
    in_band=True, olbg="9 of 13 tips (69%)",
    text=("New South Wales won the 2026 series 2-1 to claim their eighteenth shield, and they did "
          "it the hard way: 22-20 over Queensland at Accor Stadium on 27 May, a 44-24 loss at the "
          "MCG on 17 June, then 30-12 at Suncorp Stadium on 8 July to take the decider on the "
          "road. Nathan Cleary won the Wally Lewis Medal as player of the series and finished top "
          "points scorer on 36, going two tries, four conversions and a penalty in Game 3, with "
          "Selwyn Cobbo the leading try scorer on four. Total attendance across the three games "
          "was 223,309. It was New South Wales' first series win since 2024 and it ended "
          "Queensland's bid for a fourth series in five years under Billy Slater. Nine of the "
          "thirteen tips on OLBG's 2027 outright are with the Blues and our price is -171."),
    sources=[("2026 State of Origin series", "https://en.wikipedia.org/wiki/2026_State_of_Origin_series"),
             ("Sky Sports - Game 3 report",
              "https://www.skysports.com/rugby-league/news/13561516/state-of-origin-2026-queensland-12-30-new-south-wales-blues-claim-famous-victory-to-win-series"),
             ("The Guardian - Game 3 match report",
              "https://www.theguardian.com/sport/2026/jul/08/state-of-origin-2026-game-3-result-nsw-blues-vs-qld-queensland-maroons-score-winner-match-report"),
             ("OLBG rugby league tips board", "https://www.olbg.com/betting-tips/Rugby_League/10")],
    flag=None)

add(sport="Rugby League", event="State of Origin 2027",
    competition="2027 State of Origin series, New South Wales v Queensland",
    when="Series played May-July 2027", venue="Three venues, to be confirmed",
    market="Win Tournament", selection="Queensland to win the 2027 series",
    line="+172", probability=0.368, track="T", tier="B", confidence="MEDIUM",
    in_band=True, olbg="4 of 13 tips (31%)",
    text=("Queensland lost the 2026 series 2-1 but took the middle game at the Melbourne Cricket "
          "Ground on 17 June by 44-24, the widest margin of the three, and they have won three of "
          "the last five series under Billy Slater. Four of the thirteen tips on OLBG's 2027 "
          "outright sit with the Maroons, and because this is a two-horse market our price is "
          "simply the complement of the New South Wales number: +172 against -171. The series is "
          "played across three venues in May, June and July 2027, with a combined attendance of "
          "223,309 in 2026 and an average crowd of 74,436. Queensland are the value side of the "
          "market on paper, but New South Wales are the ones holding the shield."),
    sources=[("2026 State of Origin series", "https://en.wikipedia.org/wiki/2026_State_of_Origin_series"),
             ("The Guardian - Game 3 match report",
              "https://www.theguardian.com/sport/2026/jul/08/state-of-origin-2026-game-3-result-nsw-blues-vs-qld-queensland-maroons-score-winner-match-report")],
    flag=None)

add(sport="Rugby League", event="NRL 2027",
    competition="2027 National Rugby League premiership",
    when="Season runs March-October 2027", venue="17 clubs",
    market="Win Tournament", selection="Penrith Panthers to win the 2027 premiership",
    line="+565", probability=0.150, track="T", tier="D", confidence="MEDIUM",
    in_band=True, olbg="1 of 3 tips (33%)",
    text=("Penrith were the 2026 minor premiers, their sixth, finishing top of the regular season "
          "in a competition of 17 teams, 213 matches and 10,167 points scored, with an average "
          "attendance of 21,858. They did not convert it: the Sydney Roosters beat the Newcastle "
          "Knights 19-18 in the Grand Final at Accor Stadium on 4 October in front of 80,814, with "
          "James Tedesco taking the Clive Churchill Medal and Daly Cherry-Evans kicking the "
          "winning field goal after the Roosters had trailed 12-0 just before half-time. Only one "
          "of the three tips on OLBG's NRL 2027 outright sits with Penrith, and our tip-derived "
          "price across the confirmed 17-team field is +565. Three tips is a thin sample, which "
          "is what keeps this out of the top grade."),
    sources=[("2026 NRL season", "https://en.wikipedia.org/wiki/2026_NRL_season"),
             ("2026 NRL Grand Final", "https://en.wikipedia.org/wiki/2026_NRL_Grand_Final"),
             ("National Rugby League - official finals", "https://nationalrugbyleague.com.au/nrl-finals/"),
             ("BBC Sport - NRL Grand Final report",
              "https://www.bbc.com/sport/rugby-league/articles/cwdd849rr9j4o")],
    flag="The 2027 NRL field is carried over from the 17-team 2026 season; a 2027 field has not "
         "been confirmed from an official source.")

add(sport="Rugby League", event="Super League 2027",
    competition="2027 Super League",
    when="Season runs 2027", venue="To be confirmed",
    market="Win Tournament", selection="Wigan Warriors to win Super League 2027",
    line="", probability=None, track="T", tier="D", confidence="LOW",
    in_band=False, olbg="2 of 4 tips (50%)",
    text=("Wigan Warriors were the 2026 league leaders and reached the Challenge Cup final, but "
          "their season ended in the play-off semi-final with a 33-6 home defeat by Wakefield "
          "Trinity, who then beat Warrington Wolves 23-10 in the Grand Final at Old Trafford on 3 "
          "October in front of 71,728 to take their first Super League title and first championship "
          "since 1968. Two of the four tips on OLBG's Super League 2027 outright sit with Wigan. "
          "We publish no price for this runner because the 2027 Super League field has not been "
          "confirmed from an official source and there is no honest way to work out how many clubs "
          "the tip share should be spread across. The pick is directional only."),
    sources=[("2026 Super League Grand Final", "https://en.wikipedia.org/wiki/2026_Super_League_Grand_Final"),
             ("Super League Grand Final - all past results",
              "https://en.wikipedia.org/wiki/Super_League_Grand_Final"),
             ("OLBG rugby league tips board", "https://www.olbg.com/betting-tips/Rugby_League/10")],
    flag="The 2027 Super League field size is not confirmed from an official source, so no fair "
         "price is originated and the line is left blank.")

add(sport="Rugby League", event="Super League 2027",
    competition="2027 Super League",
    when="Season runs 2027", venue="To be confirmed",
    market="Win Tournament", selection="Wakefield Trinity to win Super League 2027",
    line="", probability=None, track="R", tier="R", confidence="LOW",
    in_band=False, olbg="no tips published for this runner",
    text=("Wakefield Trinity are the defending champions. They finished the 2026 regular season "
          "fourth, beat Leigh Leopards 26-16 in the Eliminator, then travelled to Wigan and won "
          "the semi-final 33-6 before beating Warrington Wolves 23-10 in the Grand Final at Old "
          "Trafford on 3 October, in front of 71,728 and refereed by Liam Moore - their first "
          "Super League title and their first championship of any kind since 1968. Tom Johnstone "
          "won the Rob Burrow Award. OLBG publishes no tips on Wakefield for the 2027 outright, "
          "only on Wigan, and the 2027 field is not confirmed from an official source, so we "
          "originate no price and grade this low. The champions are absent from the tip flow "
          "entirely."),
    sources=[("2026 Super League Grand Final", "https://en.wikipedia.org/wiki/2026_Super_League_Grand_Final"),
             ("Super League Grand Final - all past results",
              "https://en.wikipedia.org/wiki/Super_League_Grand_Final")],
    flag="OLBG publishes no tip split for the reigning champions. The 2027 Super League field size "
         "is not confirmed from an official source, so no fair price is originated.")

# =============================================================================
# GAELIC SPORTS
# =============================================================================
add(sport="Gaelic Sports", event="Kerry, All-Ireland Senior Football Championship 2027",
    competition="2027 All-Ireland Senior Football Championship",
    when="Final 25 July 2027", venue="Croke Park, Dublin",
    market="Win Tournament", selection="Kerry to win the 2027 All-Ireland SFC",
    line="+126", probability=0.442, track="T", tier="B", confidence="HIGH",
    in_band=True, olbg="6 of 8 tips (75%)",
    text=("Kerry retained the Munster Senior Football Championship in 2026 for a sixth consecutive "
          "year, beating Clare 2-19 to 1-14 in the semi-final and then Cork 1-23 to 1-15 in the "
          "final for their 87th Munster title, played for the new Corn Phaidi Ui She trophy "
          "introduced this year. OLBG's own Gaelic football editorial has the reigning All-Ireland "
          "champions as Mayo, who ended a 75-year wait in 2026 by beating Kerry in the final for "
          "their fourth title, with Kerry holding 39 all-time titles against Dublin's 31 - so "
          "Kerry go into 2027 as Munster champions and All-Ireland runners-up. Six of the eight "
          "tips on OLBG's outright sit with Kerry and our tip-derived price across a 33-county "
          "field is +126, comfortably inside the band."),
    sources=[("2026 Munster Senior Football Championship",
              "https://en.wikipedia.org/wiki/2026_Munster_Senior_Football_Championship"),
             ("Munster GAA - 2026 senior football final",
              "https://munster.gaa.ie/event/2026-munster-senior-football-championship-final/"),
             ("OLBG gaelic football tips board and editorial",
              "https://www.olbg.com/betting-tips/Gaelic_Football/25")],
    flag="The Mayo 2026 All-Ireland title is single-sourced to OLBG's own editorial page and could "
         "not be corroborated elsewhere. The 33-county field for 2027 is carried over from 2026.")

add(sport="Gaelic Sports", event="Fr Caseys v Kildimo Pallaskenry",
    competition="Limerick Senior Football Championship Final 2026",
    when="Sunday 1 November 2026, 15:30 local",
    venue="Mick Neville Park, Rathkeale (referee Jonathan Hayes, Limerick)",
    market="Handicap", selection="Kildimo-Pallaskenry +3.50",
    line="-160", probability=0.615, track="T", tier="C", confidence="MEDIUM",
    in_band=True, olbg="5 of 7 tips (71%)",
    text=("This is the Limerick county final and it is Kildimo-Pallaskenry's first ever appearance "
          "in one. They got there by beating the defending champions Mungret/St Pauls 2-16 to "
          "0-20 after extra time at Clarina, where Conor Staff's goal in the first half of extra "
          "time proved decisive - Mungret's Jack Dervan had pointed them ahead before "
          "Kildimo-Pallaskenry cleared a Peter Nash effort off the line and Staff converted the "
          "rebound. Nash finished with 0-8 for the champions and Declan Nash manages the winners. "
          "Fr Casey's beat Monaleen in the other semi-final at Sean Finn Park and were described "
          "as the only unbeaten team left in Limerick. Five of the seven tips on OLBG sit with "
          "Kildimo-Pallaskenry taking three and a half points, and our price is -160."),
    sources=[("Munster GAA - official match centre, Limerick SFC Final", "https://munster.gaa.ie/"),
             ("Hogan Stand - Kildimo-Pallaskenry beat the defending champions after extra time",
              "https://hoganstand.com/County/National/Article/Index/342139"),
             ("Limerick GAA - semi-final details",
              "https://limerickgaa.ie/kildimo-pallaskenry-mungret-st-pauls-fr-caseys-monaleen-all-fighting-for-a-county-senior-football-final-place-today/"),
             ("The Irish Times - club football championships, state of play",
              "https://www.irishtimes.com/sport/gaelic-games/2026-10-14/club-football-championships-who-are-county-champions-and-what-is-the-state-of-play-around-ireland/")],
    flag="OLBG prints this as a handicap selection with no market label attached to the row.")

add(sport="Gaelic Sports", event="Fr Caseys v Kildimo Pallaskenry",
    competition="Limerick Senior Football Championship Final 2026",
    when="Sunday 1 November 2026, 15:30 local",
    venue="Mick Neville Park, Rathkeale (referee Jonathan Hayes, Limerick)",
    market="Handicap", selection="Fr Caseys -3.50",
    line="+160", probability=0.385, track="T", tier="C", confidence="MEDIUM",
    in_band=True, olbg="2 of 7 tips (29%)",
    text=("Fr Casey's go into the Limerick final as the only unbeaten team left in the county, "
          "having reached it by beating Monaleen in the semi-final at Sean Finn Park, Rathkeale on "
          "the same weekend that Kildimo-Pallaskenry needed extra time to get past the defending "
          "champions Mungret/St Pauls. That difference in how the two sides arrived matters: a "
          "side that has gone through the championship unbeaten is giving three and a half points "
          "to a first-time finalist who needed an extra period and a goal in the first half of that "
          "extra period to get through. Two of the seven tips on OLBG sit with Fr Casey's covering "
          "the handicap, and our price is +160, the complement of the other side of this market."),
    sources=[("The Irish Times - Fr Casey's the only unbeaten team left in Limerick",
              "https://www.irishtimes.com/sport/gaelic-games/2026-10-14/club-football-championships-who-are-county-champions-and-what-is-the-state-of-play-around-ireland/"),
             ("Munster GAA - official match centre, Limerick SFC Final", "https://munster.gaa.ie/"),
             ("Hogan Stand - Limerick semi-final report",
              "https://hoganstand.com/County/National/Article/Index/342139")],
    flag="OLBG prints only the Kildimo-Pallaskenry side of this handicap with no market label; the "
         "Fr Casey's number is our own complement of that tip share.")

add(sport="Gaelic Sports", event="Kanturk v Eire Og Cor",
    competition="", when="01 November 2026, 10:30", venue="",
    market="Handicap", selection="Eire Og Cor +0.50",
    line="-300", probability=0.750, track="T", tier="C", confidence="LOW",
    in_band=False, olbg="6 of 6 tips (100%)",
    text=("All six tips posted on this OLBG market sit with the half-point handicap, and our "
          "tip-derived price is -300. We cannot identify the fixture. Munster GAA's published 2026 "
          "club championship draw names Eire Og Inis of Clare as the Clare champions and pairs "
          "them with The Nire or Rathgormack of Waterford in the quarter-final on 8 November, not "
          "with Kanturk; Kanturk beat Kilshannig 2-16 to 0-19 in the Cork Senior A quarter-final "
          "on 27 September at Fr Kelleher Park and do not appear in the provincial draw at all. "
          "With no competition and no venue confirmable from an official source, both fields are "
          "left blank and this pick is graded low - six unanimous tips on a fixture we cannot "
          "place is not a position to back."),
    sources=[("Munster GAA - official club championship draw 2026",
              "https://munster.gaa.ie/fixtures/club-championships-2026/"),
             ("2026 Cork Senior A Football Championship",
              "https://en.wikipedia.org/wiki/2026_Cork_Senior_A_Football_Championship"),
             ("Full list of 2026 county champions",
              "https://www.sportsnewsireland.com/gaa/full-list-of-senior-football-and-hurling-county-champions-2026")],
    flag="The competition could not be identified. Munster GAA's official 2026 club draw does not "
         "pair Kanturk with any club matching 'Eire Og Cor'. Competition and venue left blank.")

add(sport="Gaelic Sports", event="Galway, All-Ireland Senior Hurling Championship 2027",
    competition="2027 All-Ireland Senior Hurling Championship",
    when="Season runs 2027", venue="To be confirmed",
    market="Win Hurling", selection="Galway to win the 2027 Liam MacCarthy Cup",
    line="", probability=None, track="T", tier="A", confidence="LOW",
    in_band=False, olbg="7 of 18 tips (39%)",
    text=("Galway carry seven of the eighteen tips on OLBG's All-Ireland Senior Hurling outright, "
          "the deepest tip sample anywhere on the Gaelic board and more than any other runner. "
          "OLBG publishes a single market for hurling, labelled 'Win Hurling', with no handicap, "
          "no totals and no group-stage markets at all. We publish no price for Galway because the "
          "number of counties competing for the Liam MacCarthy Cup in 2027 has not been confirmed "
          "from an official source, and without that field size there is no honest denominator to "
          "spread 7 of 18 across. The pick is directional only, and the missing field size is "
          "flagged rather than assumed."),
    sources=[("GAA - official All-Ireland Senior Hurling Championship",
              "https://www.gaa.ie/"),
             ("OLBG gaelic football tips board", "https://www.olbg.com/betting-tips/Gaelic_Football/25")],
    flag="The number of counties competing in the 2027 All-Ireland SHC is not confirmed from an "
         "official source, so no fair price is originated and the line is left blank.")

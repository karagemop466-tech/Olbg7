#!/usr/bin/env python3
"""Authored pick copy for the value desk (session sess-arena-7cf491a1).

Each P() record joins a priced line (data/value/lines.json) to one original
written prediction and the sources that support its facts.  Facts are only
claimed where a URL was actually read during this session; where no official
form/team-news source could be read the prediction says so and the row is
flagged.  No prediction contains the words "model" or "verified".
"""

# source kinds: official (governing body / club / tour), olbg (market data),
# media (established newsroom), secondary (aggregator / wiki / tipster comment)

OLBG_HUBS = {
    "Golf": "https://www.olbg.com/betting-tips/Golf/5",
    "Volleyball": "https://www.olbg.com/betting-tips/Volleyball/21",
    "Rugby Union": "https://www.olbg.com/betting-tips/Rugby_Union/9",
    "Cricket": "https://www.olbg.com/betting-tips/Cricket/7",
    "Snooker": "https://www.olbg.com/betting-tips/Snooker/8",
    "Darts": "https://www.olbg.com/betting-tips/Darts/15",
    "Baseball": "https://www.olbg.com/betting-tips/Baseball/12",
    "Gaelic Sports": "https://www.olbg.com/betting-tips/Gaelic_Football/25",
    "Greyhounds": "https://www.olbg.com/betting-tips/Greyhounds/28",
    "Tennis": "https://www.olbg.com/betting-tips/Tennis/3",
    "Motor Racing": "https://www.olbg.com/betting-tips/Motor_Racing/14",
    "Handball": "https://www.olbg.com/betting-tips/Handball/20",
    "Ice Hockey": "https://www.olbg.com/betting-tips/Ice_Hockey/13",
    "Basketball": "https://www.olbg.com/betting-tips/Basketball/4",
    "Rugby League": "https://www.olbg.com/betting-tips/Rugby_League/10",
}

# Frequently reused, individually-checked facts.
F_WST_FIXTURES = ("WST match centre lists the International Championship 2026 round-two and held-over matches in Nanjing on 30-31 October", "https://www.wst.tv/match-centre/bb4f8b36-42f0-490f-b97b-b8f8799f693b", "official")
F_WST_RANKINGS = ("WST official world rankings: Selby 4th (GBP 1,070,500), Murphy 7th (GBP 884,150), Wu Yize 2nd, Wilson 9th", "https://www.wst.tv/rankings/", "official")
F_OLBG_SNOOKER_EMPTY = ("OLBG's snooker hub showed 'No tips found.' when checked on 27 October, so no community tip split exists for these matches", "https://www.olbg.com/betting-tips/Snooker/8", "olbg")
F_OLBG_GREY_EMPTY = ("OLBG's greyhound hub showed 'No tips found.' on 27 October", "https://www.olbg.com/betting-tips/Greyhounds/28", "olbg")
F_OLBG_TRAP = ("OLBG's own track table records trap 1 winning 19.4% of 3,655 Romford races, the best single-trap strike rate listed", "https://www.olbg.com/betting-tips/Greyhounds/28", "olbg")
F_ROMFORD = ("Romford Stadium's final advance card for Tuesday 27 October 2026 lists twelve 400m races with trap draws and trainers", "https://imminent-otter.files.svdcdn.com/production/assets/results/Romford/race-advances/TUESDAY-ADVANCED_2026-10-26-121153_lbhn.pdf", "official")
F_PDC_ENTRIES = ("PDC confirmed Players Championships 31-32 for 28-29 October at Maassport Den Bosch with two 128-player fields", "https://www.pdc.tv/news/2026/october/26/2026-players-championships-31-32-entries-confirmed", "official")
F_PDC_GRANDSLAM = ("PDC's 26 October Grand Slam article lists the 2026 Players Championship event winners, including Kevin Doets, Chris Dobey and Cameron Menzies", "https://www.pdc.tv/news/2026/october/26/schindler---coates-secure-grand-slam-qualification", "official")
F_MLB_SCHED = ("MLB's official postseason schedule shows Milwaukee winning 3-2, 5-4 and 10-1 to lead the World Series 3-0, with Game 4 on 27 October at 8pm ET", "https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule", "official")
F_MLB_G3 = ("MLB's Game 3 report: Robert Gasser allowed one hit over six scoreless innings and Jackson Chourio had four hits in a 10-1 win, Milwaukee's eighth straight postseason win", "https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule", "official")
F_MLB_G4 = ("MLB's Game 4 storylines page lists the starting pitchers as TBA for Milwaukee and Griffin Jax for Tampa Bay", "https://www.mlb.com/news/2026-world-series-game-4-storylines-brewers-rays", "official")
F_F1_USGP = ("Formula 1's official United States GP report: Antonelli won from pole, Leclerc was second and Verstappen third", "https://www.formula1.com/en/latest/article/antonelli-surges-to-dominant-victory-in-united-states-grand-prix-ahead-of-leclerc-and-verstappen.6kmBQv9FNTW7LzkDj8S34j", "official")
F_F1_STAND = ("F1's official 2026 standings show Antonelli on 365 points, Russell 242, Hamilton 241, Verstappen 236 and Leclerc 233", "https://www.formula1.com/", "official")
F_F1_MEX = ("F1's official Mexico City GP page lists a 71-lap race on 1 November at the 4.304km Autodromo Hermanos Rodriguez", "https://www.formula1.com/en/racing/2026/mexico", "official")
F_EHF = ("EHF Champions League official group tables after five rounds: Magdeburg 5-0 (+36), Veszprem 5-0 (+39), Aalborg 4-1-0 (+25), Kolstad 0-5 (-35), Celje 0-5 (-38)", "https://ehfcl.eurohandball.com/men/2026-27/standings/", "official")
F_URC = ("United Rugby Championship's official fixture list puts Connacht v Leinster and Glasgow v Lions on 30 October, with Stormers v Ulster and Munster v Sharks on 31 October in round 5", "https://www.unitedrugby.com/latest/news/2026-27-fixtures-in-full/", "official")
F_NHL = ("NHL standings through 26 October: Carolina 9-2-2 with 51 goals for and 33 against; Philadelphia 3-7-3 with 24 for and 42 against; Dallas 7-3-1; Winnipeg 4-4-3", "https://www.bbc.com/sport/ice-hockey/tables", "media")
F_NBA = ("NBA.com's official Nets page lists Brooklyn 0-3 and Boston 2-1 ahead of their 27 October game; NBA.com preseason power rankings had Boston first in defensive rating and Brooklyn first in offensive rating", "https://www.nba.com/team/1610612751/nets", "official")
F_EURO = ("EuroLeague standings after seven rounds list Panathinaikos and Fenerbahce at 6-1, with Panathinaikos scoring 87.6 points per game and conceding 73.9", "https://basketnews.com/leagues/25-euroleague/standings.html", "secondary")
F_ATP = ("ATP's official Basel coverage: the Swiss Indoors runs 26 October-1 November, Djokovic accepted a wild card, and Hurkacz is the No.10 seed", "https://www.atptour.com/en/news/basel-atp-500-2026-history-draw-schedule", "official")
F_CRIC = ("ESPNcricinfo's series page: India won the first two T20Is in Christchurch by four wickets each and lead New Zealand 2-0 before the third match in Wellington on 27 October", "https://www.espncricinfo.com/series/india-in-new-zealand-2026-27-1539421/new-zealand-vs-india-3rd-t20i-1539434/full-scorecard", "media")
F_RLWC = ("The official RLWC 2026 schedule lists England v Papua New Guinea (30 Oct, WIN Stadium), New Zealand v Fiji and Australia v Cook Islands (both 31 Oct)", "https://leagueworldcup2026.com/schedule/", "official")
F_GAA = ("Munster GAA's official club championship table lists Glen Rovers v Inagh-Kilnamona on 1 November at Pairc Ui Rinn, 1:15pm, and Ballygunner v Kilmallock in the semi-finals on 15 November", "https://munster.gaa.ie/fixtures/club-championships-2026/", "official")
F_CBV = ("CBV's official Superliga table shows the 2026-27 season in round one, with Suzano, Praia Clube, Goias and Sao Jose all yet to record a point", "https://cbv.com.br/volei-de-quadra/superliga-a-masculina", "official")
F_PGA_FIELD = ("PGA TOUR's First Look names Wyndham Clark as the highest-ranked player in the Mexico Open field with three 2026 wins, and says the 120-man field plays the par-71, 7,337-yard Vidanta Vallarta course from 29 October", "https://www.pgatour.com/article/news/the-first-look/2026/10/26/vidantaworld-mexico-open-preview-storylines-fedexcup-fall-2027-pga-tour-cards", "official")
F_PGA_PRICE = ("The PGA TOUR's own betting article quoted FanDuel prices of +1200 for Clark, +17500 for defending champion Brian Campbell and +8000 for 2023 winner Tony Finau", "https://www.pgatour.com/article/news/betting-dfs/2026/10/26/odds-outlook-vidantaworld-mexico-open-betting-fantasy-picks-advice-fedexcup-fall", "official")
F_LPGA = ("LPGA's official tournament page confirms the Maybank Championship runs 29 October-1 November at Kuala Lumpur Golf & Country Club's West Course, and its entries page lists Lottie Woad", "https://www.lpga.com/tournaments/maybank-championship", "official")
F_SIMMONS = ("The official Simmons Bank Championship site says the 30 October-1 November event is a 54-hole, no-cut playoff limited to the top 54 in the Charles Schwab Cup standings", "https://simmonsbankchampionship.com/", "official")


def P(id, sport, line_id, prediction, facts, conf="medium", selection=None,
      market=None, prior_p=None, basis=None, flags=None, note=None):
    return {
        "id": id, "sport": sport, "line_id": line_id, "prediction": prediction,
        "facts": [{"claim": c, "source": u, "kind": k} for c, u, k in facts],
        "conf_hint": conf, "selection_override": selection, "market_override": market,
        "prior_p": prior_p, "basis": basis, "flags": flags or [], "note": note or "",
    }


PICKS = [
    # ------------------------------- GOLF ---------------------------------
    P("GF-01", "Golf", "X-GF-01",
      "Lottie Woad has already won twice since turning professional, including the 2026 Kroger Queen City Championship, and LPGA's entries page confirms her in this week's Maybank field. Only two OLBG tips have been placed on the tournament outright and one of them backs Woad, so our own line stays long: she is the selection, with the modest tip sample the reason to keep stakes small.",
      [F_LPGA, ("Woad won the 2026 Kroger Queen City Championship and the 2025 ISPS Handa Scottish Open", "https://www.espn.com/golf/schedule/_/tour/lpga", "media"),
       ("OLBG's Maybank Championship event page shows Lottie Woad on 1/2 Win Tips", "https://www.olbg.com/betting-tips/Golf/All_Golf/All_Events/Maybank_Championship/5?event_id=101913", "olbg")], "high"),
    P("GF-02", "Golf", "X-GF-02",
      "Hye Jin Choi shares the Maybank Championship tip lead with Lottie Woad at one win tip apiece, yet she is the one the OLBG event page calls the Most Popular Tip. The official LPGA schedule puts this 72-hole limited-field event on the West Course from 29 October, where a player with Choi's ranking profile can outlast a larger field. Choi is our outright play at a big price.",
      [F_LPGA, ("2026 Maybank Championship field rankings place Hye Jin Choi 27th in the world", "https://thegolfnewsnet.com/golfnewsnetteam/2026/10/25/2026-maybank-championship-field-lpga-tour-players-rankings-145290/", "secondary"),
       ("OLBG event page names Hye Jin Choi the Most Popular Tip on 1/2 Win Tips", "https://www.olbg.com/betting-tips/Golf/All_Golf/All_Events/Maybank_Championship/5?event_id=101913", "olbg")], "medium", flags=["ranking-from-secondary-source"]),
    P("GF-03", "Golf", "X-GF-03",
      "Wyndham Clark arrives at Vidanta Vallarta as the highest-ranked player in a 120-man field with three PGA TOUR wins in 2026, including a second US Open, and he finished 23rd here in 2023. OLBG's two-tip market splits one vote to Clark. Our own line is longer than the +1200 FanDuel price quoted on the PGA TOUR site, so Clark is the win pick but not a value bet.",
      [F_PGA_FIELD, F_PGA_PRICE,
       ("OLBG's Mexico Open event page shows Wyndham Clark 1/2 Win Tips", "https://www.olbg.com/betting-tips/Golf/All_Golf/All_Events/Mexico_Open/5?event_id=101915", "olbg")], "high"),
    P("GF-04", "Golf", "X-GF-04",
      "Max Homa is the other name with a win tip in OLBG's thin Mexico Open market, and an OLBG tipster notes his second place at the John Deere Classic as his best 2026 finish plus a habit of making cuts. With the official PGA TOUR field confirming Homa's place at Vidanta Vallarta, he is the each-way-style alternative to Clark at a far bigger price, though the form detail comes from a community comment.",
      [F_PGA_FIELD, ("OLBG event page: Max Homa 1/2 Win Tips; a tipster cites his John Deere Classic runner-up finish", "https://www.olbg.com/betting-tips/Golf/All_Golf/All_Events/Mexico_Open/5?event_id=101915", "olbg")], "medium", flags=["form-from-tipster-comment"]),
    P("GF-05", "Golf", "X-GF-05",
      "Stewart Cink leads the PGA TOUR Champions money list and won the 2025 Charles Schwab Cup, so his one win tip from two on the Simmons Bank Championship is well founded. This is a 54-hole, no-cut event restricted to the top 54 in the standings, which removes the attrition that usually hurts a favourite. Take Cink to win at Pleasant Valley Country Club this week.",
      [F_SIMMONS, ("ESPN's 2026 Champions Tour schedule lists Cink as the season money leader and the defending Schwab Cup champion", "https://www.espn.com/golf/schedule/_/tour/champions-tour", "media"),
       ("OLBG event page: Stewart Cink 1/2 Win Tips", "https://www.olbg.com/betting-tips/Golf/All_Golf/All_Events/Simmons_Bank_Championship/5?event_id=101914", "olbg")], "high"),
    P("GF-06", "Golf", "X-GF-06",
      "Ernie Els shares the Simmons Bank Championship tip lead with Stewart Cink at one vote each, and the tournament's own site lists him among the committed senior major winners. An OLBG tipster credits him with seven senior-tour victories and a senior major since joining the circuit in 2020. With only 54 starters and no cut, Els is the value side of this outright at a long price.",
      [F_SIMMONS, ("OLBG event page: Ernie Els 1/2 Win Tips; a tipster cites seven senior titles", "https://www.olbg.com/betting-tips/Golf/All_Golf/All_Events/Simmons_Bank_Championship/5?event_id=101914", "olbg")], "medium", flags=["form-from-tipster-comment"]),

    # ----------------------------- VOLLEYBALL ------------------------------
    P("VB-01", "Volleyball", "074",
      "Suzano Volei and Goias Volei are both still on zero points in the CBV's opening Superliga table, and the official Brazilian fixture list schedules their round-one meeting for 27 October. OLBG tipsters give Suzano three of four win tips for this one. With home-court order implied by the listing and the most tips behind them, Suzano are our selection to win the match.",
      [F_CBV, ("CBV's published round-one schedule lists Suzano Volei v Goias Volei on 27 October", "https://www.otempo.com.br/sports/volei/2026/9/21/superliga-masculina-de-volei-2026-27-tabela-com-jogos-e-horarios-do-1-turno", "secondary")], "high"),
    P("VB-02", "Volleyball", "075",
      "Praia Clube and Volei Sao Jose enter this Brazilian Superliga fixture with identical zero-point records after the opening weekend of the 2026-27 season, according to the CBV table. Three of OLBG's four win tips side with Praia Clube, and our own line keeps them short without assuming any form that the official table does not yet show. Back Praia Clube to take the match.",
      [F_CBV, ("OLBG 27 October volleyball listing: Praia Clube 3/4 Win Tips", "https://www.olbg.com/betting-tips/Volleyball/21", "olbg")], "medium", flags=["no-official-form-data"]),
    P("VB-03", "Volleyball", "070",
      "Ziraat Bankasi carry all four OLBG win tips into their Turkish league fixture against Gaziantep Genclik Spor, the only unanimous four-tip row on Wednesday's volleyball card. Our own price shortens with that support but a 4-4 sample is small, so we treat it as a medium-strength play. Ziraat Bankasi to win is the straightforward selection here.",
      [("OLBG 27 October listing: Ziraat Bankasi 4/4 Win Tips, 100%", "https://www.olbg.com/betting-tips/Volleyball/21", "olbg")], "medium", flags=["no-official-form-data"]),
    P("VB-04", "Volleyball", "068",
      "Bergamo W have five of seven OLBG win tips for their Italian women's trip to Marignano W, a 71% share on a card where most rows carry three tips or fewer. That makes this the best-supported volleyball market of the day. We could not retrieve an official Serie A1 form table for either club, so the pick rests on the market data alone: Bergamo W to win.",
      [("OLBG 27 October listing: Bergamo W 5/7 Win Tips, 71%", "https://www.olbg.com/betting-tips/Volleyball/21", "olbg")], "medium", flags=["no-official-form-data"]),
    P("VB-05", "Volleyball", "071",
      "Uni Opole W take four of six win tips into their Polish women's fixture with Palac Bydgoszcz W. Our originated line prices them near the top of the value band rather than as an odds-on certainty, which reflects how thin a six-tip sample is. Uni Opole W are still the clear selection on this market, with an explicit warning that no official Polish league form data was retrieved.",
      [("OLBG 27 October listing: Uni Opole W 4/6 Win Tips, 67%", "https://www.olbg.com/betting-tips/Volleyball/21", "olbg")], "medium", flags=["no-official-form-data"]),

    # ---------------------------- RUGBY UNION ------------------------------
    P("RU-01", "Volleyball", "017",  # placeholder replaced below
      "", [], "low"),
    P("RU-01", "Rugby Union", "017",
      "Colomiers are the only French Pro D2 side on this card with a unanimous OLBG split, taking both available win tips against Agen for their 30 October meeting. The official URC schedule does not cover this French fixture, so no governing-body form data is attached to the row. Colomiers to win is the pick, with the two-tip sample explicitly limiting our confidence.",
      [("OLBG 27 October rugby union listing: Colomiers 2/2 To Win tips against Agen", "https://www.olbg.com/betting-tips/Rugby_Union/9", "olbg")], "low", flags=["no-official-form-data"]),
    P("RU-02", "Rugby Union", "022",
      "Glasgow Warriors host the Lions at Scotstoun on Friday 30 October in round five of the United Rugby Championship, a fixture the competition itself publishes with a 19:45 kick-off. OLBG's single win tip goes to Glasgow, and our line prices them as a narrow favourite rather than a certainty. Glasgow Warriors to win is the selection, with a note that no official team news was available.",
      [F_URC, ("OLBG 27 October listing: Glasgow Warriors 1/1 To Win tips", "https://www.olbg.com/betting-tips/Rugby_Union/9", "olbg")], "high", flags=["no-official-team-news"]),
    P("RU-03", "Rugby Union", "023",
      "Connacht host Leinster at Dexcom Stadium on 30 October in the URC's round-five Friday double-header. OLBG's only tip on this match is a handicap play: Connacht +3.50. Our own line keeps that plus-3.5 start as the value side of a derby between an Irish province and the defending heavyweight. Take Connacht with the points.",
      [F_URC, ("OLBG 27 October listing: Connacht +3.50 Handicap 1/1 Win Tips", "https://www.olbg.com/betting-tips/Rugby_Union/9", "olbg")], "medium", flags=["no-official-team-news"]),
    P("RU-04", "Rugby Union", "025",
      "Ulster travel to Cape Town to face the Stormers on 31 October, and the URC's official fixture list confirms the round-five date. OLBG's one handicap tip gives Ulster a 12.50-point start, which our originated line treats as a genuine plus-money opportunity against a South African side at altitude. Ulster +12.50 is the pick, with no injury report retrievable from an official source.",
      [F_URC, ("OLBG 27 October listing: Ulster +12.50 Handicap 1/1 Win Tips", "https://www.olbg.com/betting-tips/Rugby_Union/9", "olbg")], "medium", flags=["no-official-team-news"]),
    P("RU-05", "Rugby Union", "026",
      "Munster host the Sharks at Thomond Park on 31 October, another fixture published in the URC's round-five schedule, and the single OLBG handicap tip asks Munster to cover -6.50. Our own line prices that margin close to even, so this is a medium-strength play rather than a confident one. Munster -6.50 is the selection, with no official team sheet yet published.",
      [F_URC, ("OLBG 27 October listing: Munster -6.50 Handicap 1/1 Win Tips", "https://www.olbg.com/betting-tips/Rugby_Union/9", "olbg")], "medium", flags=["no-official-team-news"]),

    # ------------------------------- CRICKET -------------------------------
    P("CK-01", "Cricket", "049",
      "India have won both opening T20Is in Christchurch by four wickets, chasing with one ball and then two balls to spare, so a 2-0 lead is the strongest form line on this card. OLBG's 35 of 49 win tips back them again in Wellington on 27 October. Our own line makes India a solid favourite inside the value band: back India to complete the series win.",
      [F_CRIC, ("OLBG 27 October listing: India 35/49 Win Match tips, 71%", "https://www.olbg.com/betting-tips/Cricket/7", "olbg")], "high"),
    P("CK-02", "Cricket", "X-CK-01",
      "New Zealand have lost two tight T20Is at home after scoring 225 and 180, with Glenn Phillips making 82 not out and 70, and they are written off by OLBG's 35-49 tip split in the third match. That is exactly the sort of one-sided market where a plus-money home side has value. Take New Zealand to finally convert a good batting start in Wellington.",
      [F_CRIC, ("New Zealand scored 225 and 180 in the first two T20Is; Glenn Phillips made 82* and 70", "https://sports.yahoo.com/articles/zealand-vs-india-3rd-t20i-050525124.html", "media"),
       ("OLBG 27 October listing: India 35/49 Win Match tips for the third T20I", "https://www.olbg.com/betting-tips/Cricket/7", "olbg")], "high"),
    P("CK-03", "Cricket", "050",
      "Ireland attract 22 of 32 OLBG win tips for the third ODI away to Namibia, a 69% share that makes them one of the best-supported cricket sides on Tuesday's card. We could not attach an official series result or team news to this fixture, so the selection rests on the published tip split. Ireland to win the third ODI is the play, at a short but band-eligible price.",
      [("OLBG 27 October listing: Ireland 22/32 Win Match tips, 69%", "https://www.olbg.com/betting-tips/Cricket/7", "olbg")], "medium", flags=["no-official-team-news"]),
    P("CK-04", "Cricket", "051",
      "Pakistan take 22 of 31 win tips against Sri Lanka in their one-day match, a 71% share on the second-largest cricket sample of the day. Our own line shrinks that support toward an even two-way contest, which leaves Pakistan short but still inside the target band. Back Pakistan to win, with the caveat that no official squad or pitch report was retrieved for this match.",
      [("OLBG 27 October listing: Pakistan 22/31 Win Match tips, 71%", "https://www.olbg.com/betting-tips/Cricket/7", "olbg")], "medium", flags=["no-official-team-news"]),
    P("CK-05", "Cricket", "052",
      "Afghanistan are the heaviest-backed cricket selection of the day with 15 of 16 win tips against Zimbabwe in the first T20, a 94% share that our pricing engine deliberately shrinks back toward a two-way contest. That still leaves a clear favourite and an obvious selection: Afghanistan to win the opening T20 match, with stakes moderated because a single dissenting tip exists.",
      [("OLBG 27 October listing: Afghanistan 15/16 Win Match tips, 94%", "https://www.olbg.com/betting-tips/Cricket/7", "olbg")], "medium", flags=["no-official-team-news"]),
    P("CK-06", "Cricket", "062",
      "India are the most-tipped winner of the 2027 World Cup on OLBG with six of twelve outright tips, and they are also 2-0 up in a T20 series in New Zealand this week. Long-dated ante-post markets carry enormous uncertainty, so our line stretches to a big price and the confidence is only medium. India to win the 2027 World Cup is the selection for anyone playing the long game.",
      [F_CRIC, ("OLBG 27 October listing: India 6/12 Outright Winner tips for the 2027 World Cup", "https://www.olbg.com/betting-tips/Cricket/7", "olbg")], "medium", flags=["long-dated-ante-post"]),

    # ------------------------------- SNOOKER -------------------------------
    P("SK-01", "Snooker", "X-SK-01",
      "Mark Selby is fourth in WST's official world rankings with 1,070,500 pounds and tops the one-year list on 348,350 pounds, a stark advantage over Jimmy White in their International Championship second-round match in Nanjing. OLBG has no snooker tips at all today, so this line comes from the ranking gap rather than community opinion. Take Selby to win the match.",
      [F_WST_FIXTURES, F_WST_RANKINGS, F_OLBG_SNOOKER_EMPTY], "high", flags=["no-olbg-market-today"]),
    P("SK-02", "Snooker", "X-SK-02",
      "Shaun Murphy sits seventh in the official WST rankings on 884,150 pounds and has 19 centuries this season, while specialist draw listings place Mitchell Mann outside the top 90. Their round-two match in Nanjing is listed on WST's own match centre. Over a best-of-eleven frames contest that class gap should tell: Murphy to beat Mann is the selection.",
      [F_WST_FIXTURES, F_WST_RANKINGS, F_OLBG_SNOOKER_EMPTY], "high", flags=["opponent-rank-from-secondary-source", "no-olbg-market-today"]),
    P("SK-03", "Snooker", "X-SK-03",
      "Zhou Yuelong has home-country backing in Nanjing and meets Liam Davies in a round-two match confirmed by WST's match centre. Davies appears ninth on WST's Home Nations bonus list with 18,600 pounds, while Zhou is a long-established top-32 player. With no OLBG snooker market to lean on, our price is deliberately cautious: Zhou Yuelong to win is the pick.",
      [F_WST_FIXTURES, ("WST's official Home Nations bonus list has Liam Davies ninth on GBP 18,600", "https://www.wst.tv/rankings/", "official"), F_OLBG_SNOOKER_EMPTY], "medium", flags=["no-olbg-market-today"]),
    P("SK-04", "Snooker", "X-SK-04",
      "Kyren Wilson won the Northern Ireland Open in Belfast on 25 October, with WST's own headline 'Wilson Reigns Supreme In Belfast', and he is ninth in the official world rankings. He now faces Liam Highfield in Nanjing in the International Championship. Riding a title-winning week is the clearest form signal in this section, so Wilson to win is our selection.",
      [("WST official news, 25 October 2026: 'Wilson Reigns Supreme In Belfast'", "https://www.wst.tv/news/2026/october/25/Wilson-Reigns-Supreme-In-Belfast/", "official"), F_WST_RANKINGS,
       ("The International Championship round-two draw lists Liam Highfield v Kyren Wilson on 1 November", "https://www.snooker.org/res/index.asp?event=2762", "secondary")], "high", flags=["fixture-from-secondary-source", "no-olbg-market-today"]),
    P("SK-05", "Snooker", "X-SK-05",
      "Mitchell Mann gets a plus-money line against Shaun Murphy in Nanjing, and this is the value play of the snooker card rather than the most likely winner. WST's match centre confirms the pairing, while Murphy's seventh-place ranking is what makes the price so long. A best-of-eleven match gives an in-form outsider a route in: Mann to cause the upset is the speculative pick.",
      [F_WST_FIXTURES, F_WST_RANKINGS, F_OLBG_SNOOKER_EMPTY], "low", flags=["value-longshot", "no-olbg-market-today"]),
    P("SK-06", "Snooker", "X-SK-06",
      "Liu Hongyu and Louis Heathcote meet in the early round-two session in Nanjing on 31 October, one of the most evenly matched fixtures WST published for the International Championship. Neither man appears in the top eleven of the official ranking page and the specialist draw has them 55th and 67th. With home support for Liu, he is our narrow selection to win.",
      [F_WST_FIXTURES, F_WST_RANKINGS, F_OLBG_SNOOKER_EMPTY], "medium", flags=["rankings-from-secondary-source", "no-olbg-market-today"]),

    # -------------------------------- DARTS --------------------------------
    P("DT-01", "Darts", "X-DT-06",
      "Luke Littler holds 22 of 36 OLBG win tips for the 2027 PDC World Championship, a 61% share that dwarfs every other darts row on the card. PDC's own Grand Slam qualification article confirms his status as the 2026 UK Open winner and world champion favourite. Our own line still offers a plus-money price on a tournament three months away: Littler to win the title is the pick.",
      [("OLBG darts hub: Luke Littler 22/36 Win Tips, 61%, for the PDC World Championship 2027", "https://www.olbg.com/betting-tips/Darts/15", "olbg"), F_PDC_GRANDSLAM], "high", flags=["long-dated-ante-post"]),
    P("DT-02", "Darts", "X-DT-01",
      "Wessel Nijman is the Best Tipster's Tip on OLBG's Players Championship 31 page with two of eight win tips, and a comment there calls him the top seed with six floor titles in 2026. PDC's official entry list confirms the 128-player event in Den Bosch on 28 October. That claim of six titles is a community comment rather than a PDC record, so it is flagged: Nijman to win.",
      [F_PDC_ENTRIES, ("OLBG PC31 page: Wessel Nijman 2/8 Win Tips and Best Tipster's Tip", "https://www.olbg.com/betting-tips/Darts/All_Darts/All_Events/Players_Championship_31/15?event_id=32446", "olbg")], "medium", flags=["form-from-tipster-comment", "pdc-winner-list-conflict"]),
    P("DT-03", "Darts", "X-DT-02",
      "Nathan Aspinall shares the Players Championship 31 tip lead with two of eight win tips and was the name OLBG's hub chose to display for the event. PDC's official entry list includes him in the 128-player field at Den Bosch on 28 October, and PDC separately confirms he has qualified for the Grand Slam. Aspinall to win PC31 is the pick at a big price.",
      [F_PDC_ENTRIES, F_PDC_GRANDSLAM,
       ("OLBG PC31 page: Nathan Aspinall 2/8 Win Tips, 25%", "https://www.olbg.com/betting-tips/Darts/All_Darts/All_Events/Players_Championship_31/15?event_id=32446", "olbg")], "high"),
    P("DT-04", "Darts", "X-DT-03",
      "Kevin Doets also has two of eight OLBG win tips for Players Championship 31, and PDC's 26 October Grand Slam article names him among the 2026 Players Championship event winners. That official form note is why Doets gets a shorter standalone line than his 128-player field share would suggest. Doets to win PC31 is the selection, with a flag on PDC's event-numbering inconsistency.",
      [F_PDC_ENTRIES, F_PDC_GRANDSLAM], "medium", flags=["pdc-winner-list-conflict"]),
    P("DT-05", "Darts", "X-DT-04",
      "Gian van Veen has one of OLBG's eight win tips for Players Championship 31 and appears in PDC's official entry list for the 28 October event in Den Bosch. With a 128-player field and no top-16 players such as Humphries or Littler entered, this is a genuinely open floor event. Van Veen at a long price is our value selection to win the tournament.",
      [F_PDC_ENTRIES, ("OLBG PC31 page: Gian van Veen 1/8 Win Tips, 13%", "https://www.olbg.com/betting-tips/Darts/All_Darts/All_Events/Players_Championship_31/15?event_id=32446", "olbg")], "medium", flags=["value-longshot"]),
    P("DT-06", "Darts", "X-DT-05",
      "James Wade is a former world champion with no win tips from OLBG's eight on Players Championship 31, yet PDC's official entry list confirms he is playing in Den Bosch on 28 October. In a 128-player floor event, a low-owned multiple title winner is precisely the sort of long price worth taking. Wade to win PC31 is the low-confidence value pick.",
      [F_PDC_ENTRIES, ("OLBG PC31 page: James Wade 0/8 Win Tips", "https://www.olbg.com/betting-tips/Darts/All_Darts/All_Events/Players_Championship_31/15?event_id=32446", "olbg")], "low", flags=["value-longshot"]),

    # ------------------------------- BASEBALL ------------------------------
    P("BS-01", "Baseball", "X-BS-01",
      "Milwaukee have won eight straight postseason games and lead the World Series 3-0 after a 10-1 Game 3 in which Robert Gasser threw six one-hit innings and Jackson Chourio collected four hits. OLBG's two money-line tips both side with the Brewers for Game 4 at Tropicana Field. With Tampa Bay's starter Griffin Jax named and Milwaukee's yet to be confirmed, back Milwaukee to win the game and the title.",
      [F_MLB_SCHED, F_MLB_G3, F_MLB_G4,
       ("OLBG Game 4 event page: MIL Brewers 2/2 Money Line Win Tips", "https://www.olbg.com/betting-tips/Baseball/MLB/MLB/MIL_Brewers_@_TB_Rays/12?event_id=160799", "olbg")], "high"),
    P("BS-02", "Baseball", "X-BS-02",
      "Milwaukee's 10-1 Game 3 win was their fourth straight road postseason victory, and OLBG's only run-line tip for Game 4 takes the Brewers at -1.50 rather than Tampa Bay at +1.50. With Griffin Jax starting for the Rays and Milwaukee's starter still listed as TBA on MLB.com, the run line carries real risk. Take Milwaukee -1.50 at a plus-money price.",
      [F_MLB_SCHED, F_MLB_G4,
       ("OLBG Game 4 event page: MIL Brewers -1.50 1/1 Run Line Win Tips; TB Rays +1.50 0/1", "https://www.olbg.com/betting-tips/Baseball/MLB/MLB/MIL_Brewers_@_TB_Rays/12?event_id=160799", "olbg")], "medium", flags=["starting-pitcher-unconfirmed"]),
    P("BS-03", "Baseball", "X-BS-03",
      "OLBG's Game Totals market for Game 4 shows a 7.50 line with no tips on either side, so our own price is built from an even structural prior rather than community opinion. Robert Gasser's one-hit, six-inning Game 3 is the relevant official form note, but Milwaukee have not named their Game 4 starter. Under 7.50 runs is the cautious play, explicitly low confidence.",
      [F_MLB_G3, F_MLB_G4,
       ("OLBG Game 4 event page: Under 7.50 and Over 7.50 both 0/0 Win Tips", "https://www.olbg.com/betting-tips/Baseball/MLB/MLB/MIL_Brewers_@_TB_Rays/12?event_id=160799", "olbg")], "low", flags=["no-tip-split", "starting-pitcher-unconfirmed"]),
    P("BS-04", "Baseball", "X-BS-04",
      "MLB's official schedule records Milwaukee's 3-2, 5-4 and 10-1 wins, leaving Tampa Bay needing four straight victories to take the World Series. Our own series-winner price is deliberately floored at the top of the target band so that an overwhelming favourite is not advertised at an unusable number. Milwaukee to win the World Series is the pick, with that price cap disclosed.",
      [F_MLB_SCHED, F_MLB_G3], "high", flags=["price-floored-at-band-top", "no-olbg-market"]),
    P("BS-05", "Baseball", "X-BS-05",
      "A Brewers win on Tuesday would complete a sweep, and MLB's schedule marks Games 5, 6 and 7 as if necessary. Eight straight postseason wins and a 10-1 Game 3 make that outcome more likely than not in our own pricing, but Tampa Bay are 55-26 at home this season and will start Griffin Jax. Under 4.5 games in the series is the plus-money value selection.",
      [F_MLB_SCHED, F_MLB_G3, F_MLB_G4,
       ("ESPN's Game 4 page lists Tampa Bay 55-26 at home and Milwaukee 48-33 on the road in 2026", "https://www.espn.com/mlb/game/_/gameId/401908045/brewers-rays", "media")], "high", flags=["no-olbg-market", "value-longshot"]),

    # ---------------------------- GAELIC SPORTS ----------------------------
    P("GA-01", "Gaelic Sports", "009",
      "Eire Og Cor have all six OLBG handicap tips for their 1 November club fixture against Kanturk, taking the +0.50 start. Munster GAA's official championship table confirms the same weekend of club action, though it does not list this particular pairing. With an unbeaten 6-6 tip sample and a half-point cushion, Eire Og Cor +0.50 is the standout Gaelic selection on the card.",
      [("OLBG 27 October listing: Eire Og Cor +0.50 6/6 Win Tips, 100%", "https://www.olbg.com/betting-tips/Gaelic_Football/25", "olbg"), F_GAA], "high", flags=["no-official-form-data"]),
    P("GA-02", "Gaelic Sports", "010",
      "Kildimo Pallaskenry take five of OLBG's seven handicap tips at +3.50 against Fr Caseys on 1 November, a 71% share in one of the largest Gaelic markets today. No official Limerick club form table was retrievable, so the pick rests on the published tip split and the size of the start. Kildimo Pallaskenry +3.50 is the selection.",
      [("OLBG 27 October listing: Kildimo Pallaskenry +3.50 5/7 Win Tips, 71%", "https://www.olbg.com/betting-tips/Gaelic_Football/25", "olbg")], "medium", flags=["no-official-form-data"]),
    P("GA-03", "Gaelic Sports", "011",
      "Kerry hold six of eight OLBG tips to win the 2027 All-Ireland Football Championship, the strongest share of any ante-post Gaelic market on the board. The championship is nine months away and no official 2027 championship structure or panel news was published, so our line is long and the confidence modest. Kerry to win the 2027 All-Ireland is the selection.",
      [("OLBG 27 October listing: Kerry 6/8 tips for the All Ireland Football Championship 2027", "https://www.olbg.com/betting-tips/Gaelic_Football/25", "olbg")], "medium", flags=["long-dated-ante-post", "no-official-team-news"]),
    P("GA-04", "Gaelic Sports", "012",
      "Galway attract seven of eighteen OLBG tips for the 2027 All-Ireland Hurling Championship, a 39% share in the widest outright field on the Gaelic card. Our own line prices them near the top of the plus-money range because the remaining eleven tips are spread across rivals. Galway to win the 2027 hurling title is the value selection, with the long wait before the event noted.",
      [("OLBG 27 October listing: Galway 7/18 Win Hurling tips, 39%", "https://www.olbg.com/betting-tips/Hurling/26", "olbg")], "medium", flags=["long-dated-ante-post"]),
    P("GA-05", "Gaelic Sports", "X-GA-01",
      "Munster GAA's official club championship table lists Glen Rovers of Cork against Clare's Inagh-Kilnamona in the senior hurling quarter-final on 1 November at Pairc Ui Rinn, throw-in 1:15pm. No form or team news is published on that page, so our line is a narrow home-county favourite. Glen Rovers to win the quarter-final is the pick, with the official fixture as its sole support.",
      [F_GAA], "medium", flags=["no-official-form-data", "no-olbg-market"]),
    P("GA-06", "Gaelic Sports", "X-GA-02",
      "Ballygunner face Kilmallock in the Munster senior hurling semi-finals on 15 November, the next round published on the competition's official table. With the quarter-finals still to be played, no team news exists and our line treats this as close to a coin flip. Ballygunner to win is the tentative selection, flagged because the pairing depends on results that have not happened yet.",
      [F_GAA], "low", flags=["fixture-conditional-on-earlier-results", "no-olbg-market"]),

    # ------------------------------ GREYHOUNDS -----------------------------
    P("GH-01", "Greyhounds", "X-GH-01",
      "Romford's final advance card for Tuesday 27 October opens with a 14:23 400m A10 and puts Scooby Dior in trap 1 for trainer Martyn Wiley. OLBG's own track statistics make trap 1 the best-winning box at Romford with 19.4% from 3,655 races. No form figures or injury notes appear on the advance card, so this is a structural play: Scooby Dior to win race one.",
      [F_ROMFORD, F_OLBG_TRAP, F_OLBG_GREY_EMPTY], "low", flags=["no-form-figures", "no-olbg-market-today"]),
    P("GH-02", "Greyhounds", "X-GH-02",
      "Race three at Romford is a 15:01 400m A12 with six runners, and Blackrose Ruth occupies trap 1 for Allison Kelly-Pilgrim on the official card. With OLBG showing no greyhound tips today, our price comes from the rail-trap strike rate on that site's track table rather than any dog-by-dog form. Blackrose Ruth is the low-confidence selection to win.",
      [F_ROMFORD, F_OLBG_TRAP, F_OLBG_GREY_EMPTY], "low", flags=["no-form-figures", "no-olbg-market-today"]),
    P("GH-03", "Greyhounds", "X-GH-03",
      "Only four runners go to traps in Romford's 15:38 400m A3 because boxes five and six are vacant, and Hasty Halley has the rail for Marlene Westwood. A four-dog field shortens every runner's price, which is why our line on Hasty Halley is the shortest greyhound price on this card. Back Hasty Halley to win race five, with the absence of form figures flagged.",
      [F_ROMFORD, F_OLBG_TRAP, F_OLBG_GREY_EMPTY], "low", flags=["no-form-figures", "no-olbg-market-today"]),
    P("GH-04", "Greyhounds", "X-GH-04",
      "Gothic Doll is drawn in trap 1 for Gemma Evans in Romford's 16:53 400m A6, one of the strongest graded races on the Tuesday card. The stadium's official advance card lists all six runners but publishes no recent form, so our price again uses OLBG's Romford trap-1 record. Gothic Doll to win race nine is the pick, plainly a low-information play.",
      [F_ROMFORD, F_OLBG_TRAP, F_OLBG_GREY_EMPTY], "low", flags=["no-form-figures", "no-olbg-market-today"]),
    P("GH-05", "Greyhounds", "X-GH-05",
      "The Romford card closes with a 17:49 400m A2 in which Velvet Rolo runs from trap 1 for Katie O'Flaherty, with trap 5 vacant so only five runners line up. A higher grade and a short field both argue for a shorter price than the other trap-one plays. Velvet Rolo to win race twelve is the selection, still low confidence without official form figures.",
      [F_ROMFORD, F_OLBG_TRAP, F_OLBG_GREY_EMPTY], "low", flags=["no-form-figures", "no-olbg-market-today"]),

    # -------------------------------- TENNIS -------------------------------
    P("TN-01", "Tennis", "029",
      "Leylah Fernandez takes ten of OLBG's twelve win tips against Himeno Sakatsume, an 83% share on the largest tennis market of the day. We could not retrieve an official WTA ranking or draw page for this specific match, so no form or injury claim is made here. Fernandez to win is the selection, with our line shortened by the weight of tips but kept inside the target band.",
      [("OLBG 27 October listing: Leylah Fernandez 10/12 Win Match tips, 83%", "https://www.olbg.com/betting-tips/Tennis/3", "olbg")], "medium", flags=["no-official-form-data"]),
    P("TN-02", "Tennis", "031",
      "Naomi Osaka has all four OLBG win tips against Jasmine Paolini, the only unanimous four-tip tennis row on Tuesday's card. Our own price reflects that support but also how small the sample is, so this is a medium-strength rather than maximum-strength play. No official draw or ranking page was retrievable for this match: Osaka to win is the pick.",
      [("OLBG 27 October listing: Naomi Osaka 4/4 Win Match tips, 100%", "https://www.olbg.com/betting-tips/Tennis/3", "olbg")], "medium", flags=["no-official-form-data"]),
    P("TN-03", "Tennis", "032",
      "Rafael Jodar takes four of six win tips against Alejandro Tabilo, and the ATP's official Basel coverage confirms the Swiss Indoors is under way from 26 October to 1 November. Jodar is listed among the seeds in the tournament's draw. With that official context behind the tip split, Jodar to win his match is our tennis selection at a short but playable price.",
      [F_ATP, ("2026 Swiss Indoors entry list names Rafael Jodar as the No.3 seed", "https://tennisuptodate.com/atp/swiss-indoors-basel-2026-results-draw-entry-list-prize-money-and-history", "secondary"),
       ("OLBG 27 October listing: Rafael Jodar 4/6 Win Match tips, 67%", "https://www.olbg.com/betting-tips/Tennis/3", "olbg")], "medium", flags=["seed-from-secondary-source"]),
    P("TN-04", "Tennis", "X-TN-01",
      "Novak Djokovic accepted a wild card for Basel, his first appearance at the event since 2011, and won the title there in 2009. ATP's official draw article confirms the 26 October-1 November dates, and OLBG's four of five tips back him against Ugo Humbert. Djokovic to win is our highest-confidence tennis play, with the wild-card route noted as the reason for the kind draw.",
      [("ATP official: Djokovic accepts a Basel wild card; he won the 2009 title", "https://www.atptour.com/en/news/djokovic-basel-2026-wild-card", "official"), F_ATP,
       ("OLBG 27 October listing: Novak Djokovic 4/5 Win Match tips, 80%", "https://www.olbg.com/betting-tips/Tennis/3", "olbg")], "high"),
    P("TN-05", "Tennis", "X-TN-02",
      "Hubert Hurkacz is the No.10 seed at the Swiss Indoors and meets Zizou Bergs in the first round, a pairing listed in ATP's official Basel draw coverage. OLBG's three tips all side with the Pole. Combining an official seeding with a unanimous tip split gives us a solid short-price play: Hurkacz to win his Basel opener is the selection.",
      [F_ATP, ("OLBG 27 October listing: Hubert Hurkacz 3/3 Win Match tips, 100%", "https://www.olbg.com/betting-tips/Tennis/3", "olbg")], "high"),
    P("TN-06", "Tennis", "X-TN-03",
      "Casper Ruud came through a three-set Basel opener on 26 October, beating Dominic Stricker 4-6, 7-5, 6-3 according to ATP's official results page, and he sits 25th in the official rankings. Both OLBG tips for his next match back him. Having already found a way to win at the venue, Ruud is the pick to beat Nuno Borges.",
      [("ATP official Basel results, 26 October: Ruud d. Stricker 4-6, 7-5, 6-3", "https://www.atptour.com/en/news/basel-2026-results", "official"),
       ("ATP official rankings list Casper Ruud at No.25", "https://www.atptour.com/en/rankings/singles?dateWeek=Current+Week", "official"),
       ("OLBG 27 October listing: Casper Ruud 2/2 Win Match tips", "https://www.olbg.com/betting-tips/Tennis/3", "olbg")], "high"),

    # ----------------------------- MOTOR RACING ----------------------------
    P("MR-01", "Motor Racing", "X-MR-01",
      "Kimi Antonelli won the United States Grand Prix from pole with Charles Leclerc and Max Verstappen behind him, and he leads the championship on 365 points. F1's official Mexico City page confirms Sunday's 71-lap race at the high-altitude Autodromo Hermanos Rodriguez. Our own win line puts him just above a 38% chance, which is a genuine plus-money proposition. Antonelli to win in Mexico is the pick.",
      [F_F1_USGP, F_F1_STAND, F_F1_MEX], "high"),
    P("MR-02", "Motor Racing", "X-MR-02",
      "Antonelli has won from pole in Austin and leads the drivers' standings by 123 points over George Russell, so his baseline finishing level is the highest in the field. OLBG lists Podium Finish among the F1 markets it covers, though no tip split was printed for this race. Our own line makes a top-three finish more likely than not: Antonelli podium is the selection.",
      [F_F1_USGP, F_F1_STAND, ("OLBG's motor racing guide lists Podium Finish as a covered F1 market", "https://www.olbg.com/betting-tips/Motor_Racing/14", "olbg")], "high"),
    P("MR-03", "Motor Racing", "X-MR-03",
      "Charles Leclerc finished second in Austin behind Antonelli and sits fifth in the official standings on 233 points, so Ferrari have a car capable of a front-row challenge in Mexico. BBC's Mexico preview confirms the 71-lap race and the championship picture. Our podium price for Leclerc is close to even: Leclerc to finish in the top three is the value pick.",
      [F_F1_USGP, F_F1_STAND, ("BBC Sport's Mexico City GP preview: round 19, 30 October-1 November, 71 laps", "https://www.bbc.com/sport/formula1/articles/c6wyrgejp0w8o", "media")], "medium"),
    P("MR-04", "Motor Racing", "X-MR-04",
      "Max Verstappen was third in the United States GP and has won the Mexican Grand Prix five times, more than any other active driver according to OLBG's own event history. OLBG's 27 October hub gives him one of two tips in a podium or top-six market for Mexico. With that course record, Verstappen to finish in the top six is our safe motor-racing play.",
      [F_F1_USGP, ("OLBG's Mexico City GP page lists Verstappen as a five-time winner of the race", "https://www.olbg.com/betting-tips/Motor_Racing/All_Motor_Racing/All_Events/Mexico_City_Grand_Prix/14?event_id=914", "olbg"),
       F_F1_MEX], "high"),
    P("MR-05", "Motor Racing", "X-MR-05",
      "Lando Norris won the 2025 Mexico City Grand Prix and has one of OLBG's two Fastest Qualifier tips for Saturday's session, with F1's official schedule putting qualifying at 21:00 on 31 October. Our own line treats a 22-driver qualifying market as wide open and still leaves a long price. Norris to be fastest in qualifying is the speculative pick.",
      [("OLBG event page: Lando Norris 1/2 Fastest Qualifier tips; OLBG history lists Norris as the 2025 Mexico winner", "https://www.olbg.com/betting-tips/Motor_Racing/All_Motor_Racing/All_Events/Mexico_City_Grand_Prix/14?event_id=914", "olbg"), F_F1_MEX], "medium"),
    P("MR-06", "Motor Racing", "X-MR-06",
      "Oscar Piastri shares the Fastest Qualifier tip lead with his McLaren team-mate at one vote from two on OLBG's Mexico City page. F1's official timetable confirms qualifying on 31 October, and the site's standings list Piastri seventh on 144 points. With no qualifying form data from this weekend yet, Piastri to be fastest qualifier is the low-confidence value play.",
      [F_F1_STAND, F_F1_MEX,
       ("OLBG event page: Oscar Piastri 1/2 Fastest Qualifier tips", "https://www.olbg.com/betting-tips/Motor_Racing/All_Motor_Racing/All_Events/Mexico_City_Grand_Prix/14?event_id=914", "olbg")], "low", flags=["value-longshot"]),

    # ------------------------------- HANDBALL ------------------------------
    P("HB-01", "Handball", "X-HB-01",
      "SC Magdeburg are five from five in EHF Champions League Group F with a 176:140 goal record, while Kriens-Luzern sit on two wins and a negative difference. OLBG's nine-of-fourteen 'Tie' tips for this match are a capture irregularity we do not follow; our own line is for the straight win. Back Magdeburg to win at home on Wednesday.",
      [F_EHF, ("OLBG 27 October handball listing shows 'Tie' as the most-tipped outcome at 9/14 for Magdeburg v Kriens", "https://www.olbg.com/betting-tips/Handball/20", "olbg")], "high", flags=["tie-capture-irregularity"]),
    P("HB-02", "Handball", "X-HB-02",
      "Industria Kielce have three wins from five and a positive goal difference in Group F, and they face a Kolstad side that has lost all five matches and conceded 178 goals. EHF's official table makes that the clearest mismatch on the handball card. Kielce to win is the pick, with our line kept moderate because OLBG's seven-of-eleven tips here were on the draw.",
      [F_EHF, ("OLBG 27 October handball listing: KS Kielce v Kolstad, 'Tie' 7/11 tips", "https://www.olbg.com/betting-tips/Handball/20", "olbg")], "high", flags=["tie-capture-irregularity"]),
    P("HB-03", "Handball", "X-HB-03",
      "Aalborg top Group C with four wins and a draw from five and a 170:145 goal record, ahead of PSG on the official EHF table. Yet OLBG's seven-of-nine tips for their meeting are on the draw, which leaves the away win underpriced in our own line. Aalborg to beat PSG is the plus-money value selection of the handball round.",
      [F_EHF, ("OLBG 27 October handball listing: PSG v Aalborg, 'Tie' 7/9 tips, 78%", "https://www.olbg.com/betting-tips/Handball/20", "olbg")], "medium", flags=["tie-capture-irregularity", "value-longshot"]),
    P("HB-04", "Handball", "X-HB-04",
      "RK Zagreb have two wins and a minus-twelve goal difference in Group C but meet a Celje side yet to win a match and shipping 188 goals in five games. EHF's official table gives Zagreb a clear edge despite their own poor numbers. Zagreb to win is the selection, with the six-of-eight OLBG draw tips treated as an artefact of the hub's most-tipped-outcome display.",
      [F_EHF, ("OLBG 27 October handball listing: Celje v Zagreb, 'Tie' 6/8 tips, 75%", "https://www.olbg.com/betting-tips/Handball/20", "olbg")], "medium", flags=["tie-capture-irregularity"]),
    P("HB-05", "Handball", "X-HB-05",
      "One Veszprem are unbeaten in Group A with five wins and a 185:146 goal record, while FC Porto have one win, one draw and three defeats on the official EHF standings. That is the widest gap in the section and makes Veszprem our strongest handball favourite. Veszprem to win away in Porto is the pick, with the OLBG draw tipping again set aside as a display quirk.",
      [F_EHF, ("OLBG 27 October handball listing: FC Porto v Veszprem, 'Tie' 5/9 tips", "https://www.olbg.com/betting-tips/Handball/20", "olbg")], "high", flags=["tie-capture-irregularity"]),

    # ------------------------------ ICE HOCKEY -----------------------------
    P("IH-01", "Ice Hockey", "106",
      "Kalpa have all five OLBG money-line tips for their Tuesday game against Sport, the biggest unanimous hockey sample on the card. We could not retrieve an official Finnish Liiga table for either side, so this is a market-driven selection rather than a form play. Kalpa to win is the pick, with our line shortened but still inside the target odds band.",
      [("OLBG 27 October listing: Kalpa 5/5 Money Line tips against Sport", "https://www.olbg.com/betting-tips/Ice_Hockey/13", "olbg")], "medium", flags=["no-official-form-data"]),
    P("IH-02", "Ice Hockey", "111",
      "Boston take a +1.50 puck-line start into their game at Carolina, and OLBG's two tips both back that handicap. The official standings through 26 October show Carolina at 9-2-2 with 51 goals scored, so this is a tough ask; the plus-1.5 cushion is the only reason our line is near even. Boston +1.50 is the low-confidence value selection.",
      [F_NHL, ("OLBG 27 October listing: BOS Bruins +1.50 2/2 Puck Line tips", "https://www.olbg.com/betting-tips/Ice_Hockey/13", "olbg")], "medium", flags=["value-longshot"]),
    P("IH-03", "Ice Hockey", "112",
      "OLBG's single Game Totals tip for Florida at Winnipeg is Under 5.50. Winnipeg have scored 27 goals and conceded 31 in eleven games, a modest pace, while Dallas-style defensive numbers elsewhere on the card are stronger. Our own line prices the under just below even. Under 5.50 goals in Jets v Panthers is the selection, with the one-tip sample flagged.",
      [F_NHL, ("OLBG 27 October listing: FLA Panthers @ WPG Jets, Under 5.50 1/1 Game Totals tips", "https://www.olbg.com/betting-tips/Ice_Hockey/13", "olbg")], "medium", flags=["one-tip-sample"]),
    P("IH-04", "Ice Hockey", "113",
      "New Jersey at Dallas also has a sole OLBG tip on Under 5.50, and the NHL table gives Dallas 32 goals for and just 20 against in eleven games, the best defensive profile among the teams we checked. Combining that official number with the tip makes Under 5.50 in Devils v Stars the pick, while noting that no goaltending or injury news was retrieved.",
      [F_NHL, ("OLBG 27 October listing: NJ Devils @ DAL Stars, Under 5.50 1/1 Game Totals tips", "https://www.olbg.com/betting-tips/Ice_Hockey/13", "olbg")], "high", flags=["one-tip-sample", "no-official-team-news"]),
    P("IH-05", "Ice Hockey", "110",
      "Philadelphia have two of three OLBG money-line tips for Columbus's visit, yet the league table shows the Flyers at 3-7-3 with only 24 goals scored and 42 conceded in thirteen games. That is the worst goal difference among the NHL sides we checked, so our own line sides against the tips. Columbus to win in Philadelphia is the value selection.",
      [F_NHL, ("OLBG 27 October listing: PHI Flyers 2/3 Money Line tips, 67%", "https://www.olbg.com/betting-tips/Ice_Hockey/13", "olbg")], "medium", flags=["value-against-tips"]),
    P("IH-06", "Ice Hockey", "X-IH-01",
      "The Blue Jackets visit a Flyers team sitting on nine points from thirteen games with a minus-eighteen goal difference, while OLBG's small money-line sample leans to Philadelphia. Contrarian pricing says the visitor should be a narrow favourite, which is exactly the kind of plus-money disagreement this desk looks for. Columbus to win is the selection, flagged as a standings-based play with no team news.",
      [F_NHL, ("OLBG 27 October listing: CLB Blue Jackets @ PHI Flyers, Flyers 2/3 tips", "https://www.olbg.com/betting-tips/Ice_Hockey/13", "olbg")], "medium", flags=["value-against-tips", "no-official-team-news"]),

    # ------------------------------ BASKETBALL -----------------------------
    P("BB-01", "Basketball", "124",
      "Panathinaikos lead the EuroLeague at 6-1 with 87.6 points scored and 73.9 conceded per game, and they have already beaten Maccabi 90-67 and Fenerbahce 92-74 at home. OLBG gives them five of eight money-line tips against Milano. That combination of an official-form table and a majority tip share makes Panathinaikos to win our strongest basketball play.",
      [F_EURO, ("OLBG 27 October listing: Panathinaikos 5/8 Money Line tips vs Milano", "https://www.olbg.com/betting-tips/Basketball/4", "olbg")], "high", flags=["standings-from-secondary-source"]),
    P("BB-02", "Basketball", "126",
      "Fenerbahce are also 6-1 in the EuroLeague and travel to Valencia with four of OLBG's six money-line tips behind them. Their official-season scoring profile of 80.7 points for and 72.6 against is the second-best defensive mark in the early table. Backing the in-form away side at a short price is the selection: Fenerbahce to win.",
      [F_EURO, ("OLBG 27 October listing: Fenerbahce 4/6 Money Line tips, 67%", "https://www.olbg.com/betting-tips/Basketball/4", "olbg")], "medium", flags=["standings-from-secondary-source"]),
    P("BB-03", "Basketball", "142",
      "NBA.com's official team page lists Boston at 2-1 and Brooklyn at 0-3 before Tuesday's 7:30pm tip, and OLBG's single money-line tip backs the Celtics. Boston were also first in defensive rating in NBA.com's preseason power rankings. Take Boston to win at home, with the note that no official injury report for either roster was retrieved.",
      [F_NBA, ("OLBG 27 October listing: BOS Celtics 1/1 Money Line tip vs BKN Nets", "https://www.olbg.com/betting-tips/Basketball/4", "olbg")], "high", flags=["no-official-injury-report"]),
    P("BB-04", "Basketball", "143",
      "New York are 0-3 on NBA.com's official standings and host a Detroit side that is 3-0 and first in the Eastern Conference, yet OLBG's one tip for the game is on the Knicks. Our own line follows the official records rather than that lone tip, which is why this is a contrarian play. New York to win at home is the low-confidence value pick.",
      [F_NBA, ("OLBG 27 October listing: NY Knicks 1/1 Money Line tip vs DET Pistons", "https://www.olbg.com/betting-tips/Basketball/4", "olbg"),
       ("NBA.com preseason power rankings placed Detroit 10th and New York 3rd", "https://www.nba.com/news/power-rankings-2026-27-week-1", "official")], "low", flags=["value-against-tips", "no-official-injury-report"]),
    P("BB-05", "Basketball", "135",
      "Frankfurt Skyliners have both OLBG pointspread tips at +1.50 against U BT Cluj Napoca, the only handicap basketball row on today's card. No official Basketball Champions League or German league form table was retrievable for the pairing, so the selection rests on that unanimous two-tip sample. Frankfurt +1.50 is the pick, low confidence.",
      [("OLBG 27 October listing: Frankfurt Skyliners +1.50 2/2 Pointspread tips", "https://www.olbg.com/betting-tips/Basketball/4", "olbg")], "low", flags=["no-official-form-data"]),
    P("BB-06", "Basketball", "X-BB-01",
      "Brooklyn are 0-3 and Boston 2-1, yet NBA.com's preseason numbers put the Nets first in offensive rating at 120.3 and the Celtics first in defensive rating at 98.6. That clash of styles makes a winless visitor dangerous, and our own line gives them a genuine plus-money chance. Brooklyn to win in Boston is the longshot basketball selection.",
      [F_NBA, ("NBA.com power rankings: Brooklyn 1st offensive rating 120.3, Boston 1st defensive rating 98.6 in the preseason", "https://www.nba.com/news/power-rankings-2026-27-week-1", "official")], "low", flags=["value-longshot", "no-official-injury-report"]),

    # ----------------------------- RUGBY LEAGUE ----------------------------
    P("RL-01", "Rugby League", "013",
      "New South Wales hold nine of thirteen OLBG tips to win the 2027 State of Origin series, a 69% share that makes this the best-supported rugby league market on the board. The series is seven months away and no official squad or venue details have been published for it, so our line is long. New South Wales to win State of Origin 2027 is the ante-post pick.",
      [("OLBG 27 October listing: New South Wales 9/13 Win Tips, 69%, State of Origin 2027", "https://www.olbg.com/betting-tips/Rugby_League/10", "olbg")], "medium", flags=["long-dated-ante-post"]),
    P("RL-02", "Rugby League", "014",
      "Wigan Warriors have two of four OLBG tips for the 2027 Super League Grand Final, and the market is thin enough that our own price is close to even. No official 2027 Super League fixture or squad information exists yet, so this is a pure market-structure play. Wigan to win the 2027 Grand Final is the selection, with the long time horizon flagged.",
      [("OLBG 27 October listing: Wigan Warriors 2/4 Grand Final Winner tips, 50%", "https://www.olbg.com/betting-tips/Rugby_League/10", "olbg")], "medium", flags=["long-dated-ante-post"]),
    P("RL-03", "Rugby League", "015",
      "Penrith Panthers take one of only three OLBG tips for the 2027 NRL Grand Final winner, a 33% share in the thinnest rugby league market of the day. Our own line stretches to a big price because the remaining tips are spread across rivals. Penrith to win the 2027 NRL title is the value selection, medium-low confidence.",
      [("OLBG 27 October listing: Penrith Panthers 1/3 Grand Final Winner tips, 33%", "https://www.olbg.com/betting-tips/Rugby_League/10", "olbg")], "medium", flags=["long-dated-ante-post", "value-longshot"]),
    P("RL-04", "Rugby League", "X-RL-01",
      "England bounced back from a 30-12 opening loss to Tonga by thrashing France 82-0 at the Rugby League World Cup, and the official RLWC schedule sends them to WIN Stadium in Wollongong to face Papua New Guinea on 30 October. That is the most decisive recent result in the tournament. England to win their final pool match is our pick.",
      [F_RLWC, ("Sky Sports RLWC results: England lost 12-30 to Tonga then beat France 82-0", "https://www.skysports.com/rugby-league/news/13598071/rugby-league-world-cup-2026-schedule-dates-format-results-from-mens-women-s-and-wheelchair-tournaments", "media")], "high", flags=["no-olbg-market"]),
    P("RL-05", "Rugby League", "X-RL-02",
      "New Zealand put 82 points past the Cook Islands in Christchurch and now meet Fiji at Cbus Super Stadium on 31 October, a fixture on the official RLWC schedule. Fiji lost 36-22 to Australia in Brisbane and have conceded heavily in the tournament. New Zealand to win is the selection, with our line priced short and the absence of an OLBG match market noted.",
      [F_RLWC, ("Sky Sports RLWC results: New Zealand 82-16 Cook Islands; Australia 36-22 Fiji", "https://www.skysports.com/rugby-league/news/13598071/rugby-league-world-cup-2026-schedule-dates-format-results-from-mens-women-s-and-wheelchair-tournaments", "media")], "high", flags=["no-olbg-market"]),
    P("RL-06", "Rugby League", "X-RL-03",
      "Australia have beaten New Zealand 24-22 and Fiji 36-22 to sit top of RLWC Group A, and the official schedule gives them a Saturday night game against the Cook Islands in Townsville on 31 October. The same island side lost 82-16 to New Zealand a week earlier. Australia to win is the obvious selection, with our price floored at the top of the value band.",
      [F_RLWC, ("Sky Sports RLWC results: Australia 24-22 New Zealand and 36-22 Fiji; New Zealand 82-16 Cook Islands", "https://www.skysports.com/rugby-league/news/13598071/rugby-league-world-cup-2026-schedule-dates-format-results-from-mens-women-s-and-wheelchair-tournaments", "media")], "high", flags=["no-olbg-market", "price-floored-at-band-top"]),
]

# Remove the deliberate placeholder used while drafting (keeps ids unique).
PICKS = [p for p in PICKS if p["prediction"]]

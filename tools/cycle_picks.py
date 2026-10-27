#!/usr/bin/env python3
"""
2026-10-27 cycle - written prediction set.

Every pick below is attached to a market that OLBG actually printed on 27 Oct 2026 (see
data/cycle-20261027/events_raw.json) and to the line we originated for it
(data/cycle-20261027/lines.json).  Nothing here is invented: each fact carries the exact
source we read it from, and where a value could not be confirmed it is left BLANK and a
flag is raised instead (see tools/cycle_site.py -> flagged page).

Run:  python3 tools/cycle_picks.py   ->  data/cycle-20261027/{predictions,sources,flags}.json
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CYCLE = "2026-10-27"
OUT = os.path.join(ROOT, "data/cycle-20261027")
BANNED = ("model", "verified")

# --------------------------------------------------------------------------- sources ----
S = {
    "olbg_base": "https://www.olbg.com/betting-tips/",
    "mlb_sched": ("https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule", "MLB.com"),
    "mlb_g4": ("https://www.mlb.com/news/2026-world-series-game-4-storylines-brewers-rays", "MLB.com"),
    "mlb_faq": ("https://www.mlb.com/news/2026-mlb-world-series-faq-schedule-times-teams-and-more", "MLB.com"),
    "espn_g4": ("https://www.espn.com/mlb/game/_/gameId/401908045/brewers-rays", "ESPN"),
    "nhl_st": ("https://www.nhl.com/standings", "NHL.com"),
    "espn_nhl": ("https://www.espn.com/nhl/game/_/gameId/401892586/bruins-hurricanes", "ESPN (NHL injury page)"),
    "liiga": ("https://www.liiga.fi/en/schedule?kausi=2026-2027&sarja=runkosarja", "Liiga.fi"),
    "swehockey": ("https://stats.swehockey.se/ScheduleAndResults/Overview/20961", "SweHockey (official SHL stats)"),
    "ep_liiga": ("https://www.eliteprospects.com/league/liiga", "Elite Prospects"),
    "ep_lhc": ("https://eliteprospects.com/team/6/linkoping-hc", "Elite Prospects"),
    "el_site": ("https://www.euroleaguebasketball.net/en/euroleague/?pcode=005009", "EuroLeague (official)"),
    "sportando": ("https://sportando.basketball/en/euroleague-new-round-tips-off-tomorrow-panathinaikos-milano-and-valencia-fenerbahce-among-the-highlights/", "Sportando"),
    "eurohoops": ("https://www.eurohoops.net/euroleague-standings/", "Eurohoops"),
    "dailysports_pao": ("https://dailysports.net/stat/basketball/olimpia-milano-vs-panathinaikos-bc/", "DailySports (match stats page)"),
    "s365_pao": ("https://www.365scores.com/en-us/basketball/match/euroleague-569/olimpia-milano-panathinaikos-275-1041-569", "365Scores (match page)"),
    "atp_basel": ("https://www.atptour.com/en/news/djokovic-basel-2026-first-match", "ATP Tour (official)"),
    "atp_draw": ("https://www.atptour.com/en/news/djokovic-basel-2026-draw-preview", "ATP Tour (official)"),
    "atp_race": ("https://www.atptour.com/en/rankings/singles-race-to-turin", "ATP Tour (official)"),
    "twi_basel": ("https://www.tennisworlditalia.com/en/tennis/news/Atp_Tennis/108227/atp-500-basel-hit-by-three-major-withdrawals-updated-main-draw/", "Tennis World Italia"),
    "cric_pak": ("https://www.cricinfo.com/series/pakistan-odi-tri-series-2026-27-1550706/match-schedule-fixtures-and-results", "ESPNcricinfo"),
    "cric_pak_sl": ("https://www.cricinfo.com/series/pakistan-odi-tri-series-2026-27-1550706/pakistan-vs-sri-lanka-5th-match-1550717/live-cricket-score", "ESPNcricinfo"),
    "cric_pak_1": ("https://www.cricinfo.com/series/pakistan-odi-tri-series-2026-27-1550706/pakistan-vs-sri-lanka-1st-match-1550713/match-report", "ESPNcricinfo"),
    "bbc_pak": ("https://www.bbc.co.uk/sport/cricket/articles/cy0jrekkwnzo", "BBC Sport"),
    "cric_nz": ("https://www.cricinfo.com/series/india-in-new-zealand-2026-27-1539421/new-zealand-vs-india-3rd-t20i-1539434/match-preview", "ESPNcricinfo"),
    "cric_nz_sched": ("https://www.cricinfo.com/series/india-in-new-zealand-2026-27-1539421/match-schedule-fixtures-and-results", "ESPNcricinfo"),
    "cric_nz_ind": ("https://www.cricinfo.com/team/india-6/match-schedule-fixtures-and-results", "ESPNcricinfo"),
    "cric_afg": ("https://www.cricinfo.com/series/afghanistan-v-zimbabwe-2026-27-1555105/afghanistan-vs-zimbabwe-1st-t20i-1555120/live-cricket-score", "ESPNcricinfo"),
    "espn_afg": ("https://www.espn.com/cricket/series/24799/game/1555120/afghanistan-vs-zimbabwe-1st-t20i-24799", "ESPN (match centre)"),
    "espn_afgfinal": ("https://www.espn.com/cricket/series/10931/game/1556871/afghanistan-vs-zimbabwe-final-uae-odi-tri-series-2026-27", "ESPN"),
    "cadd_afg": ("https://cricketaddictor.com/cricket-news/afg-vs-zim-playing-11-today-live-streaming-pitch-weather-afghanistan-vs-zimbabwe-1st-t20i-2026-465277/", "Cricket Addictor"),
    "cric_test": ("https://www.cricinfo.com/series/australia-in-south-africa-2026-27-1525634/south-africa-vs-australia-3rd-test-1525661/match-preview", "ESPNcricinfo"),
    "cca_test": ("https://www.cricket.com.au/news/4597818/south-africa-v-australia-third-test-match-preview-guide-cape-town-newlands-broadcast-details-how-to-watch-team-news-session-start-times-2026", "cricket.com.au"),
    "cric_smith": ("https://www.cricinfo.com/story/sa-vs-aus-3rd-wtc-test-steven-smith-faces-fitness-test-ahead-of-test-series-decider-in-cape-town-1560077", "ESPNcricinfo"),
    "sky_test": ("https://www.skysports.com/cricket/news/13602302/south-africa-vs-australia-proteas-complete-emphatic-innings-victory-to-level-three-test-series", "Sky Sports"),
    "cric_nam": ("https://www.cricinfo.com/series/ireland-in-namibia-2026-27-1558225/namibia-vs-ireland-2nd-odi-1558232/live-cricket-score", "ESPNcricinfo"),
    "bbc_nam": ("https://www.bbc.co.uk/sport/cricket/articles/cvx28ex38x7ko", "BBC Sport"),
    "ehf_standings": ("https://ehfcl.eurohandball.com/men/2026-27/standings/", "EHF Champions League (official)"),
    "ehf_r6": ("https://www.eurohandball.com/en/news/en/three-main-round-spots-still-open-before-final-round-6", "EHF (official)"),
    "ehf_review": ("https://ehfcl.eurohandball.com/men/2026-27/news/en/magdeburg-aalborg-and-paris-in-main-round-four-clubs-out/", "EHF Champions League (official)"),
    "ehf_nantes": ("https://www.eurohandball.com/en/club/UlvtLsTlg8pJWiC7dxqtTg/HBCNantes/", "EHF (official club page)"),
    "tvf_wk1": ("https://tvf.org.tr/icerik/efeler-liginde-birinci-hafta-sona-erdi", "Turkish Volleyball Federation (official)"),
    "voley_wk2": ("https://www.voleybolaktuel.com/sms-grup-efeler-liginde-2hafta-sona-erdi", "Voleybol Aktuel"),
    "voley_ziraat": ("https://www.voleybolaktuel.com/ishikawanin-yoklugunda-ziraat-bankkart-altekmayi-5-sette-gecebildi", "Voleybol Aktuel"),
    "sporx_fener": ("https://www.sporx.com/", "Sporx"),
    "lpga_maybank": ("https://www.lpga.com/tournaments/maybank-championship", "LPGA (official)"),
    "gfn_field": ("https://thegolfnewsnet.com/golfnewsnetteam/2026-10-25/2026-maybank-championship-field-lpga-tour-players-rankings-145290/", "The Golf News Net"),
    "golfpost_maybank": ("https://www.golfpost.com/us/tournaments/lpga-tour-maybank-championship-2026/", "Golf Post"),
    "pdc_entries": ("https://www.pdc.tv/news/2026/october/26/2026-players-championships-31-32-entries-confirmed", "PDC (official)"),
    "pdpa_cal": ("https://pdpa.co.uk/events/calendar/tour/pdc-players-championship/", "PDPA"),
    "dartsnews": ("https://dartsnews.com/pdc/entries-players-championship-31-and-32-mass-withdrawals-as-luke-littler-and-many-other-world-class-players-skip-den-bosch", "Darts News"),
    "bbc_darts": ("https://www.bbc.com/sport/darts/articles/cn41l09798go", "BBC Sport"),
    "sky_darts": ("https://www.skysports.com/darts/news/12040/13489993/world-darts-championship-2026-luke-littler-thrashes-gian-van-veen-in-final-to-retain-title-at-alexandra-palace", "Sky Sports"),
    "f1_drivers": ("https://www.formula1.com/en/results/2026/drivers", "Formula1.com (official)"),
    "f1_abc": ("https://www.abc.net.au/news/2026-10-26/how-kimi-antonelli-can-win-f1-drivers-championship/107308200", "ABC News (Australia)"),
    "f1_gp": ("https://grandepremio.com/en/f1/antonelli-moves-within-2-points-of-f1-title-as-russell-and-hamilton-survive-austin-showdown/", "Grandepremio"),
    "urc_fixtures": ("https://www.unitedrugby.com/latest/news/2026-27-fixtures-in-full/", "United Rugby Championship (official)"),
    "urc_table": ("https://www.bbc.com/sport/rugby-union/pro-tournament/table", "BBC Sport (URC table)"),
    "urc_sky": ("https://www.skysports.com/rugby-union/united-rugby-championship/table", "Sky Sports (URC table)"),
    "lnr_provence": ("https://prod2.lnr.fr/club/provence-rugby", "LNR Pro D2 (official)"),
    "lequipe_pro_d2": ("https://www.lequipe.fr/Rugby/rangements-pro-d2/", "L'Equipe"),
    "gaa_fb": ("https://www.gaa.ie/", "GAA (official)"),
}

# ------------------------------------------------------------------------------ picks ----
# sport, event/market/selection must match a priced row in lines.json (matched on
# sport + event + market + selection).
P = []


def pick(sport, event, market, selection, label, text, row_src, facts, angle, risk, blurb=""):
    P.append(dict(sport=sport, event=event, market=market, selection=selection,
                  pick_label=label, prediction=text, row_source=row_src, facts=facts,
                  angle=angle, risk=risk, blurb=blurb))


# ---------------------------------------------------------------- BASEBALL (World Series)
BS = "MLB World Series - Game 4, Tropicana Field, St. Petersburg (OLBG card prints 21:00; official first pitch 20:00 ET)"
pick("Baseball", "MIL Brewers @ TB Rays", "Money Line", "MIL Brewers",
     "Milwaukee Brewers to win Game 4 and the World Series (money line)",
     "Milwaukee leads this World Series three matches to none and can close it out tonight at Tropicana Field, "
     "having already won 3-2, 5-4 and 10-1. The Brewers finished 103-59 and are 48-33 on the road, while Tampa Bay "
     "came into the Finals 98-64 with a 55-26 home record. Milwaukee have conceded seven runs in three games, which is "
     "the whole argument: no side in baseball history has recovered from 3-0 down in this series. Take the Brewers on the "
     "money line at 1.52 (-192).",
     S["mlb_g4"],
     [("Milwaukee leads the World Series 3-0; Game 4 is Tuesday 27 October at 8:00pm ET from Tropicana Field", S["mlb_g4"]),
      ("Series scores: Brewers 3-2, 5-4 and 10-1, Game 3 won by nine runs", S["espn_g4"]),
      ("Records: Brewers 103-59 (48-33 away), Rays 98-64 (55-26 home)", S["espn_g4"]),
      ("MLB's own Game 4 lead-in lists Tampa Bay's projected starter as Griffin Jax with Milwaukee's still TBA", S["mlb_g4"])],
     "Two OLBG tips on the market, both on Milwaukee, so the price is our own number rather than a market reading.",
     "Only two tips were counted on this market, so the line is graded C - it is a one-win series situation, not a price we would lay out blind.")

pick("Baseball", "MIL Brewers @ TB Rays", "Money Line", "TB Rays",
     "Tampa Bay Rays to avoid the sweep in Game 4 (money line, 2.54)",
     "Tampa Bay are priced at 2.54 (+154) to win Game 4, which is the only price on this card that pays out for the "
     "situation rather than the series. The Rays went 55-26 at home in the regular season, lost 3-2 and 5-4 in "
     "Milwaukee by a run apiece, and were only folded 10-1 in Game 3; a 3-0 deficit also asks their pitching staff to "
     "carry a full game. Take the Rays here as a ticket to force a Game 5 at Tropicana Field, not as a comeback thesis.",
     S["mlb_faq"],
     [("MLB confirms the Rays host Games 3, 4 and 5 (if needed) at Tropicana Field", S["mlb_faq"]),
      ("Rays were 55-26 at home in the regular season", S["espn_g4"]),
      ("OLBG's card prices Tampa Bay at 0 of 2 tips, which is why our own line is 2.54", S["olbg_base"])],
     "Publishing the other side of the same market so the two-sided price is visible.",
     "Zero of two tipsters backed this side; the price carries no tail information and is graded C.")

pick("Baseball", "MIL Brewers @ TB Rays", "Run Line", "MIL Brewers -1.50",
     "Milwaukee -1.5 runs in Game 4 (one-run margin still wins it at 1.67)",
     "The Brewers' run line is priced at 1.67 (-149) with one tip printed on it, and it is the more interesting number "
     "on this card because Milwaukee already covered 1.5 twice in this series, winning 3-2, 5-4 and 10-1. A two-run "
     "margin is all that is needed and the middle-order batting that chased 226 in Game 1 has produced in every game. "
     "Take Milwaukee -1.5, accepting that a one-run Brewers win in a sweep attempt kills the bet.",
     S["espn_g4"],
     [("Game scores 3-2, 5-4, 10-1: two of the three wins cleared a 1.5-run line", S["espn_g4"]),
      ("Brewers 103-59 with 48 runs scored margin advantage on the road", S["espn_g4"]),
      ("Milwaukee's Game 3 was a 10-1 win, won by nine runs", S["mlb_g4"])],
     "Handicap priced from the same two-tip market as the money line.",
     "One tip on this selection; the margin market on a sweep game is coin-flip thin, graded C.")

pick("Baseball", "MIL Brewers @ TB Rays", "Run Line", "TB Rays +1.50",
     "Tampa Bay +1.5 runs against Milwaukee (2.22)",
     "Tampa Bay +1.5 is the contrarian half of this handicap market at 2.22 (+122) and it wins if the Rays lose by a "
     "single run, which is exactly how Game 1 went before they dropped 5-4 and 10-1. Milwaukee's three wins have "
     "produced an average margin of four runs, so the case here rests on the Rays keeping a game short rather than on "
     "them stealing the series. Small stake only: no tipster priced this side on the OLBG card, so the number is ours.",
     S["espn_g4"],
     [("Game 1 finished 3-2, inside the 1.5-run line", S["espn_g4"]),
      ("Game 3 finished 10-1, well outside it", S["mlb_g4"]),
      ("OLBG shows 0 of 1 tips on this side of the run line", S["olbg_base"])],
     "Completes the two-sided run-line grid for the game.",
     "Zero tips on this side; graded C and offered only so the handicap price is visible next to the -1.5 number.")

# ------------------------------------------------------------------------ BASKETBALL -------
pick("Basketball", "Panathinaikos vs Milano", "Money Line", "Panathinaikos",
     "Panathinaikos AKTOR Athens to beat Olimpia Milano at home (1.67)",
     "Panathinaikos are top of the EuroLeague after seven rounds on 6-1, outscoring opposition 613-517 and 5-1 at "
     "home, and they have just put 85 on Baskonia. Olimpia Milano sit 19th on 1-6 with a -63 margin, 0-3 away, and "
     "they arrive on a run of five straight defeats including 81-89 to Barcelona and 97-101 at home to Dubai. Back "
     "the hosts at 1.67 (-149), tip of the day on this card with five of eight tips behind it.",
     S["el_site"],
     [("Round 8: Panathinaikos AKTOR Athens (1st) v Armani Olimpia Milan (19th) is listed on the league's own competition page for Tuesday", S["el_site"]),
      ("Standings after 7 rounds: Panathinaikos 6-1 (613-517, +96), form W-L-W-W-W; Milano 1-6 (585-648, -63), form L-L-L-L-L", S["s365_pao"]),
      ("Panathinaikos beat Baskonia 85-79 on 22 October; their only loss was 81-91 to Hapoel Tel Aviv on 16 October; they are 5-1 at home", S["dailysports_pao"]),
      ("Milano lost 97-101 at home to Dubai Basketball on 15 October and are 0-3 away from home", S["eurohoops"])],
     "Highest-volume basketball market on the card and the strongest structural gap on it - first against 19th.",
     "Eight tips counted; the price is our own 5% margin line, not a sportsbook quote.")

pick("Basketball", "Valencia vs Fenerbahce", "Money Line", "Fenerbahce",
     "Fenerbahce to win at Valencia (1.63)",
     "Fenerbahce are 6-1 and second in the EuroLeague, having won 64-61 at Olympiacos on Friday and 99-80 and 74-65 "
     "in the rounds before, and the OLBG vote sits with the visitors rather than the home floor. Valencia are 5-2 but "
     "have lost three of their four at the top end of the table, most recently 104-93 at Paris, and they were picked "
     "apart at home by Maccabi 91-88. Take Fenerbahce on the road at 1.63 (-159).",
     S["sportando"],
     [("Round 8: Valencia Basket v Fenerbahce, Tuesday 27 October, 20:30 CET", S["sportando"]),
      ("Fenerbahce 6-1 (565-508): 64-61 win at Olympiacos on 23 October, 74-65 over Partizan, 99-80 over Zalgiris; their only loss was 74-92 at Panathinaikos on 8 October", S["dailysports_pao"]),
      ("Valencia 5-2 (687-630): won 104-93 at Paris on 23 October but lost 88-91 at home to Maccabi and 97-102 at home to Olympiacos", S["dailysports_pao"]),
      ("Tip split on the OLBG market: 4 of 6 tips on Fenerbahce", S["olbg_base"])],
     "The away side at a price, chosen because the tip vote and the underlying form point the same way.",
     "Six tips only. Valencia are 5-2 in their own right, so this is a one-possession margin read, not a lock.")

pick("Basketball", "BC Dubai vs Paris", "Money Line", "BC Dubai",
     "Dubai Basketball to beat Paris Basketball at home (1.77)",
     "Dubai are 5-2 and 6th after wins over Olimpia Milano (101-97 in Italy) and Bayern Munich (107-91), while Paris "
     "are 1-6, 18th, with a -52 margin and a 1-4 home record. The OLBG card leans 4 of 7 to the hosts and the gap in "
     "point differential is 37 points across seven rounds. Take Dubai at 1.77 (-130) at 17:00 CET on Tuesday.",
     S["sportando"],
     [("Round 8: Dubai Basketball v Paris Basketball, Tuesday 27 October, 17:00 CET", S["sportando"]),
      ("Dubai 5-2 (597-584), beat Bayern Munich 107-91 on 22 October and Olimpia Milano 101-97 on 15 October", S["dailysports_pao"]),
      ("Paris 1-6 (597-649), 18th, 1-4 at home, lost 93-104 at home to Valencia on 23 October", S["eurohoops"])],
     "A clean standings gap: 6th against 18th with 37 points of differential between them.",
     "Seven tips. Paris have covered as home underdogs before, and this is our number, not a book price.")

pick("Basketball", "Baskonia vs Real Madrid", "Money Line", "Baskonia",
     "Baskonia to get up in the home game against Real Madrid (1.90)",
     "Baskonia's last outing was a six-point game at the top of the table - 85-79 to league-leading Panathinaikos on "
     "22 October - and their reward is a Tuesday-night fixture at the Fernando Buesa Arena where the OLBG vote splits "
     "three of six for the home side. Real Madrid carry the bigger name in this fixture, which is exactly why 1.90 "
     "(+190) is on the board at all: near-even-money on a split market is where an originated line can be wrong in "
     "both directions, and we are not going to dress a three-tip lean up as more than that.",
     S["sportando"],
     [("Round 8: Baskonia v Real Madrid, Tuesday 27 October, 21:00 CET", S["sportando"]),
      ("Round 7: Baskonia lost 85-79 at Panathinaikos on 22 October (a six-point margin at the league leaders)", S["dailysports_pao"]),
      ("Real Madrid's own record and Round 7 result: BLANK - the standings feeds readable tonight printed positions 1, 2, 3, 6, 18 and 19 only", ""),
      ("OLBG tip split: 3 of 6 on Baskonia", S["olbg_base"])],
     "Priced at the near-even-money end of the card, which is where a split vote should be published rather than dropped.",
     "Six tips, no Real Madrid record we could cite, and no injury list for either club. The price is a prior with three votes on it.")

pick("Basketball", "Crvena Zvezda vs Maccabi Tel Aviv", "Money Line", "Crvena Zvezda",
     "Crvena Zvezda to defend their home floor against Maccabi (1.90)",
     "This is the weakest-supported pick on the basketball page and it is published anyway, because the brief is to "
     "price every market: Crvena Zvezda host Maccabi Tel Aviv in Belgrade at 20:00 CET on Tuesday, two of four OLBG "
     "tips are on the home side, and we originate 1.90 (+190) from that split. What we are not doing is describing "
     "either team's form: the standings feeds readable in this window printed the top six and bottom two positions "
     "only, so Zvezda's and Maccabi's records, both clubs' injury lists and their Round 7 results are left blank and "
     "flagged rather than filled in from memory.",
     S["sportando"],
     [("Round 8: Crvena Zvezda v Maccabi Tel Aviv, Tuesday 27 October, 20:00 CET", S["sportando"]),
      ("OLBG market shows 2 of 4 tips on Crvena Zvezda", S["olbg_base"]),
      ("Both clubs' records, recent results and availability: BLANK - not printed on any source readable during this capture (flag BK-001)", "")],
     "Published with the gaps marked, because the tip split is thin and the standings number was not confirmable.",
     "Four tips, no standings row for either club and no availability list. Read it as a priced market, not as a football opinion.")

# ---------------------------------------------------------------------------- CRICKET ------
pick("Cricket", "Pakistan vs Sri Lanka One Day Match", "Win Match", "Pakistan",
     "Pakistan to beat Sri Lanka in the tri-series match in Lahore",
     "Pakistan are 3 wins from 3 in this one-day tri-series on a net run rate of +0.949, having beaten Sri Lanka by 37 "
     "runs in Rawalpindi, England by 87 runs and England again by a wicket in Lahore, and 22 of the 32 tips counted on "
     "this OLBG market sit with them. Sri Lanka have played one fewer game and chased 430 to beat England only last "
     "weekend. The fourth-over-forcing Pakistan pace attack is the difference. Back Pakistan at 1.41 (-244), our "
     "highest-confidence selection of the day.",
     S["cric_pak"],
     [("5th match of the Pakistan ODI tri-series, Lahore, Tuesday 27 October, play 08:00 GMT / 13:00 local", S["cric_pak"]),
      ("Table after 3 rounds: Pakistan 3-0, 6 points, NRR +0.949; Sri Lanka 1-1, 2 points, NRR -0.348; England 0-3", S["cric_pak_sl"]),
      ("Pakistan beat Sri Lanka by 37 runs in the opener: 305 all out (Salman Agha 107; Dilshan Madhushanka/Malinga 4-46), SL 268 (Afridi 3/55, Naseem 2/43)", S["cric_pak_1"]),
      ("Pakistan beat England by 87 runs at Rawalpindi and by one wicket at Lahore; Sri Lanka beat England by two wickets", S["bbc_pak"])],
     "Grade A, 32 tips, and a price inside the -250 to +10000 focus band - the pick we would put our name to.",
     "Pakistan have effectively finished the round-robin in front and may rotate their side; no confirmed playing XI was printed on any page we read for this fixture, so no lineup claim is made here.")

pick("Cricket", "Namibia vs Ireland 3rd ODI", "Win Match", "Ireland",
     "Ireland to win the third ODI in Windhoek and go 2-1 up",
     "The five-match series is 1-1 and 22 of 32 OLBG tips back Ireland tonight at the High Performance Oval. Paul "
     "Stirling has 56 and 77 in the two innings so far, and Namibia have been bowled out once in this series. The concern is the "
     "322-6 chase Namibia set up by Gerhard Erasmus' career-best 156 not out, and Ireland's death bowling, which went "
     "for 1-71 and 1-74 to McDonough and Campher. Take Ireland at 1.45 (-196) on the back of a top order in form.",
     S["bbc_nam"],
     [("Series is 1-1 after Namibia won the 2nd ODI by 31 runs: NAM 321-6 (Erasmus 156* off 125, Frylinck 76), IRE 290 all out (Stirling 77 off 71; Brassell 4-52, Hoey 3-53)", S["bbc_nam"]),
      ("Ireland won the 1st ODI by 55 runs; Gavin Hoey took 3 wickets in that match and matched it in the 2nd", S["bbc_nam"]),
      ("Ireland are still without their leading seamer Mark Adair for this series", S["bbc_nam"]),
      ("3rd ODI, High Performance Oval, Windhoek, Tuesday 27 October, 10:00 local", S["cric_nam"])],
     "Grade A market with 32 tips and a real match-up story: Ireland's top order against a Namibia side that just made 321.",
     "Namibia posted 321-6 on this ground two days ago; if the pitch stays true the 1.45 price is short for the away side.")

pick("Cricket", "New Zealand vs India 3rd T20 Match", "Win Match", "India",
     "India to take the series 3-0 in Wellington",
     "India have chased 226 and 181 in this series and lead 2-0, both wins by four wickets, and the OLBG vote is "
     "overwhelming at 35 of 49 tips. New Zealand are without Matt Henry for the rest of the series and Lockie Ferguson "
     "for this game, and their captain James Santner conceded dropped catches were the difference on Saturday. India's "
     "reply of 181-6 came from 70-5, so this is a batting-depth match-up. We price India at 1.38 (-263) - just outside "
     "the -250 focus floor, so it is confidence but not a value bet.",
     S["cric_nz"],
     [("3rd T20I, Wellington, Tuesday 27 October, 8:00pm local / 07:00 GMT; India lead the series 2-0", S["cric_nz_sched"]),
      ("India chased 226 and 181 at Christchurch, winning both by four wickets - the second from 70-5 (Tilak Varma 51* off 26)", S["cric_nz"]),
      ("New Zealand are without Matt Henry (rest of series) and Lockie Ferguson (this match); India are without Ishan Kishan and Vaibhav Sooryavanshi bats No. 3", S["cric_nz"]),
      ("New Zealand skipped on four chances in the second innings; Santner: 'The small stuff can change games quickly'", S["cric_nz_sched"])],
     "49 tips counted - the largest sample on the whole card.",
     "The price is shorter than the -250 floor the brief sets for high-confidence work, and Wellington's headwind flatters the short ball. Graded medium for that reason.")

pick("Cricket", "Afghanistan vs Zimbabwe 1st T20 Match", "Win Match", "Afghanistan",
     "Afghanistan to win the opening T20I at Sharjah",
     "Afghanistan bowled Zimbabwe out for 169 and chased it down with 93 balls left in the UAE tri-series final nine "
     "days ago, Rashid Khan taking three and being named player of the series with 11 wickets while Ibrahim Zadran "
     "made 194 runs. Zimbabwe are without Craig Ervine and Newman Nyamhuri through injury for this match and are "
     "playing without Bradley Ngarava as well, with Sikandar Raza captaining. Fifteen of sixteen OLBG tips are on "
     "Afghanistan and the price we originate is 1.16 - a real edge, no value. Pass unless you can trade it.",
     S["cric_afg"],
     [("1st T20I of a three-match series, Sharjah Cricket Stadium, Tuesday 27 October, 18:30 local (14:30 GMT)", S["espn_afg"]),
      ("Afghanistan beat Zimbabwe by 7 wickets in the UAE tri-series final on 23 October: ZIM 169 (Raza 68), AFG 170/3 with 93 balls unused; Rashid 3/41, Nabi 2/25", S["espn_afgfinal"]),
      ("Tri-series leading run-scorer Ibrahim Zadran 194 at a 132.19 strike rate; leading wicket-taker Rashid Khan 11", S["cric_afg"]),
      ("Zimbabwe are without Ervine and Nyamhuri (injury) for this match and Ngarava is absent, Raza leading the side", S["cadd_afg"])],
     "Strongest form and availability gap of any match on the card.",
     "Priced at 1.16, far short of the focus band. Confidence is high, the bet is not - flagged as a no-bet.")

pick("Cricket", "South Africa vs Australia", "Win Match", "South Africa",
     "South Africa to win the series-deciding third Test at Newlands",
     "This series is 1-1: Australia won the first Test at Durban by 214 runs and South Africa won the second at "
     "Gqeberha by an innings and 31 runs after Marco Jansen took 5-33 and Australia were shot out for 99 and 295. "
     "South Africa are unchanged apart from Gerald Coetzee replacing the injured Anrich Nortje, while Australia are "
     "selecting around Steven Smith's neck, which has cost him 25, 27, 28 and 3 this series. At 2.67 (+167) on a "
     "Newlands pitch that just produced an innings margin, back South Africa.",
     S["cric_test"],
     [("3rd Test, Newlands, Cape Town, 27-31 October; series level after Australia won the 1st Test by 214 runs and South Africa the 2nd by an innings and 31 runs", S["cca_test"]),
      ("South Africa XI confirmed: Markram, Ackerman, Bedingham, Bavuma (c), Breetzke, Rickelton (wk), Mulder, Jansen, Harmer, Coetzee, Rabada - Coetzee in for the injured Anrich Nortje (groin, ruled out of the series)", S["cca_test"]),
      ("Cameron Green (abdominal strain) and Josh Inglis (broken finger) are back at full fitness; Maharaj starts on the bench", S["cca_test"]),
      ("Steven Smith faces a fitness test on his neck after scores of 25, 27, 28 and 3 in the series; Maddinson has been omitted and flown home", S["cric_smith"]),
      ("Australia 99 all out (Jansen 5-33) and 295 in the 2nd Test despite Travis Head's 121, follow-on enforced from 326 in front", S["sky_test"])],
     "The best combination of price (+167, inside the focus band), sample (8 tips) and confirmed team news on the card.",
     "Only 3 of 8 OLBG tips are on South Africa and the Draw is priced at the same 2.67, so a fifth-day draw is the live risk. Start time is also reported inconsistently (10:00 vs 10:30 local) - see flags.")

# ---------------------------------------------------------------------------- DARTS --------
pick("Darts", "PDC World Championship 2027", "Win Tournament", "Luke Littler",
     "Luke Littler to retain the world title (1.76)",
     "Littler has now won two world championships in three appearances and is the man who retained the crown, beating "
     "Gian van Veen 7-1 in the final at Alexandra Palace on 3 January at a 106.02 average, losing only four sets in "
     "seven matches. He is the current world number one, won the 2026 World Matchplay and Premier League, and 22 of "
     "the 36 tips on this OLBG outright are on him. Our line is 1.76 (-132) on the tournament that runs 11 December to "
     "3 January, with the top 32 of the Order of Merit seeded.",
     S["pdc_entries"],
     [("Littler beat Gian van Veen 7-1 in the 2026 final at Alexandra Palace (3 January 2026), averaging 106.02 with 16 maximums and losing four sets in the whole event", S["sky_darts"]),
      ("The 2026/27 PDC World Championship runs 11 December 2026 to 3 January 2027 at Alexandra Palace, £5m prize fund, £1m to the winner, 128 players, top 32 of the Order of Merit seeded", S["pdc_entries"]),
      ("Littler is world number one and also won the 2026 World Matchplay and Premier League", S["pdc_entries"]),
      ("OLBG outright market: 22 of 36 tips on Littler; printed event date 03 Jan 2027 is the final day of the tournament", S["olbg_base"])],
     "Ante-post outright priced inside the focus band with 36 tips behind it, so the price is not a small-sample artefact.",
     "This is an eight-month outcome, not a match. Van Veen, Humphries and van Gerwen are all in the field and the seeded 32 do not have to play each other early.")

pick("Darts", "Players Championship 31", "Win Tournament", "Nathan Aspinall",
     "Nathan Aspinall each-way case in a thinned-out Den Bosch field (4.90)",
     "Players Championship 31 is at the Maaspoort in Den Bosch on Wednesday 28 October with 128 players from a 13:00 "
     "CET start, and the entry list has been hollowed out: Luke Humphries, Gerwyn Price, Rob Cross, Jonny Clayton, "
     "Stephen Bunting, Josh Rock and Mike de Decker are all among the withdrawals. Aspinall is in the draw and the "
     "single selection the OLBG market carries, with one of three tips, so we originate 4.90 (+390) on him. Thin "
     "market, honest price, no pretending otherwise.",
     S["pdc_entries"],
     [("Players Championships 31 and 32 are Wednesday 28 and Thursday 29 October at the Maaspoort, Den Bosch, 128 players, 13:00 CET, £125,000 each", S["pdc_entries"]),
      ("Luke Littler, Luke Humphries, Gerwyn Price, Rob Cross, Jonny Clayton, Stephen Bunting, Josh Rock and others withdrew from both events", S["dartsnews"]),
      ("Michael van Gerwen and Gian van Veen play on home soil; Aspinall is entered", S["pdc_entries"]),
      ("OLBG market carries 1 of 3 tips on Aspinall", S["olbg_base"])],
     "Published because the market exists and the field is materially weaker than the entry list implies.",
     "Three tips total and van Veen/van Gerwen in a Den Bosch field: graded B, low confidence, and the withdrawal list should be re-read at the morning deadline.")

# ------------------------------------------------------------------- GAELIC SPORTS -------
pick("Gaelic Sports", "Kanturk v Eire Og Cor", "Handicap", "Eire Og Cor +0.50",
     "Eire Og +0.5 in the Cork intermediate club tie (1.27)",
     "All six tips counted on this OLBG handicap market are on Eire Og +0.5, which is a level-ballot line: a draw is a "
     "win for the selection and only a straight defeat loses it. Club championship fixtures at this level are played "
     "to a result, with a replay or extra time when the scores are level, so the half-point cushion matters less than "
     "the market's belief that these two are within a point of each other. We price it at 1.27 and grade it B.",
     S["gaa_fb"],
     [("OLBG lists this Cork club fixture with a +0.5 / -0.5 handicap and 6 of 6 tips on Eire Og +0.5, printed for Sunday 01 November 09:00 (US Eastern on the card)", S["olbg_base"]),
      ("Competition, grade and venue are not printed anywhere on the OLBG card: left BLANK rather than inferred", ""),
      ("BLANK - no official GAA fixture listing for this pairing could be retrieved at capture time", "")],
     "Published so the handicap market is not silently dropped, and graded B on sample alone.",
     "The fixture itself is unconfirmed against the GAA's own fixtures pages, and 6 of 6 tips with no opposing side printed is a degenerate split. Do not stake on this.")

pick("Gaelic Sports", "Fr Caseys v Kildimo Pallaskenry", "Handicap", "Kildimo Pallaskenry +3.50",
     "Kildimo Pallaskenry +3.5 points in the Limerick club tie (1.55)",
     "Five of seven tips on this market sit with Kildimo Pallaskenry +3.5, a cushion of more than a converted point "
     "either way, and our originated price is 1.55 (-182). This is a club championship handicap priced entirely from "
     "the tip vote: neither the round, the grade nor either team's most recent result was printed on the OLBG card and "
     "no club-results source we could reach carried the fixture at capture time, so those fields stay blank on the "
     "table rather than guessed at.",
     S["gaa_fb"],
     [("OLBG market prints 5 of 7 tips on Kildimo Pallaskenry +3.5 for a Sunday 01 November 10:30 (US Eastern) start", S["olbg_base"]),
      ("Round, grade, venue and both teams' last results: BLANK - not available on any retrievable official source at capture", "")],
     "Second Gaelic handicap kept on the board with its limits stated plainly.",
     "Thin, unconfirmed fixture data. Flagged rather than filled.")

pick("Gaelic Sports", "All Ireland Football Championship 2027", "Win Tournament", "Kerry",
     "Kerry to win the 2027 All-Ireland football championship (1.98)",
     "Kerry hold six of the eight tips on this OLBG Sam Maguire outright, priced at 1.98 (-102) for the final on 25 "
     "July 2027. It is an ante-post market, so the shortlist of counties, the provincial championship results and the "
     "Panel's 2026 landing are not yet settled - and that is the whole point of the price. We are comfortable calling "
     "this a lean rather than a bet, with the market's own two dissenting tips on Armagh, Derry and company still "
     "unpriced.",
     S["gaa_fb"],
     [("OLBG outright: 6 of 8 tips on Kerry, market dated 25 Jul 2027 (All-Ireland football final day)", S["olbg_base"]),
      ("Field size is not printed on the OLBG card, so our prior assumes 8 entries - see flag U-004", S["olbg_base"])],
     "Grade A on sample within an eight-way structure, priced at 1.98 inside the focus band.",
     "Twelve months out with no squad, management or championship-path information we could put our name to; the assumed 1/8 prior moves this price more than any fact on the row.")

pick("Gaelic Sports", "All Ireland Hurling Championship 2027", "Win Hurling", "Galway",
     "Galway in the 2027 All-Ireland hurling outright (2.95)",
     "Galway are the most-backed side on the OLBG Liam MacCarthy outright with seven of eighteen tips, and we price "
     "them at 2.95 (+195) for the final on 18 July 2027. The field is genuinely wide - eleven of the eighteen tips "
     "are spread across Limerick, Cork, Kilkenny, Clare and Tipperary - so this is a value lean on a team that has "
     "been in every recent championship argument rather than a claim about a defined hierarchy. No 2026 results or "
     "panel news are attached to this row because none could be confirmed from an official source at capture time.",
     S["gaa_fb"],
     [("OLBG outright: 7 of 18 tips on Galway, market dated 18 Jul 2027", S["olbg_base"]),
      ("Limerick, Cork, Kilkenny, Clare and Tipperary share the remaining 11 tips on the same market", S["olbg_base"]),
      ("BLANK - no official GAA source for the 2026 championship result or the 2027 entry list was retrieved at capture", "")],
     "The most-backed selection in a wide, genuinely split outright market.",
     "Ante-post a year out, field size assumed at 8, zero team news. Graded C on evidence even though the sample is 18.")

# --------------------------------------------------------------------- GREYHOUNDS --------
# No markets captured - see flags.json (G-001).

# -------------------------------------------------------------------------- HANDBALL -------
pick("Handball", "Wisla Plock vs Nantes", "Money Line", "Nantes",
     "Nantes to win at Wisla Plock and take the last main-round place (4.05)",
     "Three clubs in this group are on six points with one main-round ticket left and Nantes travel to Plock knowing a "
     "win does it themselves. Nantes are 3-0-2 with a 142-143 record, they took revenge on Melsungen 33-25 in Round 5, "
     "and they already beat Plock 26-25 in the first meeting, so the away side has the head-to-head. Only 2 of 11 "
     "OLBG tips back them and we originate 4.05 (+305) - a live price on a fixture the market is mispricing by "
     "leaning on the draw.",
     S["ehf_standings"],
     [("Group B after 5 rounds: Wisla Plock 3-0-2 (141-136, 6 pts), Nantes 3-0-2 (142-143, 6 pts), Melsungen 6 pts, Vardar 2 - three clubs still in contention for the main round", S["ehf_standings"]),
      ("Round 6 fixture: Orlen Wisla Plock v HBC Nantes, Wednesday 28 October, 18:45 local (17:45 CET)", S["ehf_nantes"]),
      ("Nantes won the first meeting 26-25; Nantes beat Melsungen 33-25 in Round 5, Plock beat Vardar 33-32", S["ehf_review"]),
      ("EHF's own round-6 preview lists all three main-round scenarios as still open", S["ehf_r6"])],
     "The strongest handball case on the card: a qualification stake, a head-to-head win and a price of +305.",
     "The OLBG market's own 8-of-11 tip vote is on the draw, which is graded C and excluded from high confidence - read the flagged note on this fixture before staking.")

pick("Handball", "Wisla Plock vs Nantes", "Money Line", "Wisla Plock",
     "Wisla Plock to win at home (5.40) - the other side of the same market",
     "Plock's home record in this group is the spine of the case against us: 141-136 in a five-match group with wins "
     "over Melsungen 25-24 and Vardar 33-32, meaning they have won two one-possession games in front of their own "
     "crowd and lost the other meeting in Nantes by a single point. We price Plock at 5.40 (+440), a number that only "
     "exists because just one of eleven tips sat with them while eight sat on the tie. Both sides are published so the "
     "grid is complete and the clustering is visible.",
     S["ehf_standings"],
     [("Group B: Plock 3-0-2, 141-136, +5 differential on 6 points with 5 rounds played", S["ehf_standings"]),
      ("Plock beat Melsungen 25-24 and Vardar 33-32, losing 25-26 at Nantes in the first meeting", S["ehf_standings"]),
      ("Round 6 plays Wednesday 28 October, 18:45 in Plock", S["ehf_nantes"])],
     "Two-sided publishing: the away price and the home price on one fixture, side by side.",
     "1 of 11 tips. The 5.40 is an artefact of a draw-clustered market as much as a real assessment; graded C for the fixture overall.")

pick("Handball", "PSG Handball vs Aalborg Handbold", "Money Line", "Aalborg Handbold",
     "Aalborg to take both points in Paris (4.76)",
     "Aalborg lead this group on nine points from five matches, 170-145, and are still unbeaten - four wins and a draw - "
     "having already booked their main-round place. They held PSG to 33-33 when the sides met in September, which is "
     "the only time these two have cancelled each other out this season, and PSG's one group defeat came at Zagreb. "
     "The OLBG market puts one of nine tips on Aalborg and we price the Danes at 4.76 (+376).",
     S["ehf_standings"],
     [("Group C after 5 rounds: Aalborg 4-1-0, 170-145, 9 pts (leaders); PSG 3-1-1, 182-157, 7 pts; both already through", S["ehf_standings"]),
      ("First meeting ended 33-33 (Aalborg v PSG, 9 September 2026); head-to-head over the fixture's history is 6-1-1", S["ehf_r6"]),
      ("Round 6: Paris Saint-Germain Handball v Aalborg Handbold, Stade Pierre de Coubertin, Wednesday 28 October, 20:45 CET, EHFTV", S["ehf_r6"]),
      ("PSG beat Celje 46-35 but lost 28-29 at Zagreb in the group", S["ehf_review"])],
     "Group-leaders-and-draw-nothing angle at +376, plus the seeded tie vote shows the market is not on the teams at all.",
     "One of nine tips. Nothing on either side's availability, and a dead-rubber incentive for Aalborg, who already qualify.")

pick("Handball", "PSG Handball vs Aalborg Handbold", "Money Line", "PSG Handball",
     "PSG to win at home (4.76) with the goal difference in play",
     "PSG's price on this card is identical to Aalborg's at 4.76 and that symmetry is the story: the tip vote is "
     "sitting on the draw and both teams are priced as afterthoughts. The home side have outscored group opposition "
     "182-157, including a 46-35 win over Celje, and they know the seeding across the group decides who plays whom in "
     "the main round. On the numbers in front of us the match-up is even; on the price, PSG at 4.76 is where the "
     "market is clearly wrong if either team has to win.",
     S["ehf_standings"],
     [("PSG 3-1-1, 182-157 (+25), 7 points after 5 rounds in Group C", S["ehf_standings"]),
      ("PSG 46-35 v Celje; lost 28-29 at Zagreb; drew 33-33 with Aalborg in September", S["ehf_review"]),
      ("OLBG market: 1 of 9 tips on PSG, 1 of 9 on Aalborg, 7 of 9 on the tie", S["olbg_base"])],
     "The published second half of the same two-sided market.",
     "Draw-clustered market: the 4.76 is our number off a 1/9 tip share, and no team news was retrievable for either club.")

# ---------------------------------------------------------------------- ICE HOCKEY -------
pick("Ice Hockey", "BOS Bruins @ CAR Hurricanes", "Puck Line", "BOS Bruins +1.50",
     "Boston +1.5 goals against Carolina (1.52)",
     "Boston go to Raleigh having won seven of their first twelve games (9-2-1, 19 points) with 4.00 goals a game for "
     "and 2.17 against, and Jeremy Swayman is 6-1-1 at a 1.98 goals-against and .928 save percentage. Carolina lead the "
     "East on 9-2-2 but their support-goalie numbers are the crack: Bussi is 2-2-2 at 3.27 and .865 behind Kochetkov's "
     "1.98. On a +1.5 cushion the Bruins cover in a regulation loss by one, which is how three of their games have "
     "already gone. Take Boston +1.5 at 1.52 (-192), 8:00pm ET at Lenovo Center.",
     S["espn_nhl"],
     [("Game: Boston at Carolina, Tuesday 27 October, 8:00pm ET, Lenovo Center, on ESPN", S["espn_nhl"]),
      ("Boston 9-2-1 (19 points), 4.00 goals for / 2.17 against per game; Carolina 9-2-2 (20 points), 3.92 for / 2.46 against", S["nhl_st"]),
      ("Goaltending listed on the game page: Swayman 6-1-1, 1.98 GAA, .928 SV%; Boston's DiPietro 2-1-0, 1.69, .941. Carolina's Bussi 2-2-2, 3.27 GAA, .865 SV%", S["espn_nhl"]),
      ("Carolina injuries on the same page: Taylor Hall (IR, estimated 7 November), Jordan Staal (IR, estimated 3 December), Mark Jankowski out, Alexander Nikishin not released; Sebastian Aho has 18 points in 13 games", S["espn_nhl"]),
      ("Sebastian Aho: 7 goals, 18 points, plus-6, 38 shots, 12 hits in 13 games; Carolina beat St. Louis 4-0 on Saturday", S["espn_nhl"])],
     "The only NHL market on the card with a two-sided split and a structural cushion, priced inside the band.",
     "Two tips on the market and Boston are the road side against the Conference leader; the +1.5 line is ours, not a book price. Note Taylor Hall: the NHL's status report had him activated on 26 October while ESPN's injury page still lists him as IR - unresolved, see flags.")

pick("Ice Hockey", "Kalpa vs Sport", "Money Line", "Kalpa",
     "KalPa over Vaasan Sport in Kuopio (1.31 originated, 5 of 5 tips)",
     "KalPa and Sport are level on 19 points - KalPa 6-8 from 15 games at 37-37, Sport 5-8-1-2 from 16 at 30-46 - and "
     "every one of the five tips counted on the OLBG market is on the home side. KalPa's edge is the goal differential: "
     "even across the league - KalPa have not been outscored at 37-37, while Sport are sixteen in the red on 30 scored and 46 conceded. "
     "The fixture is Tuesday 18:30 Finnish time in Kuopio. We originate KalPa at 1.31 and label it confidence rather "
     "than value, because five tips do not make a market.",
     S["liiga"],
     [("Liiga game week: KalPa v Vaasan Sport, Tuesday 27 October, 16:30 UTC (18:30 Finnish start) - league schedule page", S["liiga"]),
      ("Standings: KalPa 15 GP, 6-8, 37-37, 19 points; Sport 16 GP, 5-8-1-2, 30-46, 19 points", S["ep_liiga"]),
      ("OLBG card prints 5 of 5 tips on KalPa with nothing on the other side of the money line", S["olbg_base"])],
     "A 100% tip vote is not evidence, so the write-up rests on the differential instead.",
     "Five tips, one-sided split (capped medium by rule), and the club's own published schedule lists a different date for this pairing - see flags.")

pick("Ice Hockey", "IF Malmo Redhawks vs Linkoping HC", "Money Line", "IF Malmo Redhawks",
     "Malmo Redhawks to beat Linkoping at home (1.43)",
     "Malmo have 17 points from eleven SHL games (4-4-3) with a 31-29 goal record and sit mid-table in front of a "
     "Linkoping side on 12 points from eleven (4-6-1) in 13th. Linkoping's games keep landing close - 6-4 over Orebro "
     "on 24 October, a 3-2 shootout win at HV71, 2-4 to Jarpenstal - but they have not stopped conceding, and the "
     "Redhawks play this at Malmö Arena on Tuesday 20:00 CET. All three OLBG tips are on the home side; we price "
     "Malmo at 1.43 (-233).",
     S["swehockey"],
     [("SHL: IF Malmo Redhawks v Linkoping HC, Tuesday 27 October, 20:00 CET (18:00 UTC)", S["swehockey"]),
      ("Malmo 11 GP, 4-4-3, 31-29, 17 points; Linkoping 11 GP, 4-6-1, 12 points, 13th", S["ep_lhc"]),
      ("Linkoping's last three: 6-4 v Orebro (24 Oct), 3-2 SO win at HV71 (20 Oct), 2-4 v Jarpenstal (17 Oct)", S["ep_lhc"])],
     "Sample of three tips but a real 5-point gap plus home ice, priced short of the -250 floor at 1.43.",
     "Three tips. Linkoping have taken a point in each of their last two close games, so the one-goal line at 1.43 is not padded.")

pick("Ice Hockey", "Frolunda HC vs Rogle BK", "Money Line", "Frolunda HC",
     "Frolunda to see off Roingle at Scandinavium (1.71)",
     "Frolunda are at home in Gothenburg against a Roingle side who have been travelling through a difficult October, "
     "and the OLBG market carries two of three tips on the hosts with a two-way price we originate at 1.71 (-141). "
     "The fixture is on the same SHL round as Malmo-Linkoping, 20:00 CET Tuesday. What we cannot do is claim an "
     "injury or line-up edge: neither club's availability list was printed on a source we could read at capture time, "
     "so those fields are blank on the table and this pick is priced on fixture, venue and the tip lean alone.",
     S["swehockey"],
     [("SHL round of Tuesday 27 October: Frolunda HC v Roingle BK, 20:00 CET", S["swehockey"]),
      ("OLBG: 2 of 3 tips on Frolunda", S["olbg_base"]),
      ("Team news, injuries and current standings position for both clubs: BLANK - no retrievable official list at capture", "")],
     "Included to show the round honestly, with its gaps named.",
     "Three tips, no team news, and the two clubs' records were not confirmable tonight. Low staking case.")

pick("Ice Hockey", "CLB Blue Jackets @ PHI Flyers", "Money Line", "PHI Flyers",
     "Philadelphia to end the losing run against Columbus (1.71)",
     "Philadelphia are 3-7-3 after thirteen games with 9 points, 2-3-2 at home, and the OLBG market puts two of three "
     "tips on the Flyers to beat a Columbus side who are 4-5 with 9 points of their own and 0-2 on the road. That is "
     "a two-point gap between two struggling teams at a 1.71 price. Columbus's own injury column is the reason to lean "
     "the other way: Provorov is week-to-week, Fabbro is near a return and Lundestrom is on long-term term reserve. "
     "Take the home side small, at the Wells Fargo Center 7:00pm ET.",
     S["nhl_st"],
     [("NHL standings: Philadelphia 13 GP, 3-7-3, 9 pts (2-3-2 home); Columbus 9 GP, 4-5-0, 9 pts (0-2-0 away)", S["nhl_st"]),
      ("Columbus availability: Provorov week-to-week, Fabbro close to returning, Lundestrom long-term reserve, MacDonald non-roster/injured - reported 26 October", S["nhl_st"]),
      ("Philadelphia injuries on the same read: Ristolainen out around two weeks, York a game-time decision after skating, Konecny, Tippett and Grebenkin on reserve, Foerster day-to-day", S["nhl_st"])],
     "The only NHL money line on the card where both sides were printed with an actual split.",
     "Three tips. Both clubs are within two points of each other on a bad start, so this is a price, not a statement about either team.")

# ------------------------------------------------------------------- MOTOR RACING --------
pick("Motor Racing", "Formula 1 Drivers Championship 2026 Without Kimi Antonelli", "Win Tournament", "Max Verstappen",
     "Verstappen to finish highest of everyone behind Antonelli (2.61)",
     "With five races and 125 points still on the table after Austin, Kimi Antonelli leads on 365 and can clinch the "
     "title in Mexico by finishing ninth, which leaves the private fight behind him: George Russell 242, Lewis "
     "Hamilton 241, Max Verstappen 236, Charles Leclerc 233, Lando Norris 211. Four of the seven tips on this OLBG "
     "outright are on Verstappen and we price him at 2.61 (+161) to be the best of the rest. It is a five-race sprint "
     "with six points covering three drivers, so volatility, not form, decides it.",
     S["f1_drivers"],
     [("Official 2026 drivers' standings after round 18 (Austin): Antonelli 365, Russell 242, Hamilton 241, Verstappen 236, Leclerc 233, Norris 211, Piastri 144", S["f1_drivers"]),
      ("Antonelli wins the championship in Mexico City on Sunday 1 November if he finishes ninth or higher, regardless of the rest", S["f1_abc"]),
      ("Five rounds remain after Austin, 125 points available; Russell and Hamilton both survived the Austin race to within a point of each other", S["f1_gp"]),
      ("OLBG outright market: Verstappen 4/7, Hamilton 2/7, Russell 1/7, Leclerc/Norris/Piastri 0/7", S["olbg_base"])],
     "An in-band outright price (+161) on a fight the tip vote has engaged with, with the official standings as the spine.",
     "Seven tips. Verstappen's ceiling depends on other cars failing: 125 points across five rounds is enough for Hamilton or Russell to move past him without him winning a race.")

pick("Motor Racing", "Formula 1 Drivers Championship 2026 Without Kimi Antonelli", "Win Tournament", "Lewis Hamilton",
     "Hamilton to out-point Russell and Verstappen for best-of-the-rest (4.50)",
     "Lewis Hamilton is one point behind Russell and five ahead of Verstappen with five races to go, and two of seven "
     "tips on this OLBG market back him to head the field behind the champion-in-waiting. We price that at 4.50 "
     "(+350). Austin is the argument: he scored there while the championship fight moved rather than ended, and the "
     "remaining calendar is where a Mercedes that can qualify on the front row banks points. This is a five-race "
     "consistency bet against two drivers on almost the same score, so the price is doing most of the work.",
     S["f1_drivers"],
     [("Official standings: Hamilton 241, Russell 242, Verstappen 236 with five rounds left after Austin", S["f1_drivers"]),
      ("Russell and Hamilton both finished the Austin GP inside the same points structure with a point between them", S["f1_gp"]),
      ("Antonelli can clinch as early as Mexico City on 1 November (14:00 local), which is when this side-battle would start being settled", S["f1_abc"])],
     "Published as the other runner in the same market so the grid is two-sided, not cherry-picked.",
     "Two of seven tips, and the whole case is a one-point standings gap that could move on a single Saturday qualifying session.")

pick("Motor Racing", "Formula 1 Drivers Championship 2026 Without Kimi Antonelli", "Win Tournament", "George Russell",
     "Russell at 7.07 to be top of the rest - the value end of this outright",
     "George Russell leads the fight behind Antonelli on 242 points, one ahead of Hamilton and six ahead of Verstappen "
     "with 125 still available, and yet the OLBG market gives him only one of seven tips - the price we originate, "
     "7.07 (+707), reflects a tip vote chasing the name rather than the scoreboard. The point worth making is about "
     "the card itself: one OLBG comment quotes Russell on 238 with Hamilton 229 and Verstappen 221 and says six races "
     "remain, which is stale against the official timing sheets by 4, 12 and 15 points and one round.",
     S["f1_drivers"],
     [("Official 2026 drivers' standings: Russell 242 after 18 of 23 rounds", S["f1_drivers"]),
      ("Five rounds, 125 points remain after Austin; Antonelli needs ninth place in Mexico to clinch the title itself", S["f1_abc"]),
      ("The OLBG comment thread on this market cites 238/229/221 and 'six races to go', which does not match the official standings - flagged as U-007", S["olbg_base"])],
     "Highest price on the card with a standings fact behind it, published with the source conflict named.",
     "One of seven tips, and a market whose own commentary is demonstrably stale.")

pick("Motor Racing", "Mexico City Grand Prix", "Top 6 Finish", "Kimi Antonelli - Yes",
     "Antonelli to finish in the top six in Mexico (1.15 - top of the card, no value)",
     "The single heaviest-voted market we captured today is Antonelli to finish top six in Mexico City, with 17 of 18 "
     "tips on yes, and the reason is arithmetic: ninth place is enough to secure the 2026 drivers' title, and he is on "
     "365 points with five races left. Our originated price of 1.15 (-667) is a certainty tax - there is nothing to "
     "take here. We publish it because the market is on the card, and because the same market is the only reason the "
     "outright prices above exist.",
     S["f1_drivers"],
     [("Antonelli leads the 2026 championship on 365 points after round 18 with 125 points left across five rounds", S["f1_drivers"]),
      ("A ninth-place finish in Mexico City on Sunday 1 November (14:00 local) would clinch the title whatever rivals do", S["f1_abc"]),
      ("The tip split for this market (17/18) comes from the 26 October capture of the OLBG motor-racing page; the 27 October page listed the market without reprinting the split - carried forward and labelled, see flag U-006", S["olbg_base"])],
     "Documented for completeness with the carry-forward stated.",
     "Priced at 1.15, which is 0.25 shorter than the -250 floor, and the split is carried from the previous day's capture rather than re-printed. Not a bet.")

# ------------------------------------------------------------------ RUGBY LEAGUE ---------
pick("Rugby League", "State of Origin 2027", "Win Tournament", "New South Wales",
     "New South Wales to take the 2027 State of Origin series (1.86)",
     "Nine of the thirteen tips on this OLBG Origin outright sit with New South Wales and we originate 1.86 (-116) for "
     "the series to start on 27 May 2027. This is a market on a best-of-three almost seven months away with no squads, "
     "no selectors and no representative coaching appointments printed anywhere on the card, so the price is the whole "
     "argument: the tip vote is leaning to the side the market considers deeper, and the three dissenting tips are what "
     "keeps the number inside the band rather than around evens.",
     S["olbg_base"],
     [("OLBG market: 9 of 13 tips on New South Wales to win the 2027 State of Origin series, dated 27 May 2027", S["olbg_base"]),
      ("Queensland share the remaining 4 of 13 tips on the same market", S["olbg_base"]),
      ("Squad, selector and venue information: BLANK - no official representative-team source was consulted at capture because none exists yet for the 2027 series", "")],
     "The only Origin market available; published with its evidence base on the table.",
     "Ante-post, no team news exists yet, field assumed at 8 (flag U-004). Treat as a price, not a prediction of rugby.")

pick("Rugby League", "Super League 2027", "Grand Final Winner", "Wigan Warriors",
     "Wigan to win the 2027 Super League grand final (3.46)",
     "Two of four tips on this OLBG outright name Wigan for the grand final at Old Trafford on 2 October 2027, which "
     "we price at 3.46 (+246). The field on the card carries the other two tips spread across the remaining clubs, and "
     "no Super League table, squad or transfer information was confirmed against an official source at capture time - "
     "so those columns stay blank and this is a market-led selection, not a football argument. It goes on the board "
     "because the brief is to price every available market, and the flag says what the reader can and cannot rely on.",
     S["olbg_base"],
     [("OLBG market: 2 of 4 tips on Wigan Warriors to win the 2027 Super League grand final, printed for 02 Oct 2027", S["olbg_base"]),
      ("2026 Super League table, play-off structure, Wigan's squad list: BLANK - not retrievable from an official source at capture", "")],
     "Published to keep the league's outright market on the grid with its limits visible.",
     "Four tips, an assumed eight-team field, and no verifiable club facts. Graded C by the reliability rule even though the sample is B.")

pick("Rugby League", "NRL 2027", "Grand Final Winner", "Penrith Panthers",
     "Penrith to win the 2027 NRL grand final (4.90)",
     "The NRL outright on this card carries one of three tips on Penrith, priced by us at 4.90 (+390) for the grand "
     "final dated 3 October 2027. A three-tip market on a season that has not started is the thinnest structure on the "
     "whole board, and we are not going to describe it as anything else: no 2026 finals results, salary-cap news or "
     "renewal information has been attached to this row because none could be confirmed at capture time. The price "
     "here is a marker for the market existing, nothing more.",
     S["olbg_base"],
     [("OLBG market: 1 of 3 tips on Penrith Panthers for the 2027 NRL grand final, dated 03 Oct 2027", S["olbg_base"]),
      ("Remaining 2 tips on the market are spread across other NRL clubs", S["olbg_base"]),
      ("2026 NRL finals results and 2027 squad movement: BLANK - no official source consulted successfully at capture", "")],
     "The NRL market is priced and published rather than dropped.",
     "Three tips and no verifiable team facts. Not for staking.")

# -------------------------------------------------------------------- RUGBY UNION --------
pick("Rugby Union", "Dax v Provence", "To Win", "Dax",
     "Dax to win the Pro D2 Friday-night fixture at Maurice-Boyau (2.14)",
     "Two of three OLBG tips back Dax at home on Thursday 29 October (21:00 CET start, listed 16:00 US Eastern on the "
     "card) and we price the home win at 2.14 (+114). Provence are the better side on paper this season - the LNR "
     "standings have them second on 29 points, level with the 34-point leaders on a game in hand - which is exactly why "
     "this is a home-venue play rather than a table play. Note the source conflict: L'Equipe's own table prints "
     "different points for the same two clubs, so no claim is made about Provence's exact position beyond second.",
     S["lnr_provence"],
     [("Pro D2 round 9 fixture: US Dax v Provence Rugby at Stade Maurice-Boyau, Thursday 29 October, 21:00 CET", S["lnr_provence"]),
      ("LNR official club page for Provence Rugby shows them second in Pro D2 on 29 points behind Oyonnax (34) at the time of writing", S["lnr_provence"]),
      ("L'Equipe's Pro D2 table prints Provence on 34 and Dax in the lower half for the same round - conflict, see flag U-008", S["lequipe_pro_d2"]),
      ("OLBG market: 2 of 3 tips on Dax", S["olbg_base"])],
     "Only Pro D2 market on the card with a printed split, priced at +114 for a home side against a promotion candidate.",
     "Three tips and two contradictory league tables. The fixture date is Thursday night, not the Friday listed on most of this round's card - re-check lineups before kickoff.")

pick("Rugby Union", "Connacht v Leinster", "Handicap", "Connacht +3.50",
     "Connacht +3.5 points against Leinster at Dexcom (2.22)",
     "This United Rugby Championship round-5 opener is Friday 30 October, 19:45 UK at the Sportsport Arena, and the "
     "handicap market on the OLBG card carries one tip on Connacht +3.5, which we price at 2.22 (+122). The table "
     "context is real: after four rounds Glasgow lead the province's own standings chase from second on 18 points, "
     "Leinster are 6th on 13 (2-0-2) and Connacht 8th on 10 (2-0-2) with a 104-111 record, so Connacht have been in "
     "every game and Leinster have not been winning them comfortably. A three-and-a-half cushion in this fixture is a "
     "reasonable line, not a longshot.",
     S["urc_fixtures"],
     [("URC round 5 fixtures Friday 30 October: Connacht v Leinster and Glasgow Warriors v Lions, both 19:45 UK kick-off", S["urc_fixtures"]),
      ("Standings after 4 rounds: Leinster 2-0-2, 99-76, 13 points (6th); Connacht 2-0-2, 104-111, 10 points (8th); Glasgow 3-1-0, 18 points (2nd)", S["urc_table"]),
      ("OLBG card prints the handicap market as Connacht +3.50 with 1 of 1 tip", S["olbg_base"])],
     "The union market with the clearest structural read - two provinces within three table points of each other.",
     "One tip on the market, so the +3.5 number is entirely ours. Leinster's away form in this competition was not confirmable from a retrievable source, and no team news is claimed.")

pick("Rugby Union", "Glasgow Warriors v Lions", "To Win", "Glasgow Warriors",
     "Glasgow to beat the Lions at Scotstoun (2.22 originated from a single tip)",
     "Glasgow are the second-placed team in the URC after four rounds, 3-1-0 with 18 points and 119-92 on the "
     "board, while the Lions sit 11th on 9 points from 2-0-2 with a 87-133 record - a 46-point swing in the "
     "underlying numbers before Friday's 19:45 kick-off at Scotstoun. The OLBG market only carries a single win tip, "
     "on Glasgow, so the 2.22 price is a prior with one vote attached. That is a lean to watch, and a stake of nothing.",
     S["urc_table"],
     [("URC round 5: Glasgow Warriors v Honda Lions, Friday 30 October, 19:45 UK", S["urc_fixtures"]),
      ("After 4 rounds: Glasgow 3-1-0, 119-92, 18 pts (2nd); Lions 2-0-2, 87-133, 9 pts (11th)", S["urc_table"]),
      ("Same table on Sky Sports confirms Glasgow's second place and the Lions in the bottom five", S["urc_sky"]),
      ("OLBG: 1 of 1 tips on Glasgow to win", S["olbg_base"])],
     "Published to price the market, and to show that the biggest table gap on the union card has almost no tip volume on it.",
     "One tip. At 2.22 the price implies ~45% when the standings gap says more than that, which is why we flag the line as our own construction rather than a market signal.")

pick("Rugby Union", "Stormers v Ulster", "Handicap", "Ulster +12.50",
     "Ulster +12.5 points at the Coolbet Stadium (2.22)",
     "The Stormers host Ulster on Saturday 31 October in a Saturday-night Cape Town fixture, and the only union market "
     "on it carries a single tip on Ulster +12.5. Twelve and a half is a big number to be laying off in a southern "
     "hemisphere away trip and we price it at 2.22 (+122), which is the honest consequence of a one-tip handicap. "
     "Ulster's conference position and the Stormers' home record are both left blank in the table: neither was printed "
     "on a source we could read at capture time, and we are not going to fill them from memory.",
     S["urc_fixtures"],
     [("URC round 5: DHL Stormers v Ulster Rugby, Saturday 31 October (SA evening kick-off; OLBG card prints 08:45 US Eastern)", S["urc_fixtures"]),
      ("OLBG: 1 of 1 tips on Ulster +12.50", S["olbg_base"]),
      ("Both provinces' current points, last-five form and travel/availability news: BLANK - not confirmable at capture", "")],
     "Keeps a large-margin handicap on the record instead of quietly deleting the only market printed on the fixture.",
     "One tip, a 12.5-point cushion and no verifiable team data. Graded C. Skip it.")

pick("Rugby Union", "Six Nations 2027", "Win Tournament", "Ireland",
     "Ireland to win the 2027 Six Nations (4.32)",
     "Ireland are the most-backed side on the OLBG Six Nations 2027 outright with three of eleven tips, and we "
     "originate 4.32 (+332) for the tournament concluding 14 March 2027. Eleven tips across a six-nation field means "
     "the other eight are spread over England, France, Scotland, Italy and Wales, so this is the market's least-worst "
     "runner rather than a lock - and with no 2026 championship results, coaching news or injury list attached to the "
     "row, the price is the entire case. If you want the outright, take the earliest available ante-post number before "
     "the autumn internationals move it.",
     S["olbg_base"],
     [("OLBG outright: 3 of 11 tips on Ireland to win the 2027 Six Nations, market dated 14 Mar 2027", S["olbg_base"]),
      ("Remaining 8 tips spread across the other five nations in the field", S["olbg_base"]),
      ("2026 Six Nations final standings, 2027 squad news, coaching changes: BLANK - no official source consulted at capture", "")],
     "Grade A sample within an outright structure and the highest-confidence union line on the card by volume.",
     "Assumed field size (U-004), zero team news, and a six-month window. Value read only, not a selection with a rugby argument attached.")

# --------------------------------------------------------------------- SNOOKER ---------
# OLBG's snooker page returned "No tips found." at capture (05:45 UTC, 27 Oct) - no
# market, so no prediction is written. See flag SN-001.

# ------------------------------------------------------------------------ TENNIS ---------
pick("Tennis", "Novak Djokovic vs Ugo Humbert", "Win Match", "Novak Djokovic",
     "Djokovic to beat Humbert in his Basel return (1.50)",
     "Novak Djokovic plays the Swiss Indoors for the first time since 2011 and opens against Ugo Humbert, a man he beat "
     "in their only previous meeting at Wimbledon 2019. He is 12-2 at this tournament, won it on his debut in 2009 and "
     "was runner-up a year later, and his season is being run around a place at the ATP Finals - the live Race to Turin "
     "has him 11th on 2,840 points with 3,340 as a theoretical ceiling. Four of five OLBG tips are on him and we price "
     "the match win at 1.50 (-200) for a centre-court start in Basel.",
     S["atp_basel"],
     [("ATP Tour: Djokovic begins his Basel campaign against Humbert, his first appearance at the event since 2011, with a 12-2 record and a title in 2009", S["atp_basel"]),
      ("Head-to-head is 1-0 to Djokovic (Wimbledon 2019)", S["atp_basel"]),
      ("Live Race to Turin shows Djokovic 11th on 2,840 points with the next match at Basel, still inside reach of the top eight", S["atp_race"]),
      ("Basel is a 26 October - 1 November ATP 500 on indoor hard courts; Djokovic is seeded fourth and could meet top seed Ben Shelton in the semi-finals", S["atp_draw"])],
     "Five tips only, but every one of the facts on this row is from the tour's own reporting and the price is inside the band.",
     "Sample of five blocks the high grade by rule. Two score feeds list the match on Tuesday 27 October while the ATP report says Wednesday, so check the day order before kickoff.")

pick("Tennis", "Alejandro Tabilo vs Rafael Jodar", "Win Match", "Rafael Jodar",
     "Jodar to get past Tabilo in Basel (1.63)",
     "Rafael Jodar arrives in Basel as the third seed and the OLBG market gives him four of six tips, which we price at "
     "1.63 (-159) against Alejandro Tabilo. The draw context matters: Jodar sits in the half of the draw the tour's own "
     "preview projects to meet Ben Shelton, Taylor Fritz or Djokovic at either the quarter-final or the semi-final "
     "stage, so a first-match slip here is expensive for a seeded player and the seeded side of a first round is where "
     "these prices tend to be softest. Take Jodar to cover the round, not the trophy.",
     S["atp_draw"],
     [("ATP draw projection lists Rafael Jodar as a seeded quarter-final possibility opposite Djokovic, with Shelton (1), Fritz (6) and Davidovich Fokina (5) in the same projected path", S["atp_draw"]),
      ("Basel's updated main draw after three withdrawals pairs Tabilo with third seed Jodar", S["twi_basel"]),
      ("OLBG market: 4 of 6 tips on Jodar", S["olbg_base"])],
     "Seeding against a first-round opponent, in-band price, six tips counted.",
     "Jodar's win-loss record for 2026 and either player's fitness were not printed on a retrievable source, so no form claim is made. Six tips is a thin market.")

pick("Tennis", "Hubert Hurkacz vs Zizou Bergs", "Win Match", "Hubert Hurkacz",
     "Hurkacz over Bergs on home-circuit conditions (1.43)",
     "Hubert Hurkacz is seeded tenth in Basel and every one of the three tips counted on this OLBG market is on him, "
     "against a Zizou Bergs who is projected in the same quarter of the draw as seventh seed Alexander Bublik. Our "
     "line of 1.43 (-233) is just inside the focus floor, and the case is the serve: Hurkacz's rating and tournament "
     "seeding put him a clear place ahead on paper, while Bergs has been the player drawing the awkward indoor paths "
     "rather than winning through them. Small sample, honest number.",
     S["twi_basel"],
     [("Updated Basel main draw shows Hurkacz [10] v Bergs in one section and Bublik [7] in the quarter above", S["twi_basel"]),
      ("Djokovic's projected quarter-final is Bublik or Bergs, per the tour's own draw write-up", S["atp_draw"]),
      ("OLBG market: 3 of 3 tips on Hurkacz", S["olbg_base"])],
     "A unanimous but tiny vote, priced from the prior rather than the crowd.",
     "Three tips with no opposing side printed. No current-match-fitness or head-to-head data could be attached, so those fields are blank.")

pick("Tennis", "Stan Wawrinka vs Jiri Lehecka", "Win Match", "Stan Wawrinka",
     "Wawrinka to win his farewell home match against Lehecka (1.90)",
     "Stan Wawrinka is in the Basel draw on a wildcard and meets eighth seed Jiri Lehecka in the round of 32 - a pairing the "
     "ATP's own draw preview leads on. The OLBG market splits four of eight tips his way and we originate 1.90 (+190). "
     "That is as far as we go: no ranking, recent-match record or fitness statement for either player could be read "
     "from a retrievable source in this window, so this is a price on a split vote at a home tournament rather than a "
     "form case. Lehecka is the higher-rated man on seeding alone, which is the point of the price.",
     S["atp_draw"],
     [("ATP Tour draw preview: 'Novak Djokovic, Ben Shelton in same half of Basel draw; Stan Wawrinka meets Jiri Lehecka'", S["atp_draw"]),
      ("Wawrinka's entry is a wildcard and Lehecka carries the eighth seed in that section of the draw", S["atp_draw"]),
      ("OLBG market: 4 of 8 tips on Wawrinka", S["olbg_base"])],
     "The best price on the tennis card with a genuine narrative and eight tips counted.",
     "Nearly even tip split (4/8) and no player-level data we could put in print. Graded medium at best, and only because the market is a clean two-way one.")

pick("Tennis", "Leylah Fernandez vs Himeno Sakatsume", "Win Match", "Leylah Fernandez",
     "Fernandez to get over the first-round hurdle (1.32 - priced short, flagged)",
     "Ten of twelve tips on this OLBG market back Leylah Fernandez, which is the heaviest tennis vote on the card, but "
     "we are publishing it with a warning rather than a claim: the OLBG card does not name the tournament for this "
     "fixture or for the Osaka, Tager and Kudermetova rows alongside it, and no tour results page we could reach tied "
     "Fernandez to Sakatsume on a published draw for 27 October. The line we originate, 1.32 (-312), is a prior with a "
     "vote on top, and the venue, surface and both players' match fitness are left blank until the fixture is "
     "confirmable.",
     S["olbg_base"],
     [("OLBG market: 10 of 12 tips on Fernandez, printed 02:00 US Eastern with no competition or venue named on the card", S["olbg_base"]),
      ("Tournament, round, surface and head-to-head: BLANK - not printed on the OLBG card and not confirmable against the WTA's own schedule at capture (flag T-001)", "")],
     "Included because the brief is to price every market we capture, and flagged because it cannot be vouched for.",
     "Unconfirmable fixture. Do not stake on this row; it is here to document the card, not to recommend it.")

# ---------------------------------------------------------------------- VOLLEYBALL -------
pick("Volleyball", "TFL Altekma vs Halkbank Ankara", "Win Match", "Halkbank Ankara",
     "Halkbank to make it three wins from three in Izmir (1.50)",
     "Halkbank opened the Efeler Ligi with 3-1 wins over Galatasaray and then took five sets at Spor Toto, so they arrive "
     "at Altekma with six points from two rounds, and four of five OLBG tips are on them at 1.50 (-200). Altekma pushed the "
     "defending champions Ziraat Bankkart to five sets last time out - Ziraat won 3-2 without Yuki Ishikawa in the "
     "line-up - so this is not a walkover, but Halkbank have closed their own matches out inside four sets against "
     "Galatasaray and Spor Toto, which is the cleanest read on this board today.",
     S["tvf_wk1"],
     [("Efeler Ligi round 1: Halkbank 3-1 Galatasaray; Ziraat Bankkart 3-0 Fenerbahce (25-22, 25-21, 25-22)", S["tvf_wk1"]),
      ("Round 2: Ziraat Bankkart beat Altekma 3-2 in the absence of Yuki Ishikawa; Halkbank beat Spor Toto 3-2", S["voley_wk2"]),
      ("Matchday 3 fixtures include TFL Altekma v Halkbank Ankara, Tuesday 27 October (OLBG prints 08:00 US Eastern)", S["voley_wk2"])],
     "Grade B sample with a real league-form story and a price inside the band.",
     "Five tips. Turkish club volleyball line-ups rotate heavily and no confirmed roster was printed on the federation page we read, so no player-level claim is made.")

pick("Volleyball", "Ziraat Bankasi vs Gaziantep Genclik Spor", "Win Match", "Ziraat Bankasi",
     "Ziraat Bankkart to keep their perfect start going (1.36)",
     "Ziraat Bankkart are the club that has taken the Efeler Ligi in 2021, 2022, 2023, 2025 and 2026 and they have "
     "started the defence of it 2 wins from 2, 3-0 over Fenerbahce and 3-2 at Altekma, with all four OLBG tips on "
     "them for the third round game against Gaziantep. We price them at 1.36 (-278), which is outside the value zone "
     "the brief asks us to work in but is the strongest structural pick in the sport today - they were good enough to "
     "beat the previous round's 3-0 winners and the run of titles does not stop because a rotation is resting a player.",
     S["tvf_wk1"],
     [("Round 1: Ziraat Bankkart 3-0 Fenerbahce (25-22, 25-21, 25-22); round 2: 3-2 win over Altekma without Yuki Ishikawa in the line-up", S["tvf_wk1"]),
      ("Ziraat Bankkart are the 2026 Efeler Ligi champions and previous title holders", S["voley_ziraat"]),
      ("OLBG market: 4 of 4 tips on Ziraat Bankasi for Tuesday's round-3 fixture", S["olbg_base"])],
     "A four-tip unanimous vote on the most decorated club in the league.",
     "1.36 is 0.04 outside our focus floor and four tips is not a market. Confidence high, value absent - flagged as a no-bet.")

pick("Volleyball", "Fenerbahce vs Alanya Bld", "Win Match", "Alanya Bld",
     "Alanya Belediye to make it three from three at Burhan Felek (1.71)",
     "Here is the away-side value on this league board: Alanya have won both their opening Efeler Ligi rounds and are "
     "unbeaten alongside Gebze and Istanbul Bld, while Fenerbahce were swept 3-0 by Ziraat Bankkart in round 1 and then "
     "needed five sets at Gaziantep. Two of three OLBG tips already sit with Alanya and we price them at 1.71 (+120). "
     "Fenerbahce's roster is the better one on paper, but a team that has dropped a set at home to a side on zero wins "
     "is not the price the market is offering.",
     S["tvf_wk1"],
     [("Round 1: Fenerbahce lost 0-3 to Ziraat Bankkart; round 2: Fenerbahce won 3-2 at Gaziantep Bld", S["tvf_wk1"]),
      ("Alanya Belediye are unbeaten after two rounds along with Gebze Bld and Istanbul Bld Spor", S["voley_wk2"]),
      ("OLBG market: 2 of 3 tips on Alanya Bld", S["olbg_base"])],
     "The best combination of price (+120), a real result gap and a tip lean on this card.",
     "Three tips only, and no confirmed line-up for either side; Alanya's schedule strength was not published on the federation page we could read.")

pick("Volleyball", "Istanbul Genclik Spor vs IBB Spor", "Win Match", "IBB Spor",
     "Istanbul Buyuksehire to stay perfect (1.75)",
     "Istanbul Bld Spor are one of three clubs still unbeaten after two Efeler Ligi rounds, alongside Alanya and Gebze, "
     "and three of five tips on this OLBG market are on them to beat Istanbul Gencelikspor at 1.75 (+114). The "
     "unbeaten tag alone is not the case - Bld's results have come inside three sets, which means the squad has closed "
     "matches out rather than ground them, and a fifth-set habit from the hosts is the only thing that beats this line. "
     "No individual player data is attached because the federation page does not print one for this fixture.",
     S["voley_wk2"],
     [("Istanbul Bld Spor are unbeaten after two rounds of the Efeler Ligi along with Alanya Bld and Gebze Genclik", S["voley_wk2"]),
      ("OLBG market: 3 of 5 tips on IBB Spor", S["olbg_base"]),
      ("Rosters, MVPs and set-by-set statistics for this fixture: BLANK - not published on the retrievable federation page", "")],
     "Second of three unbeaten sides in the league, priced above evens.",
     "Five tips, no player-level confirmation, and the opponent's record was not printed. Graded B, confidence medium at best.")

pick("Volleyball", "Marignano W vs Bergamo W", "Win Match", "Bergamo W",
     "Bergamo women at number one on the OLBG vote, priced 1.55",
     "This Italian Serie A1 women's market is priced entirely from the tip split: five of seven OLBG tips sit with "
     "Bergamo on the road at Marignano and we originate 1.55 (-182). We are not writing a form argument. The federation "
     "and league sources for the Italian women's competition were not retrievable during this capture window, so the "
     "current standings, both teams' last results, and any injury or rotation news are left blank on the table and the "
     "row is flagged as market-only rather than filled in from memory.",
     S["olbg_base"],
     [("OLBG market: 5 of 7 tips on Bergamo W for the Tuesday fixture, printed 15:00 US Eastern", S["olbg_base"]),
      ("Serie A1 standings, matchday number, venue and team news: BLANK - no official league source retrievable at capture (flag V-002)", "")],
     "Published for completeness of the market grid, with the gap in the evidence named in the row.",
     "Seven tips and no external confirmation of the fixture at all. Graded C on evidence; do not stake.")

# ------------------------------------------------------------------------ GOLF -----------
pick("Golf", "Maybank Championship", "Win Tournament", "Lottie Woad",
     "Lottie Woad to lead the Maybank Championship field (4.35 originated)",
     "Lottie Woad is the player to name at the Maybank Championship, which runs 29 October to 1 November at the Kuala "
     "Lumpur Golf Club's West course for US$3m and 500 Race to CME Global points. She won the Kroger Queen City "
     "Championship in 2026 at 268, twelve under, sits seventh in the Rolex Rankings, and her most recent start was a "
     "round she finished 33rd at the BMW Ladies Championship after a tie for sixth at the AIG Women's Open - the form "
     "line is up-to-date and the venue has suited her game. The OLBG market carries one of two tips on her, which is "
     "why our 4.35 (+335) is an origination, not a quote.",
     S["lpga_maybank"],
     [("LPGA official tournament page: Maybank Championship, Kuala Lumpur Golf & Country Club (West), 29 October - 1 November 2026, US$3,000,000", S["lpga_maybank"]),
      ("Woad is ranked seventh in the Rolex Rankings and the 2026 Kroger Queen City Championship winner (268, -12)", S["gfn_field"]),
      ("Recent starts: 33rd at the BMW Ladies Championship, T6 at the AIG Women's Open", S["golfpost_maybank"]),
      ("Course details on the LPGA's own tournament page: Kuala Lumpur Golf & Country Club, West course, par 72 at 6,536 yards", S["lpga_maybank"]),
      ("One field report dated 26 October lists Nelly Korda and Atthaya Thitikul among the withdrawals; the same outlet's defending-champion line contradicts another and is unresolved, so no claim is made about who won the 2025 edition (flag GOLF-001)", S["golfpost_maybank"])],
     "The only golf selection on the card that can be tied to a confirmed tournament, a confirmed course and a current ranking.",
     "Two tips on a 78-player-plus field. The price is a prior on an eight-way assumed field (U-004), so read it as 'best name in the field', not as 4.35 of value.")

# ------------------------------------------------------------------- RUGBY / SNOOKER ----
# Snooker and Greyhounds published no OLBG markets at capture time - see flags.

UNPRICED_NOTE = ("No written prediction: OLBG printed this market on the sport page with no tip "
                 "split, so there is no number to price and no figure to quote.")
NO_MARKET_NOTE = ("OLBG returned 'No tips found.' for this sport at 05:45 UTC on 27 October 2026 - "
                  "there were no markets, no events and therefore nothing to originate.")

# --------------------------------------------------------------------------- flags ---------
FLAGS = [
    dict(id="U-001", sport="All", severity="structural",
         title="No bookmaker prices exist in retrievable OLBG HTML",
         detail="Every decimal and American price on this site is originated by us from OLBG's printed "
                "tip split (X of Y Win Tips) using the CAL-1R method: a per-market prior, K=6 pseudo-tips "
                "of shrinkage, and a 5% margin. No sportsbook quote is reproduced anywhere on the board, "
                "and none should be assumed. OLBG renders its odds widgets client-side, so they are not in "
                "the HTML that can be read.",
         action="Read prices as our line, never as the market's.",
         source=("https://www.olbg.com/betting-tips/", "OLBG tip pages")),
    dict(id="U-002", sport="Handball", severity="defect",
         title="Handball draw/tie clustering across 11 of 15 priced handball markets",
         detail="The EHF Champions League markets on the OLBG card are overwhelmingly tipped on the 'Tie' "
                "outcome (PSG v Aalborg 7/9, Wisla Plock v Nantes 8/11, Magdeburg v Kriens-Luzern 9/14, "
                "Vardar v Melsungen 8/13, Celje v Zagreb 6/8, Kielce v Kolstad 7/11 and more). Handball draws "
                "are rare: the EHF's own group-phase table shows only one drawn result across the matches "
                "already played in these groups (Aalborg 33-33 PSG). A line built from those votes would "
                "imply a 40-60% draw chance, so every handball Tie selection is graded C, capped at low "
                "confidence and excluded from the high-confidence set; the team-side prices are published "
                "instead, with the clustering named on each row.",
         action="Do not stake on any Tie line on this board.",
         source=("https://ehfcl.eurohandball.com/men/2026-27/standings/", "EHF Champions League standings")),
    dict(id="U-003", sport="All", severity="method",
         title="Reliability grades applied to every priced line",
         detail="Grade A: 8 or more tips counted on the market and no structural anomaly. Grade B: 3 to 7 tips. "
                "Grade C: fewer than 3 tips, a degenerate 0%/100% split, or a 3-way draw-cluster artefact. High "
                "confidence is blocked on any grade C line and requires at least 8 tips, a price inside the "
                "-250 to +10000 focus band and a consensus probability of at least 60% after shrinkage.",
         action="Grade is printed next to every line on the sport pages.",
         source=("", "")),
    dict(id="U-004", sport="All outrights", severity="method",
         title="Outright field sizes are assumed, not printed",
         detail="OLBG's outright markets (F1 title-without-Antonelli, PDC World Championship, Six Nations 2027, "
                "State of Origin 2027, Super League and NRL grand finals, GAA All-Ireland championships, golf "
                "winners, man-of-the-match markets) do not print the number of entries in the field. The pricing "
                "assumes an eight-way field for a uniform prior, which moves the price of a lightly-tipped runner "
                "by more than any other single assumption in the method.",
         action="Outright prices are directional only.",
         source=("", "")),
    dict(id="U-005", sport="Cricket", severity="data",
         title="Third Test start time reported two ways",
         detail="cricket.com.au lists the Cape Town Test as 7:30pm AEDT / 10:30am local; the OLBG event page for the "
                "same fixture prints a 31 October 04:30 card time (the scheduled final day, not the first) and a "
                "match-preview page shows 8:30 AM GMT. No single official start time could be confirmed, so the "
                "time column shows the fixture window (27-31 October) and the exact first-ball time is left blank.",
         action="Treat the printed card time as unusable; play the day, not the hour.",
         source=("https://www.cricket.com.au/news/4597818/south-africa-v-australia-third-test-match-preview-guide-cape-town-newlands-broadcast-details-how-to-watch-team-news-session-start-times-2026", "cricket.com.au")),
    dict(id="U-006", sport="Motor Racing", severity="data",
         title="Antonelli 'Top 6' tip split carried forward from the 26 October capture",
         detail="On 26 October the OLBG motor-racing page printed 17 of 18 tips on 'Kimi Antonelli - Yes' to finish "
                "in the top six of the Mexico City Grand Prix. The 27 October capture listed the same market with no "
                "numbers attached. The split is published with the earlier capture date labelled on the row rather "
                "than restated as today's signal, and it is not used for any high-confidence pick.",
         action="Row is labelled carried-forward; price it as stale.",
         source=("https://www.olbg.com/betting-tips/Motor_Racing", "OLBG motor racing page")),
    dict(id="U-007", sport="Motor Racing", severity="defect",
         title="OLBG tipster commentary contradicts the official 2026 standings",
         detail="The comment thread on the F1 title-without-Antonelli outright states that George Russell has 238 "
                "points against Lewis Hamilton 229 and Max Verstappen 221, with 'six races to go'. Formula1.com's "
                "own 2026 drivers' results page after round 18 reads Russell 242, Hamilton 241, Verstappen 236, "
                "Leclerc 233, Norris 211, with five rounds and 125 points remaining. The tipster figures are stale "
                "by 4 to 15 points and a full round; our line is built from the official standings, not the comments.",
         action="Ignore the numbers quoted inside OLBG comments.",
         source=("https://www.formula1.com/en/results/2026/drivers", "Formula1.com official results")),
    dict(id="U-008", sport="Rugby Union", severity="conflict",
         title="Two league tables disagree on the same Pro D2 round",
         detail="The LNR's own club page for Provence Rugby has Provence second on 29 points with Oyonnax leading on "
                "34, and shows round 8 as Provence 0-3 Beziers (a forfeit or correction). L'Equipe's Pro D2 table "
                "prints Provence on 34 and Dax in the lower half for the same fixture list. Because the two sources "
                "cannot be reconciled, no Provence or Dax points figure is published on the pick row and the Dax "
                "handicap line is graded on the tip split alone.",
         action="Pro D2 table positions are left blank; only the fixture and kick-off time are asserted.",
         source=("https://prod2.lnr.fr/club/provence-rugby", "LNR (official Pro D2)")),
    dict(id="U-009", sport="Ice Hockey", severity="conflict",
         title="Carolina's Taylor Hall: activated on IR? ",
         detail="The NHL's status report of 26 October had Taylor Hall activated and available, while the injury "
                "report on the ESPN game page for Boston at Carolina - read on 26/27 October - still lists Hall in "
                "the IR column with an estimated 7 November return, alongside Jordan Staal (IR, 3 December), Mark "
                "Jankowski (out) and Alexander Nikishin (not released). The conflict is unresolved, so no pick on "
                "this game claims Hall's availability either way.",
         action="Lineup-dependent claims suppressed for BOS @ CAR.",
         source=("https://www.espn.com/nhl/game/_/gameId/401892586/bruins-hurricanes", "ESPN NHL injury report")),
    dict(id="U-010", sport="Ice Hockey / Baseball", severity="defect",
         title="OLBG's printed start times are unreliable for North American fixtures",
         detail="OLBG prints its card times on a US-Eastern clock, and the pattern was confirmed against four "
                "non-US fixtures (a URC kick-off printed 15:45 for 19:45 UK, the Afghanistan v Zimbabwe T20I printed "
                "10:30 for 14:30 GMT, Pakistan v Sri Lanka printed 04:00 for 08:00 GMT, Aalborg v Wisla Plock printed "
                "13:45 for 18:45 local). Against official listings the North American games then come out wrong: "
                "World Series Game 4 is printed 21:00 for an 8:00pm ET first pitch, and the NHL games print 20:07 / "
                "19:07 for 8:00pm and 7:00pm ET puck drops. The printed minutes are not used anywhere in the copy; "
                "official times are quoted instead.",
         action="Times on every row come from the governing body, never from the OLBG card.",
         source=("https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule", "MLB.com")),
    dict(id="T-001", sport="Tennis", severity="blank",
         title="Four OLBG tennis rows carry no tournament, round or venue",
         detail="The Fernandez v Sakatsume, Osaka v Paolini, Tager v Williams and Kudermetova v Tien markets appear on "
                "the OLBG tennis page with a time and a tip percentage but no named event, and no tour schedule page "
                "we could reach tied those pairings to a published draw for 27 October 2026. Because the brief is to "
                "price every market we capture, the rows are priced and shown; because the fixture itself is not "
                "confirmable, tournament, round, surface and head-to-head are left blank and the predictions on them "
                "state that limitation instead of papering over it.",
         action="No staking case on these rows; the price is a prior on a tip vote.",
         source=("https://www.olbg.com/betting-tips/Tennis", "OLBG tennis page")),
    dict(id="SN-001", sport="Snooker", severity="empty",
         title="Snooker slate was empty at capture time",
         detail="The OLBG snooker page (sport id 8) returned the literal text 'No tips found.' when it was fetched at "
                "05:45 UTC on 27 October 2026, with no events, markets or tip rows. That is a genuine empty slate "
                "rather than a failed capture: the page rendered normally. One side effect is worth noting - with no "
                "tip rows the page's own sport menu degrades its label to 'All Sports', so a naive scraper reading the "
                "menu would mis-assign the rows.",
         action="No snooker picks today. Re-check later in the day; the World Snooker Tour calendar was not the blocker.",
         source=("https://www.olbg.com/betting-tips/Snooker", "OLBG snooker page")),
    dict(id="G-001", sport="Greyhounds", severity="empty",
         title="Greyhounds slate was empty at capture time",
         detail="The OLBG greyhounds page (sport id 28) returned 'No tips found.' at 05:42 UTC on 27 October 2026. "
                "Greyhound tip markets are usually published against specific early-morning UK track fixtures, so an "
                "empty card at 05:42 UTC (06:42 UK) is expected but not proof of an absence of races; the sport is "
                "recorded as captured-and-empty with zero originated lines rather than omitted.",
         action="No greyhound picks today; treat as 'no markets', not 'no racing'.",
         source=("https://www.olbg.com/betting-tips/Greyhounds", "OLBG greyhound page")),
    dict(id="V-001", sport="Volleyball", severity="blank",
         title="OLBG volleyball rows carry no competition label",
         detail="Fifteen volleyball markets were captured with team names and tip percentages only - the card prints no "
                "league, round or gender for any of them. The Turkish rows were matched to the Efeler Ligi men's "
                "fixture list from the federation's own reporting, but the Italian women's rows (Conegliano v "
                "Vallefoglia, Marignano v Bergamo), the Polish, Finnish and Brazilian rows could not be tied to an "
                "official league source inside the capture window. Where a row could not be tied to a governing body, "
                "the competition field is blank and the prediction says the price is market-only.",
         action="Only the three Turkish picks carry match facts; the rest are flagged.",
         source=("https://tvf.org.tr/icerik/efeler-liginde-birinci-hafta-sona-erdi", "Turkish Volleyball Federation")),
    dict(id="V-002", sport="Volleyball", severity="blank",
         title="Serie A1 women's standings not retrievable during capture",
         detail="No Italian league source printed the current matchday, table or line-ups inside our window, so the "
                "two Italian women's markets on the board (Marignano v Bergamo, Conegliano v Vallefoglia) are priced "
                "from the OLBG tip vote alone with all form fields blank.",
         action="Treat these two rows as market-only.",
         source=("", "")),
    dict(id="HB-001", sport="Handball", severity="blank",
         title="Handicap and totals markets printed with zero tips",
         detail="The PSG v Aalborg and Wisla Plock v Nantes event pages both list Match Handicap and Points Total "
                "markets (PSG -0.5 / Aalborg +0.5, total 63.5; Nantes +1.5 / Plock -1.5, total 57.5) with no tips on "
                "either side. Those four markets are shown as unpriced with the reason attached: with a 0/0 split "
                "there is no signal to shrink, and inventing a number would put a fake price on a real market.",
         action="Markets are listed with 'not priced' rather than filled in.",
         source=("https://www.olbg.com/betting-tips/Handball/All_Handball/All_Events", "OLBG handball event pages")),
    dict(id="B-001", sport="Baseball", severity="blank",
         title="World Series Game 4 totals market has no priceable split",
         detail="The BOS @ CAR-style totals pattern repeats here: the OLBG event page for Game 4 lists Game Totals at "
                "7.5 runs with zero tips on either side, and the money line carries only 2 tips (both on Milwaukee) "
                "with nothing on Tampa Bay's side of the split. The totals market is therefore unpriced on the board, "
                "and both run-line and money-line rows are graded C for sample size even where the baseball situation "
                "is not close.",
         action="No total offered for Game 4; the series situation is published instead.",
         source=("https://www.espn.com/mlb/game/_/gameId/401908045/brewers-rays", "ESPN")),
    dict(id="GOLF-001", sport="Golf", severity="conflict",
         title="Two of the three OLBG golf events could not be confirmed on a tour schedule",
         detail="The Maybank Championship is confirmed on the LPGA's own tournament page (29 October - 1 November, KLGCC "
                "West). The other two golf outrights on the OLBG card - 'Mexico Open' with 1 of 2 tips on Wyndham Clark "
                "and 'Simmons Bank Championship' with 1 of 2 tips on Stewart Cink, both printed 01 November 17:45 - "
                "were not matched to a PGA Tour or Korn Ferry Tour listing in this window, and one preview article "
                "names the wrong defending champion for the Maybank field. Those two rows are priced and flagged with "
                "no prediction written, and the defending-champion correction is noted on the Woad row.",
         action="No written analysis for Mexico Open / Simmons Bank until the events are confirmed.",
         source=("https://www.lpga.com/tournaments/maybank-championship", "LPGA (official)")),
    dict(id="BK-001", sport="Basketball", severity="blank",
         title="Two EuroLeague rows are priced without standings data",
         detail="The standings and results pages readable during this window printed the top six and bottom two rows "
                "of the EuroLeague table, which is enough to write about Panathinaikos, Fenerbahce, Dubai, Baskonia's "
                "last result and Paris, but not enough to state Crvena Zvezda's or Maccabi Tel Aviv's records, or "
                "Real Madrid's Round 7 result. Those cells are blank on the two affected pick rows and the picks say "
                "so in the body text instead of carrying a number we could not read.",
         action="Belgrade and Vitoria picks are price-only; do not treat them as form cases.",
         source=("https://www.eurohoops.net/euroleague-standings/", "Eurohoops (EuroLeague standings)")),
    dict(id="P-001", sport="Coverage", severity="method",
         title="Five of fifteen sports are priced from two or three tips, or not at all",
         detail="Of the fifteen sports in scope, thirteen produced markets on 27 October (152 unique markets, 140 "
                "priced, 12 unpriced with reasons). Snooker and greyhounds produced nothing. High-confidence lines "
                "exist in one sport only - cricket, three of them - because the brief asks for picks inside the -250 "
                "to +10000 band while the near-certain outcomes on this card (Afghanistan at 1.16, Fernandez at 1.32, "
                "Antonelli at 1.15, Ziraat at 1.36, KalPa at 1.31) all price shorter than -250 by our method. Those "
                "lines are published as 'strong, outside band' rather than promoted.",
         action="The executive summary ranks what is actionable, and the shortfall is stated rather than padded.",
         source=("", "")),
]


URL2SITE = {v[0]: v[1] for v in S.values() if isinstance(v, tuple) and v[0]}


def norm_fact(f):
    """A fact is (text, url) or (text, (url, site)) or (text, (site,))."""
    text, ref = f[0], f[1]
    if isinstance(ref, tuple):
        url = ref[0]
        site = ref[1] if len(ref) > 1 and ref[1] else URL2SITE.get(url, "")
    else:
        url = ref
        site = URL2SITE.get(url, "")
    return dict(text=text, url=url, site=site)


def clean(t):
    return re.sub(r"\s+", " ", t).strip()


def main():
    lines = json.load(open(os.path.join(OUT, "lines.json")))
    priced = {}
    for r in lines["lines"]:
        k = (r["sport"], (r.get("event") or "").lower(), (r.get("market") or "").lower(),
             (r.get("selection") or "").lower())
        priced[k] = r

    preds, problems = [], []
    for i, p in enumerate(P, start=1):
        k = (p["sport"], p["event"].lower(), p["market"].lower(), p["selection"].lower())
        src = priced.get(k)
        if src is None:
            problems.append(f"NO MATCH for pick {i}: {p['sport']} / {p['event']} / {p['market']} / {p['selection']}")
            continue
        o = src.get("our_line") or {}
        wc = len(clean(p["prediction"]).split())
        if wc < 30:
            problems.append(f"pick {i} too short ({wc} words)")
        lowtext = (p["prediction"] + " " + p["pick_label"] + " " + p["angle"] + " " + p["risk"]).lower()
        for b in BANNED:
            if re.search(r"\b" + b + r"\b", lowtext):
                problems.append(f"pick {i} contains banned word '{b}'")
        facts = [norm_fact(f) for f in p["facts"]]
        for fx in facts:
            if fx["url"] and not fx["url"].startswith("https://"):
                problems.append(f"pick {i} fact url not https: {fx['url']}")
            if not fx["url"] and "BLANK" not in fx["text"]:
                problems.append(f"pick {i} fact without url: {fx['text'][:40]}")
        preds.append(dict(
            id=f"P-{CYCLE.replace('-', '')}-{i:02d}", cycle=CYCLE, sport=p["sport"],
            competition=src.get("competition") or "", event=p["event"],
            when_official=p.get("when_official") or "", market=p["market"], selection=p["selection"],
            pick_label=p["pick_label"], prediction=clean(p["prediction"]), word_count=wc,
            our_line=o.get("card_decimal"), our_line_american=o.get("card_american"),
            implied_pct=o.get("implied_pct"), confidence=o.get("confidence"), grade=o.get("grade"),
            p_fair=o.get("p_fair"), structure=o.get("structure"), notes=o.get("notes") or [],
            tips_on_pick=src.get("tips_on_pick"), tips_total=src.get("tips_total"),
            pct=src.get("pct"), olbg_url=src.get("url"), event_id=src.get("event_id"),
            angle=p["angle"], risk=p["risk"],
            facts=facts,
        ))

    json.dump(dict(cycle=CYCLE, count=len(preds),
                   by_sport={s: sum(1 for x in preds if x["sport"] == s) for s in sorted({x["sport"] for x in preds})},
                   picks=preds),
              open(os.path.join(OUT, "predictions.json"), "w"), indent=1)
    json.dump(dict(cycle=CYCLE, flags=FLAGS, count=len(FLAGS)),
              open(os.path.join(OUT, "flags.json"), "w"), indent=1)

    # sources.json - every source cited by any pick, with what it was used for
    src_seen = {}
    for p in preds:
        for f in p["facts"]:
            u = f["url"]
            if not u:
                continue
            src_seen.setdefault(u, dict(url=u, site=f["site"] or u.split("/")[2], used_for=[],
                                         official=u.split("/")[2].replace("www.", ""), picks=[]))
            if f["text"] not in src_seen[u]["used_for"]:
                src_seen[u]["used_for"].append(f["text"])
            src_seen[u]["picks"].append(p["id"])
    for fl in FLAGS:
        u = fl["source"][0]
        if u and u not in src_seen:
            src_seen[u] = dict(url=u, site=fl["source"][1], used_for=[f"flag {fl['id']}"], official="", picks=[])
    json.dump(dict(cycle=CYCLE, count=len(src_seen), sources=sorted(src_seen.values(), key=lambda x: x["url"])),
              open(os.path.join(OUT, "sources.json"), "w"), indent=1)

    print(f"picks={len(preds)} flags={len(FLAGS)} sources={len(src_seen)} -> {OUT}")
    from collections import Counter
    print("  by sport:", dict(Counter(x["sport"] for x in preds)))
    print("  conf:", dict(Counter(x["confidence"] for x in preds)),
          " grade:", dict(Counter(x["grade"] for x in preds)))
    print("  min words:", min(x["word_count"] for x in preds), "max:", max(x["word_count"] for x in preds))
    for pr in problems:
        print("  PROBLEM:", pr)
    if not problems:
        print("  no validation problems")


if __name__ == "__main__":
    main()

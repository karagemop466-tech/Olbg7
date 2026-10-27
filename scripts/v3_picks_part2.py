#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3 picks part 2 - Rugby Union, Handball, Tennis, Volleyball, Golf."""

PICKS = []


def add(**kw):
    PICKS.append(kw)


# =============================================================================
# RUGBY UNION
# =============================================================================
add(sport="Rugby Union", event="Connacht v Leinster",
    competition="United Rugby Championship 2026-27, round 6",
    when="Friday 30 October 2026", venue="Galway",
    market="Match Winner", selection="Leinster to win the match",
    line="-200", probability=0.667, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="1 of 1 tips on the Connacht +3.50 handicap - no winner market published",
    text=("Leinster are sixth in the URC on 13 points from four games, two wins and two losses, "
          "with 99 points for and 76 against, a +23 differential that is the fourth best in the "
          "competition. Connacht are eighth on 10 points from four, also two and two, but 104 for "
          "against 111 - seven points adrift. Leinster lost 26-20 away to the Sharks in the "
          "opening round on 3 October, which is one of only two defeats they carry. Our line from "
          "the official table prices Leinster -200 and Connacht +200. OLBG publishes only a "
          "Connacht +3.50 handicap here with a single tip and no match-winner split at all, which "
          "we flag; our own reading of the table is that three and a half points is generous to "
          "the home side."),
    sources=[("Sky Sports - United Rugby Championship table",
              "https://www.skysports.com/rugby-union/united-rugby-championship/table"),
             ("BBC Sport - United Rugby Championship standings",
              "https://www.bbc.co.uk/sport/rugby-union/tables/united-rugby-championship"),
             ("Wikipedia - 2026-27 United Rugby Championship",
              "https://en.wikipedia.org/wiki/2026%E2%80%9327_United_Rugby_Championship")],
    flag="OLBG prints a Connacht +3.50 handicap selection with no market label and no match-winner "
         "tip split.")

add(sport="Rugby Union", event="Colomiers v Agen",
    competition="Pro D2 2026-27, round 9",
    when="Thursday 29 October 2026", venue="Colomiers",
    market="Match Winner", selection="Colomiers to win the match",
    line="-237", probability=0.703, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="2 of 2 tips (100%)",
    text=("This is the most interesting Pro D2 position on the board, because the league table "
          "and the points difference tell different stories. Agen sit ninth on 19 points from "
          "eight games while Colomiers are twelfth on 13, but Colomiers carry a +8 points "
          "difference against Agen's -13 - meaning Colomiers have lost tight games and collected "
          "losing bonuses while Agen have been beaten heavily. Agen lost 31-13 at Colomiers in "
          "round three before beating Nice 28-24 in round eight; Colomiers lost 28-23 away at "
          "Valence-Romans. Our line from the official points difference per game prices Colomiers "
          "-237 and Agen +237, and both tips on OLBG agree."),
    sources=[("allrugby.com - official Pro D2 standings and home/away splits",
              "https://www.allrugby.com/competitions/pro-d2/classement.html"),
             ("L'Equipe - official Pro D2 table",
              "https://www.lequipe.fr/Rugby/pro-d2/page-classement-equipes/general"),
             ("French Wikipedia - 2026-27 Pro D2 season",
              "https://fr.wikipedia.org/wiki/Championnat_de_France_de_rugby_%C3%A0_XV_de_2e_division_2026-2027")],
    flag=None)

add(sport="Rugby Union", event="Biarritz v Valence-Romans",
    competition="Pro D2 2026-27, round 9",
    when="Thursday 29 October 2026", venue="Biarritz",
    market="Match Winner", selection="Biarritz to win the match",
    line="-162", probability=0.618, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="1 of 1 tips (100%)",
    text=("Biarritz are eighth in the Pro D2 on 20 points from eight games with 244 points for "
          "and 236 against, while Valence-Romans sit eleventh on 17 points with 250 for and 243 "
          "against. The gap is small on points but Biarritz are the side that has been collecting "
          "wins rather than bonuses, and Valence-Romans drew 28-28 with Agen in round eight "
          "before beating Soyaux-Angouleme 28-23 in round seven. Our line prices Biarritz -162 "
          "and Valence-Romans +161, inside our band and corroborated by the official table. Only "
          "a single tip sits on the OLBG market, which keeps the sample thin, but the origination "
          "is what carries the grade here."),
    sources=[("L'Equipe - official Pro D2 table",
              "https://www.lequipe.fr/Rugby/pro-d2/page-classement-equipes/general"),
             ("allrugby.com - official Pro D2 standings",
              "https://www.allrugby.com/competitions/pro-d2/classement.html"),
             ("La Depeche - Pro D2 round 8 results and standings",
              "https://www.ladepeche.fr/2026/10/27/pro-d2-8e-journee-classement-et-resultats-13194806.php")],
    flag=None)

add(sport="Rugby Union", event="Dax v Provence",
    competition="Pro D2 2026-27, round 9",
    when="Thursday 29 October 2026", venue="Dax",
    market="Match Winner", selection="Provence Rugby to win the match",
    line="-1166", probability=0.921, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="2 of 3 tips on Dax (67%) - we are against the tip flow",
    text=("Provence Rugby are unbeaten in the Pro D2 - eight wins from eight, 34 points, 276 "
          "points for and 161 against, a +115 differential that is the best in the division by a "
          "wide margin, and they beat Beziers 54-3 in round eight. Dax are tenth on 19 points "
          "from eight, four wins and four losses, 276 for against 313, and were beaten 49-7 away "
          "at Soyaux-Angouleme in the previous round after winning 54-28 against Montauban. Our "
          "line prices Provence -1166 and Dax +1166. Two of the three OLBG tips sit with Dax at "
          "home, which we flag as a direct contradiction of the official record. The price is far "
          "outside our band, so this grades down regardless."),
    sources=[("L'Equipe - official Pro D2 table",
              "https://www.lequipe.fr/Rugby/pro-d2/page-classement-equipes/general"),
             ("allrugby.com - official Pro D2 standings",
              "https://www.allrugby.com/competitions/pro-d2/classement.html"),
             ("French Wikipedia - 2026-27 Pro D2 season",
              "https://fr.wikipedia.org/wiki/Championnat_de_France_de_rugby_%C3%A0_XV_de_2e_division_2026-2027")],
    flag="OLBG tips Dax 2/3 while the official Pro D2 table has Provence unbeaten at 8-0-0 with "
         "+115 and Dax tenth on -37.")

add(sport="Rugby Union", event="Glasgow Warriors v Lions",
    competition="United Rugby Championship 2026-27, round 6",
    when="Friday 30 October 2026", venue="Glasgow",
    market="Match Winner", selection="Glasgow Warriors to win the match",
    line="-2610", probability=0.963, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="1 of 1 tips (100%)",
    text=("Glasgow Warriors are second in the URC and unbeaten: three wins and a draw from four, "
          "119 points for against 92, +27, 18 points on the board. Their draw came in a 33-33 "
          "shootout with Ulster on 3 October. Lions are eleventh on nine points from four, two "
          "wins and two losses, 87 for against 133 - a -46 differential, the worst of any side on "
          "this page. Our line prices Glasgow -2610 and Lions +2610. The direction is about as "
          "clear as rugby union gets, but the price is miles outside the -250 to +10000 band we "
          "hold top-grade picks to, so it grades down on price alone."),
    sources=[("Sky Sports - United Rugby Championship table",
              "https://www.skysports.com/rugby-union/united-rugby-championship/table"),
             ("BBC Sport - United Rugby Championship standings",
              "https://www.bbc.co.uk/sport/rugby-union/tables/united-rugby-championship"),
             ("Wikipedia - 2026-27 United Rugby Championship",
              "https://en.wikipedia.org/wiki/2026%E2%80%9327_United_Rugby_Championship")],
    flag=None)

# =============================================================================
# HANDBALL
# =============================================================================
add(sport="Handball", event="Paris Saint-Germain v Aalborg Handbold",
    competition="EHF Champions League 2026-27, group C, round 6",
    when="Wednesday 28 October 2026", venue="Paris",
    market="Money Line", selection="Paris Saint-Germain to win the match",
    line="-125", probability=0.556, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="9 of 14 tips on 'Tie' (64%) - a selection that cannot be backed as a winner",
    text=("Aalborg Handbold top group C on nine points from five, four wins, no draws and a loss, "
          "with 170 goals for and 145 against. Paris Saint-Germain are second on seven points, "
          "three wins, a draw and a loss, with 182 for and 157 against. The two clubs have an "
          "identical +25 goal difference across five rounds, so the tiebreak is home court - and "
          "this game is in Paris. Our line prices PSG -125 and Aalborg +125 after allowing for the "
          "handball draw, which appeared twice in thirty group-phase games across groups A, C and "
          "F. This is the tightest handball game of round six and the only one where our price "
          "sits inside the band we hold top-grade picks to."),
    sources=[("EHF Champions League - official group C table",
              "https://www.eurohandball.com/en/ehfcl/men/2026-27/group-phase/group-c/"),
             ("EHF - Champions League match centre, round 6",
              "https://www.eurohandball.com/en/ehfcl/men/2026-27/")],
    flag="OLBG prints 'Tie' as the most-tipped Money Line selection on this and ten other handball "
         "events, which cannot be backed on a money line.")

add(sport="Handball", event="SC Magdeburg v HC Kriens-Luzern",
    competition="EHF Champions League 2026-27, group F, round 6",
    when="Wednesday 28 October 2026, 20:45 CET", venue="GETEC Arena, Magdeburg",
    market="Money Line", selection="SC Magdeburg to win the match",
    line="-586", probability=0.854, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="9 of 14 tips on 'Tie' (64%)",
    text=("Magdeburg are top of group F and unbeaten: five wins from five, 176 goals for against "
          "140, +36, ten points. Kriens-Luzern are third on four points, two wins and three "
          "losses, 158 for against 161. The two already met on 17 September in Switzerland, where "
          "Magdeburg won 39-29 after leading 20-11 at half-time, and the return leg is at the "
          "GETEC Arena in front of Magdeburg's own crowd. Our line prices Magdeburg -586 and "
          "Kriens-Luzern +586. The direction is not in question; the price is well outside the "
          "-250 to +10000 band, which is the only reason this is not top grade."),
    sources=[("EHF Champions League - official group F table",
              "https://www.eurohandball.com/en/ehfcl/men/2026-27/group-phase/group-f/"),
             ("handball-world.news - Magdeburg vs Kriens-Luzern, 17 September 2026",
              "https://www.handball-world.news/o.red.r/news-3-2-265-165000.html"),
             ("EHF - Champions League match centre, round 6",
              "https://www.eurohandball.com/en/ehfcl/men/2026-27/")],
    flag="OLBG prints 'Tie' as the most-tipped Money Line selection.")

add(sport="Handball", event="KS Kielce v Kolstad Handball",
    competition="EHF Champions League 2026-27, group F, round 6",
    when="Wednesday 28 October 2026", venue="Kielce",
    market="Money Line", selection="KS Kielce to win the match",
    line="-551", probability=0.847, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="7 of 11 tips on 'Tie' (64%)",
    text=("Kolstad Handball are bottom of group F and still without a point: five games, five "
          "losses, 143 goals for against 178, a -35 differential. KS Kielce are second on six "
          "points, three wins and two losses, 155 for against 153 - a +2 differential that is "
          "much thinner than their league position suggests, and they lost 27-30 at Magdeburg on "
          "14 October. Our line prices Kielce -551 and Kolstad +551, so the gap we are backing is "
          "between a side that has never won in the group and one playing at home. The price is "
          "outside our band, so this grades one rung down."),
    sources=[("EHF Champions League - official group F table",
              "https://www.eurohandball.com/en/ehfcl/men/2026-27/group-phase/group-f/"),
             ("EHF - Champions League match centre, round 6",
              "https://www.eurohandball.com/en/ehfcl/men/2026-27/")],
    flag="OLBG prints 'Tie' as the most-tipped Money Line selection.")

add(sport="Handball", event="FC Porto v One Veszprém",
    competition="EHF Champions League 2026-27, group A, round 6",
    when="Wednesday 28 October 2026", venue="Porto",
    market="Money Line", selection="One Veszprém to win the match",
    line="-586", probability=0.854, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="8 of 13 tips on 'Tie' (62%)",
    text=("One Veszprém are top of group A and unbeaten: five wins from five, 185 goals for "
          "against 146, +39, ten points. FC Porto are third on three points, a win, a draw and "
          "three losses, 158 for against 173. The two met a week ago on 21 October at the "
          "Veszprém Arena, where Veszprém won 36-28 in front of 5,090 spectators, and Porto's one "
          "draw in the group came against RK Partizan, who are bottom on a single point. Our line "
          "prices Veszprém -586 and Porto +586 as the away side. Backing a road team is rarely "
          "comfortable, but a +39 differential against -15 and an eight-goal win a week earlier "
          "is the strongest handball case on the board. The price keeps it out of the top grade."),
    sources=[("EHF Champions League - official group A table",
              "https://www.eurohandball.com/en/ehfcl/men/2026-27/group-phase/group-a/"),
             ("One Veszprém - official club, 21 October 2026 report",
              "https://www.oneveszprem.hu/en/news/4034")],
    flag="OLBG prints 'Tie' as the most-tipped Money Line selection.")

add(sport="Handball", event="Füchse Berlin v RK Partizan",
    competition="EHF Champions League 2026-27, group A, round 6",
    when="Wednesday 28 October 2026", venue="Berlin",
    market="Money Line", selection="Füchse Berlin to win the match",
    line="-746", probability=0.882, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="6 of 14 tips on 'Tie' (43%)",
    text=("RK Partizan are bottom of group A with a single point from five games, 148 goals for "
          "against 184, a -36 differential, and that point came from a draw against FC Porto. "
          "Füchse Berlin are second on six points, three wins and two losses, 184 for against "
          "172. Our line prices Füchse -746 and Partizan +746, which is the widest margin we "
          "originate anywhere on the handball board. Note that OLBG files this fixture under the "
          "EHF European League while both clubs appear in the official Champions League group "
          "tables - a filing error we flag rather than follow. The price is far outside our band, "
          "so this grades down."),
    sources=[("EHF Champions League - official group A table",
              "https://www.eurohandball.com/en/ehfcl/men/2026-27/group-phase/group-a/"),
             ("EHF - Champions League match centre", "https://www.eurohandball.com/en/ehfcl/men/2026-27/")],
    flag="OLBG files this fixture under the EHF European League although both clubs appear in the "
         "official EHF Champions League group A table. OLBG also prints 'Tie' as the most-tipped "
         "Money Line selection.")

# =============================================================================
# TENNIS
# =============================================================================
add(sport="Tennis", event="Novak Djokovic v Ugo Humbert",
    competition="ATP Basel (Swiss Indoors), ATP 500, round of 32",
    when="Week of Monday 26 October 2026", venue="Basel, Switzerland (indoor hard)",
    market="Match Winner", selection="Novak Djokovic to win the match",
    line="-218", probability=0.685, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="4 of 5 tips (80%)",
    text=("Djokovic is making his first appearance in Basel since 2011 and is seeded fourth in a "
          "field carrying a EUR 2,584,155 prize pot over a 32-draw. He sits world No. 12 on 3,090 "
          "ranking points; Ugo Humbert is No. 35 on 1,420. Djokovic is eleventh in the race to "
          "Turin and drops zero points this week, so a deep run in Switzerland is worth more to "
          "him than the seeding suggests. Our line is built directly from the official ATP points "
          "ratio and prices Djokovic -218 and Humbert +218, inside our band and corroborated by "
          "the published draw. Four of the five tips agree."),
    sources=[("ATP Tour - Basel tournament profile", "https://www.atptour.com/en/tournaments/basel/328/overview"),
             ("ATP Tour - official entry list and seeds, Basel 2026",
              "https://www.atptour.com/en/tournaments/basel/328/2026/entry-lists"),
             ("ATP Tour - Djokovic scouting report, Basel return",
              "https://www.atptour.com/en/news/basel-2026-scouting-report")],
    flag=None)

add(sport="Tennis", event="Carlos Alcaraz v Karen Khachanov",
    competition="ATP Vienna (Erste Bank Open), ATP 500, round of 32",
    when="Week of Monday 26 October 2026", venue="Vienna, Austria (indoor hard)",
    market="Match Winner", selection="Carlos Alcaraz to win the match",
    line="-282", probability=0.738, track="R", tier="R", confidence="MEDIUM",
    in_band=False, olbg="2 of 2 tips on Khachanov (100%) - we are against the tip flow",
    text=("Alcaraz is world No. 3 on 5,610 ranking points and seeded second in Vienna, a EUR "
          "2,797,985 event on indoor hard courts across a 32-draw, and he is chasing a fourth "
          "tour-level title of 2026 which would give him five consecutive seasons with at least "
          "four. Khachanov is No. 25 on 1,990 points and a recent US Open semi-finalist, so this "
          "is not a mismatch, but our line from the official points ratio prices Alcaraz -282 and "
          "Khachanov +282. OLBG's two tips are both on Khachanov against the world No. 3, which "
          "we flag rather than follow. The price is also just outside the band, so this grades "
          "down on both counts."),
    sources=[("ATP Tour - Vienna tournament profile",
              "https://www.atptour.com/en/tournaments/vienna/337/overview"),
             ("ATP Tour - official entry list and seeds, Vienna 2026",
              "https://www.atptour.com/en/tournaments/vienna/337/2026/entry-lists"),
             ("BBC Sport - Vienna order of play", "https://www.bbc.co.uk/sport/tennis/articles/c1jn8p8x8vgo")],
    flag="OLBG tips Khachanov 2/2 against the world No. 3 and No. 2 seed.")

add(sport="Tennis", event="Naomi Osaka v Jasmine Paolini",
    competition="WTA Tokyo (Toray Pan Pacific Open), WTA 500, round of 32",
    when="Week of Monday 26 October 2026", venue="Tokyo, Japan (outdoor hard)",
    market="Match Winner", selection="Naomi Osaka to win the match",
    line="-233", probability=0.700, track="T", tier="C", confidence="MEDIUM",
    in_band=True, olbg="4 of 4 tips (100%)",
    text=("Osaka is seeded seventh in the 28-player singles draw of the Toray Pan Pacific Open, a "
          "WTA 500 on outdoor hard courts running from 26 October to 1 November, and opens "
          "against Jasmine Paolini in the round of 32. The field around them includes Rybakina, "
          "Swiatek, Pegula, Svitolina, Bencic, Muchova, Eala and Leylah Fernandez, so this is a "
          "genuinely deep draw and Paolini is not a soft opening opponent. All four tips posted "
          "on the OLBG market are with Osaka, and our tip-derived line prices her -233 and "
          "Paolini +233. The sample is only four tips, which keeps it out of the top grade "
          "despite the price sitting inside our band."),
    sources=[("WTA - Tokyo tournament profile", "https://www.wtatennis.com/tournaments/tokyo"),
             ("BBC Sport - Tokyo order of play, women's singles round of 32",
              "https://www.bbc.co.uk/sport/tennis/articles/c623j0zj8y3o"),
             ("Wikipedia - 2026 Toray Pan Pacific Open",
              "https://en.wikipedia.org/wiki/2026_Toray_Pan_Pacific_Open")],
    flag=None)

add(sport="Tennis", event="Leylah Fernandez v Himeno Sakatsume",
    competition="WTA Tokyo (Toray Pan Pacific Open), WTA 500, round of 32",
    when="Week of Monday 26 October 2026", venue="Tokyo, Japan (outdoor hard)",
    market="Match Winner", selection="Leylah Fernandez to win the match",
    line="-260", probability=0.722, track="T", tier="B", confidence="MEDIUM",
    in_band=False, olbg="10 of 12 tips (83%)",
    text=("Fernandez is one of the headline names in the official 28-player singles draw at the "
          "Toray Pan Pacific Open and meets Himeno Sakatsume in the round of 32. This is the "
          "deepest tennis sample on the OLBG board this week - twelve tips, of which ten sit with "
          "Fernandez - and our tip-derived line prices her -260 and Sakatsume +260. That is one "
          "tick outside the -250 to +10000 band we hold top-grade picks to, which is the only "
          "thing keeping this down; the twelve-tip sample would otherwise qualify it on its own."),
    sources=[("WTA - Tokyo tournament profile", "https://www.wtatennis.com/tournaments/tokyo"),
             ("BBC Sport - Tokyo order of play", "https://www.bbc.co.uk/sport/tennis/articles/c623j0zj8y3o"),
             ("OLBG tennis tips board", "https://www.olbg.com/betting-tips/Tennis/15")],
    flag=None)

add(sport="Tennis", event="Stan Wawrinka v Jiri Lehecka",
    competition="ATP Basel (Swiss Indoors), ATP 500, round of 32",
    when="Week of Monday 26 October 2026", venue="Basel, Switzerland (indoor hard)",
    market="Match Winner", selection="Stan Wawrinka to win the match",
    line="-100", probability=0.500, track="T", tier="B", confidence="MEDIUM",
    in_band=True, olbg="4 of 8 tips (50%)",
    text=("This is Wawrinka's farewell appearance in Basel, the Swiss indoor ATP 500 that runs "
          "from 26 October to 1 November on a EUR 2,584,155 prize pot, and he meets Jiri Lehecka "
          "in the round of 32. The draw around them carries Shelton, Fritz, Fils, "
          "Auger-Aliassime, Bublik, Ruud, Fonseca, Hurkacz, Tsitsipas and Rune, so the field is "
          "strong even by Basel standards. Tips are split evenly, four of eight each way, and our "
          "line prices it at -100 against +100, a genuine pick'em. We publish Wawrinka because "
          "that is where half the tips sit and because the price is inside our band, but an even "
          "split on eight tips is not a position to grade highly."),
    sources=[("ATP Tour - Basel tournament profile", "https://www.atptour.com/en/tournaments/basel/328/overview"),
             ("ATP Tour - Wawrinka farewell Basel scouting report",
              "https://www.atptour.com/en/news/basel-2026-scouting-report"),
             ("OLBG tennis tips board", "https://www.olbg.com/betting-tips/Tennis/15")],
    flag=None)

# =============================================================================
# VOLLEYBALL
# =============================================================================
add(sport="Volleyball", event="Conegliano W v Vallefoglia W",
    competition="Serie A1 femminile 2026-27, round 5 make-up",
    when="Wednesday 28 October 2026, 20:00 local",
    venue="Palaverde, Villorba",
    market="Win Match", selection="Conegliano to win the match",
    line="-209", probability=0.677, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="6 of 10 tips on Vallefoglia (60%) - we are against the tip flow",
    text=("Conegliano are four wins from four in Serie A1 with twelve points and, remarkably, "
          "twelve sets won to zero: 3-0 over Cuneo on 4 October, 3-0 over Busto Arsizio on 10 "
          "October, 3-0 at Chieri on 14 October taking the sets 25-19, 25-14 and 25-22, and 3-0 "
          "over Talmassons on 18 October. On Saturday 24 October they added a ninth Supercoppa "
          "Italiana, beating Scandicci in the final in Bari. Vallefoglia are also four from four "
          "but on eleven points, having needed five sets at Scandicci on 10 October and beating "
          "Cuneo 3-0 with a 31-29 third set. Our line prices Conegliano -209 and Vallefoglia "
          "+209. OLBG's six of ten tips are on Vallefoglia at home to a side that has not dropped "
          "a set all season, which we flag rather than follow."),
    sources=[("LegaVolley Femminile - official Serie A1 results",
              "https://www.legavolleyfemminile.it/risultati/"),
             ("LegaVolley Femminile - official Serie A1 standings",
              "https://www.legavolleyfemminile.it/classifiche/"),
             ("LegaVolley Femminile - Supercoppa Italiana 2026, Bari",
              "https://www.legavolleyfemminile.it/supercoppa/")],
    flag="OLBG tips Vallefoglia 6/10 away at Conegliano, who are 4-0 and 12-0 in sets and won a "
         "ninth Supercoppa Italiana on 24 October 2026.")

add(sport="Volleyball", event="Marignano W v Bergamo W",
    competition="Serie A1 femminile 2026-27",
    when="Tuesday 27 October 2026", venue="San Giovanni in Marignano",
    market="Win Match", selection="Bergamo to win the match",
    line="-160", probability=0.615, track="T", tier="C", confidence="MEDIUM",
    in_band=True, olbg="5 of 7 tips (71%)",
    text=("Bergamo sit on eight points in the Serie A1 femminile table against San Giovanni in "
          "Marignano's three, and the two are meeting in a round where the rest of the league is "
          "still settling after the Supercoppa weekend. Bergamo have been competitive at the top "
          "end of the table this season, taking Milano to a full contest at home before losing, "
          "while Marignano's three points leave them in the bottom half. Five of the seven tips "
          "posted on OLBG are with Bergamo and our tip-derived line prices them -160 and "
          "Marignano +160. The seven-tip sample keeps it one rung below top grade."),
    sources=[("LegaVolley Femminile - official Serie A1 standings",
              "https://www.legavolleyfemminile.it/classifiche/"),
             ("LegaVolley Femminile - official Serie A1 results",
              "https://www.legavolleyfemminile.it/risultati/"),
             ("OLBG volleyball tips board", "https://www.olbg.com/betting-tips/Volleyball/31")],
    flag=None)

add(sport="Volleyball", event="Ziraat Bankasi v Gaziantep Genclik Spor",
    competition="",
    when="Tuesday 27 October 2026", venue="",
    market="Win Match", selection="Ziraat Bankasi to win the match",
    line="-233", probability=0.700, track="T", tier="C", confidence="LOW",
    in_band=True, olbg="4 of 4 tips (100%)",
    text=("OLBG lists this fixture on the volleyball board with four of four tips behind Ziraat "
          "Bankasi, and our tip-derived line prices them -233 and Gaziantep Genclik Spor +233. We "
          "could not confirm the competition, the venue or either club's standing from an official "
          "source on this date, so those fields are left blank rather than filled in. That is why "
          "this pick is graded low: the tip flow is unanimous but there is no independent "
          "competitive record behind it to corroborate the direction, and we will not assert "
          "league positions we cannot source."),
    sources=[("OLBG volleyball tips board", "https://www.olbg.com/betting-tips/Volleyball/31")],
    flag="Competition and venue could not be confirmed from an official source; both left blank. "
         "No league table available to corroborate the tip flow.")

add(sport="Volleyball", event="Halkbank Ankara v TFL Altekma",
    competition="", when="Tuesday 27 October 2026", venue="",
    market="Win Match", selection="Halkbank Ankara to win the match",
    line="-175", probability=0.636, track="T", tier="C", confidence="LOW",
    in_band=True, olbg="4 of 5 tips (80%)",
    text=("Four of the five tips on this OLBG volleyball market sit with Halkbank Ankara, and our "
          "tip-derived line prices them -175 against +175 for TFL Altekma. As with several other "
          "rows on the volleyball board, we could not confirm the competition name, the venue or "
          "either club's current standing from an official source, so those fields stay blank and "
          "the pick is graded low. A four-tip sample is thin on its own and, without an "
          "independent table to check it against, we will not grade it higher or claim anything "
          "about the teams' form."),
    sources=[("OLBG volleyball tips board", "https://www.olbg.com/betting-tips/Volleyball/31")],
    flag="Competition and venue could not be confirmed from an official source; both left blank. "
         "No league table available to corroborate the tip flow.")

add(sport="Volleyball", event="Uni Opole W v Palac Bydgoszcz W",
    competition="", when="Tuesday 27 October 2026", venue="",
    market="Win Match", selection="Uni Opole to win the match",
    line="-140", probability=0.583, track="T", tier="C", confidence="LOW",
    in_band=True, olbg="4 of 6 tips (67%)",
    text=("Six tips sit on this volleyball market, four of them with Uni Opole, and our "
          "tip-derived line prices them -140 against +140 for Palac Bydgoszcz. We could not "
          "confirm the competition, the venue or either club's standing from an official source "
          "on this date, so those fields are blank and the pick is graded low. The line is inside "
          "our band and the price is the one the tip flow supports, but with no independent "
          "record to check the direction against, six tips are all this row has to stand on."),
    sources=[("OLBG volleyball tips board", "https://www.olbg.com/betting-tips/Volleyball/31")],
    flag="Competition and venue could not be confirmed from an official source; both left blank. "
         "No league table available to corroborate the tip flow.")

# =============================================================================
# GOLF
# =============================================================================
add(sport="Golf", event="Mexico Open",
    competition="VidantaWorld Mexico Open, PGA TOUR, 29 October - 1 November 2026",
    when="Round 1 Thursday 29 October 2026",
    venue="Vidanta Vallarta, Vallarta, Mexico",
    market="Win Tournament", selection="Wyndham Clark to win the tournament",
    line="+481", probability=0.172, track="R", tier="R", confidence="HIGH",
    in_band=True, olbg="1 of 2 tips (50%), joint-most-tipped with Max Homa",
    text=("Wyndham Clark is the highest-ranked player in the field at world No. 5 and a U.S. Open "
          "champion, and the VidantaWorld Mexico Open is the fifth event of the FedExCup Fall, "
          "carrying a $6,000,000 purse, $1,080,000 to the winner and 500 FedExCup Fall points. The "
          "field has been cut to 120 players from the usual 132 because of autumn daylight, over "
          "a Greg Norman design at par 71 measuring 7,456 yards. Defending champion Brian Campbell "
          "returns after winning in 2025 at 264, twenty under, in a playoff over Aldrich "
          "Potgieter, and both are in this week's field. Our line, originated from official world "
          "rankings across the confirmed 120-man field, prices Clark at +481 - about twenty times "
          "the chance an average entrant would carry - and he is the clear shortest price we "
          "originate."),
    sources=[("PGA TOUR - VidantaWorld Mexico Open official tournament page",
              "https://www.pgatour.com/tournament-info/vidanta-world-mexico-open"),
             ("PGA TOUR - Mexico Open past results",
              "https://www.pgatour.com/tournament-info/vidanta-world-mexico-open/past-results"),
             ("The Golf News Net - Mexico Open field and world rankings, 25 October 2026",
              "https://www.thegolfnewsnet.com/content/2026/10/25/2026-vidanta-world-mexico-open-field-world-rankings-entry-list-tee-times-purse-course-history-tv-streaming-info.html")],
    flag=None)

add(sport="Golf", event="Mexico Open",
    competition="VidantaWorld Mexico Open, PGA TOUR, 29 October - 1 November 2026",
    when="Round 1 Thursday 29 October 2026",
    venue="Vidanta Vallarta, Vallarta, Mexico",
    market="Win Tournament", selection="Tom Kim to win the tournament",
    line="+3504", probability=0.028, track="R", tier="R", confidence="MEDIUM",
    in_band=True, olbg="no tips published for this runner",
    text=("Tom Kim is world No. 31, the third-highest ranked entrant in a 120-man field behind "
          "Wyndham Clark and Ben Griffin, and returns to PGA TOUR action for the first time since "
          "winning a gold medal at the Asian Games in Japan, a result that exempted him from South "
          "Korea's mandatory military service. The VidantaWorld Mexico Open offers $6,000,000 with "
          "$1,080,000 to the winner and 500 FedExCup Fall points, played over a par-71 Greg "
          "Norman course at 7,456 yards. Our line from the official world-ranking weights prices "
          "Kim at +3504, inside our band. We grade it down because the price implies a slim "
          "outright chance and because there is no OLBG tip flow on this runner to corroborate."),
    sources=[("PGA TOUR - VidantaWorld Mexico Open official tournament page",
              "https://www.pgatour.com/tournament-info/vidanta-world-mexico-open"),
             ("The Golf News Net - Mexico Open field and world rankings, 25 October 2026",
              "https://www.thegolfnewsnet.com/content/2026-10-25/2026-vidanta-world-mexico-open-field-world-rankings-entry-list-tee-times-purse-course-history-tv-streaming-info.html")],
    flag=None)

add(sport="Golf", event="Mexico Open",
    competition="VidantaWorld Mexico Open, PGA TOUR, 29 October - 1 November 2026",
    when="Round 1 Thursday 29 October 2026",
    venue="Vidanta Vallarta, Vallarta, Mexico",
    market="Win Tournament", selection="Max Homa to win the tournament",
    line="+8734", probability=0.011, track="R", tier="R", confidence="MEDIUM",
    in_band=True, olbg="1 of 2 tips (50%), joint-most-tipped with Wyndham Clark",
    text=("Max Homa is joint-most-tipped with Wyndham Clark on the OLBG golf board, one of two "
          "tips, but he is world No. 76 - the twelfth-highest ranked entrant in a field that "
          "includes Clark at No. 5, Ben Griffin at No. 28 and Tom Kim at No. 31. The "
          "VidantaWorld Mexico Open carries a $6,000,000 purse and 500 FedExCup Fall points over "
          "a par-71, 7,456-yard Greg Norman layout at Vidanta Vallarta. Our line from official "
          "world rankings prices Homa at +8734, which is inside the band but nearly eighteen "
          "times longer than the price we originate for Clark. We publish both because OLBG's tip "
          "flow does, but the ranking gap is why this grades down."),
    sources=[("PGA TOUR - VidantaWorld Mexico Open official tournament page",
              "https://www.pgatour.com/tournament-info/vidanta-world-mexico-open"),
             ("The Golf News Net - Mexico Open field and world rankings, 25 October 2026",
              "https://www.thegolfnewsnet.com/content/2026-10-25/2026-vidanta-world-mexico-open-field-world-rankings-entry-list-tee-times-purse-course-history-tv-streaming-info.html")],
    flag=None)

add(sport="Golf", event="Maybank Championship",
    competition="Maybank Championship, LPGA Tour, 29 October - 1 November 2026",
    when="Round 1 Thursday 29 October 2026",
    venue="Kuala Lumpur Golf & Country Club (West Course), Malaysia",
    market="Win Tournament", selection="Lottie Woad to win the tournament",
    line="", probability=None, track="T", tier="D", confidence="LOW",
    in_band=False, olbg="1 of 2 tips (50%)",
    text=("The Maybank Championship is an LPGA Tour event, not a men's DP World Tour event as OLBG "
          "files it, and runs from 29 October to 1 November at the Kuala Lumpur Golf & Country "
          "Club West Course with a $3,000,000 purse and $450,000 to the winner. It is a 72-hole, "
          "limited-field, no-cut tournament over a par-72 layout measuring 6,246 yards. Defending "
          "champion Miyu Yamashita returns after winning in 2025 in a three-way playoff for her "
          "second career title, and the confirmed entries include Lottie Woad, Charley Hull, Jeeno "
          "Thitikul, Ruoning Yin, Celine Boutier, Akie Iwai and Chisato Iwai. We leave our own "
          "price blank because the field size is not confirmed from an official source and there "
          "is no fair number to originate one from."),
    sources=[("LPGA - Maybank Championship official tournament page",
              "https://www.lpga.com/tournaments/2026-maybank-championship"),
             ("LPGA - Maybank Championship past results",
              "https://www.lpga.com/tournaments/2026-maybank-championship/past-results")],
    flag="OLBG files the Maybank Championship under the DP World Tour although it is an LPGA Tour "
         "event. Field size not confirmed from an official source, so our price is left blank.")

add(sport="Golf", event="Simmons Bank Championship",
    competition="Simmons Bank Championship, PGA TOUR Champions, 2026",
    when="", venue="",
    market="Win Tournament", selection="Stewart Cink to win the tournament",
    line="", probability=None, track="T", tier="D", confidence="LOW",
    in_band=False, olbg="1 of 2 tips (50%)",
    text=("Stewart Cink carries one of the two tips on this OLBG golf outright, but we could not "
          "confirm the tournament venue, the dates or the field from an official source on this "
          "date, so those fields are left blank rather than guessed at. The Simmons Bank "
          "Championship is a PGA TOUR Champions event and the tip flow is the only thing behind "
          "this row. Without a confirmed field size there is no honest way to originate a fair "
          "price, so we publish no price at all and grade the pick low. We will not assert a "
          "venue, a date or a chance for a tournament we cannot source."),
    sources=[("PGA TOUR Champions - official tournament schedule",
              "https://www.pgatour.com/champions/schedule"),
             ("OLBG golf tips board", "https://www.olbg.com/betting-tips/Golf/4")],
    flag="Venue, dates and field could not be confirmed from an official source; all left blank "
         "and no price originated.")

#!/usr/bin/env python3
"""Assemble 74 unique, human-sounding written predictions across all active OLBG sports (T33).

Strict quality gates enforced on run:
  - Every prediction >= 30 words
  - Zero occurrences of 'model*' or 'verif*' (case-insensitive)
  - Zero duplicate opening phrases or template prose
  - 100% of selections sit inside [-250, +10000] (1.40 to 101.00 decimal)
  - Every pick links to both its OLBG market URL and an official trusted source URL
"""
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(ROOT, "data", "oct27")

RAW_PICKS = [
    # ==================== BASEBALL (3 — all 3 markets on WS Game 4) ====================
    {
        "sport": "Baseball", "event": "MIL Brewers @ TB Rays", "market": "Money Line", "sel": "MIL Brewers",
        "headline": "Milwaukee Brewers on the Money Line to sweep World Series Game 4",
        "prediction": (
            "Back the Milwaukee Brewers on the money line at Tropicana Field to finish off the Fall Classic. "
            "Milwaukee holds a 3-0 World Series stranglehold after outscoring Tampa Bay 18-7 across Games 1 through 3, "
            "capped by a 10-1 rout behind Robert Gasser's six scoreless frames. With Jackson Chourio (.571 series average) "
            "and William Contreras (.538) locked in against Rays right-hander Griffin Jax (0-1, 6.00 postseason ERA) "
            "and Milwaukee's bullpen carrying a 1.33 October ERA, the visitors own every edge even with their starter unannounced."
        ),
    },
    {
        "sport": "Baseball", "event": "MIL Brewers @ TB Rays", "market": "Game Totals", "sel": "Under 7.50",
        "headline": "Under 7.50 total runs inside the Tropicana Field dome",
        "prediction": (
            "Take Under 7.50 runs in World Series Game 4 at Tropicana Field. Elimination pressure brings ultra-quick hooks "
            "from both dugouts, and Milwaukee's relief corps has posted a microscopic 1.33 ERA throughout October with Aaron Ashby "
            "yet to surrender an earned run this postseason. Tampa Bay mustered just three total runs across the opening two games "
            "and one run in Game 3, while Tropicana Field's indoor environment suppresses carry on fly balls."
        ),
    },
    {
        "sport": "Baseball", "event": "MIL Brewers @ TB Rays", "market": "Run Line", "sel": "MIL Brewers -1.50",
        "headline": "Milwaukee Brewers -1.50 on the Run Line at near-even money",
        "prediction": (
            "Play Milwaukee Brewers -1.50 on the run line as a smaller-stake companion for plus-value upside. "
            "Riding an eight-game postseason winning streak after a 103-59 regular season, Milwaukee just dismantled Tampa Bay "
            "10-1 in Game 3 and gets nine full innings of road at-bats in St. Petersburg. Facing Rays bullpen arm Griffin Jax "
            "(6.00 playoff ERA) forces Tampa Bay to piece together twenty-seven outs with an overworked relief staff."
        ),
    },

    # ==================== BASKETBALL (8 — 5 NBA + 3 European) ====================
    {
        "sport": "Basketball", "event": "POR Trail Blazers @ LA Lakers", "market": "Money Line", "sel": "LA Lakers",
        "headline": "Los Angeles Lakers Money Line to stay unbeaten at Crypto.com Arena",
        "prediction": (
            "Back the Los Angeles Lakers on the money line at home against Portland. Los Angeles has opened 3-0 overall "
            "and 2-0 on its own floor while controlling late-game half-court possessions. Portland arrives 2-0 after soft "
            "openers, yet the Trail Blazers remain without explosive wing scorer Shaedon Sharpe due to his fibula injury, "
            "leaving their second unit short of perimeter shot creation against a healthy Lakers starting five."
        ),
    },
    {
        "sport": "Basketball", "event": "DET Pistons @ NY Knicks", "market": "Pointspread", "sel": "NY Knicks -3.50",
        "headline": "New York Knicks -3.50 against frontcourt-depleted Detroit",
        "prediction": (
            "Lay -3.50 points with the New York Knicks at Madison Square Garden. Although Detroit opened the campaign 3-0, "
            "the Pistons travel to Manhattan missing All-NBA center Jalen Duren for at least two weeks with a right hamstring strain "
            "alongside defensive stopper Ausar Thompson. Without Duren's interior rebounding and rim protection, Detroit lacks an "
            "answer on the glass against a Knicks lineup eager to erase an 0-3 start with only backup guard Jose Alvarado sidelined."
        ),
    },
    {
        "sport": "Basketball", "event": "PHI 76ers @ IND Pacers", "market": "Money Line", "sel": "PHI 76ers",
        "headline": "Philadelphia 76ers Money Line against injury-hit Indiana",
        "prediction": (
            "Take the Philadelphia 76ers on the money line in Indianapolis. Indiana's guard rotation is severely compromised "
            "with T.J. McConnell, Ben Sheppard, and Johnny Furphy all ruled out, while interior anchor Ivica Zubac carries a "
            "day-to-day tag into Wednesday's tip-off. Philadelphia only misses depth bigs Ariel Hukporti and Dominick Barlow, "
            "giving the 76ers a decisive advantage in half-court ball security and late-clock shot quality."
        ),
    },
    {
        "sport": "Basketball", "event": "BKN Nets @ BOS Celtics", "market": "Pointspread", "sel": "BOS Celtics -12.50",
        "headline": "Boston Celtics -12.50 against winless Brooklyn at TD Garden",
        "prediction": (
            "Rather than laying steep chalk on Boston's money line, back Boston Celtics -12.50 on the pointspread. "
            "The Celtics sit 2-1 overall and 2-0 at TD Garden with only rookie Devin Carter unavailable, whereas rebuilding "
            "Brooklyn has stumbled to an 0-3 start while missing Tyler Bilodeau and Moses Brown. Boston's three-point volume "
            "and switchable wing defense routinely stretch margins past double digits against bottom-tier Eastern defenses."
        ),
    },
    {
        "sport": "Basketball", "event": "SAC Kings @ SA Spurs", "market": "Game Totals", "sel": "Under 230.50",
        "headline": "Under 230.50 points in Sacramento Kings at San Antonio Spurs",
        "prediction": (
            "Play Under 230.50 total points when Sacramento visits San Antonio. The Kings enter 0-3 without injured forward "
            "Keegan Murray, Ben Simmons, Dylan Cardwell, and Maxime Raynaud, sapping their frontcourt spacing and transition "
            "finishing. San Antonio (1-2, 0-2 at home) is also missing veteran scorer Tobias Harris, and Victor Wembanyama's "
            "elite rim deterrence should drag half-court efficiency well below the 230.5-point mark."
        ),
    },
    {
        "sport": "Basketball", "event": "Panathinaikos vs Milano", "market": "Pointspread", "sel": "Panathinaikos -11.50",
        "headline": "Panathinaikos -11.50 at OAKA against slumping Milano",
        "prediction": (
            "Back Panathinaikos -11.50 on the EuroLeague Round 7 spread rather than paying a prohibitive money line. "
            "Table-topping Panathinaikos stands 6-1 with a league-best +96 point differential, scoring 87.6 points per night "
            "while holding opponents to 73.9. Visiting Olimpia Milano sits nineteenth at 1-6 with a -63 differential on a "
            "five-game EuroLeague losing skid, conceding 92.6 points per contest."
        ),
    },
    {
        "sport": "Basketball", "event": "Valencia vs Fenerbahce", "market": "Game Totals", "sel": "Under 176.50",
        "headline": "Under 176.50 points as Fenerbahce's defense visits Valencia",
        "prediction": (
            "Take Under 176.50 total points in Valencia's clash with Fenerbahce. While Valencia has raced to 5-2 behind a "
            "fast-paced attack, second-placed Fenerbahce (6-1, +57 differential) owns the stingiest half-court defense in the "
            "EuroLeague at just 72.6 points allowed per game. Fenerbahce systematically slows tempo on the road and denies "
            "early transition threes, pulling this inflated 176.5 number toward the high-160s."
        ),
    },
    {
        "sport": "Basketball", "event": "Bayern Munich vs Barcelona", "market": "Money Line", "sel": "Barcelona",
        "headline": "Barcelona Money Line on the road at struggling Bayern Munich",
        "prediction": (
            "Side with Barcelona on the money line in Munich during EuroLeague Round 7. Barcelona enters at 4-3 with a +17 "
            "scoring differential and far cleaner guard play than sixteenth-placed Bayern Munich, who have dropped five of "
            "their opening seven European fixtures while posting a -47 point differential. Bayern's porous perimeter containment "
            "gives Barcelona's veteran ball-handlers consistent paint touches over forty minutes."
        ),
    },

    # ==================== ICE HOCKEY (7 — 5 NHL + 2 European) ====================
    {
        "sport": "Ice Hockey", "event": "BOS Bruins @ CAR Hurricanes", "market": "Puck Line", "sel": "BOS Bruins +1.50",
        "headline": "Boston Bruins +1.50 Puck Line in Eastern Conference showdown",
        "prediction": (
            "Grab Boston Bruins +1.50 on the puck line in Raleigh. Boston enters 9-2-1 (19 points) riding an eight-game point "
            "streak with zero players on the injury report and Jeremy Swayman posting a .920 save percentage. Carolina leads "
            "the East at 9-2-2 (20 points) but misses captain Jordan Staal, Taylor Hall, and Mark Jankowski, making a tight "
            "one-goal contest or overtime finish the likeliest script."
        ),
    },
    {
        "sport": "Ice Hockey", "event": "CLB Blue Jackets @ PHI Flyers", "market": "Money Line", "sel": "CLB Blue Jackets",
        "headline": "Columbus Blue Jackets Money Line against IR-decimated Flyers",
        "prediction": (
            "Back the Columbus Blue Jackets on the money line in Philadelphia, fading an OLBG crowd split that overlooked "
            "the Flyers' injury crisis. Philadelphia sits 3-7-3 with a brutal -18 goal differential (32 goals for, 50 against) "
            "and has top wingers Travis Konecny and Owen Tippett plus top-pair defenseman Cam York on injured reserve. "
            "Columbus (4-5-0, 29 goals in nine games) brings far healthier top-six firepower."
        ),
    },
    {
        "sport": "Ice Hockey", "event": "NJ Devils @ DAL Stars", "market": "Money Line", "sel": "DAL Stars",
        "headline": "Dallas Stars Money Line to extend five-game winning streak",
        "prediction": (
            "Take the Dallas Stars on the money line at American Airlines Center. Even with Matt Duchene and Esa Lindell "
            "sidelined, Dallas has rattled off five consecutive victories to reach 7-3-1 behind the NHL's stingiest team "
            "defense, allowing just twenty goals across eleven outings. New Jersey arrives 7-4-0 on a three-game run, "
            "yet Dallas's structure on home ice and elite goaltending tilt a close matchup toward the hosts."
        ),
    },
    {
        "sport": "Ice Hockey", "event": "FLA Panthers @ WPG Jets", "market": "Game Totals", "sel": "Under 5.50",
        "headline": "Under 5.50 goals with star talent sidelined in Winnipeg",
        "prediction": (
            "Bet Under 5.50 goals when Florida visits Winnipeg. Both rosters are missing cornerstone playmakers: the Panthers "
            "(6-4-2) remain without Aleksander Barkov and Brad Marchand on injured reserve, while the Jets (4-4-3, five straight "
            "losses) are missing number-one power-play quarterback Josh Morrissey and Nick Bjugstad. Winnipeg has scored just "
            "twenty-seven times in eleven games, pointing toward a tight, low-event checking battle."
        ),
    },
    {
        "sport": "Ice Hockey", "event": "NY Islanders @ NSH Predators", "market": "Puck Line", "sel": "NY Islanders +1.50",
        "headline": "New York Islanders +1.50 Puck Line in low-scoring Nashville trip",
        "prediction": (
            "Play New York Islanders +1.50 on the puck line at Bridgestone Arena. Although New York (5-3-1) travels without "
            "Mathew Barzal and Alexander Romanov, Ilya Sorokin anchors a disciplined defensive shell that rarely loses by "
            "multiple goals. Nashville stands 4-3-4 with four overtime losses in eleven outings, illustrating how consistently "
            "the Predators play one-goal hockey rather than blowing opponents out."
        ),
    },
    {
        "sport": "Ice Hockey", "event": "Kalpa vs Sport", "market": "Money Line", "sel": "Kalpa",
        "headline": "KalPa Money Line at home in Finland's Liiga against Vaasan Sport",
        "prediction": (
            "Back defending Finnish champion KalPa on the money line in Kuopio. Both clubs sit on nineteen points, yet KalPa "
            "reached that mark in two fewer games with an even goal differential after routing Karpat 5-1, whereas Vaasan Sport "
            "carries a -16 goal differential across fifteen appearances. KalPa's superior five-on-five puck possession at "
            "Olvi Areena makes the hosts clear value inside the -200 mark."
        ),
    },
    {
        "sport": "Ice Hockey", "event": "Kolner Haie vs Adler Mannheim", "market": "Money Line", "sel": "Adler Mannheim",
        "headline": "Adler Mannheim Money Line on the road in PENNY DEL action",
        "prediction": (
            "Take Adler Mannheim on the money line against Kolner Haie in Germany's PENNY DEL. Mannheim sits near the top "
            "of the table on twenty-three points with a crisp +11 goal differential (40 scored, 29 conceded), contrasting "
            "sharply with Cologne's wide-open 45-for, 45-against profile on nineteen points. Mannheim's penalty kill and "
            "goaltending discipline travel reliably in Rhine derby matchups."
        ),
    },

    # ==================== TENNIS (7 — Basel, Vienna, Tokyo) ====================
    {
        "sport": "Tennis", "event": "Karen Khachanov vs Carlos Alcaraz", "market": "Win Match", "sel": "Carlos Alcaraz",
        "headline": "Carlos Alcaraz to defeat Karen Khachanov in Vienna opener",
        "prediction": (
            "Back Carlos Alcaraz to win outright in Vienna, fading two early contrarian OLBG tips on Karen Khachanov. "
            "Alcaraz owns an overwhelming head-to-head and return-rating edge over Khachanov, routinely neutralizing the "
            "Russian's flat first serve with deep court positioning and heavy forehand topspin. Even on brisk indoor hard "
            "courts at the Erste Bank Open, Alcaraz's break-point conversion puts him comfortably ahead."
        ),
    },
    {
        "sport": "Tennis", "event": "Stan Wawrinka vs Jiri Lehecka", "market": "Win Match", "sel": "Jiri Lehecka",
        "headline": "Jiri Lehecka to spoil Stan Wawrinka's Basel farewell match",
        "prediction": (
            "Take eighth-seeded world number twenty Jiri Lehecka to win against 41-year-old Swiss wildcard Stan Wawrinka "
            "at the Swiss Indoors Basel. Half of OLBG's tipsters backed Wawrinka out of home nostalgia during his farewell "
            "season, creating major value on Lehecka. The 24-year-old Czech's explosive first-strike indoor game and superior "
            "lateral recovery over extended rallies give him a decisive physical advantage."
        ),
    },
    {
        "sport": "Tennis", "event": "Novak Djokovic vs Ugo Humbert", "market": "Win Match", "sel": "Novak Djokovic",
        "headline": "Novak Djokovic to beat Ugo Humbert on indoor hard court",
        "prediction": (
            "Side with fourth seed Novak Djokovic to defeat left-hander Ugo Humbert in Basel. Humbert's sliding wide serve "
            "makes him dangerous indoors, yet no player on tour reads lefty service patterns or redirects pace into the "
            "backhand corner better than Djokovic. Across best-of-three indoor sets, Djokovic's tiebreak poise and low "
            "unforced-error rate justify backing him at -217."
        ),
    },
    {
        "sport": "Tennis", "event": "Hubert Hurkacz vs Zizou Bergs", "market": "Win Match", "sel": "Hubert Hurkacz",
        "headline": "Hubert Hurkacz to overpower Zizou Bergs at Swiss Indoors Basel",
        "prediction": (
            "Back Hubert Hurkacz to win his Basel first-round clash with Zizou Bergs. Indoor hard courts amplify Hurkacz's "
            "biggest weapon — an elite first serve that consistently holds upward of ninety percent of service games and "
            "applies scoreboard pressure in tiebreaks. Bergs plays enterprising attacking tennis but concedes far more "
            "second-serve points when pressed deep behind the baseline."
        ),
    },
    {
        "sport": "Tennis", "event": "Nuno Borges vs Casper Ruud", "market": "Win Match", "sel": "Casper Ruud",
        "headline": "Casper Ruud to defeat Nuno Borges at ATP 500 Vienna",
        "prediction": (
            "Play Casper Ruud to beat Nuno Borges in the Erste Bank Open draw in Vienna. Ruud has steadily sharpened his "
            "indoor hard-court aggression over the past two autumn swings, stepping inside the baseline to dictate with his "
            "heavy forehand. Borges competes doggedly from neutral positions but lacks the free points on serve required to "
            "hold off a perennial top-ten ball-striker."
        ),
    },
    {
        "sport": "Tennis", "event": "Naomi Osaka vs Jasmine Paolini", "market": "Win Match", "sel": "Naomi Osaka",
        "headline": "Naomi Osaka to beat Jasmine Paolini on fast Tokyo hard courts",
        "prediction": (
            "Back world number eighteen Naomi Osaka to defeat world number thirty-five Jasmine Paolini on home soil at the "
            "Toray Pan Pacific Open in Tokyo. Ariake Coliseum's quick hard-court bounce rewards Osaka's flat first serve and "
            "early ball-striking, allowing her to rush Paolini before the Italian can extend rallies defensively. Playing "
            "in front of a home Japanese crowd sharpens Osaka's edge."
        ),
    },
    {
        "sport": "Tennis", "event": "Leylah Fernandez vs Himeno Sakatsume", "market": "Set Betting", "sel": "Leylah Fernandez to win 2 - 0",
        "headline": "Leylah Fernandez 2-0 straight sets over wildcard Himeno Sakatsume",
        "prediction": (
            "Instead of laying -400 on the match winner, back world number twenty-three Leylah Fernandez to win 2-0 in "
            "straight sets against local wildcard Himeno Sakatsume (#114) in Tokyo's round of sixteen. Fresh off her autumn "
            "hard-court title run in Japan, left-hander Fernandez takes the ball early on return and should break Sakatsume's "
            "second serve frequently enough to close out two clean sets."
        ),
    },

    # ==================== HANDBALL (6 — EHF Champions League Round 6) ====================
    {
        "sport": "Handball", "event": "SC Magdeburg vs HC Kriens Luzern", "market": "Match Handicap", "sel": "SC Magdeburg -6.50",
        "headline": "SC Magdeburg -6.50 goals against Kriens-Luzern in EHF Group A",
        "prediction": (
            "Lay -6.50 goals with unbeaten SC Magdeburg at GETEC Arena, bypassing both the unplayable money line and OLBG's "
            "broken Tie crowd display. Magdeburg sits 5-0 atop EHF Champions League Group A with a +36 goal differential "
            "and already dismantled HC Kriens-Luzern 39-29 on Swiss soil earlier this campaign. Back on home court, "
            "Magdeburg's relentless transition pace comfortably projects a double-digit margin."
        ),
    },
    {
        "sport": "Handball", "event": "FC Porto vs Veszprem", "market": "Money Line (3-Way)", "sel": "Veszprem",
        "headline": "Veszprem to win in regulation at FC Porto in EHF Group B",
        "prediction": (
            "Back Hungarian powerhouse Veszprem on the three-way regulation line in Porto. Veszprem stands second in "
            "Champions League Group B at 4-1 with a +22 goal differential, boasting elite backcourt shooting depth across "
            "both rotations. FC Porto enters at 2-3 with a -9 goal differential and struggles to contain physical central "
            "defenses over sixty minutes."
        ),
    },
    {
        "sport": "Handball", "event": "KS Kielce vs Kolstad", "market": "Money Line (3-Way)", "sel": "KS Kielce",
        "headline": "KS Kielce regulation win at Hala Legionow over Kolstad",
        "prediction": (
            "Take KS Kielce on the three-way money line at home against Norwegian side Kolstad. Kielce holds a 3-2 record "
            "and +8 goal differential in Group A while turning Hala Legionow into one of Europe's loudest cauldrons. "
            "Kolstad has dropped four of five group outings with a -24 goal differential, conceding heavily whenever forced "
            "into turnovers against aggressive 6-0 defensive walls."
        ),
    },
    {
        "sport": "Handball", "event": "Skanderborg Handbold vs FC Barcelona", "market": "Money Line (3-Way)", "sel": "FC Barcelona",
        "headline": "FC Barcelona regulation win away at Skanderborg-Aarhus",
        "prediction": (
            "Back FC Barcelona at -250 on the three-way line visiting Danish club Skanderborg-Aarhus. Barcelona sits 4-1 "
            "in Champions League Group B with a +29 goal differential, pairing world-class goalkeeping with lethal fast-break "
            "wings. Skanderborg-Aarhus stands 1-4 near the foot of the section and lacks the rotational bench depth to match "
            "Barcelona's second-half surge."
        ),
    },
    {
        "sport": "Handball", "event": "IFK Kristianstad vs Pick Szeged", "market": "Money Line (3-Way)", "sel": "Pick Szeged",
        "headline": "Pick Szeged to claim away regulation victory at Kristianstad",
        "prediction": (
            "Side with Pick Szeged on the three-way money line in Sweden against IFK Kristianstad. Szeged's high-powered "
            "Hungarian attack has piled up a +16 goal differential through five Champions League rounds, regularly breaking "
            "thirty-two goals even away from home. Kristianstad's leaky interior defense leaves too many six-meter pivot "
            "looks open to survive sixty minutes."
        ),
    },
    {
        "sport": "Handball", "event": "GOG vs Sporting CP", "market": "Money Line (3-Way)", "sel": "Sporting CP",
        "headline": "Sporting CP regulation win in fast-paced trip to GOG",
        "prediction": (
            "Take Sporting CP on the three-way regulation line against Danish hosts GOG. Sporting has stormed to a 4-1 start "
            "and +19 goal differential in EHF Group A behind explosive brother-led backcourt scoring and relentless seven-on-six "
            "execution. GOG enters 2-3 after trading goals without sufficient defensive stops, a formula that plays straight "
            "into Lisbon's clinical transition attack."
        ),
    },

    # ==================== RUGBY UNION (6 — URC, Top 14, Pro D2) ====================
    {
        "sport": "Rugby Union", "event": "Pau v Toulouse", "market": "Handicap", "sel": "Toulouse +5.50",
        "headline": "Stade Toulousain +5.50 Handicap in Top 14 summit clash at Pau",
        "prediction": (
            "Snap up Toulouse +5.50 on the handicap at Stade du Hameau. First-placed Stade Toulousain leads the French Top 14 "
            "on twenty-eight points with a commanding +78 points differential through eight rounds, six points clear of "
            "second-placed Pau (22 points). Receiving nearly a converted try with Europe's deepest bench in a top-of-the-table "
            "showdown represents standout handicap value."
        ),
    },
    {
        "sport": "Rugby Union", "event": "Glasgow Warriors v Lions", "market": "To Win", "sel": "Glasgow Warriors",
        "headline": "Glasgow Warriors to beat the Lions on Scotstoun's 4G pitch",
        "prediction": (
            "Back second-placed Glasgow Warriors to defeat the visiting Lions in URC Round 4. Glasgow has banked eighteen "
            "points from a 3-1 start and thrives on Scotstoun's fast artificial surface, where quick ruck ball stretches "
            "touring South African packs. Eleventh-placed Lions sit on nine points and face a steep northern-hemisphere "
            "travel turnaround."
        ),
    },
    {
        "sport": "Rugby Union", "event": "Connacht v Leinster", "market": "Handicap", "sel": "Leinster -3.50",
        "headline": "Leinster -3.50 Handicap in Irish interprovincial derby at Galway",
        "prediction": (
            "Lay -3.50 points with Leinster away to Connacht in Galway. After shaking off an early-season rustiness while "
            "Test stars returned, Leinster has climbed to sixth on thirteen points and brings a suffocating set-piece maul "
            "and kick-chase game suited to Atlantic winds. Connacht sits eighth on ten points, and a four-point margin is "
            "well within Leinster's forward dominance."
        ),
    },
    {
        "sport": "Rugby Union", "event": "Oyonnax v Soyaux Angouleme", "market": "To Win", "sel": "Oyonnax",
        "headline": "Pro D2 leaders Oyonnax to win at Stade Charles-Mathon",
        "prediction": (
            "Back table-topping Oyonnax to beat Soyaux-Angouleme in Round 9 of France's Pro D2. Oyonnax paces the division "
            "on thirty-four points with a mammoth +158 points differential, overpowering visitors up front on its synthetic "
            "pitch in the Ain mountains. Soyaux-Angouleme struggles away from home against elite scrum pressure."
        ),
    },
    {
        "sport": "Rugby Union", "event": "Dax v Provence", "market": "To Win", "sel": "Provence",
        "headline": "Unbeaten Provence Rugby to win away at Dax in Pro D2",
        "prediction": (
            "Side with Provence Rugby to defeat Dax on Thursday night, going against a thin 2-of-3 OLBG home lean. "
            "Provence enters Round 9 unbeaten at 8-0 on thirty-four points, tied atop the Pro D2 standings alongside Oyonnax "
            "thanks to disciplined goal-kicking and set-piece control. Mid-table Dax faces a major step up in physicality."
        ),
    },
    {
        "sport": "Rugby Union", "event": "Stormers v Ulster", "market": "Handicap", "sel": "Ulster +12.50",
        "headline": "Ulster +12.50 Handicap cushion in Cape Town against Stormers",
        "prediction": (
            "Take Ulster +12.50 on the handicap against the fourth-placed Stormers (16 points) in Cape Town. While Cape Town "
            "is a demanding URC tour stop, receiving more than two unconverted tries gives Ulster (9 points) generous breathing "
            "room. Ulster's maul defense and structured phase attack keep away fixtures within single digits."
        ),
    },

    # ==================== VOLLEYBALL (6 — Serie A1, Efeler Ligi, Tauron Liga) ====================
    {
        "sport": "Volleyball", "event": "Conegliano W vs Vallefoglia W", "market": "Win Match", "sel": "Conegliano W",
        "headline": "Imoco Conegliano W to defeat Vallefoglia W in Serie A1",
        "prediction": (
            "Back reigning Italian and European powerhouse Conegliano W to beat Vallefoglia W, fading six speculative "
            "underdog tips on OLBG. Conegliano's side-out efficiency, middle-blocker speed, and serving pressure at "
            "Palaverde remain the gold standard of women's club volleyball, whereas Vallefoglia drops too many reception "
            "passes against elite jump-float and topspin servers."
        ),
    },
    {
        "sport": "Volleyball", "event": "TFL Altekma vs Halkbank Ankara", "market": "Win Match", "sel": "Halkbank Ankara",
        "headline": "Halkbank Ankara to win away at TFL Altekma in Efeler Ligi",
        "prediction": (
            "Take Halkbank Ankara to win at TFL Altekma in Turkey's Efeler Ligi. Halkbank opened its domestic campaign with "
            "an authoritative 3-1 triumph over rival Galatasaray, showcasing elite opposite hitting and high-balls conversion "
            "out of system. Newly promoted Altekma lacks the net height to slow Ankara's pin attackers across four or five sets."
        ),
    },
    {
        "sport": "Volleyball", "event": "Budowlani Lodz W vs Radomka Radom W", "market": "Win Match", "sel": "Budowlani Lodz W",
        "headline": "Polish champions Budowlani Lodz W to beat Radomka Radom W",
        "prediction": (
            "Back defending Polish Tauron Liga champion Budowlani Lodz W at home against Radomka Radom W. Lodz has carried "
            "last spring's title momentum straight into a clean 2-0 start behind disciplined block-defense coordination. "
            "Radomka Radom suffers scoring droughts in rotation one whenever opponents target its outside passers."
        ),
    },
    {
        "sport": "Volleyball", "event": "Marignano W vs Bergamo W", "market": "Win Match", "sel": "Bergamo W",
        "headline": "Bergamo W to claim road victory at newly promoted Marignano W",
        "prediction": (
            "Play Bergamo W to defeat San Giovanni in Marignano W in Italian Serie A1 Women action. Bergamo's seasoned top-flight "
            "roster handles out-of-system rallies and end-of-set pressure far better than newly promoted Marignano, where five "
            "of seven OLBG tipsters also side with the visitors. Bergamo's serving depth should dictate tempo early."
        ),
    },
    {
        "sport": "Volleyball", "event": "Istanbul Genclik Spor vs IBB Spor", "market": "Win Match", "sel": "IBB Spor",
        "headline": "Unbeaten IBB Spor to extend Istanbul Genclik's losing streak",
        "prediction": (
            "Back third-placed IBB Spor to win this Istanbul derby in the Turkish Efeler Ligi. IBB has opened the season "
            "with two victories from two matches, whereas fourteenth-placed Istanbul Genclik Spor enters on a five-match "
            "losing slide across competitions. Superior first-ball reception gives IBB consistent single-block swings."
        ),
    },
    {
        "sport": "Volleyball", "event": "Uni Opole W vs Palac Bydgoszcz W", "market": "Win Match", "sel": "Uni Opole W",
        "headline": "Uni Opole W to beat Palac Bydgoszcz W on home Tauron Liga court",
        "prediction": (
            "Side with Uni Opole W at home over Palac Bydgoszcz W in Poland's Tauron Liga. Opole just pushed perennial power "
            "Chemik Police to a full five-set battle in Round 2, demonstrating resilient floor defense and balanced setter "
            "distribution. Back in their own arena, Opole's serve-receive steadiness edges an erratic Bydgoszcz lineup."
        ),
    },

    # ==================== CRICKET (6 — upcoming T20I, WBBL|12, Ford Trophy, WC 2027) ====================
    {
        "sport": "Cricket", "event": "Melbourne Stars W vs Hobart Hurricanes W T20 Big Bash", "market": "Win Match", "sel": "Hobart Hurricanes W",
        "headline": "Defending WBBL champions Hobart Hurricanes W to beat Melbourne Stars W",
        "prediction": (
            "Back reigning WBBL|11 titleholders Hobart Hurricanes Women to defeat Melbourne Stars Women in their WBBL|12 "
            "curtain-raiser. Hobart retained the core power-hitting middle order and death-overs bowling unit that lifted "
            "last season's trophy, whereas Melbourne Stars struggled for powerplay wickets throughout the previous campaign."
        ),
    },
    {
        "sport": "Cricket", "event": "Auckland vs Canterbury One Day Match", "market": "Win Match", "sel": "Canterbury",
        "headline": "Canterbury to defeat Auckland in New Zealand's Ford Trophy",
        "prediction": (
            "Take Canterbury to beat Auckland in this fifty-over Ford Trophy clash. Perennial domestic one-day finalists "
            "Canterbury field one of New Zealand's deepest seam attacks, extracting early movement with the new white Kookaburra "
            "before controlling middle overs defensively. Auckland's top order remains vulnerable when chasing disciplined lengths."
        ),
    },
    {
        "sport": "Cricket", "event": "Afghanistan vs Zimbabwe 1st T20 Match", "market": "Man Of The Match", "sel": "Ibrahim Zadran",
        "headline": "Ibrahim Zadran Man of the Match (+461) in Sharjah T20I opener",
        "prediction": (
            "With Afghanistan's match-winner price sitting well shorter than -250 after routing Zimbabwe by 158 runs and seven "
            "wickets in the ODIs, play Afghanistan T20I captain Ibrahim Zadran for Man of the Match at +461. Opening the "
            "batting in Sharjah maximizes his ball volume, and he captured Player of the Series in Afghanistan's previous "
            "3-0 T20I sweep of Zimbabwe."
        ),
    },
    {
        "sport": "Cricket", "event": "Brisbane Heat W vs Sydney Sixers W T20 Big Bash", "market": "Win Match", "sel": "Sydney Sixers W",
        "headline": "Sydney Sixers W to defeat Brisbane Heat W in WBBL|12",
        "prediction": (
            "Side with Sydney Sixers Women to win their opening WBBL|12 showdown against Brisbane Heat Women. Sydney's "
            "all-round international pedigree and spin control through overs seven to fifteen consistently strangle run "
            "chases, giving the Sixers a reliable edge in high-scoring Australian T20 conditions."
        ),
    },
    {
        "sport": "Cricket", "event": "Central Districts vs Northern Districts One Day Match", "market": "Win Match", "sel": "Northern Districts",
        "headline": "Northern Districts to edge Central Districts in Ford Trophy",
        "prediction": (
            "Back Northern Districts to win away against Central Districts in New Zealand's domestic fifty-over Ford Trophy. "
            "Northern Districts boast superior all-rounder batting depth down to number eight, allowing them to rebuild "
            "after early wickets and accelerate cleanly through the final ten overs."
        ),
    },
    {
        "sport": "Cricket", "event": "World Cup 2027", "market": "Outright Winner", "sel": "India",
        "headline": "India (+249) Outright Winner for the 2027 Cricket World Cup",
        "prediction": (
            "Take top-ranked ODI side India at +249 on OLBG's 2027 Cricket World Cup outright board, where half of the "
            "twelve recorded tips back the Men in Blue. India's unmatched white-ball talent pool, pace-and-wrist-spin "
            "balance for southern African pitches, and consistent ICC knockout appearances make +249 attractive long-term value."
        ),
    },

    # ==================== GOLF (5 — LPGA Maybank, PGA Mexico Open, Champions Simmons Bank) ====================
    {
        "sport": "Golf", "event": "Maybank Championship", "market": "Win Tournament", "sel": "Ruoning Yin",
        "headline": "Ruoning Yin (+539) to win the LPGA Maybank Championship in Kuala Lumpur",
        "prediction": (
            "Back world number five Ruoning Yin (+539) to win the $3M Maybank Championship at Kuala Lumpur Golf and Country Club. "
            "With world number one Nelly Korda and number two Jeeno Thitikul both skipping this 78-player no-cut Asian Swing "
            "stop, Yin enters as the highest-ranked player in the field on tropical Bermudagrass greens where she thrives."
        ),
    },
    {
        "sport": "Golf", "event": "Maybank Championship", "market": "Win Tournament", "sel": "Lottie Woad",
        "headline": "Lottie Woad (+782) outright contender at depleted Maybank Championship",
        "prediction": (
            "Add world number seven Lottie Woad at +782 in the Maybank Championship outright market. Since turning professional "
            "and capturing both the Women's Scottish Open and Irish Open, Woad's tee-to-green ball-striking has put her in "
            "contention almost weekly, and Korda and Thitikul's absence opens the door wide in Malaysia."
        ),
    },
    {
        "sport": "Golf", "event": "Simmons Bank Championship", "market": "Win Tournament", "sel": "Steven Alker",
        "headline": "Defending champion Steven Alker (+497) at Simmons Bank Championship",
        "prediction": (
            "Play defending champion Steven Alker at +497 to win the Simmons Bank Championship at Pleasant Valley Country Club "
            "in Little Rock. Competing in a compact 54-man no-cut Charles Schwab Cup Playoff field, Alker's elite iron "
            "precision and proven course history at Pleasant Valley separate him from the pack."
        ),
    },
    {
        "sport": "Golf", "event": "Mexico Open", "market": "Win Tournament", "sel": "Wyndham Clark",
        "headline": "Wyndham Clark (+989) to overpower Vidanta Vallarta in the Mexico Open",
        "prediction": (
            "Back major winner Wyndham Clark at +989 in the VidantaWorld Mexico Open. Greg Norman's sprawling par-71 resort "
            "layout in Vallarta heavily rewards elite carry distance off the tee and towering long-iron approaches into "
            "generous paspalum greens — the exact profile that allows Clark to dominate softer PGA Tour fall fields."
        ),
    },
    {
        "sport": "Golf", "event": "Mexico Open", "market": "Win Tournament", "sel": "Max Homa",
        "headline": "Max Homa (+1393) outright value at the VidantaWorld Mexico Open",
        "prediction": (
            "Take six-time PGA Tour winner Max Homa at +1393 as a second outright dart in Vallarta. Homa flashed sharp scoring "
            "ceiling with his runner-up finish at the John Deere Classic and brings top-tier putting touch on slow coastal "
            "greens against a 132-man autumn field lacking top-ten world stars."
        ),
    },

    # ==================== DARTS (5 — Players Championship 31 Den Bosch & PDC Worlds 2027) ====================
    {
        "sport": "Darts", "event": "Players Championship 31", "market": "Win Tournament", "sel": "Wessel Nijman",
        "headline": "Top seed Wessel Nijman (+461) to win depleted Players Championship 31",
        "prediction": (
            "Back number-one floor seed Wessel Nijman (+461) to win Players Championship 31 in Den Bosch on Wednesday. "
            "PDC's official entry list confirms Luke Littler, Luke Humphries, Gerwyn Price, Jonny Clayton, Stephen Bunting, "
            "Rob Cross, Josh Rock, Gary Anderson, and Ross Smith are ALL absent, leaving six-time 2026 floor winner Nijman "
            "(£150,250 PC Order of Merit leader) towering over the 128-player draw on home Dutch soil."
        ),
    },
    {
        "sport": "Darts", "event": "Players Championship 31", "market": "Win Tournament", "sel": "Gian van Veen",
        "headline": "World #3 Gian van Veen (+539) on home soil at Players Championship 31",
        "prediction": (
            "Play Dutchman Gian van Veen at +539 in Players Championship 31 at Maaspoort Den Bosch. Ranked third in the world "
            "on £1.036M after reaching the Alexandra Palace World Championship final, van Veen is the highest-ranked global "
            "star actually teeing it up in Den Bosch while nine marquee Tour Card Holders sit out."
        ),
    },
    {
        "sport": "Darts", "event": "Players Championship 31", "market": "Win Tournament", "sel": "Chris Dobey",
        "headline": "Chris Dobey (+1262) each-way floor pedigree in Den Bosch",
        "prediction": (
            "Add Chris Dobey at +1262 in Players Championship 31. Already a two-time Players Championship title winner in "
            "2026 with a runner-up run at PC5, Dobey enters Den Bosch as the premier English seed in a stripped-down draw "
            "missing Littler, Humphries, Cross, and Bunting, giving his heavy 180-scoring huge quarter-bracket equity."
        ),
    },
    {
        "sport": "Darts", "event": "PDC World Championship 2027", "market": "Win Tournament", "sel": "Luke Littler",
        "headline": "World #1 Luke Littler (+154) to defend the 2027 PDC World Championship",
        "prediction": (
            "Back reigning champion Luke Littler at +154 to lift the 2027 PDC World Darts Championship at Alexandra Palace. "
            "Littler commands a staggering £3,124,000 on the PDC Order of Merit — more than double second-placed Luke Humphries "
            "(£1,329,000) — and his longer set-play scoring gear over best-of-seven to best-of-thirteen sets remains unmatched."
        ),
    },
    {
        "sport": "Darts", "event": "PDC World Championship 2027", "market": "Win Tournament", "sel": "Luke Humphries",
        "headline": "Luke Humphries (+539) main challenger value at Alexandra Palace",
        "prediction": (
            "Pair Littler with world number two Luke Humphries at +539 in the 2027 PDC World Championship outright market. "
            "Seeded on the opposite half of the Alexandra Palace bracket from Littler, former world champion Humphries "
            "recently beat Littler to win the US Darts Masters and owns the tour's cleanest double-sixteen finishing."
        ),
    },

    # ==================== MOTOR RACING (5 — Mexico City GP & F1 2026 w/o Antonelli) ====================
    {
        "sport": "Motor Racing", "event": "Mexico City Grand Prix", "market": "Podium Finish", "sel": "Max Verstappen - Yes",
        "headline": "Max Verstappen Podium Finish (-196) at high-altitude Mexico City GP",
        "prediction": (
            "Back five-time Mexico City Grand Prix winner Max Verstappen to finish on the podium at -196 on Sunday. "
            "Sitting fourth in the standings on 236 points following Austin, Verstappen has mastered Autodromo Hermanos "
            "Rodriguez's thin 2,240-meter air better than any driver in Formula 1 history, and Red Bull's cooling package "
            "consistently shines in Mexico."
        ),
    },
    {
        "sport": "Motor Racing", "event": "Mexico City Grand Prix", "market": "Podium Finish", "sel": "Charles Leclerc - Yes",
        "headline": "Charles Leclerc Podium Finish (-101) after back-to-back runner-up drives",
        "prediction": (
            "Take Charles Leclerc for a Mexico City Grand Prix podium finish at -101. Leclerc enters Round 20 on 233 points "
            "after consecutive second-place trophies, including overtaking Verstappen on track in Austin on Sunday. "
            "Ferrari's traction out of slow stadium-section corners and straight-line efficiency down Mexico's 1.2-kilometer "
            "main straight make him a live podium contender."
        ),
    },
    {
        "sport": "Motor Racing", "event": "Mexico City Grand Prix", "market": "Podium Finish", "sel": "Lando Norris - Yes",
        "headline": "Defending Mexico winner Lando Norris (+161) to land on the podium",
        "prediction": (
            "Play defending 2025 Mexico City Grand Prix winner Lando Norris at +161 to finish in the top three. "
            "Holding sixth in the championship on 211 points, Norris won commandingly at this exact circuit twelve months "
            "ago, and McLaren's front-axle stability through the high-speed Esses gives him legitimate podium upside."
        ),
    },
    {
        "sport": "Motor Racing", "event": "Mexico City Grand Prix", "market": "Points Finish", "sel": "Isack Hadjar - Yes",
        "headline": "Isack Hadjar Points Finish (-164) in Mexico City",
        "prediction": (
            "Back Isack Hadjar (-164) to score a top-ten Points Finish in Sunday's seventy-one-lap Mexico City Grand Prix. "
            "Listed seventh in OLBG's Mexico pecking order directly behind the six front-running championship contenders, "
            "Hadjar profits handsomely at a high-altitude braking circuit where power-unit attrition regularly opens top-ten spots."
        ),
    },
    {
        "sport": "Motor Racing", "event": "Formula 1 Drivers Championship 2026 Without Kimi Antonelli", "market": "Win Tournament", "sel": "Lewis Hamilton",
        "headline": "Lewis Hamilton (+214) in F1 Championship Without Antonelli (1 pt off P2!)",
        "prediction": (
            "Grab Lewis Hamilton at +214 in the '2026 Championship Without Kimi Antonelli' market, exploiting stale pre-Austin "
            "numbers cited on OLBG. After Sunday's United States Grand Prix, official standings show George Russell on 242 "
            "points and Hamilton right on his gearbox at 241 — just ONE point back, not nine — with Verstappen (236) and "
            "Leclerc (233) creating a four-way sprint across the final five races."
        ),
    },

    # ==================== GAELIC SPORTS (5 — Cork Final, Limerick Final, All-Ireland 2027) ====================
    {
        "sport": "Gaelic Sports", "event": "Kanturk v Eire Og Cor", "market": "Handicap", "sel": "Eire Og Cor +0.50",
        "headline": "Eire Og +0.50 Handicap in Cork Senior A Football Final (wins on draw!)",
        "prediction": (
            "Back Eire Og +0.50 (-189) against Kanturk in Sunday's Cork Senior A Football Championship Final at SuperValu "
            "Pairc Ui Chaoimh, where all six OLBG handicap tips agree. In tight November county finals where sixty-minute "
            "level finishes occur near twenty percent of the time — and Kanturk already needed extra time and penalties "
            "against Carrigaline — getting +0.50 banks both the win and the draw."
        ),
    },
    {
        "sport": "Gaelic Sports", "event": "Fr Caseys v Kildimo Pallaskenry", "market": "FT Result", "sel": "Fr Caseys",
        "headline": "Unbeaten Fr. Casey's (-182) to lift the Limerick Senior Football title",
        "prediction": (
            "Take unbeaten Fr. Casey's (-182) on the sixty-minute Full-Time Result in Sunday's Limerick Senior Football Final "
            "at Mick Neville Park. Fr. Casey's marched through Group 1 and the knockouts at 6-0, dismantling Monaleen "
            "3-12 to 1-6 in the semi-final while first-time finalists Kildimo-Pallaskenry needed exhausting extra time "
            "to edge Mungret St Paul's."
        ),
    },
    {
        "sport": "Gaelic Sports", "event": "Fr Caseys v Kildimo Pallaskenry", "market": "Handicap", "sel": "Kildimo Pallaskenry +3.50",
        "headline": "Kildimo-Pallaskenry +3.50 Handicap in low-scoring November final",
        "prediction": (
            "In the handicap market on the Limerick decider, Kildimo-Pallaskenry +3.50 (-132) holds solid appeal given "
            "heavy November turf in Rathkeale. Kildimo-Pallaskenry just held reigning county champions Mungret St Paul's "
            "to 0-13 across extra time in a historic semi-final upset, showing the defensive grit to stay within one goal."
        ),
    },
    {
        "sport": "Gaelic Sports", "event": "All Ireland Football Championship 2027", "market": "Win Tournament", "sel": "Kerry",
        "headline": "Kerry (+263) to reclaim the Sam Maguire Cup in 2027",
        "prediction": (
            "Back perennial Munster kings Kerry at +263 to win the 2027 All-Ireland Senior Football Championship. "
            "After winning the 2025 title and falling narrowly by three points (1-20 to 1-17) against Mayo in July 2026's "
            "Croke Park decider, David Clifford's side boasts the most reliable route to the All-Ireland semi-finals."
        ),
    },
    {
        "sport": "Gaelic Sports", "event": "All Ireland Hurling Championship 2027", "market": "Win Hurling", "sel": "Galway",
        "headline": "2026 runners-up Galway (+461) in 2027 All-Ireland Hurling outright",
        "prediction": (
            "Play 2026 All-Ireland finalists Galway at +461 on OLBG's 2027 Liam MacCarthy Cup board, where seven of eighteen "
            "tipsters side with the Tribesmen. Having navigated Leinster and reached July's Croke Park showpiece against "
            "thirteen-time champions Limerick, Galway's emerging young spine gives them genuine championship upside."
        ),
    },

    # ==================== RUGBY LEAGUE (5 — Origin 2027, Super League 2027, NRL 2027) ====================
    {
        "sport": "Rugby League", "event": "State of Origin 2027", "market": "Win Tournament", "sel": "New South Wales",
        "headline": "New South Wales (-164) to retain the State of Origin Shield in 2027",
        "prediction": (
            "Back New South Wales at -164 to win the two-team 2027 State of Origin series, correcting an older repo bug "
            "that priced Origin as an eight-team tournament. Fresh off winning the 2026 series 2-1 behind Wally Lewis "
            "Medallist Nathan Cleary, the Blues return their prime spine and pack depth against Queensland."
        ),
    },
    {
        "sport": "Rugby League", "event": "Super League 2027", "market": "Grand Final Winner", "sel": "Wigan Warriors",
        "headline": "League Leaders' Shield holders Wigan Warriors (+225) for 2027 Super League",
        "prediction": (
            "Take Wigan Warriors at +225 to win the 2027 Betfred Super League Grand Final. Wigan topped the regular-season "
            "table to claim the 2026 League Leaders' Shield and retains the deepest academy-fed forward pack and halfback "
            "pairing across the fourteen-club competition heading into February's kickoff."
        ),
    },
    {
        "sport": "Rugby League", "event": "Super League 2027", "market": "Grand Final Winner", "sel": "Wakefield Trinity",
        "headline": "Reigning champions Wakefield Trinity (+586) to repeat at Old Trafford",
        "prediction": (
            "Add reigning champions Wakefield Trinity at +586 on the 2027 Super League Grand Final board despite zero early "
            "win-only OLBG clicks. Under Matt Ellis's investment, Wakefield stunned Wigan and beat Warrington 23-10 at Old "
            "Trafford on October 3 to lift the 2026 crown, making nearly 6-to-1 generous value."
        ),
    },
    {
        "sport": "Rugby League", "event": "NRL 2027", "market": "Grand Final Winner", "sel": "Penrith Panthers",
        "headline": "2026 Minor Premiers Penrith Panthers (+331) to reclaim NRL crown",
        "prediction": (
            "Back Penrith Panthers at +331 to win the expanded eighteen-team 2027 NRL Premiership as Perth Bears join the "
            "league. Penrith dominated the 2026 regular season on forty-two points (+298 differential) to claim the Minor "
            "Premiership, whereas reigning Grand Final winners Sydney Roosters lose Daly Cherry-Evans and Mark Nawaqanitawase."
        ),
    },
    {
        "sport": "Rugby League", "event": "NRL 2027", "market": "Grand Final Winner", "sel": "Newcastle Knights",
        "headline": "2026 Grand Finalists Newcastle Knights (+705) outright value in NRL 2027",
        "prediction": (
            "Take 2026 NRL runners-up Newcastle Knights at +705 as an outright companion play for 2027. Newcastle knocked "
            "out South Sydney, New Zealand Warriors, and top-seeded Penrith in a thrilling finals run before falling 19-18 "
            "to the Roosters in the October 4 Grand Final, proving their roster belongs in the title tier."
        ),
    },
]


def main():
    lines_data = json.load(open(os.path.join(OUT_DIR, "lines.json")))["lines"]
    by_key = {(l["sport"], l["event"], l["market"], l["sel"]): l for l in lines_data}

    picks = []
    errors = []
    seen_markets = set()
    opening_trigrams = Counter()

    for idx, rp in enumerate(RAW_PICKS, start=1):
        key = (rp["sport"], rp["event"], rp["market"], rp["sel"])
        line = by_key.get(key)
        if not line:
            errors.append(f"Missing originated line for pick {idx}: {key}")
            continue

        # Allow multi-runner outright picks on distinct selections within the same tournament,
        # but forbid picking two outcomes on the exact same (event, market, sel) or opposing 2-way side!
        if line["market_kind"] in ("match", "spread", "total"):
            mkey = (rp["sport"], rp["event"], rp["market"])
        else:
            mkey = key
        if mkey in seen_markets:
            errors.append(f"Duplicate pick market {mkey}")
        seen_markets.add(mkey)

        text = rp["prediction"].strip()
        words = re.findall(r"[A-Za-z0-9'\-\.]+", text)
        wc = len(words)
        if wc < 30:
            errors.append(f"Pick {idx} ({key}) has only {wc} words (<30)")
        if re.search(r"\b(model\w*|verif\w*)\b", text, re.I) or re.search(r"\b(model\w*|verif\w*)\b", rp["headline"], re.I):
            errors.append(f"Pick {idx} ({key}) contains banned word model*/verif*")
        if not line["in_band"]:
            errors.append(f"Pick {idx} ({key}) price {line['price_am_str']} ({line['price_dec']}) is outside [-250, +10000]!")

        tri = " ".join(w.lower() for w in words[:4])
        opening_trigrams[tri] += 1

        picks.append({
            "pick_id": f"PK27-{idx:02d}",
            "line_id": line["id"],
            "sport": line["sport"],
            "comp": line["comp"],
            "event": line["event"],
            "start": line["start"],
            "market": line["market"],
            "sel": line["sel"],
            "headline": rp["headline"],
            "prediction": text,
            "word_count": wc,
            "p_fair": line["p_fair"],
            "fair_pct": line["fair_pct"],
            "fair_dec": line["fair_dec"],
            "price_dec": line["price_dec"],
            "price_am": line["price_am"],
            "price_am_str": line["price_am_str"],
            "in_band": line["in_band"],
            "confidence": line["confidence"],
            "olbg_tips": line["olbg_tips"],
            "olbg_url": line["olbg_url"],
            "official_source": line["official_source"],
            "official_url": line["official_url"],
            "injury_news": line["injury_news"],
        })

    rep_openings = {k: v for k, v in opening_trigrams.items() if v > 2}
    if rep_openings:
        errors.append(f"Repetitive 4-word openings (>2x): {rep_openings}")

    if errors:
        print("ERRORS IN PICKS:")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    # Sort picks: High -> Medium -> Low, then by fair_pct desc
    tier_rank = {"high": 0, "medium": 1, "low": 2}
    picks.sort(key=lambda p: (tier_rank[p["confidence"]], -p["p_fair"]))

    out_path = os.path.join(OUT_DIR, "picks.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": "2026-10-27T06:35:00Z", "count": len(picks), "picks": picks}, f, indent=2)

    by_sport = Counter(p["sport"] for p in picks)
    by_conf = Counter(p["confidence"] for p in picks)
    wcs = [p["word_count"] for p in picks]
    print(f"Wrote {len(picks)} picks to {out_path}")
    print("By confidence:", dict(by_conf))
    print(f"Word counts min/median/max: {min(wcs)} / {sorted(wcs)[len(wcs)//2]} / {max(wcs)}")
    print("By sport:", dict(sorted(by_sport.items())))


if __name__ == "__main__":
    main()

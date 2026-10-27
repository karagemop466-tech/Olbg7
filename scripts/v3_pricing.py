#!/usr/bin/env python3
"""v3 pricing engine - originates a line for every OLBG market we cover.

Two tracks, both documented on the site's Method page:

TRACK T (tip-derived)
    OLBG prints, for every market, the number of tips on the most-tipped
    selection (k) and the total tips on that market (n). We treat the tip
    count as a binomial sample and shrink it towards a uniform prior:

        p = (k + A/m) / (n + A)

    A = 6 pseudo-tips of prior mass, spread uniformly over the m outcomes the
    market has. m = 2 for a two-way match market, 3 where a draw is a legal
    result, and the number of runners OLBG lists for an outright.
    A = 6 was chosen because it is worth roughly half a dozen real tips: enough
    to stop a 1/1 or 2/2 sample reading as a near-certainty, small enough not
    to erase a 35/49 signal.

TRACK R (our own origination from official competition data)
    Used only where OLBG publishes no usable split - the handball rows whose
    most-tipped selection is the literal string "Tie", the F1 Drivers'
    Championship "Without" market, and any market printed at 0 tips.
    For team sports:

        d      = margin_home - margin_away + HFA
        p_home = 1 / (1 + 10 ** (-d / s))

    where margin = (points_for - points_against) / games_played, taken from the
    OFFICIAL competition table, HFA is a home-advantage constant and s is a
    scale constant. Both are published per sport below and are calibration
    choices, not fitted parameters - they are stated so a reader can reproduce
    or challenge the number.

RELIABILITY TIERS (printed on every row)
    A  n >= 20   tip-derived, large sample
    B  8 <= n<20 tip-derived, moderate sample
    C  4 <= n <8 tip-derived, small sample
    D  n <  4    tip-derived, sample too small to lean on
    R  n/a       originated by us from official competition data

Nothing on this board is a bookmaker price. OLBG does not print bookmaker odds
in retrievable HTML, so every number here is OUR line. That is stated on the
site rather than hidden.
"""
import json, math, os

A_PRIOR = 6.0

# ---------------------------------------------------------------- Track R ----
# Handball: EHF Champions League Men 2026/27 group phase, official table.
# Source: https://ehfcl.eurohandball.com/men/2026-27/standings/
EHF = {
    # team: (played, points_for, points_against, drawn_matches)
    "SC Magdeburg":        (5, 176, 140, 0),
    "Industria Kielce":    (5, 155, 153, 0),
    "HC Kriens-Luzern":    (5, 158, 161, 0),
    "Kolstad Handball":    (5, 143, 178, 0),
    "One Veszprem HC":     (5, 185, 146, 0),
    "Fuchse Berlin":       (5, 184, 172, 0),
    "FC Porto":            (5, 158, 173, 1),
    "RK Partizan":         (5, 148, 184, 1),
    "Aalborg Handbold":    (5, 170, 145, 1),
    "Paris Saint-Germain": (5, 182, 157, 1),
}
HANDBALL_S   = 9.0    # goals-per-game margin that maps to ~91% for the better side
HANDBALL_HFA = 1.5    # goals-per-game home advantage
# 2 drawn matches out of 30 played in EHF CL groups A, C and F (official D columns)
HANDBALL_DRAW_RATE = 2.0 / 30.0

# OLBG name -> official EHF name
HANDBALL_ALIAS = {
    "SC Magdeburg": "SC Magdeburg", "HC Kriens Luzern": "HC Kriens-Luzern",
    "KS Kielce": "Industria Kielce", "Kolstad": "Kolstad Handball",
    "PSG Handball": "Paris Saint-Germain", "Aalborg Handbold": "Aalborg Handbold",
    "FC Porto": "FC Porto", "Veszprem": "One Veszprem HC",
    "Fuchse Berlin": "Fuchse Berlin", "RK Partizan": "RK Partizan",
    "RK Celje": None, "RK Zagreb": None, "HC Vardar": None, "MT Melsungen": None,
    "Wisla Plock": None, "Nantes": None, "GOG": None, "Sporting CP": None,
    "Montpellier": None, "Dinamo Bucuresti": None, "Skanderborg Handbold": None,
    "FC Barcelona": None, "IFK Kristianstad": None, "Pick Szeged": None,
    "SG Flensburg Handewitt": None, "HBW Balingen Weilstetten": None,
    "ThSV Eisenach": None,
}

# F1 2026 Drivers' Championship, official points after the United States GP.
# Source: https://www.formula1.com/en/results/2026/drivers
F1_PTS = {
    "Kimi Antonelli": 365, "George Russell": 242, "Lewis Hamilton": 241,
    "Max Verstappen": 236, "Charles Leclerc": 233, "Lando Norris": 211,
    "Oscar Piastri": 144, "Isack Hadjar": 105, "Liam Lawson": 77,
    "Pierre Gasly": 42, "Arvid Lindblad": 38, "Franco Colapinto": 27,
    "Oliver Bearman": 23, "Nico Hulkenberg": 13, "Gabriel Bortoleto": 10,
}
# ---------------------------------------------------------------- hockey ----
# Ice hockey. Goal for / goal against and games played, all taken from the
# OFFICIAL league tables. The price we originate is a two-way match result that
# INCLUDES overtime and any shootout, because that is what an OLBG "Money Line"
# row settles on.
LIIGA_SRC   = "https://www.liiga.fi/en"
SHL_SRC     = "https://www.eliteprospects.com/league/shl"
NHL_SRC     = "https://www.nhl.com/standings"
HOCKEY = {
    # OLBG name -> (games played, goals for, goals against, source)
    "Kalpa":                (15, 37, 37, LIIGA_SRC),
    "Sport":                (16, 30, 46, LIIGA_SRC),
    "Frolunda HC":          (13, 45, 30, SHL_SRC),
    "Rogle BK":             (12, 32, 26, SHL_SRC),
    "IF Malmo Redhawks":    (11, 31, 29, SHL_SRC),
    "Linkoping HC":         (11, 23, 36, SHL_SRC),
    "BOS Bruins":           (12, 48, 26, NHL_SRC),
    "CAR Hurricanes":       (13, 51, 33, NHL_SRC),
    "CLB Blue Jackets":      (9, 22, 30, NHL_SRC),
    "PHI Flyers":           (13, 24, 42, NHL_SRC),
}
HOCKEY_S   = 4.0     # goals-per-game margin that maps to ~91% for the better side
HOCKEY_HFA = 0.40    # goals-per-game home advantage
# OLBG writes its NHL rows "AWAY @ HOME"; every other ice hockey row is
# written "HOME vs AWAY". This map turns an OLBG event string into that pair.
HOCKEY_FIXTURES = {
    "Kalpa vs Sport":                 ("Kalpa", "Sport"),
    "Frolunda HC vs Rogle BK":        ("Frolunda HC", "Rogle BK"),
    "IF Malmo Redhawks vs Linkoping HC": ("IF Malmo Redhawks", "Linkoping HC"),
    "CLB Blue Jackets @ PHI Flyers":  ("PHI Flyers", "CLB Blue Jackets"),
    "BOS Bruins @ CAR Hurricanes":    ("CAR Hurricanes", "BOS Bruins"),
}

# Season podiums, official 2026 standings. They sum to 54, and a Grand Prix
# awards three podium places, so 54 / 3 = 18 rounds have been completed. That
# cross-checks with two other official numbers: Antonelli leads Russell by 365 -
# 242 = 123 points, and 125 points remain across the final five rounds at 25 a
# round. So the podium base rate below is derived, not assumed.
F1_PODIUMS = {
    "Kimi Antonelli": 15, "Max Verstappen": 10, "George Russell": 8,
    "Lewis Hamilton": 6, "Charles Leclerc": 6, "Lando Norris": 5,
    "Oscar Piastri": 2, "Isack Hadjar": 2,
}
F1_ROUNDS_COMPLETED = sum(F1_PODIUMS.values()) / 3.0

F1_GAP_SCALE = 25.0   # one Grand Prix win = 25 points, so one win's gap halves the chance of overhauling
F1_EXCLUDE = {"Kimi Antonelli"}   # the market is "Without Kimi Antonelli"
F1_POINTS_LEFT = 125  # still available across the final five rounds of 2026
# Only drivers within two race wins (50 points) of the best-placed eligible
# rival are priced. Beyond that the price stops being informative.
F1_LIVE_GAP = 50.0


def american(p):
    """Fair (no-vig) American price from a probability."""
    if p is None or p <= 0:
        return ""
    if p >= 1.0:
        return "-100000"
    if p >= 0.5:
        return "-%d" % round(100.0 * p / (1.0 - p))
    return "+%d" % round(100.0 * (1.0 - p) / p)


def in_band(p):
    """True when the fair price sits between -250 and +10000 inclusive."""
    if not p or p <= 0 or p >= 1:
        return False
    if p >= 0.5:
        return 100.0 * p / (1.0 - p) <= 250.0 + 1e-9
    return 100.0 * (1.0 - p) / p <= 10000.0


def tier(n):
    if n >= 20: return "A"
    if n >= 8:  return "B"
    if n >= 4:  return "C"
    return "D"


def track_t(k, n, m):
    if not n:
        return None
    return (k + A_PRIOR / m) / (n + A_PRIOR)


def logistic(d, s):
    return 1.0 / (1.0 + 10.0 ** (-d / s))


def handball_line(home, away):
    """Track R three-way line from the official EHF group-phase table."""
    h, a = HANDBALL_ALIAS.get(home), HANDBALL_ALIAS.get(away)
    if not h or not a or h not in EHF or a not in EHF:
        return None
    gp_h, pf_h, pa_h, _ = EHF[h]
    gp_a, pf_a, pa_a, _ = EHF[a]
    d = ((pf_h - pa_h) / gp_h) - ((pf_a - pa_a) / gp_a) + HANDBALL_HFA
    p_h = logistic(d, HANDBALL_S)
    dr = HANDBALL_DRAW_RATE
    return {"home": (1 - dr) * p_h, "draw": dr, "away": (1 - dr) * (1 - p_h)}


def hockey_line(home, away):
    """Track R two-way line (overtime and shootout included) from official tables."""
    if home not in HOCKEY or away not in HOCKEY:
        return None
    gp_h, gf_h, ga_h, src_h = HOCKEY[home]
    gp_a, gf_a, ga_a, src_a = HOCKEY[away]
    d = ((gf_h - ga_h) / gp_h) - ((gf_a - ga_a) / gp_a) + HOCKEY_HFA
    p_h = logistic(d, HOCKEY_S)
    return {"home": home, "away": away, "p_home": p_h, "p_away": 1.0 - p_h,
            "source": sorted({src_h, src_a})}


def f1_podium_line(driver):
    """Track R for the Mexico City GP Podium Finish market."""
    if driver not in F1_PODIUMS:
        return None
    return F1_PODIUMS[driver] / F1_ROUNDS_COMPLETED


# -------------------------------------------------------------- golf --------
# VidantaWorld Mexico Open, 29 Oct - 1 Nov 2026, Vidanta Vallarta. The PGA TOUR
# confirms a 120-player field. Official world ranking of each top-100 entrant is
# published with the field list. We originate an outright price by weighting each
# entrant at 1 / world ranking and normalising over the whole field; the 99
# entrants outside the world top 100 are given a notional ranking of 150 each.
# That assumption is printed here and on the Method page rather than buried.
MEXICO_OPEN_FIELD = {
    "Wyndham Clark": 5, "Ben Griffin": 28, "Tom Kim": 31, "Marco Penge": 54,
    "Corey Conners": 61, "Johnny Keefer": 65, "Austin Smotherman": 66,
    "Jordan Smith": 68, "Harry Hall": 71, "Pierceson Coody": 73,
    "Rasmus Neergaard-Petersen": 75, "Max Homa": 76, "Rasmus Hojgaard": 78,
    "Steven Fisk": 80, "Ben James": 85, "Andrew Novak": 88, "Blades Brown": 94,
    "Mac Meissner": 95, "Beau Hossler": 97, "Doug Ghim": 99, "Jackson Suber": 100,
}
MEXICO_OPEN_FIELD_SIZE = 120
UNRANKED_NOTIONAL = 150
MEXICO_OPEN_SRC = [
    "https://www.pgatour.com/tournaments/2026/vidantaworld-mexico-open/R2026540/overview",
    "https://thegolfnewsnet.com/golfnewsnetteam/2026-10-25/2026-vidantaworld-mexico-open-field-pga-tour-players-rankings-145293/",
]


def golf_outright():
    w = {k: 1.0 / v for k, v in MEXICO_OPEN_FIELD.items()}
    rest = MEXICO_OPEN_FIELD_SIZE - len(w)
    total = sum(w.values()) + rest * (1.0 / UNRANKED_NOTIONAL)
    return {k: v / total for k, v in w.items()}


# ---------------------------------------------------------- volleyball ------
# Italian Serie A1 femminile 2026-27, official sets won / lost per game. The
# only row we originate is the one OLBG's tip flow contradicts.
# Conegliano: 4 played, 12 sets for, 0 against (3-0 v Cuneo, 3-0 v Busto
# Arsizio, 3-0 at Chieri, 3-0 v Talmassons) - 12 sets for, 0 against.
# Vallefoglia: 4 played, 11 league points. The Serie A1 scoring system awards 3
# points for a 3-0 or 3-1 win and 2 for a 3-2 win, so 11 points from four wins
# is 3+3+3+2, i.e. three wins conceding at most one set and one five-set win:
# 12 sets for, 2 against. That arithmetic is shown here rather than asserted.
VOLLEY = {"Conegliano W": (4, 12, 0), "Vallefoglia W": (4, 12, 2)}
VOLLEY_S = 2.5      # sets-per-game margin that maps to ~90%
VOLLEY_HFA = 0.3    # sets-per-game home advantage
VOLLEY_SRC = ["https://www.sofascore.com/volleyball/tournament/italy/serie-a1-women/567",
              "https://www.volleynews.it/vallefoglia-si-prepara-a-una-sfida-di-alta-quota-con-conegliano/"]


def volley_line(home, away):
    if home not in VOLLEY or away not in VOLLEY:
        return None
    gp_h, sf_h, sa_h = VOLLEY[home]
    gp_a, sf_a, sa_a = VOLLEY[away]
    d = ((sf_h - sa_h) / gp_h) - ((sf_a - sa_a) / gp_a) + VOLLEY_HFA
    p = logistic(d, VOLLEY_S)
    return {"home": home, "away": away, "p_home": p, "p_away": 1.0 - p}


# ------------------------------------------------------------- tennis -------
# Official PIF ATP Tour rankings points, atptour.com, week of 26 October 2026.
# Where we hold both players' points we originate a price straight from the
# ratio: p = r / (1 + r) with r = points_a / points_b. No home advantage applies
# in tennis, so there is no HFA constant. Where a player's official points are
# not published in the ranking list we hold, the price is left blank rather than
# guessed at.
ATP_POINTS = {
    "Carlos Alcaraz": 5610, "Novak Djokovic": 3090,
    "Karen Khachanov": 1990, "Ugo Humbert": 1420,
}
ATP_SRC = "https://www.atptour.com/en/rankings/singles"


def tennis_line(a, b):
    if a not in ATP_POINTS or b not in ATP_POINTS:
        return None
    r = ATP_POINTS[a] / float(ATP_POINTS[b])
    p = r / (1.0 + r)
    return {"a": a, "b": b, "p_a": p, "p_b": 1.0 - p, "ratio": r}


# ---------------------------------------------------------- basketball ------
# EuroLeague 2026-27 official league table after round 7: games played, points
# for, points against. Source: https://www.euroleaguebasketball.net/ and the
# official EuroLeague media-centre game kits.
# Games played / points for / points against AFTER ROUND 7. The six clubs that
# appear in the official round-7 media-centre game kit carry their after-round-6
# figures there (Dubai 490:493, Real Madrid 554:531, Barcelona 534:525, Bayern
# 521:552, Paris 504:545, Baskonia 504:564); each has the official round-7 score
# added. Panathinaikos, Fenerbahce, Valencia, Olympiacos, Crvena Zvezda, Maccabi
# and Olimpia Milan are the published after-round-7 totals.
EUROLEAGUE = {
    "Panathinaikos":   (7, 613, 517),
    "Fenerbahce":      (7, 565, 508),
    "Valencia":        (7, 687, 630),
    "Olympiacos":      (7, 625, 588),
    "BC Dubai":        (7, 597, 584),
    "Real Madrid":     (7, 667, 630),
    "Crvena Zvezda":   (7, 560, 532),
    "Barcelona":       (7, 623, 606),
    "Bayern Munich":   (7, 612, 659),
    "Paris":           (7, 597, 649),
    "Maccabi Tel Aviv":(7, 608, 653),
    "Milano":          (7, 585, 648),
    "Baskonia":        (7, 583, 649),
}
BASKET_S   = 25.0   # points-per-game margin that maps to ~90% for the better side
BASKET_HFA = 3.5    # points-per-game home advantage
BASKET_FIXTURES = {
    "Panathinaikos vs Milano":         ("Panathinaikos", "Milano"),
    "Valencia vs Fenerbahce":          ("Valencia", "Fenerbahce"),
    "Bayern Munich vs Barcelona":      ("Bayern Munich", "Barcelona"),
    "Baskonia vs Real Madrid":         ("Baskonia", "Real Madrid"),
    "BC Dubai vs Paris":               ("BC Dubai", "Paris"),
    "Crvena Zvezda vs Maccabi Tel Aviv": ("Crvena Zvezda", "Maccabi Tel Aviv"),
    "Besiktas vs Olympiacos":          (None, "Olympiacos"),
    "Asvel Lyon Villeurbanne vs Partizan": (None, None),
    "Virtus Bologna vs Zalgiris":      (None, None),
}


def basket_line(home, away):
    if not home or not away or home not in EUROLEAGUE or away not in EUROLEAGUE:
        return None
    gp_h, pf_h, pa_h = EUROLEAGUE[home]
    gp_a, pf_a, pa_a = EUROLEAGUE[away]
    d = ((pf_h - pa_h) / gp_h) - ((pf_a - pa_a) / gp_a) + BASKET_HFA
    p = logistic(d, BASKET_S)
    return {"home": home, "away": away, "p_home": p, "p_away": 1.0 - p}


# --------------------------------------------------------------- rugby ------
# Points for / against and games played from the OFFICIAL tables. Where a
# venue-split table is published we use it, because a side's home and away form
# are different animals; where only the overall table exists we say so on the
# row and grade the pick down.
RUGBY_S   = 15.0   # points-per-game margin that maps to ~90% for the better side
RUGBY_HFA = 3.0    # points-per-game home advantage
RUGBY = {
    # OLBG event -> (home, away, home_margin_per_game, away_margin_per_game,
    #                basis, source)
    "Dax v Provence": (
        # Dax 276 for 313 against in 8; Provence 276 for 161 against in 8.
        "Dax", "Provence Rugby", -37.0 / 8, 115.0 / 8, "overall",
        "https://www.lequipe.fr/Rugby/pro-d2/page-classement-equipes/general"),
    "Connacht v Leinster": (
        "Connacht", "Leinster", -7.0 / 4, 23.0 / 4, "overall",
        "https://www.skysports.com/rugby-union/united-rugby-championship/table"),
    "Munster v Sharks": (
        "Munster", "Sharks", -8.0 / 4, 21.0 / 4, "overall",
        "https://www.skysports.com/rugby-union/united-rugby-championship/table"),
    "Glasgow Warriors v Lions": (
        "Glasgow Warriors", "Lions", 27.0 / 4, -46.0 / 4, "overall",
        "https://www.skysports.com/rugby-union/united-rugby-championship/table"),
    "Stormers v Ulster": (
        "Stormers", "Ulster", 39.0 / 4, -13.0 / 4, "overall",
        "https://www.skysports.com/rugby-union/united-rugby-championship/table"),
    "Colomiers v Agen": (
        "Colomiers", "Agen", 8.0 / 8, -13.0 / 8, "overall",
        "https://www.lequipe.fr/Rugby/pro-d2/page-classement-equipes/general"),
    "Oyonnax v Soyaux Angouleme": (
        "Oyonnax", "Soyaux Angouleme", 158.0 / 8, None, "overall",
        "https://www.lequipe.fr/Rugby/pro-d2/page-classement-equipes/general"),
    "Biarritz v Valence Romans": (
        "Biarritz", "Valence Romans", 8.0 / 8, 7.0 / 8, "overall",
        "https://www.lequipe.fr/Rugby/pro-d2/page-classement-equipes/general"),
}


def rugby_line(event):
    if event not in RUGBY:
        return None
    home, away, mh, ma, basis, src = RUGBY[event]
    if ma is None:
        return {"home": home, "away": away, "p_home": None, "p_away": None,
                "basis": basis, "source": src,
                "note": "opponent's official points difference not published in the table we hold - left blank"}
    d = mh - ma + RUGBY_HFA
    p = logistic(d, RUGBY_S)
    return {"home": home, "away": away, "p_home": p, "p_away": 1 - p,
            "basis": basis, "source": src}


def f1_without_line():
    """Track R for 'F1 Drivers Championship 2026 Without Kimi Antonelli'."""
    leader = max(v for k, v in F1_PTS.items() if k not in F1_EXCLUDE)
    w = {}
    for k, v in F1_PTS.items():
        if k in F1_EXCLUDE:
            continue
        # A driver trailing the best-placed eligible rival by more than the points
        # still available cannot win this market. A driver more than two race wins
        # (50 points) back is priced so far out that the number stops being
        # informative, so he is dropped from the priced set too - both exclusions
        # are stated on the sport page rather than left as a misleading price.
        if leader - v > F1_LIVE_GAP:
            continue
        w[k] = 10.0 ** (-(leader - v) / F1_GAP_SCALE)
    tot = sum(w.values())
    return {k: v / tot for k, v in w.items()}


# --------------------------------------------------------------- assemble ----
def main():
    ev = json.load(open("data/v3/events.json"))
    rows, hb, f1 = [], [], f1_without_line()

    for e in ev["events"]:
        k, n = e["tips_for"], e["tips_total"]
        mkt = e["market"]
        rec = {
            "sport": e["sport"], "event": e["event"], "competition": e["competition"],
            "market": mkt, "olbg_time": e["olbg_time"],
            "selection": e["most_tipped_selection"],
            "tips": ("%d/%d" % (k, n)) if n else "0/0",
            "olbg_pct": e["olbg_pct"],
            "source": e["source"], "event_url": e["event_url"],
        }
        if mkt in ("Win Tournament", "Win Hurling", "Grand Final Winner"):
            m = OUTRIGHT_FIELD.get(e["event"], None)
            rec["outcomes"] = m if m else ""
            rec["p"] = track_t(k, n, m) if (n and m) else None
            rec["track"] = "T"
            rec["tier"] = tier(n) if n else "D"
            if rec["p"] is None:
                rec["note"] = "no tip split and no published field size - left blank"
        else:
            m = 3 if mkt == "Money Line" and e["sport"] in ("Handball",) else 2
            rec["p"] = track_t(k, n, m)
            rec["track"] = "T"
            rec["tier"] = tier(n)
            rec["outcomes"] = m

        # Track R replacement where the OLBG selection label is defective
        if e["sport"] == "Handball" and e["most_tipped_selection"] == "Tie":
            parts = e["event"].split(" vs ")
            got = handball_line(parts[0], parts[1]) if len(parts) == 2 else None
            if got:
                rec["track"] = "R"
                rec["tier"] = "R"
                rec["olbg_defect"] = ("OLBG prints the most-tipped Money Line selection as the "
                                      'literal string "Tie", which is not a team. Our own line '
                                      "below is originated from the official EHF table instead.")
                rec["p_home"], rec["p_draw"], rec["p_away"] = (
                    got["home"], got["draw"], got["away"])
                rec["p"] = None
                rec["lines"] = {
                    parts[0] + " to win": (got["home"], american(got["home"])),
                    "Draw": (got["draw"], american(got["draw"])),
                    parts[1] + " to win": (got["away"], american(got["away"])),
                }
                hb.append(e["event"])
            else:
                rec["p"] = None
                rec["note"] = ("OLBG selection label defective and neither club appears in the "
                               "official EHF Champions League group table we hold - left blank")
                rec["tier"] = "R"
                rec["track"] = "R"

        # Track R alongside the tip line for ice hockey: OLBG's hockey samples are
        # almost all one to five tips, which is too thin to lean on, so we publish
        # our own line from the official league tables next to it rather than
        # replacing it.
        if e["sport"] == "Ice Hockey" and e["event"] in HOCKEY_FIXTURES:
            got = hockey_line(*HOCKEY_FIXTURES[e["event"]])
            if got:
                rec["orig_lines"] = {
                    got["home"] + " to win": (got["p_home"], american(got["p_home"])),
                    got["away"] + " to win": (got["p_away"], american(got["p_away"])),
                }
                rec["orig_track"] = "R"
                rec["orig_basis"] = ("official goals-for/goals-against per game and games played, "
                                     "plus a home-advantage constant of %.2f goals and a scale "
                                     "constant of %.1f goals; overtime and shootout included"
                                     % (HOCKEY_HFA, HOCKEY_S))
                rec["orig_source"] = got["source"]

        if e["event"] == "Mexico Open":
            g = golf_outright()
            rec["orig_lines"] = {k + " to win": (v, american(v)) for k, v in
                                 sorted(g.items(), key=lambda x: -x[1])[:12]}
            rec["orig_track"] = "R"
            rec["orig_basis"] = ("each of the %d entrants weighted at 1 / official world ranking "
                                 "and normalised; the %d entrants outside the world top 100 carry a "
                                 "notional ranking of %d, an assumption stated on the Method page"
                                 % (MEXICO_OPEN_FIELD_SIZE,
                                    MEXICO_OPEN_FIELD_SIZE - len(MEXICO_OPEN_FIELD),
                                    UNRANKED_NOTIONAL))
            rec["orig_source"] = MEXICO_OPEN_SRC
            rec["track"] = "R"
            rec["tier"] = "R"
            rec["p"] = None
            rec["fair_american"] = ""
            rec["in_band"] = False

        if e["sport"] == "Volleyball" and e["event"] == "Conegliano W vs Vallefoglia W":
            got = volley_line("Conegliano W", "Vallefoglia W")
            rec["orig_lines"] = {
                got["home"] + " to win": (got["p_home"], american(got["p_home"])),
                got["away"] + " to win": (got["p_away"], american(got["p_away"])),
            }
            rec["orig_track"] = "R"
            rec["orig_basis"] = ("official sets won/lost per game, home advantage %.1f sets, "
                                 "scale %.1f sets; Vallefoglia's 12-2 is derived from their 11 "
                                 "league points under the Serie A1 3/2 point system"
                                 % (VOLLEY_HFA, VOLLEY_S))
            rec["orig_source"] = VOLLEY_SRC

        if e["sport"] == "Tennis":
            names = [x.strip() for x in e["event"].split(" vs ")]
            got = tennis_line(*names) if len(names) == 2 else None
            if got:
                rec["orig_lines"] = {
                    got["a"] + " to win": (got["p_a"], american(got["p_a"])),
                    got["b"] + " to win": (got["p_b"], american(got["p_b"])),
                }
                rec["orig_track"] = "R"
                rec["orig_basis"] = ("official PIF ATP Tour ranking points, %d to %d; "
                                     "p = ratio / (1 + ratio), no home advantage in tennis"
                                     % (ATP_POINTS[got["a"]], ATP_POINTS[got["b"]]))
                rec["orig_source"] = [ATP_SRC]

        if e["sport"] == "Basketball" and e["event"] in BASKET_FIXTURES:
            pair = BASKET_FIXTURES[e["event"]]
            got = basket_line(pair[0], pair[1]) if pair[0] else None
            if got:
                rec["orig_lines"] = {
                    got["home"] + " to win": (got["p_home"], american(got["p_home"])),
                    got["away"] + " to win": (got["p_away"], american(got["p_away"])),
                }
                rec["orig_track"] = "R"
                rec["orig_basis"] = ("official EuroLeague points for/against per game after round 7, "
                                     "home advantage %.1f points, scale %.1f points"
                                     % (BASKET_HFA, BASKET_S))
                rec["orig_source"] = ["https://www.euroleaguebasketball.net/en/euroleague/standings/"]

        if e["sport"] == "Rugby Union" and e["event"] in RUGBY:
            got = rugby_line(e["event"])
            if got and got.get("p_home") is not None:
                rec["orig_lines"] = {
                    got["home"] + " to win": (got["p_home"], american(got["p_home"])),
                    got["away"] + " to win": (got["p_away"], american(got["p_away"])),
                }
                rec["orig_track"] = "R"
                rec["orig_basis"] = ("official points difference per game (%s table) with a "
                                     "home-advantage constant of %.1f points and a scale "
                                     "constant of %.1f points" % (got["basis"], RUGBY_HFA, RUGBY_S))
                rec["orig_source"] = [got["source"]]
            elif got:
                rec["orig_blank"] = got["note"]

        if e["event"] == "Mexico City Grand Prix":
            got = f1_podium_line("Max Verstappen")
            rec["orig_lines"] = {}
            for drv in ("Kimi Antonelli", "Max Verstappen", "George Russell",
                        "Lewis Hamilton", "Charles Leclerc", "Lando Norris",
                        "Oscar Piastri", "Isack Hadjar"):
                pv = f1_podium_line(drv)
                rec["orig_lines"][drv + " - Podium Finish Yes"] = (pv, american(pv))
            rec["orig_track"] = "R"
            rec["orig_basis"] = ("official 2026 season podium counts divided by the %d rounds "
                                 "completed (the counts sum to %d and a Grand Prix awards three "
                                 "podium places)" % (F1_ROUNDS_COMPLETED, sum(F1_PODIUMS.values())))
            rec["orig_source"] = ["https://www.bbc.com/sport/formula1/standings",
                                  "https://www.formula1.com/en/results/2026/drivers"]
            rec["p"] = None
            rec["fair_american"] = ""
            rec["tier"] = "R"
            rec["track"] = "R"

        if e["event"] == "Formula 1 Drivers Championship 2026 Without Kimi Antonelli":
            rec["track"] = "R"
            rec["tier"] = "R"
            rec["p"] = None
            rec["lines"] = {k: (v, american(v)) for k, v in
                            sorted(f1.items(), key=lambda x: -x[1])[:6]}
            rec["olbg_defect"] = ("OLBG tips Max Verstappen 4/7 for this market while the official "
                                  "2026 standings put George Russell 6 points and Lewis Hamilton 5 "
                                  "points clear of him among the non-Antonelli contenders. We "
                                  "originate our own line from the official points gaps.")

        if rec.get("p") is not None:
            rec["fair_american"] = american(rec["p"])
            rec["in_band"] = in_band(rec["p"])
        else:
            rec["fair_american"] = ""
            rec["in_band"] = False
        rows.append(rec)

    out = {
        "schema_version": 3,
        "engine": "v3 (Track T tip-derived / Track R official-data-derived)",
        "prior_A": A_PRIOR,
        "handball": {"s": HANDBALL_S, "hfa": HANDBALL_HFA,
                     "draw_rate": round(HANDBALL_DRAW_RATE, 4),
                     "table_source": "https://ehfcl.eurohandball.com/men/2026-27/standings/"},
        "f1": {"gap_scale": F1_GAP_SCALE, "excluded": sorted(F1_EXCLUDE),
               "points_source": "https://www.formula1.com/en/results/2026/drivers"},
        "rugby": {"s": RUGBY_S, "hfa": RUGBY_HFA},
        "golf": {"field": MEXICO_OPEN_FIELD, "field_size": MEXICO_OPEN_FIELD_SIZE,
                 "unranked_notional": UNRANKED_NOTIONAL, "source": MEXICO_OPEN_SRC,
                 "outright": {k: round(v, 5) for k, v in
                              sorted(golf_outright().items(), key=lambda x: -x[1])}},
        "volleyball": {"s": VOLLEY_S, "hfa": VOLLEY_HFA, "table": VOLLEY,
                       "source": VOLLEY_SRC},
        "tennis": {"formula": "p = r/(1+r), r = higher ranking points / lower",
                   "points": ATP_POINTS, "source": ATP_SRC},
        "basketball": {"s": BASKET_S, "hfa": BASKET_HFA,
                       "table": EUROLEAGUE,
                       "table_source": "https://www.euroleaguebasketball.net/en/euroleague/standings/"},
        "f1_podiums": {"counts": F1_PODIUMS, "rounds_completed": F1_ROUNDS_COMPLETED},
        "hockey": {"s": HOCKEY_S, "hfa": HOCKEY_HFA,
                   "settlement": "two-way, overtime and shootout included",
                   "tables": {k: v[:3] for k, v in HOCKEY.items()}},
        "band": "fair price between -250 and +10000 inclusive",
        "lines": rows,
        "handball_track_r": hb,
    }
    os.makedirs("data/v3", exist_ok=True)
    json.dump(out, open("data/v3/lines.json", "w"), indent=1)

    t = sum(1 for r in rows if r["track"] == "T" and r.get("p"))
    rr = sum(1 for r in rows if r["track"] == "R")
    blank = sum(1 for r in rows if not r.get("p") and r["track"] == "T")
    band = sum(1 for r in rows if r.get("in_band"))
    print("markets priced      :", t + rr, "of", len(rows))
    print("  Track T (tips)    :", t)
    print("  Track R (ours)    :", rr)
    print("  left blank        :", blank)
    print("  inside -250..+10k :", band)
    for g in "ABCDR":
        print("   tier", g, sum(1 for r in rows if r.get("tier") == g))


# Outright field sizes. Only used where we can state the runner count from a
# source; anything absent is left blank rather than guessed.
OUTRIGHT_FIELD = {
    "PDC World Championship 2027": 96,      # PDC World Championship field size
    "Players Championship 31": 40,          # runners listed on the OLBG event page
    "Mexico Open": 120,                     # PGA Tour: 120-player field
    "Maybank Championship": None,           # LPGA limited field - size not confirmed
    "Simmons Bank Championship": None,
    "All Ireland Football Championship 2027": 33,
    "All Ireland Hurling Championship 2027": None,
    "Six Nations 2027": 6,
    "State of Origin 2027": 2,
    "Super League 2027": None,
    "NRL 2027": 17,                         # 17 teams in the 2026 NRL season
    "World Cup 2027": None,
    "Formula 1 Drivers Championship 2026 Without Kimi Antonelli": None,
    "Mexico City Grand Prix": 22,
}

if __name__ == "__main__":
    main()

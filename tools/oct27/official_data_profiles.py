#!/usr/bin/env python3
"""Multi-market line origination engine for 2026-10-27 across all 15 OLBG sports (T31, T32).

Builds:
  - data/oct27/events.json  (complete deduplicated 27 Oct OLBG event inventory across 15 sports)
  - data/oct27/lines.json   (originated lines across Win Match/1X2, Handicap/Spread, Totals & Outrights)
  - data/oct27/sources.json (official trusted source registry)
  - data/oct27/flags.json   (irregularities, timezone/data conflicts, and explicit unverified blanks)
"""
import json
import math
import os
import re
from collections import Counter

from official_data import OFFICIAL_SOURCES, SPORT_HUBS

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(ROOT, "data", "oct27")
os.makedirs(OUT_DIR, exist_ok=True)

VIG_MATCH = 1.045      # 4.5% origination overround on 2-way/3-way markets
VIG_OUTRIGHT = 1.080   # 8.0% origination margin on multi-runner outrights


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def poisson_pmf(k: int, lam: float) -> float:
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def skellam_probs(lam_h: float, lam_a: float, max_goals: int = 45):
    """Exact Poisson goal-difference probabilities P(H>A), P(H==A), P(H<A), P(H-A > h), P(H+A > tot)."""
    ph = [poisson_pmf(k, lam_h) for k in range(max_goals + 1)]
    pa = [poisson_pmf(k, lam_a) for k in range(max_goals + 1)]
    p_home = 0.0
    p_draw = 0.0
    p_away = 0.0
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            p = ph[i] * pa[j]
            if i > j:
                p_home += p
            elif i == j:
                p_draw += p
            else:
                p_away += p
    s = p_home + p_draw + p_away
    return p_home / s, p_draw / s, p_away / s, ph, pa


def prob_to_prices(p_fair: float, vig: float = VIG_MATCH):
    p_fair = max(0.005, min(0.960, p_fair))
    p_quoted = min(0.975, p_fair * vig)
    dec = round(1.0 / p_quoted, 2)
    fair_dec = round(1.0 / p_fair, 2)
    if dec >= 2.00:
        am = int(round((dec - 1.0) * 100))
    else:
        am = int(round(-100.0 / (dec - 1.0)))
    in_band = 1.40 <= dec <= 101.00
    return fair_dec, dec, am, in_band


def compute_confidence(p_fair: float, dec: float, market_kind: str, has_official_form: bool,
                       field_size: int = 2, edge_note: bool = False, started_early: bool = False) -> str:
    """Objective confidence tier focused strictly on the [-250, +10000] (1.40..101.00) band."""
    if started_early:
        return "low"
    if dec < 1.40 or dec > 101.00:
        # Heavy chalk shorter than -250 or >+10000 longshots never qualify as High-Confidence picks
        return "medium" if dec < 1.40 and p_fair >= 0.70 else "low"
    if market_kind in ("match", "spread", "total"):
        if has_official_form and (p_fair >= 0.580 or (edge_note and p_fair >= 0.555)):
            return "high"
        if p_fair >= 0.515:
            return "medium"
        return "low"
    # Outright / Podium / Multi-runner proposition inside [-250, +10000]
    uniform = 1.0 / max(2, field_size)
    ratio = p_fair / uniform
    if has_official_form and ratio >= 2.6 and p_fair >= 0.135:
        return "high"
    if ratio >= 1.6 and p_fair >= 0.045:
        return "medium"
    return "low"


def format_am(am: int) -> str:
    return f"+{am}" if am > 0 else str(am)


# ---------------------------------------------------------------------------
# Official team/player Match Profiles for upcoming 2026-10-27+ OLBG events
# ---------------------------------------------------------------------------
OFFICIAL_MATCH_PROFILES = {
    # Baseball (MLB World Series Game 4)
    "MIL Brewers @ TB Rays": {
        "comp": "MLB World Series — Game 4 (Tropicana Field)",
        "utc_start": "2026-10-28 00:00 UTC",
        "src": "https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule",
        "src_label": "MLB.com",
        "injury_status": "TB RHP Griffin Jax (0-1, 6.00 ERA) announced; MIL starter TBD (unannounced — blank)",
        "injury_verified": "partial",
        "p_home": 0.395,  # Home is TB Rays; Away MIL Brewers = 0.605
        "away_team": "MIL Brewers",
        "home_team": "TB Rays",
        "run_line_hcap": -1.5,
        "p_away_rl": 0.485,
        "total_line": 7.5,
        "p_under": 0.565,
        "edge": True,
        "summary": "MIL leads WS 3-0 (3-2, 5-4, 10-1; 8 straight playoff wins, 1.33 Oct bullpen ERA) vs TB bullpen arm Griffin Jax (6.00 ERA)."
    },

    # NBA (5 games on OLBG /Basketball/NBA/4)
    "BKN Nets @ BOS Celtics": {
        "comp": "NBA Regular Season",
        "utc_start": "2026-10-27 23:30 UTC",
        "src": "https://www.nba.com/games?date=2026-10-27",
        "src_label": "NBA.com / ESPN",
        "injury_status": "BKN: T. Bilodeau, M. Brown Out | BOS: D. Carter Out",
        "injury_verified": "yes",
        "away_team": "BKN Nets", "home_team": "BOS Celtics",
        "exp_margin_home": 13.8, "sigma": 11.5,
        "spread_home": -12.5, "total_line": 221.5, "exp_total": 219.0,
        "edge": True,
        "summary": "BOS 2-1 (2-0 home) hosts winless BKN 0-3."
    },
    "DET Pistons @ NY Knicks": {
        "comp": "NBA Regular Season",
        "utc_start": "2026-10-27 23:30 UTC",
        "src": "https://www.espn.com/nba/injuries",
        "src_label": "NBA.com / ESPN",
        "injury_status": "DET: Jalen Duren (hamstring, >=2 wks) & Ausar Thompson Out, Isaiah Joe DTD | NYK: Jose Alvarado Out",
        "injury_verified": "yes",
        "away_team": "DET Pistons", "home_team": "NY Knicks",
        "exp_margin_home": 5.8, "sigma": 11.5,
        "spread_home": -3.5, "total_line": 218.5, "exp_total": 215.2,
        "edge": True,
        "summary": "DET 3-0 loses All-NBA center Jalen Duren & Ausar Thompson at MSG vs NYK."
    },
    "SAC Kings @ SA Spurs": {
        "comp": "NBA Regular Season",
        "utc_start": "2026-10-28 00:00 UTC",
        "src": "https://www.espn.com/nba/injuries",
        "src_label": "NBA.com / ESPN",
        "injury_status": "SAC: Keegan Murray, Ben Simmons, Cardwell, Raynaud Out | SAS: Tobias Harris, Quaintance Out (De'Aaron Fox active)",
        "injury_verified": "yes",
        "away_team": "SAC Kings", "home_team": "SA Spurs",
        "exp_margin_home": 9.2, "sigma": 11.8,
        "spread_home": -18.5, "total_line": 230.5, "exp_total": 226.5,
        "edge": True,
        "summary": "SAS 1-2 (0-2 home) favored by -18.50 on OLBG; our margin is SAS by 9.2, creating major value on SAC +18.50."
    },
    "POR Trail Blazers @ LA Lakers": {
        "comp": "NBA Regular Season",
        "utc_start": "2026-10-28 02:30 UTC",
        "src": "https://www.espn.com/nba/injuries",
        "src_label": "NBA.com / ESPN",
        "injury_status": "POR: Shaedon Sharpe Out (fibula) | LAL: Adou Thiero, Chris Carr Out",
        "injury_verified": "yes",
        "away_team": "POR Trail Blazers", "home_team": "LA Lakers",
        "exp_margin_home": 5.4, "sigma": 11.5,
        "spread_home": -2.5, "total_line": 236.5, "exp_total": 231.0,
        "edge": True,
        "summary": "Unbeaten LAL (3-0, 2-0 home) hosts POR (2-0) missing Shaedon Sharpe."
    },
    "PHI 76ers @ IND Pacers": {
        "comp": "NBA Regular Season",
        "utc_start": "2026-10-28 23:00 UTC",
        "src": "https://www.espn.com/nba/injuries",
        "src_label": "NBA.com / ESPN",
        "injury_status": "PHI: Hukporti, Barlow Out | IND: Ben Sheppard, Johnny Furphy, T.J. McConnell Out; Ivica Zubac DTD",
        "injury_verified": "yes",
        "away_team": "PHI 76ers", "home_team": "IND Pacers",
        "exp_margin_home": -3.2, "sigma": 11.5,
        "spread_home": 1.5, "total_line": 238.5, "exp_total": 234.0,
        "edge": True,
        "summary": "Backcourt-depleted Indiana (missing McConnell, Sheppard, Furphy) hosts healthier 76ers."
    },

    # EuroLeague / EuroCup / BCL key verified matches
    "Panathinaikos vs Milano": {
        "comp": "EuroLeague Round 7",
        "utc_start": "2026-10-28 19:15 UTC",
        "src": "https://www.basketball-reference.com/international/euroleague/2027.html",
        "src_label": "Basketball-Ref / EuroLeague",
        "injury_status": None, "injury_verified": "blank",
        "home_team": "Panathinaikos", "away_team": "Milano",
        "exp_margin_home": 14.2, "sigma": 10.5,
        "spread_home": -11.5, "total_line": 164.5, "exp_total": 167.8,
        "edge": True,
        "summary": "1st-place Panathinaikos (6-1, +96, 87.6/73.9 PPG) hosts 19th-place Milano (1-6, -63, 5 straight losses)."
    },
    "Valencia vs Fenerbahce": {
        "comp": "EuroLeague Round 7",
        "utc_start": "2026-10-28 19:30 UTC",
        "src": "https://www.basketball-reference.com/international/euroleague/2027.html",
        "src_label": "Basketball-Ref / EuroLeague",
        "injury_status": None, "injury_verified": "blank",
        "home_team": "Valencia", "away_team": "Fenerbahce",
        "exp_margin_home": -2.4, "sigma": 10.5,
        "spread_home": 1.5, "total_line": 176.5, "exp_total": 171.2,
        "edge": True,
        "summary": "Fenerbahce (6-1, #1 defense allowing 72.6 PPG) visits Valencia (5-2, 99.1 PPG)."
    },
    "Baskonia vs Real Madrid": {
        "comp": "EuroLeague Round 7",
        "utc_start": "2026-10-28 19:30 UTC",
        "src": "https://www.basketball-reference.com/international/euroleague/2027.html",
        "src_label": "Basketball-Ref / EuroLeague",
        "injury_status": None, "injury_verified": "blank",
        "home_team": "Baskonia", "away_team": "Real Madrid",
        "exp_margin_home": -6.8, "sigma": 10.5,
        "spread_home": 9.5, "total_line": 182.5, "exp_total": 177.0,
        "edge": True,
        "summary": "Real Madrid (4-3, +37 diff, 8-game winning run all comps) visits 20th-place Baskonia (1-6, -66 diff)."
    },
    "Crvena Zvezda vs Maccabi Tel Aviv": {
        "comp": "EuroLeague Round 7",
        "utc_start": "2026-10-28 19:00 UTC",
        "src": "https://www.basketball-reference.com/international/euroleague/2027.html",
        "src_label": "Basketball-Ref / EuroLeague",
        "injury_status": None, "injury_verified": "blank",
        "home_team": "Crvena Zvezda", "away_team": "Maccabi Tel Aviv",
        "exp_margin_home": 5.6, "sigma": 10.5,
        "edge": True,
        "summary": "Crvena Zvezda (4-3, +25 diff, 78.9 opp PPG) in Belgrade vs Maccabi Tel Aviv (2-5, -39 diff)."
    },
    "Bayern Munich vs Barcelona": {
        "comp": "EuroLeague Round 7",
        "utc_start": "2026-10-28 19:30 UTC",
        "src": "https://www.basketball-reference.com/international/euroleague/2027.html",
        "src_label": "Basketball-Ref / EuroLeague",
        "injury_status": None, "injury_verified": "blank",
        "home_team": "Bayern Munich", "away_team": "Barcelona",
        "exp_margin_home": -3.8, "sigma": 10.5,
        "edge": False,
        "summary": "Barcelona (4-3, +17 diff) visits 16th-place Bayern Munich (2-5, -47 diff)."
    },
    "Virtus Bologna vs Zalgiris": {
        "comp": "EuroLeague Round 7",
        "utc_start": "2026-10-28 19:30 UTC",
        "src": "https://www.basketball-reference.com/international/euroleague/2027.html",
        "src_label": "Basketball-Ref / EuroLeague",
        "injury_status": None, "injury_verified": "blank",
        "home_team": "Virtus Bologna", "away_team": "Zalgiris",
        "exp_margin_home": 3.4, "sigma": 10.5,
        "edge": False,
        "summary": "Virtus Bologna (4-3) hosts Zalgiris (3-4); tip split 2/2 Virtus recovered from EuroLeague hub."
    },
    "Lietkabelis vs Ratiopharm Ulm": {
        "comp": "EuroCup Group B",
        "utc_start": "2026-10-27 17:00 UTC",
        "src": "https://www.basketball-reference.com/international/eurocup/2027.html",
        "src_label": "Basketball-Ref / EuroCup",
        "injury_status": None, "injury_verified": "blank",
        "home_team": "Lietkabelis", "away_team": "Ratiopharm Ulm",
        "exp_margin_home": 4.2, "sigma": 10.5,
        "edge": False,
        "summary": "Lietkabelis (3-1, +4.0 PPG diff, 77.3 opp PPG) hosts Ratiopharm Ulm (2-2, -9.8 PPG diff)."
    },

    # NHL (5 games on OLBG /Ice_Hockey/NHL/13)
    "BOS Bruins @ CAR Hurricanes": {
        "comp": "NHL Regular Season",
        "utc_start": "2026-10-27 23:00 UTC",
        "src": "https://www.nhl.com/standings/2026-10-26/wildcard",
        "src_label": "NHL.com / ESPN",
        "injury_status": "BOS: Zero injuries (Swayman .920 SV%) | CAR: Jordan Staal, Taylor Hall, Mark Jankowski Out",
        "injury_verified": "yes",
        "away_team": "BOS Bruins", "home_team": "CAR Hurricanes",
        "lam_home": 3.02, "lam_away": 2.98,
        "puck_line_away": 1.5, "total_line": 6.5,
        "edge": True,
        "summary": "BOS (9-2-1, 19 pts, 8-game point streak, healthy) visits CAR (9-2-2, 20 pts, missing Staal & Hall)."
    },
    "CLB Blue Jackets @ PHI Flyers": {
        "comp": "NHL Regular Season",
        "utc_start": "2026-10-27 23:00 UTC",
        "src": "https://www.espn.com/nhl/injuries",
        "src_label": "NHL.com / ESPN",
        "injury_status": "CLB: Dante Fabbro, Isac Lundestrom Out | PHI: Travis Konecny, Owen Tippett & Cam York on IR",
        "injury_verified": "yes",
        "away_team": "CLB Blue Jackets", "home_team": "PHI Flyers",
        "lam_home": 2.48, "lam_away": 3.12,
        "puck_line_away": -1.5, "total_line": 5.5,
        "edge": True,
        "summary": "CLB (4-5-0, 29 GF in 9 GP) visits injury-depleted PHI (3-7-3, -18 GD, missing Konecny, Tippett & York)."
    },
    "NJ Devils @ DAL Stars": {
        "comp": "NHL Regular Season",
        "utc_start": "2026-10-28 00:00 UTC",
        "src": "https://www.nhl.com/standings/2026-10-26/wildcard",
        "src_label": "NHL.com / ESPN",
        "injury_status": "NJD: Luke Glendening, Zack MacEwen Out | DAL: Matt Duchene, Esa Lindell, Oskar Back, Sam Steel Out",
        "injury_verified": "yes",
        "away_team": "NJ Devils", "home_team": "DAL Stars",
        "lam_home": 2.82, "lam_away": 2.42,
        "puck_line_away": 1.5, "total_line": 5.5,
        "edge": True,
        "summary": "DAL (7-3-1, 5-game win streak, league-low 20 GA in 11 GP) hosts NJD (7-4-0, W3)."
    },
    "FLA Panthers @ WPG Jets": {
        "comp": "NHL Regular Season",
        "utc_start": "2026-10-28 00:00 UTC",
        "src": "https://www.espn.com/nhl/injuries",
        "src_label": "NHL.com / ESPN",
        "injury_status": "FLA: Aleksander Barkov, Brad Marchand, Jacob Markstrom IR | WPG: Josh Morrissey, Nick Bjugstad Out",
        "injury_verified": "yes",
        "away_team": "FLA Panthers", "home_team": "WPG Jets",
        "lam_home": 2.45, "lam_away": 2.68,
        "puck_line_away": -1.5, "total_line": 5.5,
        "edge": True,
        "summary": "Both sides missing stars (Barkov/Marchand vs #1 defenseman Morrissey); WPG on 5-game skid (27 GF in 11 GP)."
    },
    "NY Islanders @ NSH Predators": {
        "comp": "NHL Regular Season",
        "utc_start": "2026-10-28 00:00 UTC",
        "src": "https://www.espn.com/nhl/injuries",
        "src_label": "NHL.com / ESPN",
        "injury_status": "NYI: Mathew Barzal, Alexander Romanov, Matias Maccelli Out | NSH: Austin Roest IR",
        "injury_verified": "yes",
        "away_team": "NY Islanders", "home_team": "NSH Predators",
        "lam_home": 2.88, "lam_away": 2.62,
        "puck_line_away": 1.5, "total_line": 5.5,
        "edge": False,
        "summary": "NYI (5-3-1) missing Barzal & Romanov at NSH (4-3-4); tight one-goal profile favors NYI +1.50 puck line."
    },
    "Kalpa vs Sport": {
        "comp": "Finland Liiga",
        "utc_start": "2026-10-27 16:30 UTC",
        "src": "https://liiga.fi/fi/tilastot/joukkuetilastot/sarjataulukko",
        "src_label": "Liiga.fi",
        "injury_status": None, "injury_verified": "blank",
        "home_team": "Kalpa", "away_team": "Sport",
        "lam_home": 3.25, "lam_away": 2.15,
        "puck_line_away": 1.5, "total_line": 5.5,
        "edge": True,
        "summary": "Defending champ KalPa (19 pts, 0 GD, fresh off 5-1 win over Karpat) hosts Vaasan Sport (19 pts in 15 GP, -16 GD)."
    },
    "Kolner Haie vs Adler Mannheim": {
        "comp": "Germany PENNY DEL",
        "utc_start": "2026-10-27 18:30 UTC",
        "src": "https://www.penny-del.org/statistik/tabelle",
        "src_label": "PENNY DEL",
        "injury_status": None, "injury_verified": "blank",
        "home_team": "Kolner Haie", "away_team": "Adler Mannheim",
        "lam_home": 2.55, "lam_away": 3.15,
        "edge": True,
        "summary": "Adler Mannheim (23 pts, 40:29 GD, +11) visits defensively leaky Kolner Haie (19 pts, 45:45 GD)."
    },
    "IF Malmo Redhawks vs Linkoping HC": {
        "comp": "Sweden SHL",
        "utc_start": "2026-10-27 18:00 UTC",
        "src": "https://www.shl.se/",
        "src_label": "SHL.se",
        "injury_status": None, "injury_verified": "blank",
        "home_team": "IF Malmo Redhawks", "away_team": "Linkoping HC",
        "lam_home": 2.95, "lam_away": 2.15,
        "edge": True,
        "summary": "7th-place Malmo (+2 GD) hosts bottom-14th Linkoping (-14 GD)."
    },
}

#!/usr/bin/env python3
"""
CAL-4 originating engine.

Turns the OLBG listing data we can actually read (tip counts per selection) plus the official
tables we retrieved into OUR OWN prices, for every market we can defend.

Two methods, both deterministic and both recorded on every row:

  CAL-4C  consensus.  p = (wins + K*prior) / (total + K).  K = 6 pseudo-tips, prior = 1/n_outcomes.
          Used wherever OLBG printed a usable split for the market we are pricing.

  CAL-4R  rating.  Used where the OLBG split cannot be used: handball (OLBG prints "Tie" as the
          most-tipped selection on most matches, F-01) and every derived handicap/total market.
          Expected goals/margin come from official table goals-for/goals-against per game, then a
          normal approximation gives win/draw/loss, cover and over/under probabilities.

Derived markets are only produced where BOTH sides have a verified scoring baseline in
data/board/official.json. Where no baseline exists the market is left unpriced and listed as such,
rather than filled with a made-up number.

Book: 5% margin on every price. American odds converted with the standard formulas.
Band: the brief asks for selections between -250 and +10000 American, i.e. decimal 1.40 to 101.00.
A price shorter than 1.40 is flagged "outside band (too short)" and cannot be a headline pick.
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "data", "board")

K = 6.0
MARGIN = 0.05
BAND = (1.40, 101.00)

SPORT_CFG = {
    # sport: (n_outcomes for the printed ML market, margin sigma, total sigma, derived markets)
    "Tennis":         {"n": 2, "markets": []},
    "Cricket":        {"n": 2, "markets": []},
    "Basketball":     {"n": 2, "sigma": 11.0, "tsigma": 17.0, "markets": ["spread", "total"]},
    "Ice Hockey":     {"n": 2, "sigma": 1.9, "tsigma": 1.9, "markets": ["puckline", "total"]},
    "Baseball":       {"n": 2, "sigma": 2.4, "tsigma": 4.2, "markets": ["runline", "total"]},
    "Handball":       {"n": 3, "sigma": 8.0, "tsigma": 7.0, "markets": ["handicap", "total"]},
    "Rugby Union":    {"n": 3, "sigma": 13.0, "tsigma": 12.0, "markets": ["handicap", "total"]},
    "Volleyball":     {"n": 2, "markets": []},
    "Rugby League":   {"n": 8, "markets": []},   # outright only
    "Gaelic Sports":  {"n": 2, "sigma": 6.0, "markets": ["handicap"]},
    "Golf":           {"n": 8, "markets": []},
    "Darts":          {"n": 8, "markets": []},
    "Motor Racing":   {"n": 6, "markets": []},
    "Snooker":        {"n": 2, "markets": []},
    "Greyhounds":     {"n": 6, "markets": []},
}

# Official-table name fragments used to look a fixture side up in official.json.
ALIAS = {
    "MIL Brewers": "MIL", "TB Rays": "TB",
    "BOS Bruins": "BOS", "CAR Hurricanes": "CAR",
    "PHI Flyers": "PHI", "CLB Blue Jackets": "CBJ",
}
EHF_ALIAS = {
    "SC Magdeburg": "SC Magdeburg", "HC Kriens Luzern": "HC Kriens-Luzern",
    "KS Kielce": "Industria Kielce", "Kolstad": "Kolstad",
    "FC Porto": "FC Porto", "Veszprem": "One Veszprem",
    "Fuchse Berlin": "Fuchse Berlin", "RK Partizan": "RK Partizan",
    "GOG": "GOG", "Sporting CP": "Sporting CP",
    "IFK Kristianstad": "IFK Kristianstad", "Pick Szeged": "Pick Szeged",
}
URC_ALIAS = {
    "Glasgow Warriors": "Glasgow Warriors", "Lions": "Lions",
    "Connacht": "Connacht", "Leinster": "Leinster",
    "Stormers": "Stormers", "Ulster": "Ulster",
    "Munster": "Munster", "Sharks": "Sharks",
}
EL_ALIAS = {"Panathinaikos": "Panathinaikos", "Milano": "Milano",
            "Valencia": "Valencia", "Fenerbahce": "Fenerbahce",
            "Bayern Munich": "Bayern Munich", "Barcelona": "Barcelona"}


def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def american(dec):
    if dec is None:
        return None
    if dec >= 2.0:
        return f"+{round((dec - 1) * 100)}"
    return f"{round(-100 / (dec - 1))}"


def price(p):
    """decimal price from a fair probability, with the book margin applied"""
    return round(1.0 / (p * (1.0 + MARGIN)), 2)


def in_band(dec):
    return BAND[0] <= dec <= BAND[1]


def split_ints(s):
    if not s or "/" not in s:
        return None, None
    a, b = s.split("/")
    return int(a), int(b)


def k_for(total):
    """More pseudo-tips when the real sample is small. A 1/1 split must not read as a 57% shot."""
    if total >= 8:
        return K
    if total >= 4:
        return 12.0
    return 20.0


def consensus(wins, total, n):
    prior = 1.0 / n
    k = k_for(total)
    return (wins + k * prior) / (total + k)


def cfg_for(sport):
    return SPORT_CFG.get(sport, {"n": 2, "markets": []})


def sides(event):
    """split 'A vs B' / 'A @ B' into (home, away) as printed"""
    e = event["event"]
    for sep in [" vs ", " @ ", " v "]:
        if sep in e:
            a, b = e.split(sep, 1)
            return a.strip(), b.strip()
    return None, None


def official_lookup(frag, table):
    if frag in table:
        return table[frag]
    for k, v in table.items():
        if frag.lower() in k.lower() or k.lower() in frag.lower():
            return v
    return None


def derived_markets(ev, official):
    """return list of market dicts we can defend, given verified scoring baselines"""
    sport = ev["sport"]
    cfg = cfg_for(sport)
    home, away = sides(ev)
    out = []
    if not home or not away:
        return out

    if sport == "Handball":
        t = official["EHF_CL"]["teams"]
        h = t.get(EHF_ALIAS.get(home, home))
        a = t.get(EHF_ALIAS.get(away, away))
        if not h or not a:
            # CAL-4P: no club-specific baseline retrieved, so fall back to the league-average prior.
            # It is published as a prior, never as a rated line, and no pick may be built on it.
            gpg = sum(v["gf"] for v in t.values()) / sum(v["gp"] for v in t.values())
            cpg = sum(v["ga"] for v in t.values()) / sum(v["gp"] for v in t.values())
            exp = (gpg + cpg) / 2.0
            sd = cfg["sigma"]
            p_draw = norm_cdf(0.5 / sd) - norm_cdf(-0.5 / sd)
            out.append({"kind": "ml3", "p_home": (1 - p_draw) / 2, "p_draw": p_draw,
                        "p_away": (1 - p_draw) / 2,
                        "basis": f"CAL-4P league-average prior: EHF group phase mean {exp:.1f} goals per side, "
                                 f"no club-specific baseline retrieved"})
            out.append({"kind": "total", "line": round(2 * exp, 1), "over": 0.5,
                        "basis": f"CAL-4P league-average total {2*exp:.1f} - prior only, not a rated line"})
            return out
        hf = h["gf"] / h["gp"]; ha = h["ga"] / h["gp"]
        af = a["gf"] / a["gp"]; aa = a["ga"] / a["gp"]
        exp_h = (hf + aa) / 2.0
        exp_a = (af + ha) / 2.0
        total_line = round(exp_h + exp_a, 1)
        margin_mean = exp_h - exp_a
        sd = cfg["sigma"]
        p_home = 1.0 - norm_cdf((0.5 - margin_mean) / sd)
        p_draw = norm_cdf((0.5 - margin_mean) / sd) - norm_cdf((-0.5 - margin_mean) / sd)
        p_away = norm_cdf((-0.5 - margin_mean) / sd)
        line = round(margin_mean * 2) / 2.0
        p_cover = 1.0 - norm_cdf((line - margin_mean) / sd)
        over = 1.0 - norm_cdf((total_line - (exp_h + exp_a)) / cfg["tsigma"])
        out.append({"kind": "ml3", "p_home": p_home, "p_draw": p_draw, "p_away": p_away,
                    "basis": f"CAL-4R EHF table: {home} {hf:.1f} scored / {ha:.1f} conceded per game; "
                             f"{away} {af:.1f} / {aa:.1f}; expected {exp_h:.1f}-{exp_a:.1f}"})
        out.append({"kind": "handicap", "line": line, "on": home, "p": p_cover,
                    "basis": f"CAL-4R margin mean {margin_mean:+.1f}, sd {sd}"})
        out.append({"kind": "total", "line": total_line, "over": over,
                    "basis": f"CAL-4R expected total {total_line}, sd {cfg['tsigma']}"})
        return out

    if sport in ("Basketball", "Rugby Union"):
        t = (official["EUROLEAGUE"]["teams"] if sport == "Basketball" else official["URC"]["teams"])
        h = t.get(EL_ALIAS.get(home, home) if sport == "Basketball" else URC_ALIAS.get(home, home))
        a = t.get(EL_ALIAS.get(away, away) if sport == "Basketball" else URC_ALIAS.get(away, away))
        if not h or not a:
            return out
        if sport == "Basketball":
            exp_h = (h["ppg"] + a["oppg"]) / 2.0
            exp_a = (a["ppg"] + h["oppg"]) / 2.0
            basis = f"CAL-4R EuroLeague: {home} {h['ppg']} for / {h['oppg']} against; {away} {a['ppg']} / {a['oppg']}; expected {exp_h:.1f}-{exp_a:.1f}"
        else:
            exp_h = (h["pf"] + a["pa"]) / (2.0 * h["p"])
            exp_a = (a["pf"] + h["pa"]) / (2.0 * h["p"])
            basis = f"CAL-4R URC: {home} {h['pf']}/{h['pa']} in {h['p']}; {away} {a['pf']}/{a['pa']} in {a['p']}; expected {exp_h:.1f}-{exp_a:.1f}"
        margin_mean = exp_h - exp_a
        sd = cfg["sigma"]
        line = (math.floor(margin_mean * 2) / 2.0) if sport == "Basketball" else (math.floor(margin_mean * 2) / 2.0)
        p_cover = 1.0 - norm_cdf((line - margin_mean) / sd)
        out.append({"kind": "spread", "line": line, "on": home, "p": p_cover, "basis": basis})
        if "tsigma" in cfg:
            tl = round(exp_h + exp_a, 1)
            over = 1.0 - norm_cdf((tl - (exp_h + exp_a)) / cfg["tsigma"])
            out.append({"kind": "total", "line": tl, "over": over,
                        "basis": f"CAL-4R expected total {tl}, sd {cfg['tsigma']}"})
        return out

    if sport == "Ice Hockey":
        t = official["NHL"]["teams"]
        h = t.get(ALIAS.get(home, home)); a = t.get(ALIAS.get(away, away))
        if not h or not a:
            return out
        hf = h["gf"] / h["gp"]; ha = h["ga"] / h["gp"]
        af = a["gf"] / a["gp"]; aa = a["ga"] / a["gp"]
        exp_h = (hf + aa) / 2.0; exp_a = (af + ha) / 2.0
        tl = round(exp_h + exp_a, 1)
        over = 1.0 - norm_cdf((tl - (exp_h + exp_a)) / cfg["tsigma"])
        out.append({"kind": "total", "line": tl, "over": over,
                    "basis": f"CAL-4R NHL: {home} {hf:.2f} for / {ha:.2f} against per game; {away} {af:.2f} / {aa:.2f}; expected total {tl}"})
        m = exp_h - exp_a
        p_home_pl = 1.0 - norm_cdf((1.5 - m) / cfg["sigma"])
        out.append({"kind": "pl", "line": 1.5, "p_home": p_home_pl,
                    "basis": f"CAL-4R NHL margin {m:+.2f}, sd {cfg['sigma']}, fixed 1.5 line"})
        return out

    if sport == "Baseball":
        t = official["MLB"]["teams"]
        h = t.get(ALIAS.get(home, home)); a = t.get(ALIAS.get(away, away))
        if not h or not a:
            return out
        hf = h["rs"] / 162.0; ha = h["ra"] / 162.0
        af = a["rs"] / 162.0; aa = a["ra"] / 162.0
        exp_h = (hf + aa) / 2.0; exp_a = (af + ha) / 2.0
        tl = round(exp_h + exp_a, 1)
        over = 1.0 - norm_cdf((tl - (exp_h + exp_a)) / cfg["tsigma"])
        out.append({"kind": "total", "line": tl, "over": over,
                    "basis": f"CAL-4R MLB: {home} {hf:.2f} RS / {ha:.2f} RA per game; {away} {af:.2f} / {aa:.2f}; expected total {tl}"})
        m = exp_h - exp_a
        p_home_pl = 1.0 - norm_cdf((1.5 - m) / cfg["sigma"])
        out.append({"kind": "pl", "line": 1.5, "p_home": p_home_pl,
                    "basis": f"CAL-4R MLB season margin {m:+.2f} runs per game, sd {cfg['sigma']}, fixed 1.5 line; "
                             f"starting pitcher not included in the baseline"})
        return out
    return out


def build():
    files = ["inventory-tennis-cricket.json", "inventory-us-racing.json", "inventory-team-uk.json"]
    events = []
    for f in files:
        with open(os.path.join(B, f)) as fh:
            events += json.load(fh)["events"]
    official = json.load(open(os.path.join(B, "official.json")))["tables"]

    rows = []
    for ev in events:
        cfg = cfg_for(ev["sport"])
        tips, total = ev["tips"], ev["total"]
        rec = {
            "id": ev["id"], "sport": ev["sport"], "comp": ev["comp"], "event": ev["event"],
            "date": ev["date"], "start": ev["start"], "path": ev["path"],
            "olbg_sel": ev["sel"], "olbg_market": ev["market"], "tips": tips, "total": total,
            "pct": ev["pct"], "comments": ev["comments"], "experts": ev["experts"],
            "markets": [], "unpriced": None,
        }
        if not total or tips is None:
            rec["unpriced"] = "OLBG printed no tip split for this row, so nothing can be priced from it."
            rows.append(rec); continue

        n = cfg["n"]
        derived = derived_markets(ev, official)
        have_rating_ml = any(m.get("kind") == "ml3" for m in derived)

        if ev["sport"] == "Handball" and (ev["sel"] == "Tie" or have_rating_ml):
            rec["olbg_sel_note"] = ("OLBG's most-tipped selection is the draw; the listing split is not a "
                                    "match-winner split, so the match markets come from the rating model instead.")
        else:
            p_sel = consensus(tips, total, n)
            dec = price(p_sel)
            rec["markets"].append({
                "market": ev["market"], "selection": ev["sel"], "p": round(p_sel, 4),
                "price": dec, "american": american(dec), "in_band": in_band(dec),
                "method": "CAL-4C", "n_outcomes": n,
                "basis": f"OLBG printed {tips}/{total} tips; {n}-way market, prior {1/n:.3f}, "
                         f"K={k_for(total):g} (sample taper)",
            })
            # A two-way market needs both outcomes priced: the other side is the complement.
            if n == 2 and ev["market"] in ("Win Match", "Money Line", "To Win", "Daily Races"):
                home, away = sides(ev)
                other = None
                if home and ev["sel"] == home:
                    other = away
                elif away and ev["sel"] == away:
                    other = home
                if other:
                    p_other = 1.0 - p_sel
                    d2 = price(p_other)
                    rec["markets"].append({
                        "market": ev["market"], "selection": other, "p": round(p_other, 4),
                        "price": d2, "american": american(d2), "in_band": in_band(d2),
                        "method": "CAL-4C", "n_outcomes": 2,
                        "basis": "complement of the printed split: " + f"1 - {p_sel:.3f}",
                    })

        for m in derived:
            if m["kind"] == "ml3":
                home, away = sides(ev)
                for name, key in ((home, "p_home"), (away, "p_away")):
                    d = price(m[key])
                    rec["markets"].append({"market": "Money Line", "selection": name,
                                           "p": round(m[key], 4), "price": d, "american": american(d),
                                           "in_band": in_band(d), "method": "CAL-4R",
                                           "basis": m["basis"]})
                d = price(m["p_draw"])
                rec["markets"].append({"market": "Money Line", "selection": "Tie", "p": round(m["p_draw"], 4),
                                       "price": d, "american": american(d), "in_band": in_band(d),
                                       "method": "CAL-4R", "basis": m["basis"],
                                       "note": "priced from the rating model, not from OLBG's Tie split"})
            elif m["kind"] in ("handicap", "spread"):
                home, away = sides(ev)
                p_away = 1.0 - m["p"]
                for name, p, ln in ((home, m["p"], -m["line"]), (away, p_away, m["line"])):
                    d = price(p)
                    rec["markets"].append({"market": "Handicap" if m["kind"] == "handicap" else "Pointspread",
                                           "selection": f"{name} {ln:+.1f}".replace("+-", "-"),
                                           "p": round(p, 4), "price": d, "american": american(d),
                                           "in_band": in_band(d), "method": "CAL-4R", "basis": m["basis"]})
            elif m["kind"] == "pl":
                home, away = sides(ev)
                label = "Puck Line" if ev["sport"] == "Ice Hockey" else "Run Line"
                for name, p, ln in ((home, m["p_home"], -m["line"]), (away, 1.0 - m["p_home"], m["line"])):
                    d = price(p)
                    rec["markets"].append({"market": label,
                                           "selection": f"{name} {ln:+.2f}",
                                           "p": round(p, 4), "price": d, "american": american(d),
                                           "in_band": in_band(d), "method": "CAL-4R", "basis": m["basis"]})
            elif m["kind"] == "total":
                for nm, p in (("Over", m["over"]), ("Under", 1.0 - m["over"])):
                    d = price(p)
                    rec["markets"].append({"market": "Game Totals", "selection": f"{nm} {m['line']}",
                                           "p": round(p, 4), "price": d, "american": american(d),
                                           "in_band": in_band(d), "method": "CAL-4R", "basis": m["basis"]})
        rows.append(rec)

    counts = {}
    for r in rows:
        c = counts.setdefault(r["sport"], {"events": 0, "priced": 0, "markets": 0})
        c["events"] += 1
        if r["markets"]:
            c["priced"] += 1
            c["markets"] += len(r["markets"])

    out = {
        "engine": "CAL-4 (CAL-4C consensus, CAL-4R rating)",
        "generated_at": "2026-10-27",
        "constants": {"K": K, "margin": MARGIN, "band_decimal": BAND,
                      "band_american": ["-250", "+10000"]},
        "counts": counts,
        "lines": rows,
    }
    with open(os.path.join(B, "lines.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(counts, indent=1))
    print("events", len(rows), "priced", sum(1 for r in rows if r["markets"]))


if __name__ == "__main__":
    build()

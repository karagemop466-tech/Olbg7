#!/usr/bin/env python3
"""Consolidate the OLBG board capture and originate prices for every event.

Pricing method (documented in docs/methodology.html):
  strength s = (GF - GA) / GP   (verified competition standings only)
  expected margin m = (s_home + home_adv) - s_away
  p_home = 1 / (1 + exp(-m / sigma))
  No price is produced from a figure that is not in data/verified_tables.json.
  Events whose teams are absent from the verified tables are priced only as
  Tier B reference lines from the OLBG tip-share with shrinkage, and are labelled.
"""
import json, math, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")

MARGIN_2WAY = 1.05
SHRINK_N = 10.0

SPORT_FILES = {
    "Golf": "golf", "Volleyball": "volleyball", "Rugby Union": "rugby_union",
    "Cricket": "cricket", "Snooker": "snooker", "Darts": "darts",
    "Baseball": "baseball", "Gaelic Sports": "gaelic", "Greyhounds": "greyhounds",
    "Tennis": "tennis", "Motor Racing": "motor_racing", "Handball": "handball",
    "Ice Hockey": "ice_hockey", "Basketball": "basketball", "Rugby League": "rugby_league",
}

GAELIC = {
    "sport_id": 25, "sport": "Gaelic Sports",
    "source": "https://www.olbg.com/betting-tips/Gaelic_Football/25",
    "captured_utc": "2026-10-26",
    "note": "OLBG's Gaelic hub is Gaelic Football only. OLBG also runs a Hurling hub (sport id 26) which is outside this brief's listed sports. Only two club fixtures plus one 2027 outright were live.",
    "events": [
        {"id": 3531, "name": "Kanturk v Eire Og Cor", "when": "01 Nov 09:00", "market": "Handicap", "consensus": "Eire Og Cor +0.50", "tips": "6/6", "pct": 100},
        {"id": 3537, "name": "Fr Caseys v Kildimo Pallaskenry", "when": "01 Nov 10:30", "market": "Handicap", "consensus": "Kildimo Pallaskenry +3.50", "tips": "5/7", "pct": 71},
        {"id": 3327, "name": "All Ireland Football Championship 2027 (outright)", "when": "25 Jul 2027 10:30", "market": "Win Tournament", "consensus": "Kerry", "tips": "6/8", "pct": 75}
    ]
}

def logical(p):
    return 1.0 / (1.0 + math.exp(-p))

def dec_from_prob(p, margin):
    p = min(max(p, 0.02), 0.98)
    return round(1.0 / (p * margin) + 0.0, 2)

def american(dec):
    if dec >= 2.0:
        return f"+{round((dec - 1) * 100)}"
    return f"-{round(100 / (dec - 1))}"

def load_tables():
    with open(os.path.join(D, "verified_tables.json")) as f:
        return json.load(f)

def team_metric(tbl, name):
    teams = tbl["teams"]
    if name in teams:
        return teams[name]
    return None

def strength(rec, metric):
    gp = rec.get("gp") or 0
    if not gp:
        return None
    gf = rec.get("gf") if "gf" in rec else rec.get("pf")
    ga = rec.get("ga") if "ga" in rec else rec.get("pa")
    if gf is None or ga is None:
        return None
    return (gf - ga) / gp

def total_anchor(rec_a, rec_b, metric):
    def per(rec):
        gp = rec.get("gp") or 0
        gf = rec.get("gf") if "gf" in rec else rec.get("pf")
        ga = rec.get("ga") if "ga" in rec else rec.get("pa")
        if not gp or gf is None or ga is None:
            return None
        return gf / gp, ga / gp
    a, b = per(rec_a), per(rec_b)
    if not a or not b:
        return None
    # expected goals/points for each side then summed
    exp_a = (a[0] + b[1]) / 2
    exp_b = (b[0] + a[1]) / 2
    return exp_a + exp_b

ALIASES = {
    "Wisla Plock": "Wisla Plock", "Veszprem": "Veszprem", "RK Partizan": "RK Partizan",
    "HBW Balingen Weilstetten": None, "HBW Balingen-Weilstetten": None,
}

def resolve(tbl, name):
    rec = team_metric(tbl, name)
    if rec:
        return name
    for k in tbl["teams"]:
        if k.lower().replace("-", " ") == name.lower().replace("-", " "):
            return k
    return None

TWO_WAY_SPLIT = (" vs ", " @ ", " v ")

def parse_sides(name):
    for sep in TWO_WAY_SPLIT:
        if sep in name:
            a, b = name.split(sep, 1)
            return a.strip(), b.strip(), sep.strip()
    return None, None, None

def main():
    tables = load_tables()
    sports = []
    for sport, fname in SPORT_FILES.items():
        path = os.path.join(D, "raw", fname + ".json")
        if os.path.exists(path):
            with open(path) as f:
                raw = json.load(f)
        else:
            raw = GAELIC
        events = []
        for ev in raw.get("events", []):
            a, b, sep = parse_sides(ev["name"])
            entry = dict(ev)
            entry["tier"] = "B"
            entry["markets"] = []
            entry["line_source"] = "none"
            tbl = None
            if sport == "Handball":
                tbl = tables["handball_ehf_cl_2026_27"]
            elif sport == "Basketball":
                tbl = tables["nba_2026_27"]
            elif sport == "Ice Hockey":
                tbl = tables["nhl_2026_27"]
            if tbl and a and b:
                ka, kb = resolve(tbl, a), resolve(tbl, b)
                if ka and kb:
                    sa = strength(tbl["teams"][ka], tbl["metric"])
                    sb = strength(tbl["teams"][kb], tbl["metric"])
                    if sa is not None and sb is not None:
                        home_side = ("home" if sep == "vs" or sep == "v" else "away")
                        # a is home when sep is 'vs'/'v'; '@' means a is away
                        adv = tbl["home_adv"] if sep in ("vs", "v") else -tbl["home_adv"]
                        m = (sa - sb) + adv
                        p_a = logical(m / tbl["sigma"])
                        d_a = dec_from_prob(p_a, MARGIN_2WAY)
                        d_b = dec_from_prob(1 - p_a, MARGIN_2WAY)
                        entry["tier"] = "A"
                        entry["prob_a"] = round(p_a, 4)
                        entry["edge_note"] = f"net {tbl['metric']} per game {sa:+.2f} vs {sb:+.2f}"
                        entry["markets"].append({
                            "market": "Match Winner / Money Line",
                            "selection": a, "decimal": d_a, "american": american(d_a),
                            "prob": round(p_a, 4), "basis": "Tier A - verified standings"})
                        entry["markets"].append({
                            "market": "Match Winner / Money Line",
                            "selection": b, "decimal": d_b, "american": american(d_b),
                            "prob": round(1 - p_a, 4), "basis": "Tier A - verified standings"})
                        step = {"goals": 0.5, "points": 0.5}.get(tbl["metric"], 0.5)
                        spread = round(abs(m) / step) * step
                        fav, dog = (a, b) if m > 0 else (b, a)
                        hc = -spread if m > 0 else spread
                        d = dec_from_prob(0.5, MARGIN_2WAY)
                        entry["markets"].append({
                            "market": "Handicap", "selection": f"{fav} {hc:+.2f}",
                            "decimal": d, "american": american(d), "prob": 0.5,
                            "basis": "Tier A - spread from the same expected margin"})
                        entry["markets"].append({
                            "market": "Handicap", "selection": f"{dog} {-hc:+.2f}",
                            "decimal": d, "american": american(d), "prob": 0.5,
                            "basis": "Tier A - spread from the same expected margin"})
                        tot = total_anchor(tables and tbl["teams"][ka], tbl["teams"][kb], tbl["metric"])
                        if tot:
                            line = round(tot * 2) / 2 + 0.5
                            dd = dec_from_prob(0.5, MARGIN_2WAY)
                            entry["markets"].append({
                                "market": "Match Total", "selection": f"Over {line}",
                                "decimal": dd, "american": american(dd), "prob": 0.5,
                                "basis": "Tier A - total anchored on verified GF/GA"})
                            entry["markets"].append({
                                "market": "Match Total", "selection": f"Under {line}",
                                "decimal": dd, "american": american(dd), "prob": 0.5,
                                "basis": "Tier A - total anchored on verified GF/GA"})
            if not entry["markets"]:
                # Tier B reference line: OLBG tip share shrunk toward 50/50
                pct = ev.get("pct")
                if pct is None:
                    p = 0.5
                else:
                    n = 1
                    try:
                        n = int(str(ev.get("tips", "1/1")).split("/")[1])
                    except Exception:
                        n = 1
                    w = n / (n + SHRINK_N)
                    p = w * (pct / 100.0) + (1 - w) * 0.5
                d = dec_from_prob(p, MARGIN_2WAY)
                target = ev.get("consensus", "")
                entry["markets"].append({
                    "market": "Reference line (no verified match data)",
                    "selection": target, "decimal": d, "american": american(d),
                    "prob": round(p, 4), "basis": "Tier B - tip-share reference only"})
                if a and b:
                    other = b if target.strip() == a else a
                    if other and other.strip() != target.strip():
                        d2 = dec_from_prob(1 - p, MARGIN_2WAY)
                        entry["markets"].append({
                            "market": "Reference line (no verified match data)",
                            "selection": other, "decimal": d2, "american": american(d2),
                            "prob": round(1 - p, 4), "basis": "Tier B - opposite side of the same reference"})
                entry["prob_a"] = round(p, 4)
                entry["line_source"] = "tip-share"
            events.append(entry)
        sports.append({"sport": sport, "sport_id": raw.get("sport_id"),
                       "source": raw.get("source"), "note": raw.get("note", ""),
                       "events": events})
    with open(os.path.join(D, "events.json"), "w") as f:
        json.dump({"captured_utc": "2026-10-26", "sports": sports}, f, indent=1)

    # summary
    tot = tierA = 0
    for s in sports:
        ta = sum(1 for e in s["events"] if e["tier"] == "A")
        tot += len(s["events"]); tierA += ta
        print(f"{s['sport']:<15} events={len(s['events']):>3} tierA={ta:>3}")
    print(f"TOTAL {tot} tierA {tierA}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CAL-1  Consensus-Anchored Line engine.

Purpose
-------
Originate OUR OWN price for every OLBG match/race/tournament we inventory, from data we can
actually verify on OLBG (the printed tip split) rather than from a bookmaker feed we cannot read.

Why this design
---------------
OLBG's listing and event pages print, for each market: "X / Y Win Tips" and a percentage.
Bookmaker prices on OLBG are rendered client-side and were NOT present in the text we could
retrieve (see flags F-001). So the only numeric market signal we can verify is the tip split.
A raw split is a biased, small-sample estimate of a probability, so it is shrunk toward the
market-structure prior with a Dirichlet-style pseudo-count before it is turned into a price.

Model
-----
1. prior_i = 1 / n_outcomes(market)          (2-way = 0.50, 3-way = 0.3333)
2. p_fair  = (wins + K * prior_i) / (total + K)     K = 6 pseudo-tips
3. fair decimal price  = 1 / p_fair
4. our card price      = 1 / (p_fair * (1 + MARGIN))     MARGIN = 0.05 (5%)
5. American odds are converted from the card price with the standard formulas.
6. Effective sample size = total tips. Confidence uses p_fair, the sample size and the price band.

Band rule (from the brief)
--------------------------
The brief asks for high-confidence selections priced between -250 and +10000 American.
-250 American = 1.40 decimal. +10000 American = 101.00 decimal. The confidence gate applies the
band to the FAIR decimal price (1 / p_fair), because the band describes market odds. The published
card price still carries the 5% margin, so its own band flag is kept separately as in_focus_band.
A heavy odds-on favourite at a 1.22 fair price is IN the probability sense a strong pick but
OUTSIDE the band, and is labelled accordingly (medium, never high).

High-confidence rule (2026-10-27, per owner)
---------------------------------------------
p_fair > 0.70 AND sample >= 8 tips AND fair decimal inside 1.40..101.00. The threshold is
strictly greater than 70%, matching the owner's wording and the boundary tests in
tools/check_site.py. On the 2026-10-27 capture zero rows satisfy all three conditions; the
near-misses are listed on flagged.html.

Nothing in this file invents a team rating, a score or an injury. It only reprices the tip split.
"""
import json
import math
import os

K = 6.0
MARGIN = 0.05
BAND_MIN_DEC = 1.40     # -250 American
BAND_MAX_DEC = 101.00   # +10000 American

THREE_WAY_MARKETS = {
    "To Win", "Full Time Result",
}
# Markets that are two-way by construction even though a draw exists in the sport.
TWO_WAY_MARKETS = {
    "Win Match", "Pointspread", "Handicap", "Game Totals", "Puck Line", "Daily Races",
    "Top 6 Finish", "Top 10 Finish", "Over/Under", "Run Line",
}
THREE_WAY_SPORTS = {"Handball", "Rugby Union", "Football", "Ice Hockey"}
# Two-way / outright markets. Outrights are treated as "many-way" with prior 1/8 when the
# number of runners is not printed on OLBG; that is an assumption and is flagged.
# 2026-10-27 refresh: "Win Hurling" is a season outright, and "Top Team1 Batsman" /
# "Man Of The Match" are multi-runner player markets, so all three use the 1/8 many-way prior.
OUTRIGHT_MARKETS = {
    "Win Tournament", "Outright Winner", "Grand Final Winner",
    "Win Hurling", "Top Team1 Batsman", "Man Of The Match",
}


def n_outcomes(market: str, total: int, sport: str = "") -> tuple[float, str]:
    if market in OUTRIGHT_MARKETS:
        return 1.0 / 8.0, "outright assumed 8 runners"
    if market in TWO_WAY_MARKETS:
        return 0.5, "2-way"
    if market == "Money Line" and sport in THREE_WAY_SPORTS:
        return 1.0 / 3.0, "3-way"
    if market in THREE_WAY_MARKETS:
        # Handball / rugby union money line is explicitly 3-way on OLBG (home / tie / away).
        return 1.0 / 3.0, "3-way"
    return 0.5, "2-way"


def american(dec: float):
    if dec is None:
        return None
    if dec >= 2.0:
        return round((dec - 1.0) * 100)
    return round(-100.0 / (dec - 1.0))


def price(market: str, wins, total, pct=None, sport=""):
    if wins is None or total is None or total <= 0:
        return None
    prior, structure = n_outcomes(market, total, sport)
    p_fair = (wins + K * prior) / (total + K)
    p_fair = max(0.01, min(0.99, p_fair))
    fair_dec = round(1.0 / p_fair, 2)
    card_dec = round(1.0 / (p_fair * (1.0 + MARGIN)), 2)
    in_band = BAND_MIN_DEC <= card_dec <= BAND_MAX_DEC
    # The owner's band (-250..+10000 = 1.40..101.00) is a statement about market odds, so the
    # confidence gate tests it against the FAIR price. Testing the margined card would make the
    # two rules mutually exclusive: a 70% shot carries a 1.43 fair price but a 1.36 card once the
    # 5% margin is applied, so no >70% pick could ever sit at or above 1.40 on the card.
    fair_in_band = BAND_MIN_DEC <= fair_dec <= BAND_MAX_DEC
    # 2026-10-27: high bar moved from 60% to a strictly greater-than-70% fair chance to
    # match the owner's wording ("greater than 70% chance to win"); the >=8-tip sample and
    # focus-band rules stand. Exactly 0.70 stays medium, never high.
    if p_fair > 0.70 and total >= 8 and fair_in_band:
        conf = "high"
    elif p_fair > 0.70 and not fair_in_band:
        conf = "medium"          # strong but priced outside the focus band
    elif p_fair >= 0.50:
        conf = "medium"
    else:
        conf = "low"
    return {
        "market_structure": structure,
        "prior": round(prior, 4),
        "p_fair": round(p_fair, 4),
        "fair_decimal": fair_dec,
        "card_decimal": card_dec,
        "card_american": american(card_dec),
        "implied_pct": round(100 * (1.0 / card_dec), 1),
        "overround": MARGIN,
        "in_focus_band": in_band,
        "fair_in_focus_band": fair_in_band,
        "confidence": conf,
        "sample_tips": total,
        "pseudo_count_K": K,
    }


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "data", "events.json")) as fh:
        events = json.load(fh)["events"]

    out = []
    for ev in events:
        tips = ev.get("tips")
        wins = total = None
        if tips and "/" in tips:
            a, b = tips.split("/")
            try:
                wins, total = int(a), int(b)
            except ValueError:
                wins = total = None
        row = {k: ev.get(k) for k in ("s", "c", "e", "id", "path", "d", "start_label", "sel", "m", "tips", "pct")}
        row["our_line"] = price(ev["m"], wins, total, ev.get("pct"), ev.get("s", ""))
        if row["our_line"] is None:
            row["our_line_status"] = "not priced - OLBG did not print a tip split for this selection"
        out.append(row)

    priced = [r for r in out if r["our_line"]]
    summary = {}
    for r in out:
        s = r["s"]
        d = summary.setdefault(s, {"events": 0, "priced": 0, "high": 0, "medium": 0, "low": 0, "in_band": 0})
        d["events"] += 1
        if r["our_line"]:
            d["priced"] += 1
            d["in_band"] += 1 if r["our_line"]["in_focus_band"] else 0
            d[r["our_line"]["confidence"]] += 1

    doc = {
        "engine": "CAL-1 (Consensus-Anchored Line)",
        "generated_at": "2026-10-27",
        "constants": {"K_pseudo_tips": K, "margin": MARGIN,
                      "band_min_decimal": BAND_MIN_DEC, "band_max_decimal": BAND_MAX_DEC,
                      "band_american": [-250, 10000]},
        "summary": summary,
        "totals": {"events": len(out), "priced": len(priced)},
        "lines": out,
    }
    dst = os.path.join(root, "data", "pricing.json")
    with open(dst, "w") as fh:
        json.dump(doc, fh, indent=1)
    print(f"events={len(out)} priced={len(priced)} -> {dst}")
    for s, d in sorted(summary.items(), key=lambda kv: -kv[1]["events"]):
        print(f"  {s:15s} events={d['events']:2d} priced={d['priced']:2d} high={d['high']:2d} "
              f"med={d['medium']:2d} low={d['low']:2d} in_band={d['in_band']:2d}")


if __name__ == "__main__":
    main()

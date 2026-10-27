#!/usr/bin/env python3
"""price_today.py - originate our own line for every OLBG market captured today.

Engine "TS-27". Two inputs per row, blended where both exist:

  market input   the OLBG tip split, shrunk toward a market-structure prior
  form input     a win% / points% / win-rate pulled from an official league table,
                 turned into a home-away probability by a logistic function

Nothing is typed by hand into data/today/lines.json: this script produces it.

Run:  python3 tools/price_today.py
"""
import json
import math
import os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPTURE = os.path.join(ROOT, "data", "today", "capture.json")
FORM = os.path.join(ROOT, "data", "today", "form.json")
OUT = os.path.join(ROOT, "data", "today", "lines.json")

# --- constants, all published on the method page -------------------------------
SHRINK_K = 6.0          # pseudo-tips pulling a split toward the prior
MARGIN = 1.02           # 2% margin: a 70% chance lands on -250, the floor of our band
HOME_EDGE = 0.05        # added to the home side's strength differential
SCALE = 0.70            # logistic scale on a win-percentage differential
SPREAD = {"Basketball": 11.5, "Ice Hockey": 1.9, "Baseball": 3.2, "Handball": 6.5}
LINE_RE = True
BAND_LOW = -250.0       # shortest price we will publish as a pick
BAND_HIGH = 10000.0
PRIOR_TWO_WAY = 0.50
PRIOR_THREE_WAY = 0.42
PRIOR_OUTRIGHT = 0.10
W_FORM = 0.50
W_MARKET = 0.50

OUTRIGHT = {"Win Tournament", "Grand Final Winner", "Outright Winner"}
HANDICAP_MARKETS = {"Handicap", "Pointspread", "Puck Line", "Run Line", "Game Totals", "Podium Finish"}
THREE_WAY_SPORTS = {"Handball", "Rugby Union", "Ice Hockey"}


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def inv_phi(p):
    """Bisection on phi(). No dependency, plenty accurate at 60 iterations."""
    lo, hi = -8.0, 8.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def parse_line(sel):
    """'Panathinaikos -13.50' -> -13.5 ; 'BOS Bruins +1.50' -> 1.5 ; None otherwise."""
    for tok in sel.split():
        try:
            if tok[0] in "+-" and len(tok) > 1 and tok[1].isdigit():
                return float(tok)
        except IndexError:
            continue
    return None


def to_american(dec):
    if dec >= 2.0:
        return round((dec - 1.0) * 100.0)
    return round(-100.0 / (dec - 1.0))


def band_ok(am):
    return BAND_LOW <= am <= BAND_HIGH


def prior_for(row):
    if row["market"] in OUTRIGHT:
        return PRIOR_OUTRIGHT
    if row["market"] in HANDICAP_MARKETS:
        return PRIOR_TWO_WAY
    if row["sport"] in THREE_WAY_SPORTS:
        return PRIOR_THREE_WAY
    return PRIOR_TWO_WAY


DRAW_SHARE = 0.09       # EHF Champions League draw rate carried into our handball sides


def p_market(row):
    w, t = row.get("tips_w"), row.get("tips_t")
    if w is None or t is None or t <= 0:
        return None, None
    if t == 0:
        return None, None   # market with no tips at all: no market input exists
    if row.get("sel") == "Tie":
        # OLBG's handball listing prints "Tie" as the most popular pick on 13 of the
        # 15 events. A split for a draw cannot be turned into a side price, so the
        # row is not used as market input at all (flag F-02).
        return None, None
    prior = prior_for(row)
    return (w + SHRINK_K * prior) / (t + SHRINK_K), prior


def split_teams(event):
    """Return (home-ish, away-ish) from an OLBG event title."""
    for sep in (" vs ", " v ", " @ "):
        if sep in event:
            a, b = event.split(sep, 1)
            if sep == " @ ":
                return b.strip(), a.strip()   # away @ home
            return a.strip(), b.strip()
    return None, None


def lookup(alias_map, name):
    key = alias_map.get(name)
    if not key:
        return None
    table, team = key.split(":")
    return table, team


def strength(table_name, tables, team):
    t = tables[table_name]["teams"][team]
    if "win_pct" in t:
        return t["win_pct"]
    if "pct" in t:
        return t["pct"]
    if "win_rate" in t:
        return t["win_rate"]
    if "series_wins" in t:
        return t["series_wins"] / 4.0
    return None


def p_form(row, form):
    """Logistic home-away model, only where an official table covers both sides."""
    tables, aliases = form["tables"], form["aliases"]
    sel = row["sel"].split(" +")[0].split(" -")[0].strip()
    home, away = split_teams(row["event"])
    if not home or not away:
        return None, None
    hs, as_ = None, None
    for cand, store in ((sel, "sel"),):
        pass
    lk_home, lk_away = lookup(aliases, home), lookup(aliases, away)
    lk_sel = lookup(aliases, sel)
    if not lk_sel:
        return None, None
    if lk_home and lk_away and lk_home[0] == lk_away[0] == lk_sel[0]:
        hs = strength(lk_home[0], tables, lk_home[1])
        as_ = strength(lk_home[0], tables, lk_away[1])
        ss = strength(lk_home[0], tables, lk_sel[1])
        if hs is None or as_ is None or ss is None:
            return None, None
        diff = (hs - as_) + HOME_EDGE
        p_home = sigmoid(diff / SCALE)
        p_sel = p_home if lk_sel[1] == lk_home[1] else 1.0 - p_home
        info = {"table": lk_home[0], "p_home": round(p_home, 4),
                "home_strength": hs, "away_strength": as_,
                "source": tables[lk_home[0]]["source"]}
        if row["market"] in HANDICAP_MARKETS:
            line = parse_line(row["sel"])
            sigma = SPREAD.get(row["sport"])
            if line is None or sigma is None:
                return None, None
            # expected margin for the selection, from the same win probability
            if lk_sel[1] == lk_home[1]:
                p_win = p_home
            else:
                p_win = 1.0 - p_home
            p_win = min(max(p_win, 0.001), 0.999)
            margin = sigma * inv_phi(p_win)
            p_sel = phi((margin + line) / sigma)
            info.update({"line": line, "sigma": sigma, "expected_margin": round(margin, 2)})
        return p_sel, info
    return None, None


def confidence(p, t, form_used, band):
    """High is deliberately scarce: it needs both a strong chance and a reason to
    believe the chance, either a large tip sample or an official table behind it."""
    t = t or 0
    if p >= 0.64 and (t >= 8 or form_used):
        base = "high"
    elif p >= 0.545:
        base = "medium"
    else:
        base = "low"
    if not band:
        return base + "-outside-band"
    return base


def main():
    cap = json.load(open(CAPTURE))
    form = json.load(open(FORM))
    lines = []
    for i, row in enumerate(cap["rows"]):
        pm, prior = p_market(row)
        pf, finfo = p_form(row, form)
        if pm is None and pf is None and (row.get("tips_t") == 0):
            p, basis = prior_for(row), "prior"
        elif pm is None and pf is None:
            p = None
            basis = "none"
        elif pf is None:
            p, basis = pm, "market"
        elif pm is None:
            p, basis = pf, "form"
        else:
            p = W_MARKET * pm + W_FORM * pf
            basis = "market+form"
        rec = dict(row)
        rec["id"] = "L%03d" % (i + 1)
        rec["prior"] = prior
        rec["p_market"] = None if pm is None else round(pm, 4)
        rec["p_form"] = None if pf is None else round(pf, 4)
        rec["form_input"] = finfo
        rec["basis"] = basis
        if p is None:
            rec.update({"p": None, "fair": None, "price_dec": None, "price_am": None,
                        "confidence": "unpriced", "band": None})
        else:
            dec = (1.0 / p) / MARGIN
            am = to_american(dec)
            rec.update({
                "p": round(p, 4),
                "fair": round(1.0 / p, 3),
                "price_dec": round(dec, 3),
                "price_am": am,
                "confidence": ("unrated" if basis == "prior"
                               else confidence(p, row.get("tips_t"), pf is not None, band_ok(am))),
                "band": "in" if band_ok(am) else ("too-short" if am < BAND_LOW else "too-long"),
            })
        lines.append(rec)

    # --- handball: derive a price for each side, because the captured market row
    # is a draw price. P_draw is carved out first, then the logistic decides the rest.
    extra = []
    seen = set()
    for r in lines:
        if r["sport"] != "Handball" or r.get("sel") != "Tie" or r["event"] in seen:
            continue
        seen.add(r["event"])
        home, away = split_teams(r["event"])
        if not home or not away:
            continue
        lh, la = lookup(form["aliases"], home), lookup(form["aliases"], away)
        if not (lh and la and lh[0] == la[0]):
            continue
        hs = strength(lh[0], form["tables"], lh[1])
        as_ = strength(la[0], form["tables"], la[1])
        if hs is None or as_ is None:
            continue
        p_home_nd = sigmoid(((hs - as_) + HOME_EDGE) / SCALE)
        for side, alias, p_nd in ((home, lh, p_home_nd), (away, la, 1 - p_home_nd)):
            p = p_nd * (1 - DRAW_SHARE)
            dec = (1.0 / p) / MARGIN
            am = to_american(dec)
            extra.append({
                "id": r["id"] + ("H" if side == home else "A"),
                "sport": "Handball", "comp": r.get("comp"), "event": r["event"],
                "start": r["start"], "market": "Money Line (side)", "sel": side,
                "tips_w": None, "tips_t": None, "pct": None, "link": r["link"],
                "note": "side derived: OLBG's captured row is the draw", "derived": True,
                "prior": None, "p_market": None, "p_form": round(p / (1 - DRAW_SHARE), 4),
                "form_input": {"table": lh[0], "p_home": round(p_home_nd, 4),
                               "home_strength": hs, "away_strength": as_,
                               "source": form["tables"][lh[0]]["source"],
                               "draw_share": DRAW_SHARE},
                "basis": "form", "p": round(p, 4), "fair": round(1 / p, 3),
                "price_dec": round(dec, 3), "price_am": am,
                "confidence": confidence(p, 0, True, band_ok(am)),
                "band": "in" if band_ok(am) else ("too-short" if am < BAND_LOW else "too-long"),
            })
    # --- opposite side of any form-backed two-way win market, so that a pick against
    # the crowd opinion can be priced on the same rules as one with it.
    opp = []
    WIN_MARKETS = {"Money Line", "To Win", "Win Match"}
    for r in lines:
        if r.get("derived") or r["market"] not in WIN_MARKETS or not r.get("form_input"):
            continue
        home, away = split_teams(r["event"])
        if not home or not away:
            continue
        sel = r["sel"]
        other = away if sel == home else (home if sel == away else None)
        if not other or r["p"] is None or r["sport"] == "Handball":
            continue
        p = 1.0 - r["p"]
        dec = (1.0 / p) / MARGIN
        am = to_american(dec)
        rec = dict(r)
        rec.update({"id": r["id"] + "X", "sel": other, "tips_w": None, "tips_t": None,
                    "pct": None, "p_market": None, "p_form": round(1 - (r["p_form"] or 0), 4),
                    "p": round(p, 4), "fair": round(1 / p, 3), "price_dec": round(dec, 3),
                    "price_am": am, "basis": "form",
                    "note": "opposite side of the captured OLBG selection",
                    "confidence": confidence(p, 0, True, band_ok(am)),
                    "band": "in" if band_ok(am) else ("too-short" if am < BAND_LOW else "too-long")})
        opp.append(rec)
    lines.extend(opp)
    lines.extend(extra)

    def count(pred):
        return sum(1 for r in lines if pred(r))

    lines.sort(key=lambda r: (r["sport"], r["event"], r["market"], r["sel"]))
    summary = {
        "rows": len(lines),
        "priced": count(lambda r: r["p"] is not None),
        "unpriced": count(lambda r: r["p"] is None),
        "by_basis": {b: count(lambda r, b=b: r["basis"] == b) for b in ("market", "form", "market+form", "none")},
        "by_confidence": {c: count(lambda r, c=c: r["confidence"] == c)
                          for c in ("high", "medium", "low", "high-outside-band",
                                    "medium-outside-band", "unrated", "unpriced")},
        "in_band": count(lambda r: r["band"] == "in"),
        "too_short": count(lambda r: r["band"] == "too-short"),
    }
    json.dump({
        "engine": "TS-27",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "constants": {"shrink_k": SHRINK_K, "margin": MARGIN, "home_edge": HOME_EDGE, "scale": SCALE,
                      "band": [BAND_LOW, BAND_HIGH], "priors": {"two_way": PRIOR_TWO_WAY,
                      "three_way": PRIOR_THREE_WAY, "outright": PRIOR_OUTRIGHT},
                      "weights": {"form": W_FORM, "market": W_MARKET}},
        "summary": summary,
        "lines": lines,
    }, open(OUT, "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()

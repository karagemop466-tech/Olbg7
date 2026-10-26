#!/usr/bin/env python3
"""
Originate our own prices for every market row captured from OLBG.

Method (deliberately simple, fully documented, no hidden inputs)
---------------------------------------------------------------
1. Data. For each market row we know how many OLBG tipsters backed the selection
   (`tips`) out of all tips on that market (`total`). The tip share is
       s = tips / total
   A tip share is NOT a probability: 1 tip out of 1 is a 100% share but nowhere
   near a 100% chance, and 1 tip out of 2 in a 70-runner golf field is not 50%.

2. Shrinkage to a base rate. Each market carries `outcomes` (how many possible
   results the market has, e.g. 2 for a money line, 3 for a 90-minute handball
   line, 70 for a golf outright). The base rate is b = 1 / outcomes.
       w = n / (n + K)      with n = total tips on the market, K = 10
       p = w * s + (1 - w) * b
   With n = 1 the weight is only 0.09, so a single tip barely moves the price.
   With n = 40 the weight is 0.80 and the tip share dominates.

3. Price. We quote a price with a 5% theoretical overround split evenly, i.e.
       decimal = (1 - 0.025) / p = 0.975 / p
   American odds are derived from the decimal price.

4. Confidence label
       HIGH   : n >= 8 and p >= 0.62
       MEDIUM : n >= 3 and p >= 0.58
       LOW    : everything else
   A HIGH label therefore requires both a large sample of tips and a genuinely
   likely outcome - never a single tipster at 100%.

5. Selection rule. One pick per event: the eligible market row with the highest
   modelled probability wins the event; ties break on number of tips, then on
   market family (match winner > handicap > total). Per sport we then keep the
   five highest-confidence distinct events.

6. Requested odds band. Picks must price between -250 (decimal 1.40) and
   +10000 (decimal 101). Rows outside the band are priced but not picked.
"""
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

K_PSEUDO_TIPS = 10
OVERROUND = 0.05
BAND_MIN, BAND_MAX = 1.40, 101.0

FAMILY_ORDER = {"match winner": 0, "handicap": 1, "total": 2, "outright": 3, "other": 4}


def family(market_name: str) -> str:
    m = market_name.lower()
    if "money line" in m or "to win" in m or "win match" in m or "win hurling" in m:
        return "match winner"
    if "handicap" in m or "puck line" in m or "run line" in m or "pointspread" in m:
        return "handicap"
    if "total" in m:
        return "total"
    if "tournament" in m or "outright" in m or "grand final" in m:
        return "outright"
    return "other"


def to_american(dec: float) -> str:
    if dec >= 2.0:
        return f"+{round((dec - 1) * 100):d}"
    return f"-{round(100 / (dec - 1)):d}"


def probability(tips, total, outcomes):
    if not tips or not total or not outcomes:
        return None, None
    s = tips / total
    b = 1.0 / outcomes
    w = total / (total + K_PSEUDO_TIPS)
    return w * s + (1 - w) * b, w


def confidence(p, total):
    if p is None or not total:
        return "none"
    if total >= 8 and p >= 0.62:
        return "high"
    if total >= 3 and p >= 0.58:
        return "medium"
    return "low"


def main():
    raw = json.loads((DATA / "events.json").read_text())
    lines = []
    for ev in raw["events"]:
        for mk in ev["markets"]:
            p, w = probability(mk.get("tips"), mk.get("total"), mk.get("outcomes"))
            row = {
                "event_id": ev["id"],
                "sport": ev["sport"],
                "competition": ev.get("competition", ""),
                "event": ev["event"],
                "start": ev["start"],
                "url": ev["url"],
                "market": mk["market"],
                "selection": mk["selection"],
                "tips": mk.get("tips"),
                "total": mk.get("total"),
                "pct": mk.get("pct"),
                "outcomes": mk.get("outcomes"),
                "family": family(mk["market"]),
                "notes": ev.get("notes", ""),
            }
            if p is None:
                row.update({
                    "probability": None,
                    "price_decimal": None,
                    "price_american": None,
                    "confidence": "none",
                    "in_band": False,
                    "excluded": "OLBG did not publish a tip count for this row",
                })
            else:
                dec = round(0.975 / p, 2)
                in_band = BAND_MIN <= dec <= BAND_MAX
                row.update({
                    "probability": round(p, 4),
                    "shrink_weight": round(w, 4),
                    "price_decimal": dec,
                    "price_american": to_american(dec),
                    "confidence": confidence(p, mk.get("total")),
                    "in_band": in_band,
                    "excluded": None if in_band else "price outside the requested -250 to +10000 band",
                })
            # anomalies that disqualify a row from being a pick
            if mk["selection"].strip().lower() == "tie":
                row["excluded"] = "market-mapping anomaly: OLBG lists 'Tie' as the top selection for nearly every handball match"
            if ev["id"] == "gh-0824-tow":
                row["excluded"] = "race already marked Expired on the OLBG page"
            lines.append(row)

    # one pick per event
    by_event = {}
    for row in lines:
        if row["price_decimal"] is None or row["excluded"]:
            continue
        key = (row["probability"], row["total"], -FAMILY_ORDER[row["family"]])
        best = by_event.get(row["event_id"])
        if best is None or key > (best["probability"], best["total"], -FAMILY_ORDER[best["family"]]):
            by_event[row["event_id"]] = row

    rank = {"high": 3, "medium": 2, "low": 1, "none": 0}
    by_sport = {}
    for row in by_event.values():
        by_sport.setdefault(row["sport"], []).append(row)

    picks = []
    for sport, rows in by_sport.items():
        rows.sort(key=lambda r: (rank[r["confidence"]], r["probability"], r["total"]), reverse=True)
        for i, r in enumerate(rows[:5], start=1):
            r = dict(r)
            r["sport_rank"] = i
            picks.append(r)

    picks.sort(key=lambda r: (rank[r["confidence"]], r["probability"]), reverse=True)

    (DATA / "lines.json").write_text(json.dumps({
        "method": {
            "pseudo_tips_K": K_PSEUDO_TIPS,
            "overround": OVERROUND,
            "band_decimal": [BAND_MIN, BAND_MAX],
            "confidence_rules": {
                "high": "n >= 8 tips on the market AND p >= 0.62",
                "medium": "n >= 3 AND p >= 0.58",
                "low": "otherwise",
            },
        },
        "count": len(lines),
        "lines": lines,
    }, indent=1))

    (DATA / "picks.json").write_text(json.dumps({
        "snapshot_utc": raw["snapshot_utc"],
        "count": len(picks),
        "picks": picks,
    }, indent=1))

    print(f"lines: {len(lines)}   events priced: {len(by_event)}   picks: {len(picks)}")
    for s in sorted(by_sport):
        n = len([p for p in picks if p["sport"] == s])
        ev = len(by_sport[s])
        print(f"  {s:15s} events={ev:2d} picks={n}")
    print()
    for p in picks:
        print(f"{p['confidence']:6s} {p['sport']:14s} {p['probability']:.3f} {p['price_american']:>7s} "
              f"{p['tips']}/{p['total']:<3} {p['event'][:45]:45s} | {p['market']} - {p['selection']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CAL-1R - Consensus-Anchored Line, refreshed for the 2026-10-27 cycle.

What it does
------------
Originate OUR OWN price for every OLBG market we captured on 2026-10-27, using the only numeric
market signal OLBG prints in retrievable HTML: the tip split ("X / Y Win Tips" and the % share).
Bookmaker prices are rendered client-side on OLBG and are not in the HTML we can read, so they are
never quoted here (see flag U-001).

Changes vs tools/pricing.py (prior cycle), each of them a defect we found while reading that code:
  1. `n_outcomes()` contained two stacked blocks; everything after the first `return` was dead code,
     so market structure silently came from the first rule that matched. Here it is one explicit
     lookup with a documented reason per sport.
  2. THREE_WAY_SPORTS was keyed on "Ice Hockey" while the data key is "Ice_Hockey", so ice-hockey
     money lines fell through to the 2-way prior. Sport keys are normalised before matching.
  3. Outright fields used a hard 1/8 prior. Where OLBG does not print the field size we still assume
     8 and flag it (U-004), but the flag is attached to the row instead of being invisible.
  4. A selection can only be labelled `high` if its own price is inside the focus band
     (-250 .. +10000 American) AND at least 8 tips were counted on the market. Small samples and
     0%/100% extremes are capped at `medium`.

Method
------
  prior   = 1 / n_outcomes(market, sport)
  p_fair  = (wins + K*prior) / (total + K)          K = 6 pseudo-tips, shrinks small samples
  fair    = 1 / p_fair
  ourcard = 1 / (p_fair * (1 + margin))             margin = 5%
  american conversion is the standard ±100 formula.
No team rating, score or injury is invented here - this file only reprices a tip split.
"""
import json
import os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CYCLE = "2026-10-27"
K = 6.0
MARGIN = 0.05
BAND_MIN_DEC, BAND_MAX_DEC = 1.40, 101.00      # -250 .. +10000 American
MIN_TIPS_FOR_HIGH = 8

NORMALISE_SPORT = {
    "Ice_Hockey": "Ice Hockey", "Ice Hockey": "Ice Hockey",
    "Rugby_Union": "Rugby Union", "Rugby_League": "Rugby League",
    "Motor_Racing": "Motor Racing", "Gaelic_Sports": "Gaelic Sports",
}
# Markets where a draw/level is a genuine third priced outcome in the OLBG market we captured.
THREE_WAY = {("Handball", "Money Line"),          # EHF CL: home / tie / away all listed
             ("Rugby Union", "To Win"),           # OLBG prints a draw line on union markets
             ("Rugby Union", "Handicap"),
             ("Gaelic Sports", "Win Tournament")}
OUTRIGHT = {"Win Tournament", "Outright Winner", "Grand Final Winner", "Win Hurling"}
BINARY = {"Money Line", "Win Match", "Pointspread", "Handicap", "Game Totals", "Puck Line",
          "Run Line", "Top 6 Finish", "Top 10 Finish", "Daily Races", "Top Team1 Batsman",
          "Man Of The Match", "To Win", "To Qualify"}


def structure(sport, market, event="", comp="", has_draw_row=False):
    """Return (n_outcomes, prior, label) with the reason recorded."""
    m = (market or "").lower()
    ev = (event or "").lower() + " " + (comp or "").lower()
    if "man of the match" in m or m.startswith("top ") or "player to" in m:
        return 8, 1 / 8.0, "player outright - field size not printed, 8 assumed (U-004)"
    if market in OUTRIGHT:
        return 8, 1 / 8.0, "outright - field size not printed on OLBG, 8 assumed (U-004)"
    if (sport, market) in THREE_WAY:
        return 3, 1 / 3.0, "3-way (draw is a listed outcome)"
    # Only a *multi-day* cricket match can be drawn; a T20/ODI goes to a Super Over.
    # We treat a cricket match market as 3-way when the event is a Test, or when OLBG
    # itself printed a Draw/Tie row alongside it.
    if sport == "Cricket" and has_draw_row:
        return 3, 1 / 3.0, "3-way (OLBG printed a Draw/Tie row on this match)"
    if sport == "Cricket" and "test" in ev and ("win match" in m or "money line" in m):
        return 3, 1 / 3.0, "3-way (a Test match can be drawn)"
    if market in BINARY:
        return 2, 0.5, "2-way"
    return 2, 0.5, "2-way (default)"


def american(dec):
    if dec is None:
        return None
    return round((dec - 1.0) * 100) if dec >= 2.0 else round(-100.0 / (dec - 1.0))


def line(sport, market, selection, wins, total, event="", comp="", has_draw_row=False):
    if wins is None or total is None or int(total) <= 0:
        return None, "not priced - OLBG printed no tip split on this selection"
    wins, total = int(wins), int(total)
    sel = (selection or "")
    n, prior, label = structure(sport, market, event, comp, has_draw_row)
    p = (wins + K * prior) / (total + K)
    p = max(0.01, min(0.99, p))
    fair = round(1.0 / p, 2)
    card = round(1.0 / (p * (1.0 + MARGIN)), 2)
    in_band = BAND_MIN_DEC <= card <= BAND_MAX_DEC
    notes = []
    if total < MIN_TIPS_FOR_HIGH:
        notes.append(f"thin sample: {total} tip(s) counted")
    if wins in (0, total):
        notes.append("0%/100% split - no information in the tail, capped at medium")
    if p >= 0.60 and total >= MIN_TIPS_FOR_HIGH and in_band and wins not in (0, total):
        conf = "high"
    elif p >= 0.60 and wins not in (0, total) and total >= MIN_TIPS_FOR_HIGH:
        conf = "medium"
        notes.append("strong but outside the -250..+10000 focus band" if not in_band else "strong")
    elif p >= 0.50:
        conf = "medium"
    else:
        conf = "low"
    # --- reliability grade: how much the *structure* of this market can be trusted ----
    grade = "A" if total >= 8 else ("B" if total >= 3 else "C")
    if label.startswith("3-way") and "tie" in sel.lower():
        grade = "C"
        notes.append("STRUCTURAL DEFECT: tip vote is clustered on the draw/tie outcome")
    if sport == "Handball" and "tie" in sel.lower():
        grade = "C"
        conf = "low"
        notes.append("handball tie: capped at low - EHF Champions League 2026-27 group stage had "
                     "1 drawn match in 30 played, so a 70%+ draw vote is a tipster artefact, not price")
    if grade == "C" and conf == "high":
        conf = "medium"
        notes.append("grade C line: high confidence blocked")
    return {
        "structure": label, "n_outcomes": n, "prior": round(prior, 4), "p_fair": round(p, 4),
        "fair_decimal": fair, "card_decimal": card, "card_american": american(card),
        "implied_pct": round(100 / card, 1), "margin": MARGIN, "in_focus_band": in_band,
        "confidence": conf, "grade": grade, "sample_tips": total, "notes": notes,
    }, None


def main():
    raw = json.load(open(os.path.join(ROOT, "data/cycle-20261027/events_raw.json")))
    # events where OLBG printed a Draw / Tie row -> that market really is three-way
    draw_rows = {(r.get("event_id"), (r.get("market") or "").lower())
                 for r in raw if (r.get("selection") or "").lower() in ("tie", "draw")}
    # the sport listing and the event page can both carry the same market - keep one row,
    # preferring the copy that has the larger tip total and a named competition.
    best = {}
    order = []
    for r in raw:
        k = (r.get("sport"), r.get("event_id"), (r.get("market") or "").lower(),
             (r.get("selection") or "").lower())
        rank = (r.get("tips_total") or 0, 1 if r.get("competition") else 0)
        if k not in best:
            best[k] = r
            order.append(k)
        elif rank > (best[k].get("tips_total") or 0, 1 if best[k].get("competition") else 0):
            best[k] = r
    merged = []
    for k in order:
        r = best[k]
        if (r.get("sport"), r.get("event_id"), (r.get("market") or "").lower(),
                (r.get("selection") or "").lower()) == k and r not in merged:
            merged.append(r)
    dupes = len(raw) - len(merged)
    raw = merged
    out = []
    for e in raw:
        sport = NORMALISE_SPORT.get(e["sport"], e["sport"])
        row = dict(e)
        row["sport"] = sport
        ln, why = line(sport, e.get("market"), e.get("selection"), e.get("tips_on_pick"),
                       e.get("tips_total"), e.get("event", ""), e.get("competition", ""),
                       (e.get("event_id"), (e.get("market") or "").lower()) in draw_rows)
        row["our_line"] = ln
        if ln is None:
            row["unpriced_reason"] = why
        out.append(row)
    summary = defaultdict(lambda: Counter())
    for r in out:
        s = r["sport"]
        summary[s]["events"] += 1
        if r["our_line"]:
            summary[s]["priced"] += 1
            summary[s][r["our_line"]["confidence"]] += 1
            summary[s]["in_band"] += 1 if r["our_line"]["in_focus_band"] else 0
            summary[s]["grade_" + r["our_line"]["grade"]] += 1
    doc = {
        "engine": "CAL-1R (Consensus-Anchored Line, refreshed)",
        "duplicate_rows_removed": dupes,
        "cycle": CYCLE,
        "constants": {"K_pseudo_tips": K, "margin": MARGIN, "band_min_decimal": BAND_MIN_DEC,
                      "band_max_decimal": BAND_MAX_DEC, "band_american": [-250, 10000],
                      "min_tips_for_high": MIN_TIPS_FOR_HIGH},
        "summary": {k: dict(v) for k, v in sorted(summary.items())},
        "totals": {"markets": len(out),
                   "priced": sum(1 for r in out if r["our_line"]),
                   "unpriced": sum(1 for r in out if not r["our_line"]),
                   "high": sum(1 for r in out if r["our_line"] and r["our_line"]["confidence"] == "high")},
        "lines": out,
    }
    dst = os.path.join(ROOT, "data/cycle-20261027/lines.json")
    json.dump(doc, open(dst, "w"), indent=1)
    print(f"markets={doc['totals']['markets']} priced={doc['totals']['priced']} "
          f"unpriced={doc['totals']['unpriced']} high={doc['totals']['high']} -> {dst}")
    for s, d in sorted(doc["summary"].items(), key=lambda kv: -kv[1]["events"]):
        print(f"  {s:14s} ev={d.get('events',0):2d} priced={d.get('priced',0):2d} high={d.get('high',0):2d} "
              f"med={d.get('medium',0):2d} low={d.get('low',0):2d} band={d.get('in_band',0):2d} "
              f"A/B/C={d.get('grade_A',0)}/{d.get('grade_B',0)}/{d.get('grade_C',0)}")


if __name__ == "__main__":
    main()

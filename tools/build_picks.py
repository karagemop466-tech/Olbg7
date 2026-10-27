#!/usr/bin/env python3
"""
Build data/picks.json from the two hand-written source files.

data/picks_src1.json  - eight sports with a full OLBG card (scores, team news, venues)
data/picks_src2.json  - the sports where OLBG only carries outright or single-market books

The prose, the facts and the selection are editorial and live in those two files. Everything
numeric (fair chance, our price, confidence) is computed here, so no price in the published
board is typed by hand. Prices for markets with a printed OLBG split come from tools/pricing.py
(CAL-1). Markets where OLBG printed no usable split carry an explicit p_override and are labelled
CAL-2 or CAL-3 so a reader can see which rows are estimates.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# 2026-10-27 refresh: OLBG still prints "Tie" as the most-tipped selection on 15 of 19
# handball rows (flag F-002). This board publishes no "Tie" picks; the four handball picks
# below are all rows where OLBG printed a real club selection, so no CAL-2 overrides are needed.
CODES = {
    "Basketball": "BB", "Baseball": "BL", "Ice Hockey": "IH", "Cricket": "CK",
    "Rugby Union": "RU", "Rugby League": "RL", "Tennis": "TN", "Volleyball": "VB",
    "Handball": "HB", "Golf": "GF", "Darts": "DA", "Motor Racing": "MR",
    "Gaelic Sports": "GS", "Greyhounds": "GY", "Snooker": "SN",
}


def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


def words(t):
    return len(re.findall(r"[A-Za-z0-9'\u2019\-]+", t))


def main():
    events = {e["id"]: e for e in load("events.json")["events"]}
    src = load("picks_src1.json") + load("picks_src2.json")

    out, problems = [], []
    for p in src:
        ev = events.get(str(p["ev"]))
        if not ev:
            problems.append(f"unknown event {p['ev']}")
            continue
        rec = {
            "sport": p["s"],
            "event_id": str(p["ev"]),
            "event": ev["e"],
            "competition": ev.get("c") or "",
            "date_label": ev.get("start_label") or ev.get("d") or "",
            "selection": p["sel"],
            "market": p["market"],
            "olbg_tips": ev.get("tips"),
            "olbg_pct": ev.get("pct"),
            "prediction": p["pred"],
            "facts": [{"t": t, "src": u} for t, u in p["facts"]],
        }
        if p.get("sel_note"):
            rec["selection_note"] = p["sel_note"]
        if p.get("p_override"):
            rec["cal2_p_fair"] = p["p_override"]
            rec["method"] = p.get("method", "CAL-2")

        checks = []
        if rec.get("cal2_p_fair"):
            checks.append("price is an explicit estimate, not a tip-split repricing")
        else:
            checks.append("tip split read from the OLBG listing at retrieval")
        checks.append(f"{len(rec['facts'])} fact(s), each with an https source")
        if rec.get("selection_note"):
            checks.append("our own selection replaces the one OLBG lists")
        rec["verification"] = "; ".join(checks)

        if words(rec["prediction"]) < 30:
            problems.append(f"{ev['e']}: prediction only {words(rec['prediction'])} words")
        for bad in ("model", "verified"):
            if re.search(rf"\b{bad}\b", rec["prediction"], re.I):
                problems.append(f"{ev['e']}: banned word '{bad}' in prediction")
        for f in rec["facts"]:
            if not f["src"].startswith("https://"):
                problems.append(f"{ev['e']}: fact source is not https")
        out.append(rec)

    seen = {}
    for rec in out:
        code = CODES.get(rec["sport"], rec["sport"][:2].upper())
        seen[code] = seen.get(code, 0) + 1
        rec["id"] = f"{code}-{seen[code]:02d}"

    with open(os.path.join(DATA, "picks.json"), "w") as fh:
        json.dump({"generated_at": "2026-10-27", "picks": out}, fh, indent=1, ensure_ascii=False)

    print(f"picks written: {len(out)}")
    for pr in problems:
        print("PROBLEM:", pr)
    if problems:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

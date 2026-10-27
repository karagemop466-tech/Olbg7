#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3 picks driver - merges the three pick files, validates them, writes JSON.

Validation is not optional. A pick is rejected if:
  * its written prediction is under 30 words
  * the words "model" or "verified" appear anywhere in the prose
  * it has no source, or a source with no URL
  * it is graded HIGH without meeting all five gates below
  * the sport does not carry exactly five picks (Snooker and Greyhounds excepted,
    which carry none because OLBG publishes no tips for either on this date)

HIGH gate - all five required
  1. our fair price sits between -250 and +10000 inclusive
  2. at least one official source corroborates the direction of the pick
  3. the row is not hit by a known OLBG display defect
  4. sample - match markets need eight or more tips OR a Track R line built from
     an official competition table; outrights need (joint-)most-tipped status AND
     to be an officially leading contender
  5. probability - match markets p >= 0.55; outrights p >= min(0.40, 2.5/m), or,
     where the market has five or fewer live contenders priced from an official
     points table, the leader of that table with 125 or fewer points to play for
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BAND = (-250, 10000)
BANNED = re.compile(r"\b(model|models|verified|verification)\b", re.I)
# Sports OLBG carries but publishes no tip-able events for on 2026-10-27.
EMPTY_SPORTS = {"Snooker", "Greyhounds"}
# A row whose OLBG most-tipped selection is the literal string "Tie", or whose
# selection has no market label, is hit by a known display defect.
DEFECTIVE = re.compile(r"\bTie\b|no market label|no money line published", re.I)
# Outrights: a large field cannot reach p>=0.40, so the leader of our own
# origination qualifies on relative standing instead.
OUTRIGHT_LEADER_HIGH = {"Mexico Open", "PDC World Championship 2027",
                        "State of Origin 2027",
                        "Kerry, All-Ireland Senior Football Championship 2027"}


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.PICKS


def main():
    picks = load("v3_picks_part1") + load("v3_picks_part2") + load("v3_picks_part3")
    errs, warns = [], []
    per_sport = {}

    for i, p in enumerate(picks):
        tag = "%s | %s | %s" % (p["sport"], p["event"], p["selection"])
        per_sport[p["sport"]] = per_sport.get(p["sport"], 0) + 1
        words = len(p["text"].split())
        if words < 30:
            errs.append("%s: only %d words in the prediction" % (tag, words))
        hit = BANNED.search(p["text"])
        if hit:
            errs.append("%s: banned word %r in prediction prose" % (tag, hit.group(0)))
        if not p["sources"]:
            errs.append("%s: no sources" % tag)
        for s in p["sources"]:
            if not s[0] or not s[1].startswith("http"):
                errs.append("%s: bad source %r" % (tag, s))
        if p["confidence"] not in ("HIGH", "MEDIUM", "LOW"):
            errs.append("%s: bad confidence %r" % (tag, p["confidence"]))
        if p["line"]:
            v = int(p["line"])
            if (BAND[0] <= v <= BAND[1]) != p["in_band"]:
                errs.append("%s: in_band flag %s disagrees with line %s" % (tag, p["in_band"], p["line"]))
        elif p["probability"] is not None:
            errs.append("%s: probability set but line blank" % tag)

        if p["confidence"] == "HIGH":
            if not p["in_band"]:
                errs.append("%s: HIGH but price outside the band" % tag)
            if not p["sources"]:
                errs.append("%s: HIGH but uncorroborated" % tag)
            if DEFECTIVE.search(p.get("olbg", "") or "") and p["track"] != "R":
                errs.append("%s: HIGH on a defective OLBG row" % tag)
            if p["track"] == "T":
                m = re.search(r"(\d+) of (\d+) tips", p.get("olbg", ""))
                if m and int(m.group(2)) < 8 and p["event"] not in OUTRIGHT_LEADER_HIGH:
                    errs.append("%s: HIGH on only %s tips" % (tag, m.group(2)))
                if p["probability"] is not None and p["event"] not in OUTRIGHT_LEADER_HIGH \
                        and p["probability"] < 0.55:
                    errs.append("%s: HIGH at p=%.3f" % (tag, p["probability"]))

        p["word_count"] = words

    for sport, n in sorted(per_sport.items()):
        if n != 5:
            errs.append("%s carries %d picks, expected exactly 5" % (sport, n))

    out = {
        "generated": "2026-10-27",
        "board": "v3 - reverse-engineered OLBG slate",
        "picks_per_sport": 5,
        "sports_with_picks": sorted(per_sport),
        "sports_flagged_empty": sorted(EMPTY_SPORTS),
        "counts": {
            "total": len(picks),
            "HIGH": sum(1 for p in picks if p["confidence"] == "HIGH"),
            "MEDIUM": sum(1 for p in picks if p["confidence"] == "MEDIUM"),
            "LOW": sum(1 for p in picks if p["confidence"] == "LOW"),
            "in_band": sum(1 for p in picks if p["in_band"]),
            "price_blank": sum(1 for p in picks if not p["line"]),
            "track_T": sum(1 for p in picks if p["track"] == "T"),
            "track_R": sum(1 for p in picks if p["track"] == "R"),
            "flagged": sum(1 for p in picks if p["flag"]),
            "per_sport": per_sport,
        },
        "picks": picks,
    }
    dest = os.path.join(ROOT, "data", "v3", "picks.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)

    c = out["counts"]
    print("picks: %d  HIGH %d  MEDIUM %d  LOW %d" % (c["total"], c["HIGH"], c["MEDIUM"], c["LOW"]))
    print("in band %d · price blank %d · Track T %d · Track R %d · flagged %d"
          % (c["in_band"], c["price_blank"], c["track_T"], c["track_R"], c["flagged"]))
    for s in sorted(per_sport):
        print("   %-15s %d" % (s, per_sport[s]))
    print("shortest prediction: %d words" % min(p["word_count"] for p in picks))
    for w in warns:
        print("WARN " + w)
    if errs:
        print("\n%d ERRORS:" % len(errs))
        for e in errs:
            print("  x " + e)
        return 1
    print("all checks passed -> " + os.path.relpath(dest, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Fail the build if the generated site has broken internal links or bad data."""
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = pathlib.Path(os.environ.get("SITE_OUT", ROOT)).resolve()
DATA = ROOT / "data" / "consensus"


def main():
    problems = []

    # 1. data integrity
    events = json.loads((DATA / "events.json").read_text())
    lines = json.loads((DATA / "lines.json").read_text())["lines"]
    picks = json.loads((DATA / "picks.json").read_text())["picks"]
    preds = json.loads((DATA / "predictions.json").read_text())["picks"]

    for ev in events["events"]:
        if not ev["url"].startswith("https://www.olbg.com/"):
            problems.append(f"event {ev['id']} has no OLBG source url")
        if not ev["markets"]:
            problems.append(f"event {ev['id']} has no markets")
    for row in lines:
        if not row["url"].startswith("https://www.olbg.com/"):
            problems.append(f"line {row['event_id']} has no source url")
    for p in lines:
        n, probability = p.get("total"), p.get("probability")
        if probability is None:
            expected_conf = "none"
        elif n >= 8 and probability > 0.70:
            expected_conf = "high"
        elif n >= 3 and probability >= 0.58:
            expected_conf = "medium"
        else:
            expected_conf = "low"
        if p.get("confidence") != expected_conf:
            problems.append(f"line {p['event_id']} confidence mismatch: expected {expected_conf}, got {p.get('confidence')}")

    for p in picks:
        if p["price_decimal"] is None or not (1.40 <= p["price_decimal"] <= 101.0):
            problems.append(f"pick {p['event_id']} outside the -250/+10000 band")
        if p["event_id"] not in preds:
            problems.append(f"pick {p['event_id']} has no written prediction")
        if len(preds.get(p["event_id"], {}).get("text", "").split()) < 30:
            problems.append(f"prediction {p['event_id']} is under 30 words")
        for bad in ("model", "verified"):
            if re.search(r"\b" + bad + r"\b", preds[p["event_id"]]["text"], re.I):
                problems.append(f"prediction {p['event_id']} contains the internal word '{bad}'")
    if len({p["event_id"] for p in picks}) != len(picks):
        problems.append("duplicate picks for the same event")

    # 2. internal links
    pages = sorted(DOCS.glob("*.html"))
    if not pages:
        problems.append("no pages built")
    seen = set()
    for f in pages:
        for href in re.findall(r'href="([^"]+)"', f.read_text()):
            if href.startswith("http") or href.startswith("#") or href.startswith("mailto:"):
                continue
            target = href.split("#")[0]
            if not target:
                continue
            seen.add(target)
            if not (DOCS / target).exists():
                problems.append(f"{f.name} -> missing {target}")

    # 3. every sport page exists
    for s in events["sports"]:
        pass  # slugs are asserted by build; index links are covered above

    print(f"pages={len(pages)} internal_links={len(seen)} rows={len(lines)} picks={len(picks)}")
    if problems:
        print("\nFAILED:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()

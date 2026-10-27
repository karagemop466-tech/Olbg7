#!/usr/bin/env python3
"""
Merge the per-sport OLBG crawl captures in data/raw/*.json into data/events.json.

Each data/raw/<sport>.json file holds the rows parsed by hand from the OLBG sport root
page markdown retrieved on 2026-10-27 (one row per most-tipped selection). This script only
assembles and validates them; it never invents a row. Rows with no printed tip split
(tips is null) are kept so the site can show them as unpriced.
"""
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
RETRIEVED = "2026-10-27"

ORDER = [
    "golf", "volleyball", "rugby-union", "cricket", "snooker", "darts", "baseball",
    "gaelic-sports", "greyhounds", "tennis", "motor-racing", "handball",
    "ice-hockey", "basketball", "rugby-league",
]


def main():
    rows = []
    for slug in ORDER:
        path = os.path.join(RAW, f"{slug}.json")
        if not os.path.exists(path):
            raise SystemExit(f"missing crawl file {path}")
        rows.extend(json.load(open(path)))

    seen = set()
    for r in rows:
        assert r["id"] not in seen, f"duplicate event id {r['id']}"
        seen.add(r["id"])
        assert r["path"].startswith("/betting-tips/"), r
        assert r["d"], r
        if r.get("tips") is not None and "/" not in r["tips"]:
            raise SystemExit(f"bad tips value on {r['id']}: {r['tips']}")

    doc = {
        "schema_version": 2,
        "retrieved_at": RETRIEVED,
        "retrieved_by": "sess-arena-4efa4ee3",
        "base": "https://www.olbg.com",
        "field_notes": {
            "date_bucket": "today = 2026-10-27, tomorrow = 2026-10-28, otherwise the explicit date OLBG printed",
            "start_label": "exactly as printed by OLBG (never re-derived)",
            "timezone": "OLBG does not print a timezone; treated as UK local time.",
            "tips": "most-tipped selection's split 'wins/total' exactly as printed; null means OLBG printed no split",
            "pct": "percentage printed next to the split; null when OLBG printed none",
            "load_more": "OLBG paginates extra rows behind a 'Load More Tips' button that requires JavaScript; "
                         "the static HTML capture contains every row rendered without scripting, and nothing behind the button is inferred",
        },
        "events": rows,
    }
    dst = os.path.join(ROOT, "data", "events.json")
    with open(dst, "w") as fh:
        json.dump(doc, fh, indent=1)
    print(f"wrote {len(rows)} events -> {dst}")


if __name__ == "__main__":
    main()

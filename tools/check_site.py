#!/usr/bin/env python3
"""Line-by-line checks on the built site and the data behind it.

Fails (exit 1) on: broken internal links, a pick with no source, a pick under 30 words,
a banned word inside a prediction, a missing sport page, a duplicate pick id, or an
inventory row without an OLBG link.
"""
import json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

SPORTS = ["golf", "volleyball", "rugby-union", "cricket", "snooker", "darts", "baseball",
          "gaelic-sports", "greyhounds", "tennis", "motor-racing", "handball",
          "ice-hockey", "basketball", "rugby-league"]
BANNED = ["model", "verified"]
TARGET = 5


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == "href" and v:
                self.hrefs.append(v)
            if k == "src" and v:
                self.hrefs.append(v)


def main():
    errors, warns = [], []
    events = json.load(open(os.path.join(DATA, "events.json")))["events"]
    picks = json.load(open(os.path.join(DATA, "picks.json")))["picks"]
    pricing = json.load(open(os.path.join(DATA, "pricing.json")))

    # --- data checks -------------------------------------------------------
    ids = {}
    for p in picks:
        ids[p["id"]] = ids.get(p["id"], 0) + 1
        for k in ("id", "sport", "event", "market", "selection", "prediction", "facts", "verification"):
            if not p.get(k):
                errors.append(f"{p.get('id','?')}: missing field {k}")
        wc = len(re.findall(r"[A-Za-z0-9'\-]+", p["prediction"]))
        if wc < 30:
            errors.append(f"{p['id']}: prediction is {wc} words (minimum 30)")
        for w in BANNED:
            if re.search(rf"\b{w}\b", p["prediction"], re.I):
                errors.append(f"{p['id']}: banned word '{w}' inside the prediction")
        if not p.get("facts"):
            errors.append(f"{p['id']}: no facts listed")
        for f in p.get("facts", []):
            if not f.get("src", "").startswith("https://"):
                errors.append(f"{p['id']}: fact source is not https - {f.get('src')}")
        if len({f["src"] for f in p.get("facts", [])}) == 0:
            errors.append(f"{p['id']}: no distinct source links")
    for k, v in ids.items():
        if v > 1:
            errors.append(f"duplicate pick id {k}")

    # every inventory row must carry a source path
    for e in events:
        if not e.get("path", "").startswith("/betting-tips/"):
            errors.append(f"event {e['id']}: inventory row has no OLBG path")
        if not e.get("d"):
            errors.append(f"event {e['id']}: no date bucket")

    # every priced line must have a probability and a price
    unpriced = 0
    for r in pricing["lines"]:
        if r.get("our_line"):
            ol = r["our_line"]
            if not (0 < ol["p_fair"] < 1):
                errors.append(f"line {r['id']}/{r['sel']}: p_fair out of range")
            if ol["card_decimal"] < 1.01:
                errors.append(f"line {r['id']}/{r['sel']}: impossible price")
        else:
            unpriced += 1

    # picks per sport against the target
    per = {}
    for p in picks:
        per[p["sport"]] = per.get(p["sport"], 0) + 1
    for s in SPORTS:
        name = {"gaelic-sports": "Gaelic Sports", "rugby-union": "Rugby Union",
                "motor-racing": "Motor Racing", "ice-hockey": "Ice Hockey",
                "rugby-league": "Rugby League"}.get(s, s.title())
        n = per.get(name, 0)
        if n < TARGET:
            warns.append(f"{name}: {n} picks (target {TARGET}) - must be flagged on the site")

    # --- html checks -------------------------------------------------------
    pages = ["index.html", "all-events.html", "olbg-map.html", "methodology.html",
             "sources.html", "flagged.html", "freshness.html"] + [f"sports/{s}.html" for s in SPORTS]
    total_links = 0
    for page in pages:
        path = os.path.join(ROOT, page)
        if not os.path.exists(path):
            errors.append(f"missing page {page}")
            continue
        html_src = open(path, encoding="utf-8").read()
        lp = Links()
        lp.feed(html_src)
        base = os.path.dirname(path)
        for h in lp.hrefs:
            if h.startswith("http://") or h.startswith("https://"):
                continue
            if h.startswith("#") or h.startswith("mailto:"):
                continue
            target = os.path.normpath(os.path.join(base, h.split("#")[0]))
            total_links += 1
            if not os.path.exists(target):
                errors.append(f"{page}: broken internal link -> {h}")
        if 'class="pill' not in html_src and page.startswith("sports/") and "snooker" not in page:
            warns.append(f"{page}: no confidence pills rendered")

    hi = sum(1 for p in picks if p.get("_conf") == "high")
    print(f"pages checked: {len(pages)}  internal links: {total_links}")
    print(f"events: {len(events)}  priced: {pricing['totals']['priced']}  unpriced: {unpriced}")
    print(f"picks: {len(picks)}  sports covered: {len(per)}/{len(SPORTS)}")
    print(f"facts with https source: {sum(len(p['facts']) for p in picks)}")
    print(f"word counts: min {min(len(re.findall(chr(91)+'A-Za-z0-9'+chr(39)+chr(92)+'-'+chr(93)+'+', p['prediction'])) for p in picks)}, "
          f"max {max(len(re.findall(chr(91)+'A-Za-z0-9'+chr(39)+chr(92)+'-'+chr(93)+'+', p['prediction'])) for p in picks)}")
    for w in warns:
        print("WARN:", w)
    if errors:
        print("\nFAILURES:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()

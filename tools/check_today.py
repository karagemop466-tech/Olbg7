#!/usr/bin/env python3
"""check_today.py - verification pass for the 27 October 2026 board.

Fails (exit 1) on:
  * a broken internal link
  * a pick with no https source, or a market row with no OLBG link
  * a prediction under 30 words, or containing 'model' / 'verified'
  * a pick whose price falls outside the -250 to +10000 band without the
    'outside band' label being shown on the page
  * a duplicate pick on the same market
Also prints the band and length summary it checked.
"""
import json
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from picks_source import PICKS  # noqa: E402
from price_today import confidence  # noqa: E402

LINES = {r["id"]: r for r in json.load(open(os.path.join(ROOT, "data", "today", "lines.json")))["lines"]}
SPORTS = ["Golf", "Volleyball", "Rugby Union", "Cricket", "Snooker", "Darts", "Baseball",
          "Gaelic Sports", "Greyhounds", "Tennis", "Motor Racing", "Handball", "Ice Hockey",
          "Basketball", "Rugby League"]
SLUG = {s: s.lower().replace(" ", "-") for s in SPORTS}

problems = []
# Confidence boundary regression tests: strictly above 70%, with evidence and in-band.
if confidence(0.70, 8, False, True) == "high":
    problems.append("confidence rule labels exactly 70% as high")
if confidence(0.701, 8, False, True) != "high":
    problems.append("confidence rule does not label an in-band estimate above 70% as high")
if confidence(0.80, 8, False, False) == "high":
    problems.append("confidence rule labels an out-of-band estimate as high")
pages = ["index.html"] + [os.path.join("board", SLUG[s] + ".html") for s in SPORTS] + [
    os.path.join("board", p) for p in ("all-markets.html", "method.html", "sources.html", "flagged.html")]

# ---- internal links
link_re = re.compile(r'(?:href|src)="([^"]+)"')
checked = 0
for rel in pages:
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        problems.append("missing page: %s" % rel)
        continue
    body = open(path).read()
    for href in link_re.findall(body):
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = href.split("#")[0]
        if not target:
            continue
        resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
        checked += 1
        if not os.path.exists(resolved):
            problems.append("broken link: %s -> %s" % (rel, href))

# ---- confidence policy: a High label must be strictly >70% and in band
for r in LINES.values():
    if r["confidence"].startswith("high") and not (r["p"] is not None and r["p"] > 0.70 and r["band"] == "in"):
        problems.append("line %s is labelled High without >70%% and in-band price" % r["id"])

# ---- picks
words = []
seen = {}
for p in PICKS:
    line = LINES.get(p["id"])
    if not line:
        problems.append("pick %s has no line" % p["id"])
        continue
    w = len(p["prediction"].split())
    words.append(w)
    if w < 30:
        problems.append("pick %s is %d words" % (p["id"], w))
    if re.search(r"\b(model|models|modelled|verified|verify)\b", p["prediction"], re.I):
        problems.append("pick %s contains a banned word" % p["id"])
    if not p["facts"] or any(not f["src"].startswith("https://") for f in p["facts"]):
        problems.append("pick %s has a fact without an https source" % p["id"])
    key = (line["event"], line["market"], line["sel"])
    if key in seen:
        problems.append("duplicate pick on %s" % (key,))
    seen[key] = p["id"]
    if not line["link"].startswith("https://www.olbg.com/"):
        problems.append("pick %s: OLBG link is not an olbg.com URL" % p["id"])

# ---- band
for r in LINES.values():
    if r["price_am"] is None:
        continue
    if not (-250 <= r["price_am"] <= 10000):
        if r["band"] != "outside":
            pass  # engine already labels it; checked below on the sport pages

band_out = [p for p in PICKS if LINES[p["id"]]["price_am"] is not None
            and not (-250 <= LINES[p["id"]]["price_am"] <= 10000)]
for p in band_out:
    page = os.path.join(ROOT, "board", SLUG[LINES[p["id"]]["sport"]] + ".html")
    if "outside band" not in open(page).read():
        problems.append("pick %s is outside the band and the page does not say so" % p["id"])

# ---- every market row on the all-markets page must carry a link
am = open(os.path.join(ROOT, "board", "all-markets.html")).read()
market_rows = re.findall(r"<tr><td>.*?</tr>", am, re.S)
if len(market_rows) != len(LINES):
    problems.append("all-markets page has %d rows but engine has %d market lines" % (len(market_rows), len(LINES)))
for i, row in enumerate(market_rows, 1):
    if not re.search(r'<a href="https://www\.olbg\.com/', row):
        problems.append("all-markets row %d has no OLBG source link" % i)

print("pages checked: %d" % len(pages))
print("internal links resolved: %d" % checked)
print("picks: %d, words min/median/max: %d/%d/%d" % (
    len(PICKS), min(words), sorted(words)[len(words) // 2], max(words)))
print("picks outside the -250/+10000 band: %d (%s)" % (
    len(band_out), ", ".join(p["id"] for p in band_out) or "none"))
print("sports with 5+ picks: %d of %d" % (
    sum(1 for s in SPORTS if sum(1 for p in PICKS if LINES[p["id"]]["sport"] == s) >= 5), len(SPORTS)))
if problems:
    print("\nPROBLEMS (%d):" % len(problems))
    for x in problems:
        print(" -", x)
    sys.exit(1)
print("\nall checks passed")

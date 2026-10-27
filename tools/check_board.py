#!/usr/bin/env python3
"""Verify the built board: internal links, prediction quality gates, and data invariants."""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_PAGES = [p for p in sorted(os.listdir(ROOT)) if p.endswith(".html") and p != "all-events.html"]
PAGES = ROOT_PAGES + ["sports/" + p for p in sorted(os.listdir(os.path.join(ROOT, "sports")))
                      if p.endswith(".html")]

def local_links(text, page):
    hrefs = re.findall(r'href="([^"]+)"', text)
    out = []
    for h in hrefs:
        if h.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = h.split("#")[0]
        if not target:
            continue
        base = os.path.dirname(os.path.join(ROOT, page))
        out.append((h, os.path.normpath(os.path.join(base, target))))
    return out

fails = []
links = 0
for page in PAGES:
    path = os.path.join(ROOT, page)
    if not os.path.exists(path):
        fails.append(f"missing page {page}")
        continue
    text = open(path).read()
    for h, target in local_links(text, page):
        links += 1
        if not os.path.exists(target):
            fails.append(f"{page}: broken link {h}")
    if '<link rel="stylesheet"' in text:
        css = re.search(r'href="([^"]*assets/board.css)"', text)
        if css:
            p = os.path.normpath(os.path.join(os.path.dirname(path), css.group(1)))
            if not os.path.exists(p):
                fails.append(f"{page}: css missing {css.group(1)}")

lines = json.load(open(os.path.join(ROOT, "data/board/lines.json")))["lines"]
picks = json.load(open(os.path.join(ROOT, "data/board/picks-team.json"))) + \
        json.load(open(os.path.join(ROOT, "data/board/picks-individual.json")))

seen_pred = set()
for p in picks:
    w = len(re.findall(r"[A-Za-z0-9'’\-]+", p["pred"]))
    if w < 30:
        fails.append(f"{p['id']}: prediction only {w} words")
    if p["pred"] in seen_pred:
        fails.append(f"{p['id']}: duplicate prose")
    seen_pred.add(p["pred"])
    for bad in ("model", "verified"):
        if re.search(rf"\b{bad}\b", p["pred"], re.I):
            fails.append(f"{p['id']}: banned word '{bad}' in prose")
    if not any(f[1].startswith("https://") for f in p["facts"]):
        fails.append(f"{p['id']}: no https fact")
    first_sentence = p["pred"].split(".")[0].lower()
    tokens = [t.lower() for t in re.findall(r"[A-Za-z]{4,}", p["sel"])]
    if p["sel"].lower() not in p["pred"].lower() and not any(t in first_sentence for t in tokens):
        fails.append(f"{p['id']}: selection '{p['sel']}' not named in the opening sentence")

for r in lines:
    for m in r["markets"]:
        if not (0 < m["p"] < 1):
            fails.append(f"{r['id']}: probability out of range {m['p']}")
        if m["price"] <= 1.0:
            fails.append(f"{r['id']}: price <= 1.0")
        if not m.get("basis"):
            fails.append(f"{r['id']}: market without a stated basis")
    if not r["markets"] and not r["unpriced"]:
        fails.append(f"{r['id']}: unpriced without a reason")

ids = [p["id"] for p in picks]
if len(ids) != len(set(ids)):
    fails.append("duplicate pick ids")

print(f"pages {len(PAGES)}  internal links {links}  picks {len(picks)}  "
      f"events {len(lines)}  markets {sum(len(r['markets']) for r in lines)}")
WORD = re.compile(r"[A-Za-z0-9'\u2019\-]+")
counts = [len(WORD.findall(x["pred"])) for x in picks]
print("prediction words: min %d, max %d, mean %.0f" % (min(counts), max(counts), sum(counts)/len(counts)))
if fails:
    print("FAILURES:")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("all checks passed")

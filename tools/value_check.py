#!/usr/bin/env python3
"""Verify the value desk data and the generated site.

Run: python3 tools/value_check.py   (exit 1 on any failure)
Writes data/value/verification.json with the full result.
"""
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V = ROOT / "data" / "value"
D = ROOT / "value-desk"

errors, warnings, checked = [], [], Counter()


def ok(cond, msg):
    if not cond:
        errors.append(msg)
    return cond


def warn(cond, msg):
    if not cond:
        warnings.append(msg)


def load(name):
    return json.loads((V / f"{name}.json").read_text())


summary = load("summary")
picks = load("picks")["picks"]
lines = load("lines")["lines"]
flags = load("flags")["flags"]
sources = load("sources")["sources"]

# ------------------------------------------------------------------ data ---
ok(len(picks) == summary["picks"], "summary pick count mismatch")
ok(len(lines) == summary["lines"], "summary line count mismatch")
ok(len(set(p["id"] for p in picks)) == len(picks), "duplicate pick ids")
ok(len(set(l["id"] for l in lines)) == len(lines), "duplicate line ids")
ok(len(set(p["prediction"] for p in picks)) == len(picks), "duplicate prediction text")

SPORTS = list(summary["per_sport"])
per = Counter(p["sport"] for p in picks)
for s in SPORTS:
    ok(per[s] >= 5, f"{s} has fewer than five picks ({per[s]})")
    ok(set(p["sport"] for p in picks) <= set(SPORTS), f"unknown sport {s}")

for p in picks:
    checked["picks"] += 1
    i = p["id"]
    ok(p["word_count"] >= 30, f"{i}: prediction under 30 words")
    ok(len(p["prediction"].split()) == p["word_count"], f"{i}: word count mismatch")
    ok(not re.search(r"\b(model|verified|verification)\b", p["prediction"], re.I),
       f"{i}: banned word in prediction")
    ok(p["confidence"] in ("low", "medium", "high"), f"{i}: bad confidence label")
    ok(1.40 - 1e-9 <= p["price_dec"] <= 101.0 + 1e-9, f"{i}: price outside band")
    ok(p["olbg_url"].startswith("https://"), f"{i}: missing OLBG source URL")
    ok(any(f["source"].startswith("https://") for f in p["facts"]),
       f"{i}: no https source link on facts")
    ok(all(f["source"].startswith("https://") for f in p["facts"]),
       f"{i}: a fact has a non-https source")
    ok(bool(p["selection"]) and bool(p["event"]), f"{i}: blank selection or event")
    ok(bool(p["price_american"]), f"{i}: blank american price")
    for f in p["facts"]:
        checked["facts"] += 1
        ok(f["kind"] in ("official", "olbg", "media", "secondary"),
           f"{i}: unknown fact kind {f['kind']}")
    # high-confidence rule
    if p["confidence"] == "high":
        kinds = {f["kind"] for f in p["facts"]}
        ok(len(p["facts"]) >= 2 and kinds & {"official", "olbg"} and p["p_fair"] >= 0.07,
           f"{i}: high label does not satisfy the published rule")

for l in lines:
    checked["lines"] += 1
    ok((l["olbg_url"] or l["official_url"]).startswith("https://"),
       f"{l['id']}: line has no https source URL")
    ok(1.40 - 1e-9 <= l["price_dec"] <= 101.0 + 1e-9, f"{l['id']}: line outside band")
    ok(0 < l["p_fair"] < 1, f"{l['id']}: invalid fair probability")
    ok(bool(l["method"]), f"{l['id']}: no pricing method")

for s in sources:
    checked["sources"] += 1
    ok(s["url"].startswith("https://"), f"source without https: {s['url']}")

for f in flags:
    checked["flags"] += 1
    ok(any(u.startswith("https://") for u in f["sources"]),
       f"{f['id']}: flag has no https source link")

# ------------------------------------------------------------------ html ---
PAGES = ["index.html", "picks.html", "value.html", "lines.html", "sports.html",
         "sources.html", "flagged.html", "method.html"] + [
         f"sports/{re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')}.html" for s in SPORTS]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.ids = []
        self.rows = []
        self._row = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "tr":
            self._row = []
        if self._row is not None and tag == "a" and a.get("href"):
            self._row.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None


all_text = {}
for rel in PAGES:
    path = D / rel
    ok(path.exists(), f"missing page {rel}")
    if not path.exists():
        continue
    text = path.read_text()
    all_text[rel] = text
    checked["pages"] += 1
    ok("<nav>" in text and "style.css" in text, f"{rel}: missing nav or stylesheet")
    ok("Flagged for review" in text, f"{rel}: nav missing flagged link")
    parser = Links()
    parser.feed(text)
    # duplicate ids
    dup = [k for k, c in Counter(parser.ids).items() if c > 1]
    ok(not dup, f"{rel}: duplicate HTML ids {dup[:4]}")
    # local links resolve
    for href in parser.hrefs:
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = (path.parent / href.split("#")[0]).resolve()
        ok(target.exists(), f"{rel}: broken internal link {href}")
        if "#" in href:
            frag = href.split("#", 1)[1]
            if not frag:
                continue
            dest_rel = (path.parent / href.split("#")[0]).resolve()
            if dest_rel.suffix == ".html" and dest_rel.exists():
                dest_txt = all_text.get(dest_rel.relative_to(D).as_posix(), dest_rel.read_text())
                ok(f'id="{frag}"' in dest_txt, f"{rel}: missing anchor #{frag} in {dest_rel.name}")
    # every data table row carries an https source link
    for n, row in enumerate(parser.rows, 1):
        if not row:
            continue
        if any(h.startswith("https://") for h in row):
            checked["html_rows_with_source"] += 1
        else:
            errors.append(f"{rel}: table row {n} has no https source link ({row[:3]})")
    # banned words must not appear in rendered prediction copy
    body = text.split("<main", 1)[-1]
    if rel.startswith("sports/") or rel in ("picks.html",):
        ok(not re.search(r"\b(model|verified)\b", body, re.I),
           f"{rel}: banned word appears on the page")

# every pick must have a reachable anchor on its sport page
for p in picks:
    sp = f"sports/{re.sub(r'[^a-z0-9]+','-',p['sport'].lower()).strip('-')}.html"
    ok(f'id="{p["id"]}"' in all_text.get(sp, ""), f"{p['id']}: no prediction anchor on {sp}")

# site must not claim bookmaker odds
for rel, text in all_text.items():
    ok("bookmaker odds" not in text.lower() or "no bookmaker" in text.lower()
       or "blank" in text.lower(), f"{rel}: unqualified bookmaker-odds claim")

# --------------------------------------------------------------- result ----
result = {
    "date": "2026-10-27",
    "session": "sess-arena-7cf491a1",
    "passed": not errors,
    "errors": errors,
    "warnings": warnings,
    "checked": dict(checked),
    "counts": {
        "sports": len(SPORTS), "picks": len(picks), "lines": len(lines),
        "facts": sum(len(p["facts"]) for p in picks), "sources": len(sources),
        "flags": len(flags), "pages": len(PAGES),
        "high": sum(p["confidence"] == "high" for p in picks),
        "plus_money": sum(p["plus_money"] for p in picks),
    },
}
(V / "verification.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
print(json.dumps(result["counts"], indent=2))
print(f"checked: {dict(checked)}")
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings[:20]:
        print(" -", w)
if errors:
    print(f"FAILED ({len(errors)} errors):")
    for x in errors[:40]:
        print(" -", x)
    sys.exit(1)
print("PASS — all data rows sourced, all pages linked, no banned words, no broken links.")

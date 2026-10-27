#!/usr/bin/env python3
"""Checks on the built 2026-10-27 board and the data behind it.

Exit 1 on any of: missing page, broken internal link or anchor, a pick under 30 words, a
banned word in any visible page text, a pick without an https source, a duplicate pick id,
a market row without an OLBG source link, a high-confidence line on a grade C market, a
price outside sanity range, or a sports shortfall that is not flagged on the site.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data/cycle-20261027")
CYCLE = "2026-10-27"
SPORTS = ["Golf", "Volleyball", "Rugby Union", "Cricket", "Snooker", "Darts", "Baseball",
          "Gaelic Sports", "Greyhounds", "Tennis", "Motor Racing", "Handball", "Ice Hockey",
          "Basketball", "Rugby League"]
SLUG = {s: s.lower().replace(" ", "-") for s in SPORTS}
BANNED = ("model", "verified", "verified", "verifying")
TARGET = 5


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.ids, self.text = [], set(), []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip += 1
        if a.get("href"):
            self.hrefs.append(a["href"])
        if a.get("id"):
            self.ids.add(a["id"])

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def main():
    err, warn = [], []
    lines = json.load(open(os.path.join(D, "lines.json")))
    preds = json.load(open(os.path.join(D, "predictions.json")))["picks"]
    flags = json.load(open(os.path.join(D, "flags.json")))["flags"]
    srcs = json.load(open(os.path.join(D, "sources.json")))["sources"]

    pages = (["index.html", "all-events.html", "flagged.html", "sources.html", "methodology.html"]
             + [f"sports/{SLUG[s]}.html" for s in SPORTS])

    ids_by_page, hrefs, pending = {}, {}, []
    for pg in pages:
        path = os.path.join(ROOT, pg)
        if not os.path.exists(path):
            err.append(f"missing page {pg}")
            continue
        html_src = open(path, encoding="utf-8").read()
        par = P()
        par.feed(html_src)
        ids_by_page[pg], hrefs[pg] = par.ids, par.hrefs
        visible = " ".join(par.text)
        for w in BANNED:
            for m in re.finditer(r"\b" + w + r"\b", visible, re.I):
                ctx = visible[max(0, m.start() - 45):m.end() + 35].replace("\n", " ")
                err.append(f"{pg}: banned word '{w}' in visible text ...{ctx}...")
        # internal links + anchors
        base = os.path.dirname(path)
        for h in par.hrefs:
            if h.startswith(("http://", "https://", "mailto:", "javascript:")):
                continue
            f, _, frag = h.partition("#")
            tgt = os.path.normpath(os.path.join(base, f)) if f else path
            if not os.path.exists(tgt):
                err.append(f"{pg}: broken internal link -> {h}")
            elif frag:
                pending.append((pg, h, os.path.relpath(tgt, ROOT), frag))
        if pg.endswith(".css"):
            continue

    # external links must be well formed
    for pg, hs in hrefs.items():
        for h in hs:
            if h.startswith("https://"):
                if " " in h or not re.match(r"^https://[A-Za-z0-9._\-]+(/[A-Za-z0-9._~:/?#@!$&'()*+,;=%\-]*)?$", h):
                    err.append(f"{pg}: malformed external link {h}")
            elif h.startswith("http://"):
                err.append(f"{pg}: insecure link {h}")

    for pg, h, tgt, frag in pending:
        if frag not in ids_by_page.get(tgt, set()):
            err.append(f"{pg}: anchor #{frag} does not exist on {tgt}")

    # picks
    seen = set()
    per = {}
    for p in preds:
        per[p["sport"]] = per.get(p["sport"], 0) + 1
        if p["id"] in seen:
            err.append(f"duplicate pick id {p['id']}")
        seen.add(p["id"])
        wc = len(re.findall(r"[A-Za-z0-9'\-]+", p["prediction"]))
        if wc < 30:
            err.append(f"{p['id']}: {wc} words (<30)")
        if not p["facts"]:
            err.append(f"{p['id']}: no facts")
        https = [f for f in p["facts"] if (f.get("url") or "").startswith("https://")]
        if not https:
            err.append(f"{p['id']}: no https source on any fact")
        if p["confidence"] == "high" and p["grade"] == "C":
            err.append(f"{p['id']}: high confidence on a grade C market")
        if p["our_line"] and not (1.01 <= p["our_line"] <= 1000):
            err.append(f"{p['id']}: implausible price {p['our_line']}")
        if p["our_line"] and p["confidence"] == "high" and not (1.40 <= p["our_line"] <= 101.0):
            err.append(f"{p['id']}: high confidence outside the focus band")
        for page in [f"sports/{SLUG[p['sport']]}.html"]:
            if p["id"] not in ids_by_page.get(page, set()):
                err.append(f"{p['id']}: no anchor on {page}")
    # the page must be reachable from the index by anchor (second pass: all ids known now)
    for p in preds:
        link = f"sports/{SLUG[p['sport']]}.html#{p['id']}"
        if link not in hrefs.get("index.html", []):
            err.append(f"{p['id']}: index does not link to {link}")

    # coverage of all 15 sports, with shortfall flagged on the site
    flagtxt = open(os.path.join(ROOT, "flagged.html"), encoding="utf-8").read()
    for s in SPORTS:
        page = f"sports/{SLUG[s]}.html"
        if not os.path.exists(os.path.join(ROOT, page)):
            err.append(f"missing sport page {page}")
            continue
        n = per.get(s, 0)
        if n < TARGET:
            body = open(os.path.join(ROOT, page), encoding="utf-8").read()
            if s in ("Snooker", "Greyhounds"):
                if "No tips found" not in body:
                    err.append(f"{s}: empty slate not explained on the sport page")
            elif "and not five" not in open(os.path.join(ROOT, page), encoding="utf-8").read():
                err.append(f"{s}: {n} picks (target {TARGET}) but the sport page does not explain the shortfall")
        if s in ("Snooker", "Greyhounds") and f"{s}" not in flagtxt:
            err.append(f"{s}: empty-slate flag missing from flagged.html")

    # every market row must appear on all-events.html with an OLBG link
    alle = open(os.path.join(ROOT, "all-events.html"), encoding="utf-8").read()
    missing = 0
    for r in lines["lines"]:
        if str(r.get("event_id") or "no-events") not in alle and r["event"].replace(" ", "") not in alle.replace(" ", ""):
            missing += 1
    if missing:
        warn.append(f"{missing} captured market(s) not obviously present on all-events.html")
    if alle.count("olbg.com") < len(lines["lines"]):
        err.append(f"all-events.html: only {alle.count('olbg.com')} OLBG links for {len(lines['lines'])} rows")

    # data integrity
    grades = {"A": 0, "B": 0, "C": 0}
    for r in lines["lines"]:
        o = r.get("our_line")
        if o:
            grades[o["grade"]] += 1
            if not (0 < o["p_fair"] < 1):
                err.append(f"{r['event']}/{r['selection']}: p_fair out of range")
            if o["card_decimal"] < 1.01:
                err.append(f"{r['event']}/{r['selection']}: impossible price")
            if o["grade"] == "C" and o["confidence"] == "high":
                err.append(f"{r['event']}/{r['selection']}: high confidence on grade C")
        elif not r.get("unpriced_reason"):
            err.append(f"{r['event']}/{r['selection']}: unpriced with no reason recorded")
    seen_f = set()
    for f in flags:
        if f["id"] in seen_f:
            err.append(f"duplicate flag id {f['id']}")
        seen_f.add(f["id"])
        for k in ("id", "sport", "title", "detail", "action", "severity"):
            if not f.get(k):
                err.append(f"flag {f.get('id')}: missing {k}")

    # Neighbour boards. The 2026-10-27 merge took the root page names from session
    # a799d1c9's Coverage Desk and republished its board under desk/; this guard fails if
    # anyone drops, truncates or unlinks the relocated pages, or leaves a stale link behind.
    desk_pages = []
    desk_root = os.path.join(ROOT, "desk")
    for dirpath, _dirs, files in os.walk(desk_root):
        desk_pages += [os.path.join(dirpath, fn) for fn in sorted(files) if fn.endswith(".html")]
    if len(desk_pages) != 21:
        err.append(f"desk/: {len(desk_pages)} html pages, expected 21 (5 root pages + archive index + "
                   f"15 sport pages of the relocated Coverage Desk)")
    else:
        moved = re.compile(r'(?:href|src)="(?!https?:|mailto:|#)([^"#]+)')
        for pg in desk_pages:
            rel = os.path.relpath(pg, ROOT)
            txt = open(pg, encoding="utf-8").read()
            if "Moved here on 27 Oct 2026" not in txt:
                err.append(f"{rel}: the relocated board is missing its move notice")
            for m in moved.finditer(txt):
                tgt = os.path.normpath(os.path.join(os.path.dirname(pg), m.group(1)))
                if not os.path.exists(tgt):
                    err.append(f"{rel}: broken link {m.group(1)}")
        index_txt = open(os.path.join(desk_root, "index.html"), encoding="utf-8").read()
        for must in ("data-snapshot", "data-expiry", "assets/desk.js"):
            if must not in index_txt:
                err.append(f"desk/index.html: relocated page lost its {must} attribute/file")

    print(f"pages: {len(pages)}   links: {sum(len(v) for v in hrefs.values())}   "
          f"markets: {len(lines['lines'])} (priced {lines['totals']['priced']}, unpriced {lines['totals']['unpriced']})")
    print(f"picks: {len(preds)} over {len(per)}/{len(SPORTS)} sports   grades: {grades}   "
          f"flags: {len(flags)}   sources: {len(srcs)}")
    print("picks per sport:", ", ".join(f"{s}={per.get(s,0)}" for s in SPORTS))
    for w in warn:
        print("WARN:", w)
    if err:
        print("\nFAILURES:")
        for e in err:
            print(" -", e)
        sys.exit(1)
    print("\nAll cycle checks passed.")


if __name__ == "__main__":
    main()

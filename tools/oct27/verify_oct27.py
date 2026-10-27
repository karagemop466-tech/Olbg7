#!/usr/bin/env python3
"""End-to-end verification suite for the 27 October 2026 15-sport dashboard."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(ROOT, "data", "oct27")

ALLOWED_SPORTS = {
    "Golf", "Volleyball", "Rugby Union", "Cricket", "Snooker",
    "Darts", "Baseball", "Gaelic Sports", "Greyhounds", "Tennis",
    "Motor Racing", "Handball", "Ice Hockey", "Basketball", "Rugby League"
}
SLUGS = [s.lower().replace(" ", "-") for s in sorted(ALLOWED_SPORTS)]


def main():
    errors = []
    events = json.load(open(os.path.join(DATA_DIR, "events.json")))["events"]
    lines = json.load(open(os.path.join(DATA_DIR, "lines.json")))["lines"]
    picks = json.load(open(os.path.join(DATA_DIR, "picks.json")))["picks"]
    flags = json.load(open(os.path.join(DATA_DIR, "flags.json")))["flags"]

    # 1. Sport scope check
    for collection_name, rows in (("events", events), ("lines", lines), ("picks", picks)):
        bad = {r["sport"] for r in rows if r["sport"] not in ALLOWED_SPORTS}
        if bad:
            errors.append(f"{collection_name} contains off-scope sports: {bad}")

    # 2. Originated lines completeness & source links
    for l in lines:
        if l.get("price_dec") is None or l.get("price_am") is None or l.get("p_fair") is None:
            errors.append(f"Line {l['id']} is missing originated price/probability")
        if l.get("confidence") not in ("high", "medium", "low"):
            errors.append(f"Line {l['id']} has invalid confidence {l.get('confidence')}")
        if l["confidence"] == "high" and not (1.40 <= l["price_dec"] <= 101.00):
            errors.append(f"High-confidence line {l['id']} ({l['price_am_str']}) is outside [-250, +10000]")
        if not str(l.get("olbg_url", "")).startswith("https://www.olbg.com/"):
            errors.append(f"Line {l['id']} missing valid OLBG URL")
        if not str(l.get("official_url", "")).startswith("https://"):
            errors.append(f"Line {l['id']} missing valid official https URL")

    # 3. Written predictions checks
    banned_re = re.compile(r"\b(model\w*|verif\w*)\b", re.I)
    for p in picks:
        wc = len(re.findall(r"[A-Za-z0-9'\-\.]+", p["prediction"]))
        if wc < 30:
            errors.append(f"Pick {p['pick_id']} has {wc} words (<30)")
        if banned_re.search(p["prediction"]) or banned_re.search(p["headline"]):
            errors.append(f"Pick {p['pick_id']} contains banned word (model*/verif*)")
        if not (-250 <= p["price_am"] <= 10000) or not (1.40 <= p["price_dec"] <= 101.00):
            errors.append(f"Pick {p['pick_id']} price {p['price_am_str']} ({p['price_dec']}) outside [-250, +10000]")
        if not p["olbg_url"].startswith("https://www.olbg.com/") or not p["official_url"].startswith("https://"):
            errors.append(f"Pick {p['pick_id']} missing https source URL")

    # 4. HTML pages & internal link + anchor resolution + rendered card banned-word check
    pages = ["index.html"] + [
        f"oct27/{p}" for p in ("all-markets.html", "flagged.html", "repo-audit.html", "methodology.html", "sources.html")
    ] + [f"oct27/sports/{slug}.html" for slug in SLUGS]

    href_re = re.compile(r'(?:href|src)="([^"]+)"')
    id_re = re.compile(r'\bid="([^"]+)"')
    card_re = re.compile(r'<article class="pick-card".*?</article>', re.S)

    id_cache = {}
    for rel in pages:
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            errors.append(f"Missing generated HTML page: {rel}")
            continue
        txt = open(full, encoding="utf-8").read()
        id_cache[os.path.normpath(full)] = set(id_re.findall(txt))

        # Check rendered pick cards for banned words
        for card_html in card_re.findall(txt):
            clean = re.sub(r"<[^>]+>", " ", card_html)
            m = banned_re.search(clean)
            if m:
                errors.append(f"Rendered pick card in {rel} contains banned word '{m.group(0)}'")

    resolved_links = 0
    for rel in pages:
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            continue
        txt = open(full, encoding="utf-8").read()
        for href in href_re.findall(txt):
            if href.startswith(("http://", "https://", "mailto:", "javascript:")):
                continue
            if href.startswith("#"):
                anchor = href[1:]
                if anchor and anchor not in id_cache[os.path.normpath(full)]:
                    errors.append(f"Broken local anchor in {rel}: {href}")
                continue
            parts = href.split("#", 1)
            target_rel = parts[0]
            anchor = parts[1] if len(parts) > 1 else ""
            target_full = os.path.normpath(os.path.join(os.path.dirname(full), target_rel))
            resolved_links += 1
            if not os.path.exists(target_full):
                errors.append(f"Broken internal link in {rel}: {href} -> {target_full}")
            elif anchor:
                if target_full not in id_cache:
                    id_cache[target_full] = set(id_re.findall(open(target_full, encoding="utf-8").read()))
                if anchor not in id_cache[target_full]:
                    errors.append(f"Broken cross-page anchor in {rel}: {href}")

    # 5. Check every row in oct27/all-markets.html has both OLBG and official source links
    am_txt = open(os.path.join(ROOT, "oct27", "all-markets.html"), encoding="utf-8").read()
    tr_rows = re.findall(r"<tr data-sport=.*?</tr>", am_txt, re.S)
    if len(tr_rows) != len(lines):
        errors.append(f"all-markets.html row count {len(tr_rows)} != lines count {len(lines)}")
    for idx, tr in enumerate(tr_rows, start=1):
        if "https://www.olbg.com/" not in tr or tr.count('target="_blank"') < 2:
            errors.append(f"all-markets.html row {idx} missing dual OLBG + official source links")

    print(f"Checked {len(pages)} HTML pages and {resolved_links} internal links.")
    print(f"Verified {len(events)} OLBG events, {len(lines)} originated lines, {len(picks)} picks, {len(flags)} flags.")
    if errors:
        print(f"VERIFICATION FAILED ({len(errors)} errors):")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("ALL OCT27 VERIFICATION CHECKS PASSED!")


if __name__ == "__main__":
    main()

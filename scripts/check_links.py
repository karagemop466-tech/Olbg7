#!/usr/bin/env python3
"""Fail the build if any internal link in docs/ points at a missing file."""
import os, re, sys
S = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
bad = []
for root, _, files in os.walk(S):
    for f in files:
        if not f.endswith(".html"):
            continue
        path = os.path.join(root, f)
        for href in re.findall(r'href=[\'"]([^\'"#]+)', open(path).read()):
            if href.startswith(("http", "mailto")):
                continue
            tgt = os.path.normpath(os.path.join(root, href.split("?")[0]))
            if not os.path.exists(tgt):
                bad.append((path, href))
print(f"checked docs/ : {len(bad)} broken internal links")
for b in bad[:25]:
    print("  BROKEN", b)
sys.exit(1 if bad else 0)

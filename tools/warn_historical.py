#!/usr/bin/env python3
"""Add a non-destructive archive warning to each preserved, previously generated page."""
from pathlib import Path
import os
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    changed = 0
    for base in ('docs', 'olbg-tips'):
        for path in (ROOT / base).rglob('*.html'):
            content = path.read_text(encoding='utf-8')
            if 'id="historical-warning"' in content:
                continue
            url = os.path.relpath(ROOT / 'archive.html', path.parent).replace(os.sep, '/')
            warning = (f'<div id="historical-warning" role="note" style="padding:14px 20px;background:#fff0cd;color:#543800;'
                       f'border-bottom:2px solid #c99a42;font:600 15px/1.5 system-ui,sans-serif">'
                       f'ARCHIVED HISTORICAL BOARD — fixtures, odds and confidence labels are dated and not rechecked. '
                       f'Do not treat them as current or reliable. <a style="color:#163c4d;text-decoration:underline" '
                       f'href="{url}">Archive warning and current desk</a>.</div>')
            result, n = re.subn(r'(<body(?:\s[^>]*)?>)', lambda m: m.group(1)+warning, content, count=1, flags=re.I)
            if n != 1:
                raise SystemExit(f'No body tag found: {path.relative_to(ROOT)}')
            path.write_text(result, encoding='utf-8'); changed += 1
    print(f'Added archive warnings to {changed} preserved HTML pages')


if __name__ == '__main__': main()

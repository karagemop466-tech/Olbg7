#!/usr/bin/env python3
"""Add an idempotent archive warning without deleting preserved historic pages."""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import html
import os
import re

ROOT = Path(__file__).resolve().parents[1]


def redirect_legacy_root_links(content):
    """Keep old root deep links on their matching archived CAL-4 pages."""
    mirrored = {'index.html','picks.html','lines.html','method.html','olbg-map.html','sources.html','flagged.html','archive.html'}
    def replace(match):
        raw = html.unescape(match.group(2)); ref = urlsplit(raw)
        if ref.scheme or ref.netloc or not ref.path or ref.path.startswith('/'):
            return match.group(0)
        if ref.path not in mirrored and not ref.path.startswith('sports/'):
            return match.group(0)
        updated = urlunsplit(('', '', 'legacy-cal4/' + ref.path, ref.query, ref.fragment))
        return match.group(1) + '="' + html.escape(updated, quote=True) + '"'
    return re.sub(r'\b(href|src)="([^"]*)"', replace, content)


def main():
    changed = 0
    paths = [path for base in ('docs', 'olbg-tips', 'board', 'legacy-cal4') for path in (ROOT/base).rglob('*.html')]
    paths += [ROOT / name for name in ('picks.html', 'lines.html', 'method.html') if (ROOT / name).exists()]
    for path in paths:
        content = path.read_text(encoding='utf-8')
        if 'id="historical-warning"' in content:
            continue
        if path.parent == ROOT:
            content = redirect_legacy_root_links(content)
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

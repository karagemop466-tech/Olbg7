#!/usr/bin/env python3
"""Offline structural checks for the published snapshot (not external fact checking)."""
from collections import Counter
from datetime import datetime, timedelta
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
D = json.loads((ROOT / 'data/current.json').read_text(encoding='utf-8'))
ERRORS = []


def require(condition, message):
    if not condition: ERRORS.append(message)


def timestamp(value, label):
    try:
        if not isinstance(value, str) or not value.endswith('Z'): raise ValueError('UTC Z required')
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        ERRORS.append(f'{label}: invalid UTC timestamp {value!r}')
        return None


def url(value, label, official=False):
    parsed = urlsplit(value or '')
    require(parsed.scheme == 'https' and bool(parsed.netloc), f'{label}: invalid HTTPS source {value!r}')
    if official:
        require(not parsed.netloc.endswith('olbg.com'), f'{label}: official source cannot be OLBG')


meta = D['metadata']
start = timestamp(meta['snapshot_at'], 'snapshot start')
end = timestamp(meta['snapshot_expires'], 'snapshot expiry')
if start and end: require(timedelta(0) < end - start <= timedelta(hours=24), 'snapshot must expire within 24 hours')
require(meta.get('live_ingestion') is False, 'snapshot must not claim working ingestion')
sports = {s['slug']: s for s in D['sports']}
require(len(sports) == len(D['sports']) == 15, 'there must be 15 distinct sports')
for s in D['sports']:
    url(s['hub'], s['name'] + ' hub')
    url(s['official'], s['name'] + ' official', official=True)
    for x in s.get('extra_hubs', []): url(x['url'], s['name'] + ' extra hub')

records = D['events'] + D['watchlist']
ids = [e['id'] for e in records]
require(len(ids) == len(set(ids)), 'event/watchlist IDs must be unique')
events = {e['id']: e for e in D['events']}
for e in records:
    label = f"{e['sport']} {e['id']}"
    require(e['sport'] in sports, f'{label}: unknown sport')
    url(e['olbg'], label + ' OLBG')
    url(e['official'], label + ' official', official=True)
    if e['id'] in events:
        require(e['official_confirmed'] is True, f'{label}: scheduled row must have official match source')
        until = timestamp(e['display_until_utc'], label + ' cutoff')
        if start and until: require(until > start, f'{label}: cutoff is not after snapshot start')
        if e['start_utc']:
            event_start = timestamp(e['start_utc'], label + ' start')
            if until and event_start: require(until <= event_start, f'{label}: cutoff is later than event start')
        require(bool(e['markets']), f'{label}: markets must be observed or represented as unknown')
    else:
        require(e['official_confirmed'] is False and e['scope'] == 'unconfirmed', f'{label}: watchlist must be flagged')
        require(all(e.get(k) is None for k in ('date_label', 'start_utc', 'display_until_utc', 'markets')), f'{label}: unconfirmed fields must be blank')
        require(bool(e.get('observed_at')) and bool(e.get('note')), f'{label}: capture and uncertainty required')

pick_ids = set()
event_picks = set()
for p in D['picks']:
    label = f"pick {p['id']}"
    require(p['id'] not in pick_ids, f'{label}: duplicate pick ID'); pick_ids.add(p['id'])
    require(p['event_id'] in events, f'{label}: missing scheduled event')
    require(p['event_id'] not in event_picks, f'{label}: multiple notes for one event'); event_picks.add(p['event_id'])
    require(p['confidence'] in ('low', 'medium', 'high'), f'{label}: invalid confidence')
    require(len(p['text'].split()) >= 30, f'{label}: fewer than 30 words')
    require(not re.search(r'\b(model|verified)\b', p['text'], re.I), f'{label}: banned prose term')
    require(bool(p['selection']) and bool(p['market']) and bool(p['sources']), f'{label}: missing selection, market or evidence')
    for s in p['sources']: url(s['url'], label + ' evidence', official=True)
    if p.get('reported_quote'):
        q = p['reported_quote']
        require(bool(q.get('published')) and bool(q.get('bookmaker')), f'{label}: historical quote needs date and bookmaker')
        url(q.get('url'), label + ' historical quote')


class Parse(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []; self.ids = set(); self.fresh = []; self.rows = []
        self.row = None; self.row_has_td = False; self.warnings = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            require(a['id'] not in self.ids, f'duplicate HTML id {a["id"]!r}')
            self.ids.add(a['id'])
            if a['id'] == 'historical-warning': self.warnings += 1
        if tag in ('a','link') and a.get('href'): self.refs.append(a['href'])
        if tag in ('script','img') and a.get('src'): self.refs.append(a['src'])
        if 'data-fresh' in a: self.fresh.append(a)
        if tag == 'tr': self.row = []; self.row_has_td = False
        if self.row is not None and tag == 'td': self.row_has_td = True
        if self.row is not None and tag == 'a' and a.get('href'): self.row.append(a['href'])
    def handle_endtag(self, tag):
        if tag == 'tr' and self.row is not None:
            if self.row_has_td: self.rows.append(self.row)
            self.row = None


published = [ROOT/x for x in ('index.html','all-events.html','flagged.html','methodology.html','sources.html','archive.html','olbg-map.html')]
published += sorted((ROOT/'sports').glob('*.html'))
historical = [p for base in ('docs', 'olbg-tips', 'board', 'legacy-cal4') for p in sorted((ROOT/base).rglob('*.html'))]
historical += [ROOT/name for name in ('picks.html','lines.html','method.html','freshness.html')]
parsed = {}
for path in published + historical:
    require(path.is_file(), f'missing HTML: {path.relative_to(ROOT)}')
    if not path.is_file(): continue
    parser = Parse(); parser.feed(path.read_text(encoding='utf-8')); parsed[path.resolve()] = parser
    if path in historical: require(parser.warnings == 1, f'{path.relative_to(ROOT)}: historical warning missing or duplicated')
    else:
        for attrs in parser.fresh:
            require(bool(attrs.get('data-until')), f'{path.relative_to(ROOT)}: freshness row without cutoff')
            require(attrs.get('data-kind') in ('event','pick'), f'{path.relative_to(ROOT)}: unknown freshness kind')
        for links in parser.rows:
            require(any((u:=urlsplit(x)).scheme == 'https' and u.netloc and not u.netloc.endswith('olbg.com') for x in links), f'{path.relative_to(ROOT)}: table row lacks official source')

for path, parser in parsed.items():
    for raw in parser.refs:
        ref = urlsplit(raw)
        if ref.scheme or ref.netloc or raw.startswith('//'): continue
        if not ref.path: target = path
        elif ref.path.startswith('/'): target = (ROOT / ref.path.lstrip('/')).resolve()
        else: target = (path.parent / unquote(ref.path)).resolve()
        if target.is_dir(): target = target / 'index.html'
        require(target.is_relative_to(ROOT), f'{path.relative_to(ROOT)}: link escapes site: {raw}')
        require(target.exists(), f'{path.relative_to(ROOT)}: broken internal link: {raw}')
        if target in parsed and ref.fragment:
            require(unquote(ref.fragment) in parsed[target].ids, f'{path.relative_to(ROOT)}: missing anchor {raw}')

coordination = (ROOT/'COORDINATION.md').read_text(encoding='utf-8')
require(not re.search(r'^(<<<<<<< |=======|>>>>>>> )', coordination, re.M), 'unresolved coordination conflict markers')
for old in ('tools/build_board.py', 'tools/build_today.py'):
    require('LEGACY_BUILD' in (ROOT/old).read_text(encoding='utf-8'), f'{old}: missing archive rebuild guard')

css = (ROOT/'assets/desk.css').read_text(encoding='utf-8')
require('[data-fresh]' in css and '.is-visible' in css, 'fail-closed visibility CSS is missing')
if ERRORS: raise SystemExit('\n'.join(ERRORS))
counts = Counter(events[p['event_id']]['sport'] for p in D['picks'])
print(f"Checked {len(published)} dashboard and {len(historical)} historical pages; {len(events)} schedule rows, {len(D['watchlist'])} flagged rows, {len(D['picks'])} cited notes")
print('Notes by sport: ' + ', '.join(f'{sports[s]["name"]} {counts[s]}' for s in sports))
print('Offline checks do not establish factual correctness, live availability or external link health.')

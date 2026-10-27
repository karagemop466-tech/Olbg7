#!/usr/bin/env python3
"""Build the source-linked, fail-closed Pages snapshot. No network or dependencies."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/current.json').read_text(encoding='utf-8'))
META = DATA['metadata']
SPORTS = {s['slug']: s for s in DATA['sports']}
EVENTS = {e['id']: e for e in DATA['events']}
PICKS = DATA['picks']


def h(s):
    return escape(str(s), quote=True)


def link(url, text):
    return f'<a href="{h(url)}" rel="noopener noreferrer">{h(text)} ↗</a>'


def utc(value):
    if not value:
        return '—'
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return f'{dt.day} {dt:%b %Y · %H:%M} UTC'


def when(event):
    if event['start_utc']:
        return utc(event['start_utc'])
    return f"{h(event['date_label'])} <small>Exact start: —</small>"


def header(prefix, active=''):
    nav = [('Overview', 'index.html', 'overview'), ('All events', 'all-events.html', 'events'),
           ('Review flags', 'flagged.html', 'flags'), ('How it works', 'methodology.html', 'method')]
    links = ''.join(f'<a href="{prefix}{url}"' + (' aria-current="page"' if key == active else '') + f'>{label}</a>' for label, url, key in nav)
    return f'''<a class="sr-only" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="{prefix}index.html"><span class="brand-mark">CD</span><span class="brand-text"><strong>Coverage Desk</strong><small>OLBG research board</small></span></a><nav class="nav" aria-label="Main navigation">{links}</nav></div></header>
<div class="snapshot-strip" id="snapshot-status" role="status" aria-live="polite"><div class="wrap"><span class="dot" aria-hidden="true"></span><span id="snapshot-message">Manual snapshot began {utc(META['snapshot_at'])}. Checking this device clock; no automated refresh is running.</span></div></div>
<noscript><div class="notice"><strong>JavaScript is off.</strong> Current selections and scheduled rows are hidden because their freshness cannot be checked. Source and review links remain available.</div></noscript>'''


def footer(prefix):
    return f'''<footer class="footer"><div class="wrap footer-inner"><div><strong>Coverage Desk</strong><p>Independent research, not a live odds service. 18+. Betting carries risk.</p></div><div class="foot-links"><a href="{prefix}sources.html">Sources</a><a href="{prefix}archive.html">Historical boards</a><a href="https://www.gamcare.org.uk/" rel="noopener noreferrer">GamCare ↗</a><a href="https://www.gambleaware.org/" rel="noopener noreferrer">GambleAware ↗</a></div></div></footer>'''


def page(title, content, prefix='', active='', description='A source-linked, time-limited OLBG research snapshot.'):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{h(description)}"><title>{h(title)} | Coverage Desk</title><link rel="stylesheet" href="{prefix}assets/desk.css"><script src="{prefix}assets/desk.js" defer></script></head>
<body data-snapshot="{h(META['snapshot_at'])}" data-expiry="{h(META['snapshot_expires'])}">{header(prefix, active)}{content}{footer(prefix)}</body></html>\n'''


def freshness(event, kind):
    return f'data-fresh data-kind="{kind}" data-until="{h(event["display_until_utc"])}"'


def pick_card(pick, prefix='', compact=False):
    e = EVENTS[pick['event_id']]
    sport = SPORTS[e['sport']]
    level = pick['confidence']
    quote = pick.get('reported_quote')
    quote_html = ''
    if quote:
        quote_html = f'<div class="quote">Historical opening quote: <strong>+{h(quote["american"])}</strong>, {h(quote["bookmaker"])}, published {h(quote["published"])}. Not a live or confirmed available price. {link(quote["url"], "Report")}</div>'
    sources = [(e['olbg'], 'OLBG event'), (e['official'], 'Official schedule')] + [(s['url'], s['label']) for s in pick['sources']]
    seen = set(); links = []
    for url, name in sources:
        if url not in seen:
            links.append(link(url, name)); seen.add(url)
    copy = '' if compact else f'<p class="pick-copy">{h(pick["text"])}</p>'
    return f'''<article class="pick-card" {freshness(e, 'pick')}>
<div class="pick-top"><span class="pick-meta">{h(sport['name'])} / {h(pick['market'])}</span><span class="tag {h(level)}">{h(level.title())} confidence</span></div>
<h3>{h(pick['selection'])}</h3><p class="event-name">{h(e['title'])} · {when(e)}</p>{copy}
<div class="pick-details"><span>Current market price <strong>—</strong></span><span>Own numeric line <strong>—</strong></span><span>Odds band <strong>unconfirmed</strong></span></div>{quote_html}<div class="links">{' '.join(links)}</div></article>'''


def event_rows(events, prefix='', show_sport=False):
    result = []
    for e in sorted(events, key=lambda x: (x['display_until_utc'] or '9999', x['title'])):
        sport_col = f'<td>{h(SPORTS[e["sport"]]["name"])}</td>' if show_sport else ''
        result.append(f'''<tr {freshness(e, 'event')}>{sport_col}<td><strong>{h(e['title'])}</strong><small>{h(e['note'])}</small></td><td>{when(e)}</td><td>{h(e['markets'])}<small>Current prices: —</small></td><td>{link(e['olbg'], 'OLBG')}<br>{link(e['official'], 'Official schedule')}</td></tr>''')
    return ''.join(result)


def event_table(events, prefix='', show_sport=False):
    if not events:
        return '<p class="empty">No schedule-linked events are in this snapshot for this sport.</p>'
    sport_th = '<th scope="col">Sport</th>' if show_sport else ''
    return f'''<div class="table-wrap"><table><thead><tr>{sport_th}<th scope="col">Event</th><th scope="col">Official time / date</th><th scope="col">Observed markets</th><th scope="col">Sources</th></tr></thead><tbody>{event_rows(events,prefix,show_sport)}</tbody></table></div><p class="empty" data-empty-for="event">No unexpired schedule-linked rows are available on this page. The snapshot may have expired or every event may have reached its cutoff.</p>'''


def watch_table(items, show_sport=False):
    if not items:
        return '<p class="empty">No unconfirmed listings were retained for this sport. This does not establish that the OLBG inventory is empty.</p>'
    rows = []
    for w in sorted(items, key=lambda x: (x['sport'], x['title'])):
        sport_col = f'<td>{h(SPORTS[w["sport"]]["name"])}</td>' if show_sport else ''
        rows.append(f'''<tr>{sport_col}<td><strong>{h(w['title'])}</strong><small>{h(w['note'])}</small></td><td>—<small>Not established</small></td><td>{h(w['observed_at'])}</td><td>{link(w['olbg'], 'OLBG listing')}<br>{link(w['official'], 'Official body (not fixture proof)')}</td></tr>''')
    sport_th = '<th scope="col">Sport</th>' if show_sport else ''
    return f'''<div class="table-wrap"><table class="flag-table"><thead><tr>{sport_th}<th scope="col">Listing / review required</th><th scope="col">Date &amp; start</th><th scope="col">Captured</th><th scope="col">Sources</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>'''


def intro(eyebrow, title, text, prefix=''):
    return f'''<section class="page-intro"><div class="wrap"><div class="breadcrumbs"><a href="{prefix}index.html">Overview</a> / {h(title)}</div><div class="eyebrow">{h(eyebrow)}</div><h1>{h(title)}</h1><p>{h(text)}</p></div></section>'''


def index():
    confirmed = Counter(e['sport'] for e in DATA['events'])
    pred = Counter(EVENTS[p['event_id']]['sport'] for p in PICKS)
    sport_cards = []
    for s in DATA['sports']:
        sport_cards.append(f'''<a class="sport-card" href="sports/{h(s['slug'])}.html"><div class="sport-head"><span class="sport-code">{h(s['code'])}</span><span class="arrow" aria-hidden="true">↗</span></div><h3>{h(s['name'])}</h3><p><span class="coverage">{pred[s['slug']]} notes</span> · {confirmed[s['slug']]} schedule-linked events at snapshot</p></a>''')
    featured = [p for p in PICKS if p['confidence'] == 'medium'][:6]
    content = f'''<main id="main"><section class="hero"><div class="wrap hero-inner"><div><div class="eyebrow">Independent research · 15 sports</div><h1>Make sense of<br><em>the next game.</em></h1><p class="hero-copy">A source-linked look at OLBG listings, official schedules and the evidence behind each lean. Useful context, with the unknowns left in plain sight.</p><div class="hero-actions"><a class="button" href="#sports">Explore the sports <span aria-hidden="true">↘</span></a><a class="button secondary" href="flagged.html">See what needs review</a></div></div><aside class="hero-panel"><div class="panel-label">Priced high-confidence selections</div><div class="panel-number">0</div><p>No current bookmaker quote could be established, so no selection qualifies for the requested −250 to +10000 price band.</p><hr><div class="mini-line"><span>Snapshot began</span><strong>27 Oct · 05:23 UTC</strong></div><div class="mini-line"><span>Updates</span><strong>Manual only</strong></div><div class="mini-line"><span>Confidence</span><strong>Subjective, not a probability</strong></div></aside></div></section>
<div class="wrap main"><div class="stats"><div class="stat"><strong>15</strong><span>Sports covered</span><small>Category pages</small></div><div class="stat"><strong>{len(DATA['events'])}</strong><span>Schedule-linked events</span><small>At snapshot, not a complete inventory</small></div><div class="stat"><strong>{len(PICKS)}</strong><span>Written research notes</span><small>At snapshot, before expiry</small></div><div class="stat"><strong>0</strong><span>Current market prices</span><small>Unconfirmed values left blank</small></div></div>
<section class="section"><div class="section-heading"><div><div class="eyebrow">The brief</div><h2>What to know before the picks</h2><p>These are editorial leans, not priced recommendations. Official schedules can change; team news and the full OLBG inventory are not complete.</p></div><a class="inline-link" href="methodology.html">Read the methodology →</a></div><div class="notice"><strong>Research snapshot, not a live feed.</strong> Unexpired notes are hidden at the earlier of their event cutoff and {utc(META['snapshot_expires'])}, using your device clock. Prices, independent numeric lines, injuries and lineup changes remain unconfirmed unless explicitly sourced. <a href="flagged.html">See all flags.</a></div></section>
<section class="section"><div class="section-heading"><div><div class="eyebrow">Research highlights</div><h2>Most supported leans</h2><p>The strongest published qualitative notes are medium confidence. None has a confirmed current price or a demonstrated betting edge.</p></div><a class="inline-link" href="#sports">View sport pages →</a></div><div class="picks-grid">{''.join(pick_card(p, compact=True) for p in featured)}</div><p class="empty" data-empty-for="pick">No unexpired highlights. Revisit the linked source pages; this snapshot does not update itself.</p></section>
<section class="section" id="sports"><div class="section-heading"><div><div class="eyebrow">Browse by sport</div><h2>All 15 categories</h2><p>Snapshot counts below are historical totals, not a claim that every note or event is still upcoming.</p></div><a class="inline-link" href="all-events.html">Open the event inventory →</a></div><div class="sport-grid">{''.join(sport_cards)}</div></section>
<section class="section"><div class="notice info"><strong>Where the gaps are.</strong> Snooker and greyhound hubs returned “No tips found”; that does not mean there are no events. Some listings were not individually corroborated, and no valid numeric price has been originated for this snapshot. <a href="flagged.html">Open the review register →</a></div></section></div></main>'''
    return page('Overview', content, active='overview')


def sport_page(s):
    slug = s['slug']; ev = [e for e in DATA['events'] if e['sport'] == slug]
    picks = [p for p in PICKS if EVENTS[p['event_id']]['sport'] == slug]
    watch = [w for w in DATA['watchlist'] if w['sport'] == slug]
    shortfall = max(0, 5-len(picks))
    target = f"{len(picks)} of the daily target of 5 distinct-event notes in the snapshot; shortfall {shortfall}." if shortfall else f"{len(picks)} distinct-event notes in the snapshot meet the target of 5, before any cutoffs."
    extras = ''.join(' · '+link(x['url'],x['label']) for x in s.get('extra_hubs', []))
    cards = ''.join(pick_card(p, '../') for p in picks)
    pick_part = f'<div class="picks-grid">{cards}</div><p class="empty" data-empty-for="pick">No unexpired notes are currently available. This may reflect an event cutoff or the expiry of the whole snapshot.</p>' if picks else '<p class="empty">No predictions were published for this sport in the snapshot. Do not infer an empty fixture calendar.</p>'
    content = f'''<main id="main">{intro('Sport / '+s['code'],s['name'],s['note'],'../')}<div class="wrap page-main"><div class="notice info"><strong>Snapshot coverage:</strong> {h(target)} Counts are not a live total. All notes are unpriced, and a selection can disappear at its cutoff. {link(s['hub'], 'OLBG sport hub')}{extras} · {link(s['official'], 'Official sport source')}</div>
<section class="section"><div class="section-heading"><div><div class="eyebrow">Our perspective</div><h2>Written predictions</h2><p>Qualitative confidence describes the strength of the editorial case, not an estimated probability or verified edge.</p></div><span class="tag warn">Market prices unconfirmed</span></div>{pick_part}</section>
<section class="section"><div class="section-heading"><div><div class="eyebrow">Source-linked schedule</div><h2>Events in this snapshot</h2><p>Official schedule references corroborate the event; they do not establish current odds or final lineups. All displayed times are UTC.</p></div></div>{event_table(ev, '../')}</section>
<section class="section"><div class="section-heading"><div><div class="eyebrow">Needs more checking</div><h2>Unconfirmed listings</h2><p>These are not asserted to be upcoming. Start, official fixture and market fields are deliberately blank; older captures are labelled.</p></div><a class="inline-link" href="../flagged.html">All review flags →</a></div>{watch_table(watch)}</section></div></main>'''
    return page(s['name'], content, prefix='../')


def all_events():
    content=f'''<main id="main">{intro('Inventory','Event inventory','A partial manual snapshot, split between official schedule-linked events and listings that still need review. It is not a live or complete OLBG inventory.')}<div class="wrap page-main"><div class="notice"><strong>Time safety:</strong> scheduled rows disappear at their cutoff or the snapshot expiry. An exact time is shown only when sourced; an earlier conservative cutoff is not a start time. Markets describe what was observed, not current prices.</div><section class="section"><div class="section-heading"><div><div class="eyebrow">Schedule corroborated</div><h2>Events with official references</h2><p>Event-specific official schedule links are provided for each row. These are not assertions that odds or lineups have been checked.</p></div></div>{event_table(DATA['events'],show_sport=True)}</section><section class="section"><div class="section-heading"><div><div class="eyebrow">Do not treat as upcoming</div><h2>Listings awaiting checks</h2><p>Some are older captures. Each generic official-body link is a starting point, not proof of the listed fixture.</p></div></div>{watch_table(DATA['watchlist'],show_sport=True)}</section></div></main>'''
    return page('Event inventory',content,active='events')


def flags():
    pred = Counter(EVENTS[p['event_id']]['sport'] for p in PICKS)
    rows=[]
    for s in DATA['sports']:
        count=pred[s['slug']]
        rows.append(f'''<tr><td><strong>{h(s['name'])}</strong></td><td>{count}</td><td>{max(0,5-count)}</td><td>{h(s['note'])}</td><td>{link(s['hub'], 'OLBG hub')}<br>{link(s['official'], 'Official sport source')}</td></tr>''')
    timed=[e for e in DATA['events'] if not e['start_utc']]
    timing_rows=''.join(f'<tr><td><strong>{h(e["title"])}</strong></td><td>—</td><td>{h(e["note"])}</td><td>{link(e["olbg"],"OLBG")}<br>{link(e["official"],"Official schedule")}</td></tr>' for e in timed)
    content=f'''<main id="main">{intro('Transparency','Flagged for review','Uncertainty is kept visible rather than filled with estimates. Flags do not mean that an event or prediction has been proved false.')}<div class="wrap page-main"><section><div class="notice"><strong>All {len(DATA['events'])} schedule-linked events:</strong> current bookmaker prices, selection eligibility for the requested odds band, a reliable independent numeric line and final injury/lineup information have not been established. Where relevant, draw or settlement rules also need checking. Go to <a href="all-events.html">the event table</a> for an official and OLBG link on each row.</div></section>
<section class="section"><div class="section-heading"><div><div class="eyebrow">System-wide flags</div><h2>What is missing</h2></div></div><div class="prose"><ul><li><strong>Automatic refresh:</strong> the declared GitHub Actions probe was denied by OLBG's robots rules on the three tested paths. It did not retrieve listings; there is no ingest pipeline and no scheduled content refresh. <a href="https://www.olbg.com/robots.txt">OLBG robots.txt ↗</a></li><li><strong>Price band:</strong> no current sourced quote was obtained. A single historical opening quote in golf is labelled separately and is not actionable evidence.</li><li><strong>Estimates:</strong> older tip-share-derived lines and arbitrary prior/override values are not calibrated or corroborated. They are quarantined in historical boards, not used here.</li><li><strong>Timings:</strong> OLBG labels did not establish a timezone. Official times were used where available; sequential tennis and tournament starts are left blank and conservatively hidden.</li><li><strong>Partial inventory:</strong> OLBG hubs are not proof of all markets or all events. Some old captures were not checked again, and team availability may change.</li></ul></div></section>
<section class="section"><div class="section-heading"><div><div class="eyebrow">Coverage gaps</div><h2>Five-per-sport target</h2><p>Counts and shortfalls refer to the original snapshot, not the number still unexpired.</p></div></div><div class="table-wrap"><table><thead><tr><th scope="col">Sport</th><th scope="col">Notes</th><th scope="col">Shortfall</th><th scope="col">Open issue</th><th scope="col">Sources</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<section class="section"><div class="section-heading"><div><div class="eyebrow">Date confirmed, time unknown</div><h2>Conservative cutoffs</h2><p>These are not start times. Every row links the official schedule used.</p></div></div><div class="table-wrap"><table><thead><tr><th scope="col">Event</th><th scope="col">Exact start</th><th scope="col">Reason</th><th scope="col">Sources</th></tr></thead><tbody>{timing_rows}</tbody></table></div></section>
<section class="section"><div class="section-heading"><div><div class="eyebrow">Individual rows</div><h2>Unconfirmed listings</h2><p>For each, date and event status remain blank pending an event-specific official source.</p></div></div>{watch_table(DATA['watchlist'],show_sport=True)}</section></div></main>'''
    return page('Flagged for review',content,active='flags')


def methodology():
    content=f'''<main id="main">{intro('Methodology','How to read this desk','A cautious, reproducible publishing method for a manually researched and time-limited snapshot.')}<div class="wrap page-main prose"><h2>What was checked</h2><p>OLBG sport hubs and selected event pages were manually inspected beginning {utc(META['snapshot_at'])}. Event-specific official competition sources corroborate the schedules shown in the main event table. A source link supports a stated fact; it does not certify future lineups, withdrawals, event status or bookmaker terms.</p><p>The watchlist is deliberately separate. Its generic official-body links are research starting points, not evidence that a particular listing exists. Some retained entries are older captures from 26 October; others were reported in a concurrent 27 October capture and have not been individually rechecked here. Neither set is asserted to remain available.</p><h2>Our predictions and confidence</h2><p>Each note is an independent editorial direction using the cited form and schedule information. <strong>Medium</strong> means the cited case looks stronger relative to the other notes in this snapshot; <strong>low</strong> indicates a tentative preference or a wide field. These labels are subjective, are not calibrated win probabilities, and should not be read as evidence of value. No high-confidence priced picks were established.</p><h2>Prices and the requested range</h2><p>A current quoted American bookmaker price between −250 and +10000 is a market-price criterion, not a win-probability or confidence criterion. No current executable quote was established in this snapshot. We therefore leave both the current market price and our numeric line blank. A single 26 October FanDuel opening price cited by the PGA Tour is clearly labelled as historical, not a current offer. We make no claim of an edge.</p><p>Earlier boards converted tip shares using arbitrary priors and overrides. Tip counts are not independent outcomes or calibrated probabilities; those historic figures are not used in this desk. <a href="archive.html">Read the archive warning.</a></p><h2>Time and expiry</h2><p>Official times were converted to UTC when a timezone was clear. Where a match follows earlier contests or only a date is available, the exact start is blank. A conservative earlier cutoff is used solely to stop displaying the note. The browser also hides all scheduled rows and notes at {utc(META['snapshot_expires'])}. It uses the device clock; if JavaScript is disabled or the clock is earlier than the snapshot, the pages fail closed.</p><h2>Updates and access</h2><p>There is no automatic ingestion or content refresh. A GitHub-hosted probe checked <a href="https://www.olbg.com/robots.txt">OLBG's robots.txt</a> with the declared CoverageDeskResearch agent and was denied for the three tested paths. It did not bypass the denial. A future maintainer needs an authorized, rate-limited source and must record retrieval times and failures before replacing this snapshot.</p><h2>Rebuild and checks</h2><p>The canonical research is <code>data/current.json</code>. Run <code>python3 tools/build_current.py</code> to render and <code>python3 tools/check_current.py</code> plus <code>node --test tests/freshness.test.js</code> to test. The checks prove structure, expiry behavior, internal links and source presence, not that external facts are automatically true or that quotes remain available.</p></div></main>'''
    return page('Methodology',content,active='method')


def sources():
    sections=[]
    for s in DATA['sports']:
        refs={(s['hub'],'OLBG hub'),(s['official'],'Official sport source')}
        refs.update((x['url'],x['label']) for x in s.get('extra_hubs',[]))
        for e in DATA['events']:
            if e['sport']==s['slug']:
                refs.add((e['olbg'],'OLBG event'));refs.add((e['official'],'Official event schedule'))
        for w in DATA['watchlist']:
            if w['sport']==s['slug']:
                refs.add((w['olbg'],'OLBG watchlist listing'));refs.add((w['official'],'Official body (not fixture proof)'))
        for p in PICKS:
            if EVENTS[p['event_id']]['sport']==s['slug']:
                refs.update((a['url'],a['label']) for a in p['sources'])
        lis=''.join(f'<li>{link(url,label)}<br><small>{h(url)}</small></li>' for url,label in sorted(refs,key=lambda x:(x[1],x[0])))
        sections.append(f'<section class="section"><h2>{h(s["name"])}</h2><ul class="source-list">{lis}</ul></section>')
    content=f'''<main id="main">{intro('Evidence','Source register','Sources used or starting points for each sport. They may change after capture; generic official home pages are not fixture confirmation.')}<div class="wrap page-main prose">{''.join(sections)}</div></main>'''
    return page('Sources',content)


def archive():
    content=f'''<main id="main">{intro('Archive','Historical boards','Preserved for audit only. They are not current, and their lines and confidence labels should not be relied on.')}<div class="wrap page-main prose"><div class="notice"><strong>Read before opening:</strong> Earlier boards contain dated fixtures, unsupported prices, arbitrary priors and claims that have not been rechecked. They are not comparable to this desk and are not a source of current picks.</div><ul class="source-list"><li><a href="legacy-cal4/index.html">27 October CAL-4 dashboard (session 3b1b6ed4)</a> — 114 reported events, 57 notes and historical derived prices; preserved for comparison, not rechecked here.</li><li><a href="board/all-markets.html">27 October board (session 81a54336)</a> — earlier capture and derived lines.</li><li><a href="docs/index.html">Earlier 15-sport board</a> — dated historical material.</li><li><a href="docs/board-review/index.html">Board review</a> — 26 October 2026 snapshot.</li><li><a href="olbg-tips/index.html">Tip-consensus board</a> — 26 October 2026 snapshot.</li></ul><p>Direct links into each historic board carry the same warning. The source data and earlier generators remain in the repository for audit.</p></div></main>'''
    return page('Historical boards',content)


def mapping():
    content=f'''<main id="main">{intro('Guide','OLBG structure','Entry points used during manual research. A sport hub is not a complete market or fixture feed.')}<div class="wrap page-main prose"><p>The supported sport hubs are linked from the <a href="sources.html">source register</a>. Gaelic Sports uses separate football and hurling hubs. Event pages and their observed markets are linked in the <a href="all-events.html">event inventory</a>.</p><p>Automatic access for the declared probe was denied by robots rules on the paths tested. No endpoint, bot identity, or access restriction was changed to evade that result.</p></div></main>'''
    return page('OLBG structure',content)


def build():
    files={'index.html':index(),'all-events.html':all_events(),'flagged.html':flags(),'methodology.html':methodology(),'sources.html':sources(),'archive.html':archive(),'olbg-map.html':mapping()}
    files.update({f'sports/{slug}.html':sport_page(s) for slug,s in SPORTS.items()})
    return files


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    errors=[]
    for path,content in build().items():
        file=ROOT/path
        if args.check:
            if not file.exists() or file.read_text(encoding='utf-8')!=content:errors.append(path)
        else:
            file.parent.mkdir(parents=True,exist_ok=True);file.write_text(content,encoding='utf-8')
    if errors:
        raise SystemExit('Generated files differ: '+', '.join(errors))
    print(('Checked' if args.check else 'Generated')+f' {len(build())} snapshot pages')

if __name__=='__main__':main()

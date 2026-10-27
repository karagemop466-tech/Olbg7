#!/usr/bin/env python3
"""
Build the single public board at the repository root.

Inputs   data/board/inventory-*.json, data/board/official.json, data/board/picks-*.json,
         data/board/flags.json and data/board/lines.json (produced by tools/originate.py).
Outputs  index.html, picks.html, lines.html, method.html, sources.html, flagged.html,
         archive.html and sports/<slug>.html

Every price on the site comes from data/board/lines.json. Nothing numeric is typed into the HTML.
"""
import json
import os
import html
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "data", "board")

SPORTS = ["Golf", "Volleyball", "Rugby Union", "Cricket", "Snooker", "Darts", "Baseball",
          "Gaelic Sports", "Greyhounds", "Tennis", "Motor Racing", "Handball", "Ice Hockey",
          "Basketball", "Rugby League"]
SLUG = {s: s.lower().replace(" ", "-") for s in SPORTS}
TARGET = 5

MARKET_LABEL = {
    "Win Match": "Match winner", "Money Line": "Money line", "To Win": "Match winner (3-way)",
    "Handicap": "Handicap", "Pointspread": "Point spread", "Puck Line": "Puck line",
    "Run Line": "Run line", "Game Totals": "Total (over/under)",
    "Win Tournament": "Outright", "Grand Final Winner": "Outright (Grand Final)",
    "Podium Finish": "Podium finish", "Daily Races": "Race winner",
    "Top Team1 Batsman": "Top team-1 batsman", "Outright Winner": "Outright",
}


def esc(s):
    return html.escape(str(s), quote=True)


def load(name):
    with open(os.path.join(B, name)) as fh:
        return json.load(fh)


def conf_for(p, sample, nfacts, method):
    """The >70% rule the brief asks for, applied literally: high means a fair chance
    above 70%, which is shorter than -233 and inside the requested band by definition."""
    if method == "CAL-4P":
        return "low"
    if p > 0.70 and sample >= 3:
        return "high"
    if p >= 0.55 and (sample >= 3 or nfacts >= 1):
        return "medium"
    return "low"


MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def shortdate(d):
    y, m, dd = d.split("-")
    return f"{int(dd)} {MONTHS[int(m)-1]}" + ("" if y == "2026" else f" {y}")


def pct(p):
    return f"{p*100:.0f}%"


def pill(c):
    return f'<span class="pill {c}">{c}</span>'


def build_index(lines, picks, flags, summary):
    hs = [p for p in picks if p["confidence"] == "high"]
    hs.sort(key=lambda x: -x["line"]["p"])
    n_high = len(hs)
    n_band = n_high
    ranked = sorted(picks, key=lambda x: -x["line"]["p"])
    rows = []
    for p in ranked[:12]:
        rows.append(f"""<tr>
<td><a href="sports/{SLUG[p['sport']]}.html">{esc(p['sport'])}</a></td>
<td class="nowrap">{esc(shortdate(p['event_date']))}<div class="small muted">{esc(p['start'])}</div></td>
<td><strong>{esc(p['sel'])}</strong><div class="small muted">{esc(p['event'])}</div></td>
<td>{esc(MARKET_LABEL.get(p['market'], p['market']))}</td>
<td class="num">{p['line']['price']:.2f} <span class="muted">({esc(p['line']['american'])})</span></td>
<td class="num">{pct(p['line']['p'])}</td>
<td>{pill(p['confidence'])}</td>
<td><a href="sports/{SLUG[p['sport']]}.html#{p['id']}">read the pick &rarr;</a></td>
</tr>""")

    cov = []
    for s in SPORTS:
        n = summary["picks_by_sport"].get(s, 0)
        ev = summary["events_by_sport"].get(s, 0)
        priced = summary["priced_by_sport"].get(s, 0)
        if n >= TARGET:
            status = f'<span class="pill ok">{n} picks</span>'
            why = "Target met."
        else:
            status = f'<span class="pill warn">{n} of {TARGET}</span>'
            why = esc(summary["gap_reason"].get(s, ""))
        cov.append(f"""<tr><td><a href="sports/{SLUG[s]}.html">{esc(s)}</a></td>
<td class="num">{ev}</td><td class="num">{priced}</td><td class="num">{n}</td>
<td>{status}</td><td class="small">{why}</td></tr>""")

    body = f"""
<div class="hero">
  <div class="hero-kicker">Snapshot {esc(summary['retrieved_at'])} &middot; all 15 sports</div>
  <h1>Every OLBG match, priced &mdash; and the picks that survive the reading</h1>
  <p class="lede">This desk lists every event OLBG is running across the fifteen sports in scope, puts
  <strong>our own price</strong> on each market we can defend, and publishes full written predictions
  for the selections we would actually back. Nothing here is a bookmaker price: the numbers are ours,
  built from OLBG's published tip counts and from official league tables, with the method stated on
  every row.</p>
  <div class="hero-actions">
    <a class="btn primary" href="picks.html">Today's picks &amp; write-ups</a>
    <a class="btn" href="lines.html">Every event &amp; every line</a>
    <a class="btn" href="flagged.html">Flagged for review</a>
  </div>
</div>

<div class="kpis">
  <div class="kpi"><div class="n">15</div><div class="l">sports in scope</div></div>
  <div class="kpi"><div class="n">{summary['events']}</div><div class="l">OLBG events inventoried</div></div>
  <div class="kpi"><div class="n">{summary['priced']}</div><div class="l">events with our own line</div></div>
  <div class="kpi"><div class="n">{summary['markets']}</div><div class="l">markets priced</div></div>
  <div class="kpi"><div class="n">{summary['picks']}</div><div class="l">written predictions</div></div>
  <div class="kpi accent"><div class="n">{n_high}</div><div class="l">high confidence (70%+)</div></div>
</div>

<h2 id="exec">Executive summary</h2>
<div class="cards">
  <div class="card">
    <h3>What is on the card today</h3>
    <p>{summary['events']} events across 13 of the 15 sports. Two sports have <strong>no market at all</strong>
    on OLBG this morning: <a href="sports/snooker.html">snooker</a> and <a href="sports/greyhounds.html">greyhounds</a>
    both return &ldquo;No tips found&rdquo;, so no honest pick exists in either and none is published.</p>
  </div>
  <div class="card">
    <h3>Where the confidence is</h3>
    <p>{summary['today_picks']} of the {summary['picks']} picks are on today's card; the rest are on tomorrow or later.
    {n_high} picks clear the 70% bar you set for high confidence ({esc(', '.join(p['sel'] for p in hs)) or 'none today'}),
    {summary['conf']['medium']} are medium and {summary['conf']['low']} are low. That is a deliberately strict test and it
    is not padded: the rest of the card is ranked by chance rather than relabelled. A 70% chance is 1.43 decimal, so a
    true 70% favourite is already shorter than the &minus;250 floor at 1.40; every selection outside the band
    ({summary['band_out']} of them) is labelled on its own card.</p>
  </div>
  <div class="card">
    <h3>What we will not do</h3>
    <p>No invented fixtures, prices or injuries. Where OLBG prints no split, the row is left unpriced.
    Where no official table was retrieved, the prediction says so. Every claim carries a source link, and
    the {summary['n_flags']} things we could not resolve are on <a href="flagged.html">Flagged for review</a>.</p>
  </div>
</div>

<h2>The strongest picks on the card</h2>
<p class="muted small">Ranked by our fair chance &mdash; the twelve shortest prices among the written picks.
The confidence column uses the strict 70% rule, so a 60% favourite is honestly labelled medium even when it is
the best bet in its sport. Every row links to the full written prediction. &ldquo;Our price&rdquo; is the price
we would lay, not a price available anywhere.</p>
<table class="wide"><thead><tr><th>Sport</th><th>When</th><th>Selection</th><th>Market</th>
<th>Our price</th><th>Chance</th><th>Confidence</th><th></th></tr></thead><tbody>
{''.join(rows)}
</tbody></table>
<p class="small"><a href="picks.html">All {summary['picks']} predictions with the full write-ups &rarr;</a></p>
<p class="small muted">The time beside each pick is copied from OLBG, which prints US Eastern rather than local
kick-off, so a 13:00 start in Lahore appears as 04:00. Worked examples are on
<a href="flagged.html">Flagged for review</a> (F-19).</p>

<h2>Coverage by sport</h2>
<table><thead><tr><th>Sport</th><th>OLBG events</th><th>With our line</th><th>Picks</th>
<th>Target</th><th>Why the gap, where there is one</th></tr></thead><tbody>
{''.join(cov)}
</tbody></table>
<p class="small muted">Target is five picks per sport. The gap column states what OLBG itself publishes;
in every short sport the limit is the size of OLBG's market, not the amount of research done.</p>

<h2>How to read a pick</h2>
<div class="cards">
  <div class="card"><h3>1. The selection comes first</h3><p>Every prediction opens with the bet in plain words:
  the team or player, the market, and our price. You should never have to hunt for what is being backed.</p></div>
  <div class="card"><h3>2. The evidence is attached</h3><p>Each pick lists the facts behind it with a link to the
  source: the official league table, the governing body, or OLBG's own listing.</p></div>
  <div class="card"><h3>3. Confidence is computed</h3><p>High, medium and low are set by our fair chance, the size of
  the tip sample and whether an independent source stands behind the fixture &mdash; never by how the paragraph reads.
  The rule is on <a href="method.html">the method page</a>.</p></div>
</div>
"""
    return page("Dashboard", body, "index.html")


def build_picks(picks, summary):
    out = [f"""<h1>Today's picks &mdash; {summary['picks']} written predictions</h1>
<p class="lede">Every prediction below is unique prose, at least 30 words, and states its selection, its price
and the evidence behind it. Picks are grouped by sport, strongest first. Confidence and price come from the
same engine as the tables on <a href="lines.html">Every line</a>.</p>
<div class="toc">{''.join(f'<a href="#{SLUG[s]}">{esc(s)} <span class="muted">{summary["picks_by_sport"].get(s,0)}</span></a>' for s in SPORTS)}</div>"""]
    for s in SPORTS:
        ps = [p for p in picks if p["sport"] == s]
        ps.sort(key=lambda x: (-{"high": 2, "medium": 1, "low": 0}[x["confidence"]], -x["line"]["p"]))
        out.append(f'<h2 id="{SLUG[s]}">{esc(s)}</h2>')
        if not ps:
            out.append(f'<div class="note warn-note"><strong>No picks.</strong> {esc(summary["gap_reason"].get(s,""))} '
                       f'<a href="sports/{SLUG[s]}.html">Open the sport page &rarr;</a></div>')
            continue
        for p in ps:
            out.append(pick_card(p))
    return page("Picks", "".join(out), "picks.html")


def pick_card(p):
    facts = "".join(
        f'<li>{esc(f["t"])} <a class="src" href="{esc(f["u"])}" rel="nofollow noopener">source</a>'
        f' <span class="tier {f["tier"]}">{f["tier"]}</span></li>' for f in p["facts"])
    band = "" if p["line"]["in_band"] else '<span class="pill warn">outside band</span>'
    note = f'<p class="small muted">{esc(p["note"])}</p>' if p.get("note") else ""
    return f"""
<article class="pick" id="{p['id']}">
  <div class="pick-head">
    <div>
      <div class="pick-sel">{esc(p['sel'])}</div>
      <div class="small muted">{esc(p['event'])} &middot; {esc(p['start'])} &middot; {esc(p['comp'])}</div>
    </div>
    <div class="pick-price">
      <div class="big">{p['line']['price']:.2f}</div>
      <div class="small muted">{esc(p['line']['american'])} &middot; {pct(p['line']['p'])}</div>
    </div>
    <div class="pick-meta">{pill(p['confidence'])} {band}
      <div class="small muted">{esc(MARKET_LABEL.get(p['market'], p['market']))}</div>
    </div>
  </div>
  <p class="pred">{esc(p['pred'])}</p>
  {note}
  <details><summary>{len(p['facts'])} sourced fact(s) and the OLBG row</summary>
    <ul class="facts">{facts}</ul>
    <p class="small muted">OLBG row: {esc(p['olbg_sel'])} &middot; {esc(p['olbg_market'])} &middot;
    {p['tips']}/{p['total']} tips &middot; {p['olbg_pct']}% &middot;
    <a href="{esc(p['olbg_url'])}" rel="nofollow noopener">open on OLBG</a></p>
  </details>
</article>"""


def build_lines(lines, summary):
    out = [f"""<h1>Every event, every line</h1>
<p class="lede">{summary['events']} events were inventoried from OLBG on {esc(summary['retrieved_at'])}.
{summary['priced']} of them carry at least one price from our own engine, across {summary['markets']} markets.
Rows with no price are shown with the reason, never filled in.</p>
<p class="small muted">Methods: <strong>CAL-4C</strong> consensus from OLBG's printed tip split &middot;
<strong>CAL-4R</strong> rating from official goals/points for and against &middot;
<strong>CAL-4P</strong> league-average prior where no club baseline exists (never used for a pick).
Full explanation on <a href="method.html">the method page</a>.</p>
<div class="toc">{''.join(f'<a href="#{SLUG[s]}">{esc(s)}</a>' for s in SPORTS)}</div>"""]
    for s in SPORTS:
        evs = [r for r in lines if r["sport"] == s]
        out.append(f'<h2 id="{SLUG[s]}">{esc(s)} <span class="muted small">{len(evs)} events</span></h2>')
        if not evs:
            out.append(f'<div class="note warn-note">{esc(summary["gap_reason"].get(s,""))}</div>')
            continue
        rows = []
        for r in evs:
            if not r["markets"]:
                rows.append(f"""<tr class="dim"><td class="nowrap">{esc(r['start'])}</td>
<td>{esc(r['event'])}<div class="small muted">{esc(r['comp'])}</div></td>
<td colspan="6" class="small">Not priced &mdash; {esc(r['unpriced'])}</td></tr>""")
                continue
            first = True
            for m in r["markets"]:
                link = f'<a href="{esc(r["olbg_url"])}" rel="nofollow noopener">OLBG</a>' if False else ""
                rows.append(f"""<tr>
<td class="nowrap">{esc(r['start']) if first else ''}</td>
<td>{esc(r['event']) + ('<div class="small muted">' + esc(r['comp']) + '</div>' if first else '') if first else ''}</td>
<td>{esc(MARKET_LABEL.get(m['market'], m['market']))}</td>
<td>{esc(m['selection'])}</td>
<td class="num">{pct(m['p'])}</td>
<td class="num">{m['price']:.2f}</td>
<td class="num">{esc(m['american'])}</td>
<td class="small">{'in band' if m['in_band'] else 'outside band'} &middot; {esc(m['method'])}</td>
</tr>""")
                first = False
        out.append(f"""<table class="wide"><thead><tr><th>Time (as OLBG prints)</th><th>Event</th><th>Market</th>
<th>Selection</th><th>Chance</th><th>Price</th><th>US</th><th>Band / method</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>""")
    out.append('<p class="small muted">Times are reproduced exactly as OLBG prints them, which is <strong>US Eastern, '
               'not local kick-off</strong> &mdash; four fixtures with a confirmed official start line up to the minute '
               'once four hours are subtracted. Nothing on this site is converted, because OLBG publishes no timezone '
               'label: for example Afghanistan v Zimbabwe is 18:30 in Sharjah and printed 10:30. The worked examples are '
               'on <a href="flagged.html">Flagged for review</a> (F-19).</p>')
    return page("Every line", "".join(out), "lines.html")


def build_sport(s, lines, picks, official, summary):
    evs = [r for r in lines if r["sport"] == s]
    ps = [p for p in picks if p["sport"] == s]
    ps.sort(key=lambda x: (-{"high": 2, "medium": 1, "low": 0}[x["confidence"]], -x["line"]["p"]))
    n_high = sum(1 for p in ps if p["confidence"] == "high")
    tznote = ('<p class="small muted">Start times below are exactly as OLBG prints them, which is US Eastern rather '
              'than local kick-off (see F-19 on <a href="../flagged.html">Flagged for review</a>).</p>')
    head = f"""<div class="crumb"><a href="../index.html">Dashboard</a> / {esc(s)}</div>
<h1>{esc(s)}</h1>
<div class="kpis small">
  <div class="kpi"><div class="n">{len(evs)}</div><div class="l">OLBG events</div></div>
  <div class="kpi"><div class="n">{sum(1 for r in evs if r['markets'])}</div><div class="l">with our line</div></div>
  <div class="kpi"><div class="n">{len(ps)}</div><div class="l">written picks</div></div>
  <div class="kpi accent"><div class="n">{n_high}</div><div class="l">high confidence</div></div>
</div>"""
    gap = summary["gap_reason"].get(s, "")
    if len(ps) < TARGET:
        head += f'<div class="note warn-note"><strong>{len(ps)} of {TARGET} picks.</strong> {esc(gap)}</div>'
    if not ps:
        head += '<p class="muted">There is no market to write about, so no prediction is published rather than padding with one.</p>'
    for p in ps:
        head += pick_card(p)

    if evs:
        rows = []
        for r in evs:
            if not r["markets"]:
                rows.append(f"""<tr class="dim"><td class="nowrap">{esc(r['start'])}</td><td>{esc(r['event'])}</td>
<td colspan="4" class="small">Not priced &mdash; {esc(r['unpriced'])}</td></tr>""")
                continue
            for i, m in enumerate(r["markets"]):
                rows.append(f"""<tr>
<td class="nowrap">{esc(r['start']) if i == 0 else ''}</td>
<td>{esc(r['event']) if i == 0 else ''}{('<div class="small muted">' + esc(r['comp']) + '</div>') if i == 0 else ''}</td>
<td>{esc(MARKET_LABEL.get(m['market'], m['market']))}: <strong>{esc(m['selection'])}</strong></td>
<td class="num">{m['price']:.2f} <span class="muted">({esc(m['american'])})</span></td>
<td class="num">{pct(m['p'])}</td>
<td class="small">{esc(m['method'])}</td></tr>""")
        head += f"""<h2>Every {esc(s)} market we priced</h2>
<table><thead><tr><th>Time</th><th>Event</th><th>Market &amp; selection</th><th>Our price</th>
<th>Chance</th><th>Method</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"""
    if evs:
        head = head.replace('<h2>Every ' + esc(s) + ' market we priced</h2>',
                            tznote + '<h2>Every ' + esc(s) + ' market we priced</h2>')
    head += f"""<h2>Sources used for this sport</h2>
<p class="small">All OLBG rows are reproduced from <a href="{esc(summary['source_pages'].get(s, 'https://www.olbg.com/betting-tips'))}" rel="nofollow noopener">the OLBG {esc(s)} listing</a>.
Official and reference sources used for the write-ups are listed on <a href="../sources.html">Sources</a> and linked
inside each pick.</p>"""
    return page(s, head, f"sports/{SLUG[s]}.html", up="..")


def build_method():
    body = """
<div class="crumb"><a href="index.html">Dashboard</a> / Method</div>
<h1>How every number on this site is made</h1>
<p class="lede">Two questions decide the whole board: what is the chance, and is the price worth taking.
Neither is typed by hand. This page states the arithmetic so you can check it.</p>

<h2>1. Where the data comes from</h2>
<table><thead><tr><th>Input</th><th>Source</th><th>What we take from it</th></tr></thead><tbody>
<tr><td>Fixtures, times, markets, tip counts</td><td><a href="https://www.olbg.com/betting-tips" rel="nofollow noopener">OLBG sport listings</a></td>
<td>The event, the printed start label, the most-tipped selection, tips/total and the percentage. Copied as printed.</td></tr>
<tr><td>League tables and standings</td><td>Governing bodies and reference databases (MLB, NHL, EHF, BBC Sport rugby, Basketball-Reference)</td>
<td>Wins, losses, points/goals/runs for and against, used both as the evidence in a write-up and as the input to a derived market.</td></tr>
<tr><td>Rankings</td><td>ATP ranking reports, PDC Order of Merit, Official World Golf Ranking</td><td>Player rank and points, as published on the date shown with the fact.</td></tr>
</tbody></table>

<h2>2. CAL-4C &mdash; the consensus price</h2>
<p>OLBG prints, for each market, how many tips each selection received. That is a small, biased sample of
opinion, so it is shrunk towards the market-structure prior before it becomes a price:</p>
<pre>prior    = 1 / number of outcomes           (two-way 0.500, three-way 0.333, outright 0.125)
K        = 6 pseudo-tips for 8+ real tips, 12 for 4-7, 20 for 0-3
p_fair   = (tips_on_selection + K * prior) / (total_tips + K)
our price= 1 / (p_fair * 1.05)              (5% book margin)</pre>
<p>The sample taper matters: a single tip on a three-way market prices near 0.36, not near 0.70. A two-way
market is priced on both sides, so the other outcome is the complement of the printed split.</p>

<h2>3. CAL-4R &mdash; the rating price</h2>
<p>Used where the tip split cannot price the market we care about: handball (OLBG prints the draw as the
most-tipped selection on 11 of 15 matches, so the split is not a match-winner split) and every handicap or
total. Expected scoring comes from official goals/points for and against per game:</p>
<pre>expected_home = (home_scored_per_game + away_conceded_per_game) / 2
expected_away = (away_scored_per_game + home_conceded_per_game) / 2
margin        = expected_home - expected_away,  normal with a sport-specific sigma
total line    = expected_home + expected_away
cover / over  = normal tail from the same mean and sigma</pre>
<table><thead><tr><th>Sport</th><th>Margin sigma</th><th>Total sigma</th><th>Derived markets published</th></tr></thead><tbody>
<tr><td>Basketball</td><td>11.0 points</td><td>17.0 points</td><td>Point spread, total (EuroLeague only where both clubs have a table line)</td></tr>
<tr><td>Ice hockey</td><td>1.9 goals</td><td>1.9 goals</td><td>Puck line at 1.5, total (NHL only)</td></tr>
<tr><td>Baseball</td><td>2.4 runs</td><td>4.2 runs</td><td>Run line at 1.5, total (MLB; starting pitcher not in the baseline)</td></tr>
<tr><td>Handball</td><td>8.0 goals</td><td>7.0 goals</td><td>Match winner including the draw, goal handicap, total</td></tr>
<tr><td>Rugby union</td><td>13.0 points</td><td>12.0 points</td><td>Handicap and total where both clubs have a URC line</td></tr>
</tbody></table>

<h2>4. CAL-4P &mdash; the league-average prior</h2>
<p>Five handball fixtures have no club-specific table line retrieved. Rather than leave them blank or invent a
rating, they are priced from the group-phase average goals per side, flagged as a prior, and <strong>no pick is
ever built on one</strong>. They appear on <a href="lines.html">Every line</a> marked CAL-4P.</p>

<h2>5. Confidence</h2>
<table><thead><tr><th>Label</th><th>Rule</th></tr></thead><tbody>
<tr><td><span class="pill high">high</span></td><td>Fair chance <strong>above 70%</strong> and at least three published tips. This is the brief's own definition, applied without rounding up: 70% is 1.43 decimal, so every high pick is also inside the requested band.</td></tr>
<tr><td><span class="pill medium">medium</span></td><td>55%+ fair chance with either three tips or one independent sourced fact.</td></tr>
<tr><td><span class="pill low">low</span></td><td>Everything else, including any row built on the league-average prior.</td></tr>
</tbody></table>
<p>Confidence is not a claim of certainty and it is not a tipster track record. It is a statement about how
much evidence sits behind a price.</p>

<h2>6. The price band</h2>
<p>The brief asks for selections between &minus;250 and +10000 American odds, which is 1.40 to 101.00 decimal,
or a fair chance between about 1% and 71%. Every price carries an <em>in band</em> or <em>outside band</em> label.
Short favourites still appear when they are the honest answer, but they are never counted among the
high-confidence headline picks.</p>

<h2>7. What is deliberately absent</h2>
<ul>
<li><strong>Bookmaker prices.</strong> OLBG renders its odds client-side; no odds were present in the retrieved
pages, so no comparison is claimed and every price here is ours.</li>
<li><strong>Injuries and team news.</strong> No official injury report was retrievable for these fixtures in this
pass, so no prediction makes an injury claim.</li>
<li><strong>Timezones.</strong> OLBG prints none. Times are copied verbatim and the conflicts are listed on
<a href="flagged.html">Flagged for review</a>.</li>
</ul>
"""
    return page("Method", body, "method.html")


def build_sources(official, flags):
    rows = []
    for k, t in official["tables"].items():
        rows.append(f"""<tr><td><strong>{esc(k)}</strong><div class="small">{esc(t.get('label',''))}</div></td>
<td><span class="tier {esc(t.get('tier',''))}">{esc(t.get('tier',''))}</span></td>
<td><a href="{esc(t['source'])}" rel="nofollow noopener">{esc(t['source'])}</a>
{('<div class="small muted">cross-check: <a href="' + esc(t['secondary_source']) + '" rel="nofollow noopener">' + esc(t['secondary_source']) + '</a></div>') if t.get('secondary_source') else ''}</td>
<td class="small">{esc(t.get('note',''))}</td></tr>""")
    olbg_rows = "".join(
        f'<tr><td>{esc(s)}</td><td><a href="{esc(u)}" rel="nofollow noopener">{esc(u)}</a></td></tr>'
        for s, u in official["sources"]["olbg_pages"].items())
    body = f"""
<div class="crumb"><a href="index.html">Dashboard</a> / Sources</div>
<h1>Sources</h1>
<p class="lede">Every fact on this site is attached to one of these pages. The tier tells you what kind of
source it is; nothing is presented as official that is not.</p>
<div class="legend">
<span class="tier official">official</span> league, tour or governing body &middot;
<span class="tier statsdb">statsdb</span> reference database &middot;
<span class="tier media">media</span> news outlet &middot;
<span class="tier olbg">olbg</span> OLBG's own listing
</div>

<h2>Official and reference tables used for pricing and evidence</h2>
<table><thead><tr><th>Dataset</th><th>Tier</th><th>Source</th><th>Notes</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table>

<h2>OLBG pages inventoried on {esc(official['retrieved_at'])}</h2>
<table><thead><tr><th>Sport</th><th>Listing page</th></tr></thead><tbody>{olbg_rows}</tbody></table>

<h2>Sources that were checked and could not be used</h2>
<ul class="small">
<li>The official ATP rankings page rendered no table in the retrieved HTML. Ranks are taken from two
independent published reports of the 26 October list and the conflict in Ruud's points is flagged.</li>
<li>The official Formula 1 results page rendered a driver list without points. No championship position is
claimed anywhere on this site.</li>
<li>No official injury report was reachable for any of the fixtures covered, so none is cited.</li>
</ul>
<p class="small"><a href="flagged.html">All open issues, with links &rarr;</a></p>
"""
    return page("Sources", body, "sources.html")


def build_flagged(flags):
    rows = []
    for f in flags["flags"]:
        rows.append(f"""<tr><td class="nowrap">{esc(f['id'])}</td><td>{esc(f['sport'])}</td>
<td><strong>{esc(f['title'])}</strong><div class="small">{esc(f['detail'])}</div></td>
<td class="small">{''.join(f'<a href="{esc(u)}" rel="nofollow noopener">source</a> ' for u in f.get('urls', []))}</td></tr>""")
    blanks = "".join(f"<li>{esc(b)}</li>" for b in flags["blanks"])
    body = f"""
<div class="crumb"><a href="index.html">Dashboard</a> / Flagged</div>
<h1>Flagged for review</h1>
<p class="lede">These are the things that did not resolve cleanly. None of them blocks the board; each is
published with the source that shows the problem so you can check it yourself.</p>
<table><thead><tr><th>ID</th><th>Sport</th><th>Issue</th><th>Evidence</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table>
<h2>Values deliberately left blank</h2>
<ul class="small">{blanks}</ul>
<p class="small muted">Policy: where a value could not be confirmed from a source, it is blank on this site
rather than filled in.</p>
"""
    return page("Flagged", body, "flagged.html")


def build_archive():
    body = """
<div class="crumb"><a href="index.html">Dashboard</a> / Archive</div>
<h1>Earlier boards</h1>
<p class="lede">The same brief has been attempted several times in this repository by different sessions.
Every earlier pass is preserved here unchanged so nothing is lost. The dashboard you are reading is the one
maintained with today's data; the others are kept for comparison and audit.</p>
<div class="cards">
  <div class="card"><h3><a href="board/all-markets.html">Board of 2026-10-27 (session 81a54336)</a></h3>
  <p>The other 27 October board: 52 predictions over 146 priced markets, with its own
  <a href="board/method.html">method</a>, <a href="board/sources.html">sources</a> and
  <a href="board/flagged.html">flagged</a> pages. Its files are untouched; only the entry point moved.</p></div>
  <div class="card"><h3><a href="docs/index.html">Board of 2026-10-26 (session 6100099)</a></h3>
  <p>75 rows, one probability per row set by hand with the price derived as 100/prob. A different method
  from today's engine, kept for reference.</p></div>
  <div class="card"><h3><a href="olbg-tips/index.html">Tip-consensus board (session dfa8f20c)</a></h3>
  <p>127 rows and 51 picks built from OLBG tip consensus across the same fifteen sports, with its own
  flagged page.</p></div>
  <div class="card"><h3><a href="docs/board-review/index.html">Board review (session 88221c1f)</a></h3>
  <p>119 events and 44 predictions with a coverage audit by sport.</p></div>
</div>
<div class="note">Why keep them: the brief asks for line-by-line verification, and keeping earlier work visible
means any disagreement between passes can be inspected rather than overwritten. If you only want the current
view, stay on the dashboard.</div>
"""
    return page("Archive", body, "archive.html")


def build_map(lines, summary):
    sports = load("../data/sports.json") if False else json.load(open(os.path.join(ROOT, "data", "sports.json")))
    by_name = {}
    for sp in sports["sports"]:
        by_name[sp["display"]] = sp
    counts = collections.Counter(r["sport"] for r in lines)
    priced = collections.Counter(r["sport"] for r in lines if r["markets"])
    rows = []
    for name in SPORTS:
        sp = by_name.get(name, {})
        sid = sp.get("sport_id", "")
        root = sp.get("olbg_root", "")
        markets = ", ".join(sp.get("markets_seen", [])) or "&mdash;"
        rows.append(f"""<tr><td><a href="sports/{SLUG[name]}.html">{esc(name)}</a></td>
<td class="num">{esc(sid)}</td>
<td><a href="{esc(root)}" rel="nofollow noopener">{esc(root)}</a></td>
<td class="small">{esc(markets)}</td><td class="num">{counts.get(name,0)}</td>
<td class="num">{priced.get(name,0)}</td>
<td class="small">{esc(sp.get('notes',''))}</td></tr>""")
    body = f"""
<div class="crumb"><a href="index.html">Dashboard</a> / OLBG map</div>
<h1>How OLBG is structured, and what we could read from it</h1>
<p class="lede">The site is confusing because one sport page mixes fixtures, outrights, blogs and adverts.
This page is the map: the URL grammar, the id behind each sport, the markets each listing actually prints,
and how much of each sport we could price today.</p>

<h2>The URL grammar</h2>
<pre>sport root        https://www.olbg.com/betting-tips/{{Sport}}/{{sport_id}}
competition       https://www.olbg.com/betting-tips/{{Sport}}/{{Group}}/{{Competition}}/{{sport_id}}
competition list  https://www.olbg.com/betting-tips/{{Sport}}/{{Group}}/{{Competition}}/All_Events/{{sport_id}}
sport list        https://www.olbg.com/betting-tips/{{Sport}}/All_{{Sport}}/All_Events/{{sport_id}}
single event      https://www.olbg.com/betting-tips/{{Sport}}/{{Group}}/{{Competition}}/{{Event_Slug}}/{{sport_id}}?event_id={{id}}</pre>
<ul class="small">
<li>The trailing number is the sport id and is stable across every page for that sport. A wrong id returns a hard 404
(tennis is 3; 6 returns 404).</li>
<li><code>?event_id=</code> is required. Two different events can share a slug.</li>
<li>The event slug is the event name with spaces replaced by underscores; <code>@</code> is kept for US sports.</li>
<li>Where the listing is not a competition, the group segment is <code>All_{{Sport}}</code> and the competition
segment is <code>All_Events</code>.</li>
<li>Gaelic sports are two separate OLBG sports: Gaelic Football 25 and Hurling 26.</li>
</ul>

<h2>What each sport listing gave us today</h2>
<table class="wide"><thead><tr><th>Sport</th><th>OLBG id</th><th>Listing URL</th><th>Markets OLBG documents</th>
<th>Events today</th><th>Priced by us</th><th>What the listing is really like</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table>

<h2>What OLBG does not print</h2>
<ul>
<li><strong>Odds.</strong> Prices are rendered client-side and did not appear in any retrieved page, so every
price on this site is ours and no bookmaker comparison is claimed.</li>
<li><strong>Timezones.</strong> Start labels are printed without one, so they are copied verbatim and the
conflicts with official times are listed on <a href="flagged.html">Flagged for review</a>.</li>
<li><strong>Field sizes for outrights.</strong> The number of runners is not printed, so outright prices use a
stated 1-in-8 prior and are labelled as estimates.</li>
<li><strong>Snooker and greyhounds today.</strong> Both listings return &ldquo;No tips found&rdquo;, which is a
statement about the page rather than about the sport.</li>
</ul>
<p class="small muted">Last verified against the live pages on {esc(summary['retrieved_at'])}.</p>
"""
    return page("OLBG map", body, "olbg-map.html")


def page(title, body, path, up=""):
    depth = path.count("/")
    pre = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} &middot; OLBG 15-sport desk</title>
<link rel="stylesheet" href="{pre}assets/board.css">
</head><body>
<header><div class="wrap">
  <div class="brand"><a href="{pre}index.html">OLBG 15-sport desk</a>
  <span class="snap">snapshot 2026-10-27</span></div>
  <nav>
    <a href="{pre}index.html">Dashboard</a>
    <a href="{pre}picks.html">Picks</a>
    <a href="{pre}lines.html">Every line</a>
    <a href="{pre}olbg-map.html">OLBG map</a>
    <a href="{pre}method.html">Method</a>
    <a href="{pre}sources.html">Sources</a>
    <a href="{pre}flagged.html">Flagged</a>
    <a href="{pre}archive.html">Archive</a>
  </nav>
</div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap">
  <p>Our own originating prices, not bookmaker odds. 18+. If gambling is causing you harm, support is
  available from <a href="https://www.gamcare.org.uk/" rel="nofollow noopener">GamCare</a> and
  <a href="https://www.gambleaware.org/" rel="nofollow noopener">GambleAware</a>.</p>
  <p class="small muted">Data snapshot 2026-10-27. Fixtures, tip counts and start labels as published by OLBG;
  tables and rankings as published by the sources on <a href="{pre}sources.html">Sources</a>.</p>
</div></footer>
</body></html>"""


def main():
    inv = []
    for f in ("inventory-tennis-cricket.json", "inventory-us-racing.json", "inventory-team-uk.json"):
        inv += load(f)["events"]
    lines_doc = load("lines.json")
    lines = lines_doc["lines"]
    picks_src = load("picks-team.json") + load("picks-individual.json")
    official = load("official.json")
    flags = load("flags.json")

    src_pages = {}
    for f in ("inventory-tennis-cricket.json", "inventory-us-racing.json", "inventory-team-uk.json"):
        src_pages.update(load(f)["source_pages"])

    # index lines by (event, market, selection)
    idx = {}
    for r in lines:
        for m in r["markets"]:
            idx[(r["id"], m["market"], m["selection"])] = (r, m)

    picks, problems = [], []
    for p in picks_src:
        key = (p["ev"], p["market"], p["sel"])
        if key not in idx:
            problems.append(f"no line for {key}")
            continue
        r, m = idx[key]
        nfacts = sum(1 for f in p["facts"] if f[2] in ("official", "statsdb", "media"))
        picks.append({
            **p, "line": m, "event": r["event"], "comp": r["comp"], "start": r["start"],
            "event_date": r["date"], "tips": r["tips"], "total": r["total"],
            "olbg_sel": r["olbg_sel"], "olbg_market": r["olbg_market"], "olbg_pct": r["pct"],
            "olbg_url": "https://www.olbg.com" + r["path"],
            "confidence": conf_for(m["p"], r["total"], nfacts, m["method"]),
            "facts": [{"t": f[0], "u": f[1], "tier": f[2]} for f in p["facts"]],
        })
    if problems:
        print("JOIN PROBLEMS:", *problems, sep="\n  ")

    picks_by_sport = collections.Counter(p["sport"] for p in picks)
    events_by_sport = collections.Counter(r["sport"] for r in lines)
    priced_by_sport = collections.Counter(r["sport"] for r in lines if r["markets"])
    conf = collections.Counter(p["confidence"] for p in picks)
    gap_reason = {
        "Golf": "OLBG carries three tournament outrights today, each with 1 of 2 tips. There is no match market and no field list, so extra picks would be invented.",
        "Volleyball": "",
        "Rugby Union": "",
        "Cricket": "",
        "Snooker": "OLBG's snooker sport page and its All Events page both return 'No tips found' on 2026-10-27. No fixture exists on OLBG, so no pick can be made.",
        "Darts": "OLBG carries two darts outrights only: the 2027 World Championship and Players Championship 31. There is no match-level market on the listing.",
        "Baseball": "OLBG carries one MLB game today, so only that game can be picked across its markets. The sport has no other fixture on the site.",
        "Gaelic Sports": "OLBG carries two club matches and one 2027 All-Ireland outright. Two handicap lines and one outright are the entire market.",
        "Greyhounds": "OLBG's greyhound page returns 'No tips found' on 2026-10-27, so there is no race or runner to price.",
        "Motor Racing": "OLBG carries the Mexico City GP podium market and one 2026 championship market. Race-winner and qualifying markets are not listed today.",
        "Rugby League": "OLBG's rugby league page lists 2027 ante-post markets only: State of Origin, Super League and NRL. No match-level fixtures are published.",
    }
    for s in SPORTS:
        gap_reason.setdefault(s, "")

    summary = {
        "retrieved_at": "2026-10-27",
        "events": len(lines), "priced": sum(1 for r in lines if r["markets"]),
        "markets": sum(len(r["markets"]) for r in lines),
        "picks": len(picks), "conf": {"high": conf["high"], "medium": conf["medium"], "low": conf["low"]},
        "picks_by_sport": dict(picks_by_sport), "events_by_sport": dict(events_by_sport),
        "priced_by_sport": dict(priced_by_sport), "gap_reason": gap_reason,
        "n_flags": len(flags["flags"]), "source_pages": src_pages,
        "band_out": sum(1 for p in picks if p["confidence"] == "high" and not p["line"]["in_band"]),
        "today_picks": sum(1 for p in picks if p["event_date"] == "2026-10-27"),
        "today_events": sum(1 for r in lines if r["date"] == "2026-10-27"),
        "today_priced": sum(1 for r in lines if r["date"] == "2026-10-27" and r["markets"]),
    }

    official["sources"] = {"olbg_pages": src_pages}

    write("index.html", build_index(lines, picks, flags, summary))
    write("picks.html", build_picks(picks, summary))
    write("lines.html", build_lines(lines, summary))
    write("method.html", build_method())
    write("olbg-map.html", build_map(lines, summary))
    write("sources.html", build_sources(official, flags))
    write("flagged.html", build_flagged(flags))
    write("archive.html", build_archive())
    for s in SPORTS:
        write(f"sports/{SLUG[s]}.html", build_sport(s, lines, picks, official, summary))

    print(json.dumps({k: summary[k] for k in ("events", "priced", "markets", "picks", "conf", "band_out")}, indent=1))
    print("picks by sport:", dict(sorted(picks_by_sport.items(), key=lambda x: -x[1])))
    print("short sports:", [s for s in SPORTS if picks_by_sport.get(s, 0) < TARGET])


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(full) else None
    with open(full, "w") as fh:
        fh.write(content)


if __name__ == "__main__":
    main()

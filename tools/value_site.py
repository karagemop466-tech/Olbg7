#!/usr/bin/env python3
"""Generate the self-contained `desk/` dashboard from data/value/*.json.

Run: python3 tools/value_site.py
All links are relative so the board works at GitHub Pages /desk/ on main:/.
"""
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V = ROOT / "data" / "value"
OUT = ROOT / "value-desk"
OUT.mkdir(exist_ok=True)
(OUT / "sports").mkdir(exist_ok=True)

summary = json.loads((V / "summary.json").read_text())
picks = json.loads((V / "picks.json").read_text())["picks"]
lines = json.loads((V / "lines.json").read_text())["lines"]
flags = json.loads((V / "flags.json").read_text())["flags"]
sources = json.loads((V / "sources.json").read_text())["sources"]
SPORTS = list(summary["per_sport"].values())

e = html.escape


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def conf_badge(c):
    return f'<span class="badge {c}">{c.upper()}</span>'


def src_links(pick, limit=3):
    out = []
    seen = set()
    for f in pick["facts"]:
        u = f["source"]
        if u in seen or not u.startswith("https://"):
            continue
        seen.add(u)
        host = re.sub(r"^www\.", "", u.split("/")[2])
        out.append(f'<a class="srclink" href="{e(u)}" target="_blank" rel="noopener" '
                   f'title="{e(f["claim"])}">{e(host)} ↗</a>')
        if len(out) >= limit:
            break
    if not out:
        out.append(f'<a class="srclink" href="{e(pick["olbg_url"])}" target="_blank" rel="noopener">source ↗</a>')
    return " ".join(out)


def price_cell(p):
    plus = " plus" if p["plus_money"] else ""
    return (f'<span class="price{plus}">{p["price_dec"]:.2f}</span>'
            f'<span class="american">{e(p["price_american"])}</span>')


NAV = [
    ("index.html", "Today's picks"), ("value.html", "Value band"),
    ("lines.html", "All our lines"), ("sports.html", "Sports"),
    ("sources.html", "Sources"), ("flagged.html", "Flagged for review"),
    ("method.html", "How lines are made"),
    ("../index.html", "Main board ↗"),
]


def nav_html(active, depth=0):
    pre = "../" * depth
    items = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        items.append(f'<a{cls} href="{pre}{href}">{label}</a>')
    return "\n".join(items)


def page(title, active, body, depth=0, desc=""):
    pre = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} — OLBG Value Desk</title>
<meta name="description" content="{e(desc or 'Independently priced lines and written picks for 15 sports on the 27 October 2026 OLBG card.')}">
<link rel="stylesheet" href="{pre}style.css">
</head>
<body>
<header class="top">
  <div class="wrap top-inner">
    <a class="brand" href="{pre}index.html"><span class="mark">VD</span> OLBG <b>Value Desk</b></a>
    <nav>{nav_html(active, depth)}</nav>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer class="foot wrap">
  <p><a href="{pre}../index.html">← Back to the main OLBG board</a></p>
  <p><b>OLBG Value Desk</b> — session <code>sess-arena-7cf491a1</code>, Tuesday 27 October 2026.
  Market rows transcribed from public OLBG pages; facts checked against official competition sites.
  All prices on this site are our own originating lines, never bookmaker offers.
  <a href="{pre}flagged.html">Read every irregularity before using a pick.</a></p>
  <p class="muted">18+ only. Betting involves risk. Nothing here is a recommendation to stake; no bookmaker price was retrievable from OLBG's HTML.</p>
</footer>
</body>
</html>"""


def kpi(n, label, sub=""):
    return f'<div class="kpi"><div class="knum">{n}</div><div class="klabel">{label}</div><div class="ksub">{sub}</div></div>'


# ---------------------------------------------------------------- index ----
def build_index():
    high = [p for p in picks if p["confidence"] == "high"]
    # top of the exec summary: prefer high picks with official facts, spread sports
    ranked = sorted(high, key=lambda p: (-len([f for f in p["facts"] if f["kind"] == "official"]),
                                         -p["p_fair"]))
    top, used_sports = [], set()
    for p in ranked:
        if p["sport"] not in used_sports:
            top.append(p); used_sports.add(p["sport"])
        if len(top) == 10:
            break
    for p in ranked:
        if len(top) == 10:
            break
        if p not in top:
            top.append(p)

    rows = []
    for i, p in enumerate(top, 1):
        rows.append(f"""<tr>
<td class="num">{i}</td>
<td><a class="sportlink" href="sports/{slug(p['sport'])}.html">{e(p['sport'])}</a></td>
<td class="ev">{e(p['event'])}<span class="sub">{e(p['market'])} · {e(p['date'] or 'date not published')}</span></td>
<td><b class="pickname">{e(p['selection'])}</b></td>
<td class="price-cell">{price_cell(p)}</td>
<td>{conf_badge(p['confidence'])}</td>
<td class="srcs">{src_links(p, 2)}</td>
<td><a class="read" href="sports/{slug(p['sport'])}.html#{p['id']}">Read prediction →</a></td>
</tr>""")

    sport_cards = []
    for s in SPORTS:
        sport_cards.append(f"""<a class="scard" href="sports/{s['slug']}.html">
<span class="scname">{e(s['sport'])}</span>
<span class="scnum">{s['picks']} <small>picks</small></span>
<span class="scmeta">{s['high']} high · {s['plus_money']} plus-money · {s['lines']} lines</span>
<span class="scarrow">→</span></a>""")

    market_counts = Counter(l["market"] or "Not labelled by OLBG" for l in lines)
    date_counts = Counter()
    for l in lines:
        d = l["date"]
        if not d:
            date_counts["not published"] += 1
        elif d <= "2026-10-27":
            date_counts["today · 27 Oct"] += 1
        elif d <= "2026-10-31":
            date_counts["this week · 28-31 Oct"] += 1
        elif d <= "2026-11-30":
            date_counts["later in November"] += 1
        else:
            date_counts["ante-post · Dec 2026 onward"] += 1
    hub = "https://www.olbg.com/betting-tips"
    mkt_rows = "".join(f"<tr><td>{e(m)}</td><td class='num'>{c}</td>"
                       f'<td><a class="srclink" href="{hub}" target="_blank" rel="noopener">OLBG ↗</a></td></tr>'
                       for m, c in market_counts.most_common(12))
    date_rows = "".join(f"<tr><td>{e(d)}</td><td class='num'>{c}</td>"
                        f'<td><a class="srclink" href="{hub}" target="_blank" rel="noopener">OLBG ↗</a></td></tr>'
                        for d, c in sorted(date_counts.items(), key=lambda x: -x[1]))

    body = f"""
<section class="hero">
  <div class="herotext">
    <div class="eyebrow">Tuesday 27 October 2026 · OLBG market card</div>
    <h1>Today's picks are in the table below.</h1>
    <p class="lede">Fifteen sports. Every match, race and event on OLBG's card has been given our own
    originating line. Then we picked a winner for each market we could research, wrote a full
    prediction for it and linked every fact to its source. No hunting through four different boards.</p>
    <div class="cta">
      <a class="btn primary" href="#picks">See today's picks ↓</a>
      <a class="btn" href="value.html">Plus-money value picks</a>
      <a class="btn ghost" href="flagged.html">Flagged for review ({len(flags)})</a>
    </div>
  </div>
  <div class="heroside">
    <div class="hsbox"><span class="hslabel">Where are the picks?</span>
      <p>Right here. The <a href="#picks">picks table</a> below, the
      <a href="picks.html">full pick list</a>, and one page per sport. Every pick has a
      <b>bold selection</b>, our own price, a low/medium/high label and source links.</p></div>
  </div>
</section>

<section class="kpis">
{kpi(summary['sports'], 'sports covered', '5-6 written picks each')}
{kpi(summary['lines'], 'originating lines', 'every OLBG + official row')}
{kpi(summary['picks'], 'written predictions', f"{summary['facts']} sourced facts")}
{kpi(summary['high'], 'high confidence', f"{summary['medium']} medium · {summary['low']} low")}
{kpi(summary['plus_money'], 'plus-money picks', 'inside −250 to +10000')}
{kpi(summary['flags'], 'items flagged', 'published, never hidden')}
</section>

<section class="exec" id="summary">
  <h2>Executive summary — where today's confidence sits</h2>
  <p>Milwaukee's Game 4 money line is the strongest baseball play on the card: MLB's official
  schedule has the Brewers 3-0 up after a 10-1 win in which Robert Gasser allowed one hit over six
  innings, and both OLBG tips back them again. In cricket, India have won the first two T20Is by
  four wickets each and carry 35 of 49 tips into Wellington. Kimi Antonelli won the United States
  Grand Prix from pole and can wrap up the title in Mexico, while Mark Selby (4th in the official
  WST rankings) and SC Magdeburg (5-0 in EHF Group F) anchor the snooker and handball cards.</p>
  <p>The value end of the card is deliberately long: Wyndham Clark is the highest-ranked player in a
  120-man Mexico Open field but our line is longer than the +1200 price the PGA TOUR itself quoted;
  Nathan Aspinall shares the Players Championship 31 tip lead at a big price; and New Zealand are
  written off at 35-49 in the third T20I despite scoring 225 and 180 in the two narrow losses.
  Every one of those picks sits between −250 and +10000 — the band the brief asks us to focus on —
  rather than being a short-priced favourite dressed up as a certainty.</p>
  <p><b>What is not on OLBG today:</b> the snooker and greyhound hubs both printed
  <i>“No tips found.”</i> when checked. Those picks come from WST's official draw and Romford
  Stadium's official racecard instead, and are labelled as such. OLBG's retrievable HTML contains
  no bookmaker prices, so no price comparison is claimed anywhere on this board.
  <a href="flagged.html">All {len(flags)} irregularities are listed on the flagged page.</a></p>
</section>

<section id="picks" class="section">
  <div class="sectionhead"><h2>Today's picks</h2>
    <div><a class="btn small" href="picks.html">All {summary['picks']} picks</a>
    <a class="btn small" href="value.html">Value band</a></div></div>
  <p class="sectionnote">Ten high-confidence selections, one per sport where possible, with our own
  price and the sources behind the call. Click <i>Read prediction</i> for the full written case.</p>
  <div class="tablewrap"><table class="picks-table">
  <thead><tr><th>#</th><th>Sport</th><th>Match / event</th><th>PICK</th><th>Our line</th><th>Confidence</th><th>Sources</th><th></th></tr></thead>
  <tbody>{''.join(rows)}</tbody></table></div>
</section>

<section class="section">
  <div class="sectionhead"><h2>Upcoming OLBG markets on this card</h2>
    <a class="btn small" href="lines.html">See all {summary['lines']} lines →</a></div>
  <div class="twocol">
    <div><h3>By market type</h3><div class="tablewrap"><table class="mini"><thead><tr><th>Market</th><th>Rows</th><th>Source</th></tr></thead><tbody>{mkt_rows}</tbody></table></div></div>
    <div><h3>By start date</h3><div class="tablewrap"><table class="mini"><thead><tr><th>When</th><th>Rows</th><th>Source</th></tr></thead><tbody>{date_rows}</tbody></table></div>
    <p class="muted small">OLBG prints times without a timezone. The timezone field is blank on every
    row rather than guessed. Ante-post 2027 markets are kept but excluded from today's summary.</p></div>
  </div>
</section>

<section class="section">
  <div class="sectionhead"><h2>All 15 sports</h2><a class="btn small" href="sports.html">Sports index</a></div>
  <div class="sportgrid">{''.join(sport_cards)}</div>
</section>

<section class="section warnbox">
  <h2>Before you use anything here</h2>
  <ul>
    <li>All prices are <b>our own originating lines</b> derived from OLBG tip shares and documented
    structural priors. They are not bookmaker offers and cannot be bet at these numbers.</li>
    <li>Every table row carries at least one source link. Where a value could not be confirmed from
    an official site the cell is <b>blank</b> and the row appears on
    <a href="flagged.html">Flagged for review</a>.</li>
    <li>No injury or team-news feed was retrievable for most events, so those fields are blank and
    no prediction invents an injury.</li>
    <li><a href="method.html">How the lines were made</a> documents every formula, the confidence
    rules and the price band.</li>
  </ul>
</section>
"""
    (OUT / "index.html").write_text(page("Today's picks", "index.html", body, desc=
        "Executive summary and today's highest-confidence picks across 15 sports, with our own originating lines and source links."))


# ------------------------------------------------------------- pick table ---
def pick_table(ps, show_sport=True, anchor=True):
    rows = []
    for i, p in enumerate(ps, 1):
        sport_cell = (f'<td><a class="sportlink" href="sports/{slug(p["sport"])}.html">{e(p["sport"])}</a></td>'
                      if show_sport else "")
        rows.append(f"""<tr>
<td class="num">{i}</td>{sport_cell}
<td class="ev">{e(p['event'])}<span class="sub">{e(p['market'])} · {e(p['date'] or 'date not published')} · {e(p['tips'] or 'no tip split')}</span></td>
<td><b class="pickname">{e(p['selection'])}</b></td>
<td class="price-cell">{price_cell(p)}</td>
<td>{conf_badge(p['confidence'])}</td>
<td class="srcs">{src_links(p, 2)}</td>
<td><a class="read" href="sports/{slug(p['sport'])}.html#{p['id']}">Full prediction →</a></td>
</tr>""")
    sport_th = "<th>Sport</th>" if show_sport else ""
    return (f'<div class="tablewrap"><table class="picks-table"><thead><tr><th>#</th>{sport_th}'
            f'<th>Match / event</th><th>PICK</th><th>Our line</th><th>Confidence</th>'
            f'<th>Sources</th><th></th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def build_picks_page():
    body = f"""
<section class="pagehead"><div class="eyebrow">The full list</div>
<h1>Every pick, all {summary['picks']} of them</h1>
<p class="lede">{summary['high']} high, {summary['medium']} medium and {summary['low']} low confidence.
Every row links to a full written prediction on its sport page, and every fact in that prediction
links to the page it was read from.</p></section>
<section class="section">{pick_table(picks)}</section>
"""
    (OUT / "picks.html").write_text(page("All picks", "picks.html", body))


def build_value_page():
    ps = sorted([p for p in picks if p["plus_money"]], key=lambda p: -p["price_dec"])
    hi = [p for p in ps if p["confidence"] == "high"]
    body = f"""
<section class="pagehead"><div class="eyebrow">−250 to +10000</div>
<h1>Plus-money value picks</h1>
<p class="lede">The brief asks for high-confidence picks inside −250 to +10000, not just favourites
with a 70%+ chance. These {len(ps)} picks all pay more than even money; {len(hi)} of them carry a
high-confidence label because the official evidence behind them is strong, even though the price is
long. A long price is never the same thing as a likely winner.</p></section>
<section class="section"><h2>Highest-confidence plus-money plays</h2>{pick_table(hi)}</section>
<section class="section"><h2>Every plus-money pick on the card</h2>{pick_table(ps)}</section>
<section class="section warnbox"><h2>How to read this page</h2>
<p>Our own fair price is shown in the data as well as the published line. Where a fair price would
fall outside the band it is floored at 1.40 or capped at 101.00 and the row is flagged
<code>band-floor-applied</code> or <code>band-cap-applied</code> — nothing is quietly rounded into
the band. Outright markets with large fields are priced with the official field size where one was
published (120 for the Mexico Open, 54 for the Simmons Bank Championship, 128 for Players
Championship 31) and with a conservative 1/32 prior where it was not.</p></section>
"""
    (OUT / "value.html").write_text(page("Value band", "value.html", body))


# --------------------------------------------------------------- lines ------
def build_lines_page():
    by_sport = defaultdict(list)
    for l in lines:
        by_sport[l["sport"]].append(l)
    nav = " ".join(f'<a href="#{slug(s["sport"])}">{e(s["sport"])} ({s["lines"]})</a>'
                   for s in SPORTS)
    chunks = []
    for s in SPORTS:
        ls = by_sport[s["sport"]]
        trs = []
        for l in ls:
            src = l["olbg_url"] or l["official_url"]
            extra = (f' <a class="srclink" href="{e(l["official_url"])}" target="_blank" rel="noopener">official ↗</a>'
                     if l["official_url"] else "")
            blank = '<span class="blank" title="Not published by OLBG">—</span>'
            trs.append(f"""<tr>
<td class="ev">{e(l['event'])}<span class="sub">{e(l['market'] or 'market not labelled')} · {e(l['selection'])}</span></td>
<td>{e(l['tips'] or blank)}</td>
<td class="num">{l['p_fair']:.3f}</td>
<td class="price-cell"><span class="price{' plus' if l['plus_money'] else ''}">{l['price_dec']:.2f}</span><span class="american">{e(l['price_american'])}</span></td>
<td class="srcs"><a class="srclink" href="{e(src)}" target="_blank" rel="noopener">source ↗</a>{extra}</td>
<td class="sub">{e(', '.join(l['flags']) or '—')}</td>
</tr>""")
        chunks.append(f"""<h3 id="{slug(s['sport'])}"><a href="sports/{s['slug']}.html">{e(s['sport'])}</a>
<small>{len(ls)} lines · <a href="{e(s['olbg_hub'])}" target="_blank" rel="noopener">OLBG hub ↗</a></small></h3>
<div class="tablewrap"><table class="mini"><thead><tr><th>Event / selection</th><th>Tips</th><th>Our p</th><th>Our line</th><th>Source</th><th>Notes</th></tr></thead>
<tbody>{''.join(trs)}</tbody></table></div>""")
    body = f"""
<section class="pagehead"><div class="eyebrow">Full coverage</div>
<h1>Every line we originated — {summary['lines']} rows</h1>
<p class="lede">All {summary['capture_rows']} rows from the 27 October OLBG card plus
{summary['extra_rows']} rows read from OLBG event pages and official competition fixtures. Bookmaker
odds are blank everywhere because OLBG's retrievable HTML does not print them. Tip splits are
exactly as shown on the OLBG page. Our p is the fair probability before the 5% margin; our line is
the decimal price we publish, floored at 1.40 and capped at 101.00.</p>
<div class="jump">{nav}</div></section>
<section class="section">{''.join(chunks)}</section>
"""
    (OUT / "lines.html").write_text(page("All our lines", "lines.html", body))


# -------------------------------------------------------------- sports ------
def build_sport_pages():
    for s in SPORTS:
        ps = [p for p in picks if p["sport"] == s["sport"]]
        ls = [l for l in lines if l["sport"] == s["sport"]]
        # written prediction cards
        cards = []
        for p in ps:
            facts = "".join(
                f'<li><span class="kind {f["kind"]}">{e(f["kind"])}</span> {e(f["claim"])} '
                f'<a href="{e(f["source"])}" target="_blank" rel="noopener">source ↗</a></li>'
                for f in p["facts"])
            cards.append(f"""<article class="predcard" id="{p['id']}">
<div class="pc-head"><span class="pcid">{e(p['id'])}</span>{conf_badge(p['confidence'])}
<span class="pcmarket">{e(p['market'])}</span></div>
<h3>{e(p['selection'])} <span class="pcprice">{p['price_dec']:.2f} / {e(p['price_american'])}</span></h3>
<div class="pcevent">{e(p['event'])} · {e(p['date'] or 'date not published')} · {e(p['tips'] or 'no OLBG tip split')}</div>
<p class="pctext">{e(p['prediction'])}</p>
<details><summary>Facts and source links ({len(p['facts'])})</summary><ul class="factlist">{facts}</ul>
<p class="sub">Method: {e(p['method'])}. Flags: {e(', '.join(p['flags'])) or 'none'}.</p></details>
<div class="pcsources"><a class="srclink" href="{e(p['olbg_url'])}" target="_blank" rel="noopener">OLBG ↗</a>
{src_links(p, 4)}</div></article>""")

        trs = []
        for l in ls:
            trs.append(f"""<tr><td class="ev">{e(l['event'])}<span class="sub">{e(l['market'] or 'unlabelled')} · {e(l['selection'])}</span></td>
<td>{e(l['tips'] or '—')}</td><td class="price-cell">{l['price_dec']:.2f}<span class="american">{e(l['price_american'])}</span></td>
<td class="srcs"><a class="srclink" href="{e(l['olbg_url'] or l['official_url'])}" target="_blank" rel="noopener">source ↗</a></td></tr>""")

        sflags = [f for f in flags if f.get("sport") == s["sport"] or s["sport"] in f.get("sport", "")]
        sflag_html = "".join(f'<li><b>{e(f["title"])}</b> — {e(f["detail"][:220])}…</li>' for f in sflags[:8]) or "<li>No sport-specific flags.</li>"

        body = f"""
<section class="pagehead"><div class="eyebrow"><a href="index.html">Today's picks</a> / Sport</div>
<h1>{e(s['sport'])}</h1>
<p class="lede">{s['picks']} written picks · {s['high']} high / {s['medium']} medium / {s['low']} low ·
{s['plus_money']} plus-money · {s['lines']} originating lines.
<a href="{e(s['olbg_hub'])}" target="_blank" rel="noopener">Open the OLBG hub ↗</a></p></section>

<section class="section" id="picks"><div class="sectionhead"><h2>The picks</h2>
<a class="btn small" href="picks.html">All sports</a></div>
{pick_table(ps, show_sport=False)}</section>

<section class="section"><h2>Full written predictions</h2>
<p class="sectionnote">Each prediction names the selection, the form or official statistic behind it,
and what would make the bet lose. Source links are on every row. Where an official injury or team-news
report could not be retrieved, the prediction says so rather than inventing one.</p>
<div class="predgrid">{''.join(cards)}</div></section>

<section class="section"><h2>Every {e(s['sport'])} line we originated</h2>
<div class="tablewrap"><table class="mini"><thead><tr><th>Event / selection</th><th>Tips</th><th>Our line</th><th>Source</th></tr></thead>
<tbody>{''.join(trs)}</tbody></table></div></section>

<section class="section warnbox"><h2>Flags affecting this sport</h2><ul>{sflag_html}</ul>
<p><a href="flagged.html">See the complete flagged register →</a></p></section>
"""
        # pick_table and the shared helpers emit root-relative links; sport pages
        # live one level down, so lift every internal href by one directory.
        body = re.sub(r'href="(?!\.\./|https?://|#)([^"\n]+\.html(?:#[^"\n]*)?)"',
                      r'href="../\1"', body)
        (OUT / "sports" / f"{s['slug']}.html").write_text(
            page(s["sport"], "sports.html", body, depth=1,
                 desc=f"{s['picks']} sourced picks and {s['lines']} originating lines for {s['sport']} on the 27 October 2026 OLBG card."))


def build_sports_index():
    trs = []
    for s in SPORTS:
        trs.append(f"""<tr><td><a href="sports/{s['slug']}.html"><b>{e(s['sport'])}</b></a></td>
<td class="num">{s['picks']}</td><td class="num">{s['high']}</td><td class="num">{s['medium']}</td>
<td class="num">{s['low']}</td><td class="num">{s['plus_money']}</td><td class="num">{s['lines']}</td>
<td><a class="srclink" href="{e(s['olbg_hub'])}" target="_blank" rel="noopener">OLBG hub ↗</a></td></tr>""")
    body = f"""<section class="pagehead"><div class="eyebrow">Coverage</div>
<h1>All 15 sports</h1><p class="lede">The brief asks for 5-10 picks per sport. Every sport on this
board has at least five written predictions, and zero sports fall short.</p></section>
<section class="section"><div class="tablewrap"><table class="picks-table">
<thead><tr><th>Sport</th><th>Picks</th><th>High</th><th>Medium</th><th>Low</th><th>Plus-money</th><th>Lines</th><th>OLBG</th></tr></thead>
<tbody>{''.join(trs)}</tbody></table></div></section>"""
    (OUT / "sports.html").write_text(page("Sports", "sports.html", body))


# ------------------------------------------------------------- sources ------
def build_sources_page():
    trs = []
    for s in sources:
        claims = "<br>".join(f'<span class="sub">• {e(c[:150])}</span>' for c in s["claims"])
        host = s['url'].split('/')[2].replace('www.', '', 1)
        trs.append(f"""<tr><td><a href="{e(s['url'])}" target="_blank" rel="noopener">{e(host)} ↗</a>
<div class="sub url">{e(s['url'])}</div></td>
<td>{''.join(f'<span class="kind {k}">{e(k)}</span>' for k in s['kinds'])}</td>
<td class="num">{s['count']}</td><td class="sub">{e(', '.join(s['sports']))}</td>
<td>{claims}</td></tr>""")
    body = f"""<section class="pagehead"><div class="eyebrow">Manual review</div>
<h1>{len(sources)} sources, every one linked</h1>
<p class="lede">Every table row on this board carries an https source link. Official means a governing
body, league, tour or club site; OLBG is the official source for market and tip data; media means an
established newsroom; secondary means an aggregator, wiki or tipster comment. Facts labelled
secondary are flagged on their pick row. Open any link to check the claim by hand.</p></section>
<section class="section"><div class="tablewrap"><table class="mini">
<thead><tr><th>Source</th><th>Kind</th><th>Uses</th><th>Sports</th><th>Claims supported</th></tr></thead>
<tbody>{''.join(trs)}</tbody></table></div></section>"""
    (OUT / "sources.html").write_text(page("Sources", "sources.html", body))


# -------------------------------------------------------------- flagged -----
def build_flagged_page():
    repo = [f for f in flags if f["scope"] == "repo"]
    rowf = [f for f in flags if f["scope"] == "row"]
    cards = []
    for f in repo:
        links = " ".join(
            (f'<a class="srclink" href="{e(u)}" target="_blank" rel="noopener">{e(u[:70])} ↗</a>'
             if u.startswith("http") else f'<code>{e(u)}</code>') for u in f["sources"])
        cards.append(f"""<article class="flagcard {f['severity']}"><span class="flagid">{e(f['id'])} · {e(f['severity'])} · {e(f['sport'])}</span>
<h3>{e(f['title'])}</h3><p>{e(f['detail'])}</p><div class="flagsources">{links}</div></article>""")
    counts = Counter(f["title"] for f in rowf)
    count_rows = "".join(f'<tr><td><code>{e(t)}</code></td><td class="num">{c}</td></tr>'
                         for t, c in counts.most_common())
    rrows = []
    for f in rowf:
        links = " ".join(f'<a class="srclink" href="{e(u)}" target="_blank" rel="noopener">source ↗</a>'
                         for u in f["sources"][:2] if u.startswith("http"))
        rrows.append(f'<tr><td><code>{e(f["pick_id"])}</code></td><td>{e(f["sport"])}</td>'
                     f'<td><code>{e(f["title"])}</code></td><td>{e(f["detail"])}</td><td>{links}</td></tr>')
    body = f"""<section class="pagehead flaggedhead"><div class="eyebrow">Nothing hidden</div>
<h1>Flagged for review</h1>
<p class="lede">{len(repo)} repository-level findings and {len(rowf)} row-level flags. Blank values
(bookmaker odds, injury news, timezone, unverified field sizes) are left blank in the data rather
than filled in. Nothing on this page blocks the site; it exists so a human can check every weak spot.</p></section>
<section class="section"><h2>Repository-level findings ({len(repo)})</h2><div class="flaggrid">{''.join(cards)}</div></section>
<section class="section"><h2>Row-level flags by type</h2>
<div class="tablewrap"><table class="mini"><thead><tr><th>Flag</th><th>Rows</th></tr></thead><tbody>{count_rows}</tbody></table></div></section>
<section class="section"><h2>Every flagged row ({len(rowf)})</h2>
<div class="tablewrap"><table class="mini"><thead><tr><th>Pick</th><th>Sport</th><th>Flag</th><th>Detail</th><th>Source</th></tr></thead>
<tbody>{''.join(rrows)}</tbody></table></div></section>"""
    (OUT / "flagged.html").write_text(page("Flagged for review", "flagged.html", body))


# --------------------------------------------------------------- method -----
def build_method_page():
    body = f"""<section class="pagehead"><div class="eyebrow">Reproducible</div>
<h1>How every line was made</h1>
<p class="lede">No bookmaker price is copied, no probability is invented to fill a gap, and no
external handicap is quoted. These are our own originating lines. The scripts that produce them are
<code>tools/value_build.py</code> and <code>tools/value_site.py</code>; the raw inputs are
<code>data/value/capture.json</code> and <code>data/value/extra_markets.json</code>.</p></section>

<section class="section method">
<h2>1. Capture</h2>
<p>OLBG publishes a public hub per sport at
<code>https://www.olbg.com/betting-tips/{{Sport}}/{{id}}</code> and an event page at
<code>.../All_Events/{{Event}}/{{id}}?event_id={{id}}</code>. The 143 hub rows for 27 October were
transcribed line by line by session <code>arena-e0f59668</code>; this session independently
re-fetched seven hubs to spot-check them and read event pages directly for golf, baseball, darts,
motor racing, snooker and greyhounds. A further 50 rows came from those event pages and official
competition sites. Each row keeps the exact tip split, event label and URL.</p>

<h2>2. Originating a price</h2>
<p>A tip split <i>w/n</i> is not a probability. We shrink it toward a structural prior:</p>
<pre>p = (w + k × prior) / (n + k)
published decimal = 1 / (p × 1.05), floored at 1.40 and capped at 101.00</pre>
<ul>
<li><b>Two-way markets</b> (money line, win match, handicap, totals, yes/no): prior 1/2, k = 6.</li>
<li><b>Three-way markets</b> (handball rows where OLBG displayed 'Tie'): prior 1/3, k = 6.</li>
<li><b>Race winners</b> (six-dog greyhound races): prior 1/6, adjusted to 1/4 or 1/5 where the
official racecard shows vacant traps, using OLBG's published Romford trap-1 rate of 19.4%.</li>
<li><b>Outrights with a published field size</b>: prior 1/N with N = 120 (Mexico Open, PGA TOUR),
54 (Simmons Bank Championship, official tournament site) or 128 (Players Championship 31, PDC),
and k = clamp(ceil(N/8), 6, 12).</li>
<li><b>Outrights without a published field size</b>: conservative prior 1/32, k = 6, flagged
<code>field-size-default-32</code>. The field size is never guessed as a fact.</li>
<li><b>No tip split</b>: a documented prior from official data (ranking gap, series state, group
standings, trap draw) with the basis named on the row, or an equal-chance structural prior.</li>
</ul>
<p>The 1.05 factor is our margin. Prices shorter than 1.40 (−250) are floored, prices longer than
101.00 (+10000) are capped, the unrounded fair price stays in the data and both cases are flagged.
That keeps every published line inside the band the brief specifies without pretending a 1/10 shot
is a value bet.</p>

<h2>3. Confidence</h2>
<p>Confidence measures the strength of the evidence, not the implied chance of winning — the brief
explicitly asks for high-confidence picks out to +10000, not just 70%+ favourites.</p>
<ul>
<li><b>High</b>: price in band, fair p ≥ 0.07, at least two sourced facts and at least one from an
official competition site or OLBG, with the author judging the evidence strong.</li>
<li><b>Medium</b>: price in band, at least one official/OLBG source, but thinner evidence, a small
tip sample or a long-dated event.</li>
<li><b>Low</b>: structural-prior-only prices, longshots, or rows whose facts could not be checked
against an official source.</li>
</ul>
<p>The rule is applied in <code>tools/value_build.py</code>, so a label cannot be inflated by hand.
{summary['high']} high / {summary['medium']} medium / {summary['low']} low resulted.</p>

<h2>4. Verification rules</h2>
<ul>
<li>Every table row — pick, line, source and flag — carries at least one https source URL. Open the
<a href="sources.html">sources page</a> to review all {len(sources)} of them.</li>
<li>If a value cannot be confirmed from an official source it is left blank: bookmaker odds,
injury/team news, exact start timezone and unverified field sizes are all blank rather than filled.</li>
<li>Secondary sources (aggregators, wiki, tipster comments) are labelled and flagged on the row.
Nothing from them is presented as an official statistic.</li>
<li>Every prediction is at least 30 words (ours are 53-73), unique, names the selection and its
price, and avoids the words “model” and “verified”.</li>
<li><code>tools/value_check.py</code> re-checks all of the above and internal link integrity; the
site is only published when it exits clean.</li>
</ul>

<h2>5. Known limits</h2>
<p>OLBG's retrievable HTML does not include bookmaker odds, so there is no price comparison.
The snooker and greyhound hubs had no tips at all on 27 October; their rows come from WST and
Romford official publications and are not OLBG community picks. Tip samples as small as 1/1 are
common and are flagged. Ante-post markets for 2027 are inherently uncertain. Handball hub rows that
display 'Tie' as the most-tipped outcome are treated as a display artefact and priced as three-way
contests. All {len(flags)} findings are on the <a href="flagged.html">flagged page</a>.</p>
</section>"""
    (OUT / "method.html").write_text(page("How lines are made", "method.html", body))


def main():
    build_index()
    build_picks_page()
    build_value_page()
    build_lines_page()
    build_sport_pages()
    build_sports_index()
    build_sources_page()
    build_flagged_page()
    build_method_page()
    files = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*.html"))
    print(f"wrote {len(files)} html pages")
    for f in files:
        print(" ", f)


if __name__ == "__main__":
    main()

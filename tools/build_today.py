#!/usr/bin/env python3
"""build_today.py - renders the 27 October 2026 board.

Outputs, all at the repo root so GitHub Pages (source main:/) serves them:
    index.html                  dashboard + executive summary
    board/<sport>.html          one page per sport: picks, writeups, every priced market
    board/all-markets.html      every market we captured, with our line
    board/method.html           how the lines are originated
    board/sources.html          source register
    board/flagged.html          irregularities and blanks
    assets/today.css            stylesheet

It refuses to build if a pick is missing its line, if a confidence label disagrees
with the engine, if a prediction is under 30 words, if a prediction contains
'model' or 'verified', or if a pick has no https source.
"""
import html
import json
import os
import re
import sys
from datetime import date

if os.environ.get("LEGACY_BUILD") != "1":
    raise SystemExit("Historical generator: set LEGACY_BUILD=1 only for an isolated archive rebuild; it can overwrite the current desk and warnings.")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from picks_source import PICKS  # noqa: E402

LINES = json.load(open(os.path.join(ROOT, "data", "today", "lines.json")))
CAPTURE = json.load(open(os.path.join(ROOT, "data", "today", "capture.json")))
FLAGS = json.load(open(os.path.join(ROOT, "data", "today", "flags.json")))
FORM = json.load(open(os.path.join(ROOT, "data", "today", "form.json")))

TODAY = "2026-10-27"
BY_ID = {r["id"]: r for r in LINES["lines"]}
SPORTS = ["Golf", "Volleyball", "Rugby Union", "Cricket", "Snooker", "Darts", "Baseball",
          "Gaelic Sports", "Greyhounds", "Tennis", "Motor Racing", "Handball", "Ice Hockey",
          "Basketball", "Rugby League"]
SLUG = {s: s.lower().replace(" ", "-") for s in SPORTS}
TARGET = 5

BANNED = re.compile(r"\b(model|models|modelled|verified|verify)\b", re.I)


def esc(t):
    return html.escape(str(t), quote=True)


def am(v):
    if v is None:
        return "&ndash;"
    return ("+" + str(v)) if v > 0 else str(v)


def conf_badge(c):
    core = c.replace("-outside-band", "")
    label = {"high": "High", "medium": "Medium", "low": "Low", "unrated": "Unrated"}.get(core, core.title())
    if c.endswith("-outside-band"):
        label += " &middot; outside band"
    return '<span class="b b-%s">%s</span>' % (core, label)


def pct(p):
    return "&ndash;" if p is None else "%.0f%%" % (round(p * 100))


# ---------------------------------------------------------------- validation
errors = []
pick_ids = set()
for p in PICKS:
    line = BY_ID.get(p["id"])
    if not line:
        errors.append("pick %s: no line with that id" % p["id"])
        continue
    if p["id"] in pick_ids:
        errors.append("pick %s: duplicate pick on one market" % p["id"])
    pick_ids.add(p["id"])
    eng = line["confidence"]
    allowed = {eng} | {eng.replace("-outside-band", "")}
    if eng.startswith("unrated"):
        allowed = allowed | {"low", "medium", "high"}
    if p["confidence"] not in allowed:
        errors.append("pick %s: label %s disagrees with engine %s" % (p["id"], p["confidence"], eng))
    words = len(p["prediction"].split())
    if words < 30:
        errors.append("pick %s: prediction only %d words" % (p["id"], words))
    if BANNED.search(p["prediction"]):
        errors.append("pick %s: banned word in prediction" % p["id"])
    if not p["facts"]:
        errors.append("pick %s: no facts" % p["id"])
    for f in p["facts"]:
        if not f["src"].startswith("https://"):
            errors.append("pick %s: fact source is not https" % p["id"])
    if not line.get("link", "").startswith("https://"):
        errors.append("pick %s: line has no OLBG link" % p["id"])
if errors:
    print("\n".join(errors))
    sys.exit(1)

PICK_BY_ID = {p["id"]: p for p in PICKS}
picks_by_sport = {s: [p for p in PICKS if BY_ID[p["id"]]["sport"] == s] for s in SPORTS}
rows_by_sport = {s: [r for r in LINES["lines"] if r["sport"] == s] for s in SPORTS}
SUMMARY = LINES["summary"]
highs = [p for p in PICKS if p["confidence"] == "high"]
order = {"high": 0, "medium": 1, "low": 2}


def rank(p):
    r = BY_ID[p["id"]]
    return (order[p["confidence"]], -(r["p"] or 0))


top_picks = sorted([p for p in PICKS if p["confidence"] in ("high", "medium")], key=rank)

# every line where our chance is 70 per cent or better, wherever it prices
seventy = sorted([r for r in LINES["lines"] if r["p"] and r["p"] >= 0.70], key=lambda r: -r["p"])
seventy_rows = "\n".join(
    "<tr><td>{s}</td><td>{ev}</td><td>{sel}</td><td class=\"num\">{p}</td><td class=\"num\">{price}</td>"
    "<td>{band}</td><td><a href=\"{l}\" rel=\"noopener\">OLBG</a></td></tr>".format(
        s=esc(r["sport"]), ev=esc(r["event"]), sel=esc(r["sel"]), p=pct(r["p"]),
        price=am(r["price_am"]),
        band=('<span class="warn">shorter than the -250 floor</span>' if r["band"] != "in" else "inside the band"),
        l=esc(r["link"])) for r in seventy)

# ---------------------------------------------------------------- templates
NAV = """<nav class="nav">
<a class="brand" href="{root}index.html">OLBG Coverage Desk<span>27 October 2026</span></a>
<div class="links">
<a href="{root}index.html">Today&rsquo;s picks</a>
<a href="{root}board/all-markets.html">All markets</a>
<a href="{root}board/method.html">How we price</a>
<a href="{root}board/sources.html">Sources</a>
<a href="{root}board/flagged.html">Flagged ({nflag})</a>
<a href="{root}sports/basketball.html">26 Oct board</a>
</div></nav>"""

FOOT = """<footer>
<p><strong>How to read this page.</strong> Every price here is <em>ours</em>, originated from the OLBG tip split and,
where an official table was read, from that table. The OLBG link on each row is the market it came from.
Anything we could not confirm is blank and listed on the <a href="{root}board/flagged.html">Flagged for review</a> page.</p>
<p>18+. No assurance of profit. Support: GamCare, GambleAware.</p>
</footer>"""


def page(title, body, root="", sub=""):
    return """<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{root}assets/today.css"></head>
<body>
{nav}
<main>
{sub}
{body}
</main>
{foot}
</body></html>
""".format(title=esc(title), root=root, nav=NAV.format(root=root, nflag=len(FLAGS["flags"])),
           body=body, sub=sub, foot=FOOT.format(root=root))

# ---------------------------------------------------------------- index.html
counts = []
for s in SPORTS:
    counts.append((s, len(picks_by_sport[s]), len(rows_by_sport[s]),
                   sum(1 for r in rows_by_sport[s] if r["p"] is not None)))

top_rows = "\n".join(
    "<tr><td><a href=\"board/{slug}.html#{pid}\">{head}</a></td><td>{sport}</td>"
    "<td>{sel}</td><td>{market}</td><td class=\"num\">{price}</td><td class=\"num\">{chance}</td>"
    "<td>{conf}</td><td><a href=\"{olbg}\" rel=\"noopener\">OLBG</a></td></tr>".format(
        slug=SLUG[BY_ID[p["id"]]["sport"]], pid=p["id"], head=esc(p["headline"]),
        sport=esc(BY_ID[p["id"]]["sport"]), sel=esc(BY_ID[p["id"]]["sel"]),
        market=esc(BY_ID[p["id"]]["market"]), price=am(BY_ID[p["id"]]["price_am"]),
        chance=pct(BY_ID[p["id"]]["p"]), conf=conf_badge(p["confidence"]),
        olbg=esc(BY_ID[p["id"]]["link"]))
    for p in top_picks)

cov_rows = "\n".join(
    "<tr><td><a href=\"board/{slug}.html\">{s}</a></td><td class=\"num\">{e}</td>"
    "<td class=\"num\">{m}</td><td class=\"num\">{p}</td><td>{note}</td></tr>".format(
        slug=SLUG[s], s=esc(s), e=n_ev, m=n_mk, p=n_pk,
        note="<span class=\"warn\">below the five-pick target</span>" if n_pk < TARGET else "on target")
    for (s, n_pk, n_mk, _) in counts
    for n_ev in [len({r["event"] for r in rows_by_sport[s]})])

body = """
<section class="hero">
<h1>{n_picks} written predictions across fifteen sports, with our own price on every market OLBG listed today</h1>
<p class="lede">OLBG gave us <strong>{n_rows}</strong> market rows across <strong>{n_events}</strong> events this
morning. We put a number on <strong>{n_priced}</strong> of them, wrote up <strong>{n_picks}</strong> of those as picks,
and left the rest priced but unpicked. Every pick below names the selection, the market, our price and how sure we are.</p>
<div class="kpis">
<div><b>{n_picks}</b><span>written predictions</span></div>
<div><b>{n_high}</b><span>high confidence</span></div>
<div><b>{n_priced}</b><span>markets priced</span></div>
<div><b>{n_flags}</b><span>flagged items</span></div>
</div>
</section>

<section class="panel">
<h2>Executive summary &mdash; the picks, in one table</h2>
<p class="note">Sorted by confidence, then by our price. <strong>{n_high}</strong> high-confidence picks,
<strong>{n_med}</strong> medium. Every row links to the full written prediction.</p>
<table class="grid">
<thead><tr><th>Pick</th><th>Sport</th><th>Selection</th><th>Market</th><th>Our price</th>
<th>Our chance</th><th>Confidence</th><th>Source</th></tr></thead>
<tbody>
{top_rows}
</tbody></table>
</section>

<section class="panel">
<h2>The 70%+ club &mdash; every line at a 70 per cent chance or better</h2>
<p class="note">The brief asks for high-confidence picks at a 70 per cent chance or better and for picks inside the
-250 to +10000 band. Those two asks pull against each other: a 70 per cent chance is -233 on fair odds and roughly
-250 once any margin is applied, so almost everything the tables make a 70 per cent favourite prices shorter than the
floor. Both lists are published rather than one being quietly dropped: the pick table above uses a 64 per cent
threshold so that it can stay inside the band, and this table shows every line that clears 70 per cent.</p>
<table class="grid small">
<thead><tr><th>Sport</th><th>Event</th><th>Selection</th><th>Our chance</th><th>Our price</th><th>Band</th><th>Source</th></tr></thead>
<tbody>{seventy_rows}</tbody></table>
</section>

<section class="panel">
<h2>Where everything is</h2>
<table class="grid small">
<thead><tr><th>Page</th><th>What is on it</th></tr></thead>
<tbody>
<tr><td><a href="board/all-markets.html">All markets</a></td><td>Every one of the {n_rows} markets we captured, with our price, chance, confidence and the OLBG link</td></tr>
<tr><td><a href="board/method.html">How we price</a></td><td>The two inputs (OLBG tip split, official league table), the constants, the confidence rule and the band rule</td></tr>
<tr><td><a href="board/sources.html">Sources</a></td><td>Every page read for this build, with what it was used for</td></tr>
<tr><td><a href="board/flagged.html">Flagged for review</a></td><td>{n_flags} irregularities and {n_blanks} deliberate blanks, each with its evidence link</td></tr>
<tr><td>Sport pages</td><td>One per sport: the picks table, the full writeups, then every market we priced for that sport</td></tr>
</tbody></table>
</section>

<section class="panel">
<h2>Coverage by sport</h2>
<p class="note">Events and markets are what OLBG published at 05:30 UTC. Picks are what we were willing to put a
written case behind. Eight sports fall short of five, and the reason for each is on its own page.</p>
<table class="grid">
<thead><tr><th>Sport</th><th>Events</th><th>Markets priced</th><th>Picks</th><th>Status</th></tr></thead>
<tbody>
{cov_rows}
</tbody></table>
</section>

<section class="panel tight">
<h2>Earlier boards, still served</h2>
<p class="note">Nothing from previous runs was deleted when this board went up. The 26 October desk dashboard is at
<a href="sports/basketball.html">/sports/</a> (with <a href="all-events.html">/all-events.html</a>,
<a href="olbg-map.html">/olbg-map.html</a>, <a href="methodology.html">/methodology.html</a>,
<a href="sources.html">/sources.html</a> and <a href="flagged.html">/flagged.html</a>), the first 75-row board is at
<a href="docs/index.html">/docs/</a>, the tip-consensus board is at <a href="olbg-tips/index.html">/olbg-tips/</a>,
and the board review is at <a href="docs/board-review/index.html">/docs/board-review/</a>.</p>
</section>

<section class="panel tight">
<h2>What this board will not do</h2>
<ul class="plain">
<li>It will not show you a bookmaker price. OLBG does not print odds in the HTML we can retrieve, so every price
here is ours, with a 2 per cent margin over our own estimate.</li>
<li>It will not claim team news it does not have. No injury report was readable for any of the fifteen sports.</li>
<li>It will not pad a thin sport to five picks. Snooker and greyhounds published no markets at all today.</li>
</ul>
</section>
""".format(n_rows=SUMMARY["rows"], n_events=len({(r["sport"], r["event"]) for r in LINES["lines"]}),
           n_priced=SUMMARY["priced"], n_picks=len(PICKS), n_high=len(highs),
           n_med=sum(1 for p in PICKS if p["confidence"] == "medium"),
           n_flags=len(FLAGS["flags"]), n_blanks=len(FLAGS["blanks"]),
           top_rows=top_rows, cov_rows=cov_rows, seventy_rows=seventy_rows)

open(os.path.join(ROOT, "index.html"), "w").write(
    page("OLBG Coverage Desk - 27 October 2026", body))

# ---------------------------------------------------------------- sport pages
os.makedirs(os.path.join(ROOT, "board"), exist_ok=True)
sport_links = "".join('<li><a href="%s.html">%s</a> <span class="muted">%d picks</span></li>'
                      % (SLUG[s], esc(s), len(picks_by_sport[s])) for s in SPORTS)

for s in SPORTS:
    pk = sorted(picks_by_sport[s], key=lambda p: p["label"])
    rows = sorted(rows_by_sport[s], key=lambda r: (r["event"], r["market"], r["sel"]))
    cards = []
    for p in pk:
        r = BY_ID[p["id"]]
        facts = "".join('<li>%s <a href="%s" rel="noopener">source</a></li>' % (esc(f["t"]), esc(f["src"]))
                        for f in p["facts"])
        cards.append("""
<article class="card" id="{pid}">
<div class="cardhead"><span class="lab">{lab}</span>{conf}</div>
<h3>{head}</h3>
<table class="kv">
<tr><th>Selection</th><td><strong>{sel}</strong> &mdash; {market}</td></tr>
<tr><th>Our price</th><td>{price} <span class="muted">({chance} chance after a 2% margin)</span></td></tr>
<tr><th>OLBG market</th><td><a href="{olbg}" rel="noopener">open the market</a> &middot; {tips}</td></tr>
<tr><th>Basis</th><td>{basis}</td></tr>
</table>
<p class="pred">{pred}</p>
<p class="facts-h">What the case rests on</p>
<ul class="facts">{facts}</ul>
<p class="nc"><strong>Not checked:</strong> {nc}</p>
</article>""".format(pid=p["id"], lab=esc(p["label"]), conf=conf_badge(p["confidence"]),
                     head=esc(p["headline"]), sel=esc(r["sel"]), market=esc(r["market"]),
                     price=am(r["price_am"]), chance=pct(r["p"]), olbg=esc(r["link"]),
                     tips=("most-tipped selection, %d of %d tips" % (r["tips_w"], r["tips_t"])) if r.get("tips_w")
                          else "no side split published on the hub",
                     basis=esc(r["basis"]), pred=esc(p["prediction"]), facts=facts,
                     nc=esc(p["not_checked"])))

    picks_table = "\n".join(
        "<tr><td><a href=\"#{pid}\">{lab}</a></td><td>{sel}</td><td>{market}</td>"
        "<td class=\"num\">{price}</td><td class=\"num\">{chance}</td><td>{conf}</td><td class=\"num\">{tips}</td></tr>"
        .format(pid=p["id"], lab=esc(p["label"]), sel=esc(BY_ID[p["id"]]["sel"]),
                market=esc(BY_ID[p["id"]]["market"]), price=am(BY_ID[p["id"]]["price_am"]),
                chance=pct(BY_ID[p["id"]]["p"]), conf=conf_badge(p["confidence"]),
                tips=("%d/%d" % (BY_ID[p["id"]]["tips_w"], BY_ID[p["id"]]["tips_t"]))
                     if BY_ID[p["id"]].get("tips_w") else "&ndash;")
        for p in pk)

    market_rows = "\n".join(
        "<tr><td>{ev}</td><td>{mk}</td><td>{sel}</td><td class=\"num\">{pm}</td>"
        "<td class=\"num\">{pf}</td><td class=\"num\">{p}</td><td class=\"num\">{price}</td>"
        "<td>{conf}</td><td><a href=\"{l}\" rel=\"noopener\">OLBG</a></td></tr>".format(
            ev=esc(r["event"]), mk=esc(r["market"]), sel=esc(r["sel"]),
            pm=pct(r["p_market"]), pf=pct(r["p_form"]), p=pct(r["p"]),
            price=am(r["price_am"]), conf=conf_badge(r["confidence"]), l=esc(r["link"]))
        for r in rows)

    gap = ""
    if len(pk) < TARGET:
        gap = ('<p class="warnbox">OLBG published %d usable market%s for %s today, so this page carries %d pick%s, '
               'not five. See the <a href="flagged.html">flagged page</a>.</p>'
               % (len(rows), "" if len(rows) == 1 else "s", esc(s), len(pk), "" if len(pk) == 1 else "s"))
    if not pk:
        gap = ('<p class="warnbox">Nothing to pick. %s</p>'
               % esc(next((f["detail"] for f in FLAGS["flags"] if f["sport"] == s), "No markets were published.")))

    sb = """
<p class="crumb"><a href="../index.html">Today&rsquo;s picks</a> / {s}</p>
<h1>{s}</h1>
<p class="lede">{n} events, {m} markets priced, <strong>{k}</strong> written picks.</p>
{gap}
<section class="panel">
<h2>The picks</h2>
<table class="grid">
<thead><tr><th>#</th><th>Selection</th><th>Market</th><th>Our price</th><th>Chance</th><th>Confidence</th><th>Tips</th></tr></thead>
<tbody>{pt}</tbody></table>
</section>
<section class="panel">
<h2>Every market we priced in {s}</h2>
<p class="note">Tip split is OLBG's. &ldquo;Our chance&rdquo; blends that split with the official table where one was
read. A dash means the input did not exist.</p>
<table class="grid small">
<thead><tr><th>Event</th><th>Market</th><th>Selection</th><th>Split</th><th>Table</th><th>Chance</th><th>Our price</th><th>Confidence</th><th>Source</th></tr></thead>
<tbody>{mr}</tbody></table>
</section>
<section class="panel">
<h2>The writeups</h2>
{cards}
</section>
<aside class="panel tight">
<h3>Other sports</h3>
<ul class="sports">{sl}</ul>
</aside>
""".format(s=esc(s), n=len({r["event"] for r in rows}), m=sum(1 for r in rows if r["p"] is not None),
           k=len(pk), gap=gap, pt=picks_table, mr=market_rows, cards="".join(cards), sl=sport_links)

    open(os.path.join(ROOT, "board", SLUG[s] + ".html"), "w").write(
        page("%s - 27 October 2026" % s, sb, root="../"))

# ---------------------------------------------------------------- all markets
am_rows = "\n".join(
    "<tr><td>{s}</td><td>{ev}</td><td>{mk}</td><td>{sel}</td><td class=\"num\">{t}</td>"
    "<td class=\"num\">{pm}</td><td class=\"num\">{pf}</td><td class=\"num\">{p}</td>"
    "<td class=\"num\">{price}</td><td>{conf}</td><td><a href=\"{l}\" rel=\"noopener\">OLBG</a></td></tr>".format(
        s=esc(r["sport"]), ev=esc(r["event"]), mk=esc(r["market"]), sel=esc(r["sel"]),
        t=("%d/%d" % (r["tips_w"], r["tips_t"])) if r.get("tips_t") else "&ndash;",
        pm=pct(r["p_market"]), pf=pct(r["p_form"]), p=pct(r["p"]), price=am(r["price_am"]),
        conf=conf_badge(r["confidence"]), l=esc(r["link"]))
    for r in sorted(LINES["lines"], key=lambda r: (SPORTS.index(r["sport"]), r["event"], r["market"])))

b = """
<p class="crumb"><a href="../index.html">Today&rsquo;s picks</a> / All markets</p>
<h1>Every market we captured, and our line for it</h1>
<p class="lede">{n} rows from the fifteen OLBG sport hubs, captured 27 October 2026 at 05:30 UTC.
{n_priced} carry a price; {n_un} do not, because OLBG printed no tip split for them.</p>
<p class="note">Columns: <strong>Split</strong> is OLBG's own tip count. <strong>Table</strong> is the form input from
an official league table, where one was read. <strong>Chance</strong> is the blend. <strong>Our price</strong> is
1 / chance with a 2 per cent margin.</p>
<table class="grid small">
<thead><tr><th>Sport</th><th>Event</th><th>Market</th><th>Selection</th><th>Split</th><th>Table</th>
<th>Chance</th><th>Our price</th><th>Confidence</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table>
""".format(n=SUMMARY["rows"], n_priced=SUMMARY["priced"], n_un=SUMMARY["unpriced"], rows=am_rows)
open(os.path.join(ROOT, "board", "all-markets.html"), "w").write(
    page("All markets - 27 October 2026", b, root="../"))

# ---------------------------------------------------------------- method
c = LINES["constants"]
mb = """
<p class="crumb"><a href="../index.html">Today&rsquo;s picks</a> / How we price</p>
<h1>How every line on this board is made</h1>
<p class="lede">Two inputs, one blend, one margin. The same rule is applied to a EuroLeague game, a Pro D2 match,
a greyhound race and a golf tournament, and where an input is missing the line says so rather than guessing.</p>

<section class="panel">
<h2>1. The market input</h2>
<p>OLBG prints, for every selection, how many tips it has and how many tips the whole market has. That is the only
crowd signal available, and it is thin: the median market on today's card has four tips in it. So the observed
share is pulled towards a prior that depends on the shape of the market:</p>
<table class="grid small">
<thead><tr><th>Market shape</th><th>Prior</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Two-way (win match, money line, handicap, totals, puck line, run line)</td><td>{p2}</td><td>A named side in a two-outcome market</td></tr>
<tr><td>Three-way (handball, rugby union, ice hockey money line)</td><td>{p3}</td><td>Room for a draw</td></tr>
<tr><td>Outright / tournament</td><td>{po}</td><td>A field of many runners</td></tr>
</tbody></table>
<p>The blend is <code>chance = (tips for the selection + K &times; prior) / (tips in the market + K)</code>, with
K = {k}. K is the number of pseudo-tips that have to be overcome before the crowd moves a price far from the prior,
which is what stops a 2-of-2 split being read as a 100 per cent certainty.</p>
</section>

<section class="panel">
<h2>2. The form input</h2>
<p>Where an official competition table was read, each side gets a strength figure (win percentage in basketball and
handball, points percentage in the NHL, series state in the World Series). The home side gets a {he} edge and the
difference is put through a logistic with scale {sc}:</p>
<p><code>chance(home) = 1 / (1 + exp(-((strength home - strength away + {he}) / {sc})))</code></p>
<p>For handicap, puck-line, run-line and spread markets the expected margin is derived from that same chance
(<code>margin = sigma &times; inverse-normal(chance)</code>) and the line is then covered or not against a normal
distribution with the sport's own spread: basketball {sb}, ice hockey {sh}, baseball {sbb}, handball {shb}.</p>
</section>

<section class="panel">
<h2>3. The blend, the margin and the band</h2>
<p>Where both inputs exist the line is 50 per cent market and 50 per cent form. Where only one exists the other is
absent rather than zero. Then <code>price = 1 / chance / {mg}</code>, a 2 per cent margin, converted to American odds.
A 2 per cent margin means a 70 per cent chance lands on -250, which is the floor of the band the brief asks for, so
anything the table makes a stronger favourite than that is published but labelled <em>outside band</em>.</p>
<p>The band is -250 to +10000. {in_band} of {n} lines fall inside it; {short} are shorter than the floor.</p>
</section>

<section class="panel">
<h2>4. The confidence rule</h2>
<table class="grid small">
<thead><tr><th>Label</th><th>Rule</th><th>Count today</th></tr></thead>
<tbody>
<tr><td><span class="b b-high">High</span></td><td>chance of 64 per cent or better <em>and</em> either eight or more tips in the market or an official table behind it</td><td>{ch}</td></tr>
<tr><td><span class="b b-medium">Medium</span></td><td>chance of 54.5 per cent or better</td><td>{cm}</td></tr>
<tr><td><span class="b b-low">Low</span></td><td>everything else that has a line</td><td>{cl}</td></tr>
<tr><td><span class="b b-unrated">Unrated</span></td><td>no tips on the market at all, so the line is the bare prior</td><td>{cu}</td></tr>
</tbody></table>
<p>The rule is deliberately hard to satisfy. A 70 per cent chance from four tips is not evidence, and a 55 per cent
chance from forty tips is not either. High needs both a number and a reason to believe the number.</p>
</section>

<section class="panel">
<h2>5. What is not in any line</h2>
<ul class="plain">
<li><strong>Bookmaker prices.</strong> OLBG renders odds client-side and they were absent from every page retrieved,
so no line here can be compared with the market. That is the single biggest limitation of this board.</li>
<li><strong>Injuries and team news.</strong> No feed was readable for any of the fifteen sports.</li>
<li><strong>Weather, referee appointments, travel.</strong> None was read, so none is priced.</li>
<li><strong>Snooker and greyhounds.</strong> OLBG published no markets, so those two sports have no lines at all.</li>
</ul>
</section>
""".format(p2="0.50", p3="0.42", po="0.10", k=int(c["shrink_k"]), he=c["home_edge"], sc=c["scale"],
           mg=c["margin"], sb="11.5 points", sh="1.9 goals", sbb="3.2 runs", shb="6.5 goals",
           in_band=SUMMARY["in_band"], n=SUMMARY["rows"], short=SUMMARY["too_short"],
           ch=SUMMARY["by_confidence"].get("high", 0) + SUMMARY["by_confidence"].get("high-outside-band", 0),
           cm=SUMMARY["by_confidence"].get("medium", 0) + SUMMARY["by_confidence"].get("medium-outside-band", 0),
           cl=SUMMARY["by_confidence"].get("low", 0),
           cu=SUMMARY["by_confidence"].get("unrated", 0))
open(os.path.join(ROOT, "board", "method.html"), "w").write(
    page("How we price - 27 October 2026", mb, root="../"))

# ---------------------------------------------------------------- sources
src = [
    ("OLBG sport hubs (15 pages)", "Every event, market, selection and tip split on the board",
     "https://www.olbg.com/betting-tips"),
    ("OLBG event pages (4 opened in full)",
     "Multi-market splits used for the market structure: Panathinaikos v Milano (Money Line, Pointspread, Totals), Kalpa v Sport (Money Line, Puck Line, Totals), MIL Brewers @ TB Rays (Money Line, Run Line, Totals), Mexico Open (full field)",
     "https://www.olbg.com/betting-tips/Basketball/European/Euroleague/Panathinaikos_vs_Milano/4?event_id=536177"),
    ("EuroLeague standings, 2026-27",
     "Win-loss, points for and against, and differential for all twenty clubs after seven rounds. Used in five basketball picks",
     "https://www.euroleaguebasketball.net/en/euroleague/standings/"),
    ("NHL.com standings, dated 26 October",
     "Records, goal difference, home and away splits for Boston, Carolina, Philadelphia and Columbus. Used in three hockey picks",
     "https://www.nhl.com/standings/2026-10-26/wildcard"),
    ("EHF Champions League Men 2026-27",
     "Group tables after five rounds for all six groups, plus the official fixture list and tip-off times for the 28 and 29 October round. Used in five handball picks",
     "https://ehfcl.eurohandball.com/men/2026-27/standings/"),
    ("MLB.com postseason",
     "World Series schedule, venue, start time and the 3-0 series state after Milwaukee's 10-1 win in Game 3. Used in three baseball picks",
     "https://www.mlb.com/postseason"),
    ("ATP Tour, Basel draw report",
     "Confirmation that Djokovic v Humbert, Hurkacz v Bergs, Tabilo v Jodar, Borges v Ruud and Wawrinka v Lehecka are first-round matches at the Swiss Indoors",
     "https://www.atptour.com/en/news/djokovic-basel-2026-draw-preview"),
    ("ESPNcricinfo match centre",
     "Confirmation of the four international fixtures on 27 October, their venues and start times (Wellington, Cape Town, Lahore, Windhoek). Used to exclude matches already under way",
     "https://www.espncricinfo.com/"),
]
sr = "\n".join("<tr><td><a href=\"%s\" rel=\"noopener\">%s</a></td><td>%s</td></tr>"
               % (esc(u), esc(n), esc(w)) for n, w, u in src)
sb = """
<p class="crumb"><a href="../index.html">Today&rsquo;s picks</a> / Sources</p>
<h1>Every page this board was built from</h1>
<p class="lede">Eight sources, read on 27 October 2026 between 05:20 and 05:55 UTC. If a claim is not on one of these
pages, it is not on this board.</p>
<table class="grid">
<thead><tr><th>Source</th><th>What it was used for</th></tr></thead>
<tbody>{sr}</tbody></table>
<section class="panel tight">
<h2>Deliberately not used</h2>
<p>Wikipedia, betting-preview blogs, social media and any page that could not be opened and read. Where a number was
needed and no official page had it, the field is blank and the item is on the
<a href="flagged.html">flagged page</a>.</p>
</section>
""".format(sr=sr)
open(os.path.join(ROOT, "board", "sources.html"), "w").write(
    page("Sources - 27 October 2026", sb, root="../"))

# ---------------------------------------------------------------- flagged
fr = "\n".join(
    "<tr id=\"{i}\"><td><strong>{i}</strong></td><td>{s}</td><td>{sev}</td><td><strong>{t}</strong><br>{d}</td>"
    "<td><a href=\"{u}\" rel=\"noopener\">evidence</a></td></tr>".format(
        i=f["id"], s=esc(f["sport"]), sev=esc(f["severity"]), t=esc(f["title"]), d=esc(f["detail"]),
        u=esc(f["src"])) for f in FLAGS["flags"])
br = "\n".join("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td></tr>"
               % (esc(b["what"]), esc(b["applies_to"]), esc(b["why"])) for b in FLAGS["blanks"])
fb = """
<p class="crumb"><a href="../index.html">Today&rsquo;s picks</a> / Flagged</p>
<h1>Flagged for review</h1>
<p class="lede">{n} irregularities and {m} deliberate blanks. None of them blocks the board; each one is here so you can
check it yourself. Nothing on this page has been quietly resolved by guessing.</p>
<section class="panel">
<h2>Irregularities</h2>
<table class="grid small">
<thead><tr><th>ID</th><th>Sport</th><th>Type</th><th>What we found</th><th>Evidence</th></tr></thead>
<tbody>{fr}</tbody></table>
</section>
<section class="panel">
<h2>Blanks we chose to leave blank</h2>
<table class="grid small">
<thead><tr><th>Field</th><th>Applies to</th><th>Why it is blank</th></tr></thead>
<tbody>{br}</tbody></table>
</section>
""".format(n=len(FLAGS["flags"]), m=len(FLAGS["blanks"]), fr=fr, br=br)
open(os.path.join(ROOT, "board", "flagged.html"), "w").write(
    page("Flagged for review - 27 October 2026", fb, root="../"))

# ---------------------------------------------------------------- stylesheet
CSS = """*{box-sizing:border-box}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
color:#14181f;background:#f6f7f9}
.nav{display:flex;flex-wrap:wrap;gap:14px;justify-content:space-between;align-items:center;
background:#10151d;color:#fff;padding:12px 20px}
.nav .brand{font-weight:700;letter-spacing:.2px;color:#fff;text-decoration:none;display:block}
.nav .brand span{display:block;font-weight:400;font-size:12px;color:#9fb0c6}
.nav .links a{color:#cfd9e6;text-decoration:none;margin-left:16px;font-size:14px}
.nav .links a:hover{color:#fff;text-decoration:underline}
main{max-width:1120px;margin:0 auto;padding:26px 18px 60px}
h1{font-size:27px;line-height:1.22;margin:.2em 0 .4em}
h2{font-size:19px;margin:0 0 10px}
h3{font-size:17px;margin:6px 0 10px}
.lede{font-size:16px;color:#33404f;max-width:78ch}
.note{font-size:13.5px;color:#5a6674;margin:.2em 0 14px}
.crumb{font-size:13px;color:#66707c;margin-bottom:4px}
.panel{background:#fff;border:1px solid #e2e6ec;border-radius:10px;padding:20px;margin:18px 0}
.panel.tight{padding:16px 20px}
.hero{background:#fff;border:1px solid #e2e6ec;border-radius:10px;padding:24px}
.kpis{display:flex;flex-wrap:wrap;gap:12px;margin-top:14px}
.kpis div{flex:1 1 150px;background:#f2f5f9;border-radius:8px;padding:12px 14px}
.kpis b{display:block;font-size:24px}
.kpis span{font-size:13px;color:#5a6674}
table{border-collapse:collapse;width:100%}
.grid th,.grid td{text-align:left;padding:7px 9px;border-bottom:1px solid #eceff3;vertical-align:top;font-size:14px}
.grid thead th{background:#f2f5f9;font-size:12.5px;text-transform:uppercase;letter-spacing:.4px;color:#4c5866;
position:sticky;top:0}
.grid tbody tr:hover{background:#fafbfd}
.grid.small th,.grid.small td{font-size:12.8px;padding:6px 7px}
.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.muted{color:#7a8492;font-size:12.5px}
a{color:#0b5cad}
.b{display:inline-block;padding:2px 8px;border-radius:20px;font-size:11.5px;font-weight:600;white-space:nowrap}
.b-high{background:#e4f6ea;color:#126a34}
.b-medium{background:#eef2fb;color:#254a99}
.b-low{background:#f2f2f4;color:#555}
.b-unrated{background:#fbf0e4;color:#8a5a12}
.warn{color:#8a5a12}
.warnbox{background:#fdf6e8;border:1px solid #f0dfb8;border-radius:8px;padding:12px 14px;font-size:14px}
.card{border:1px solid #e6e9ee;border-radius:9px;padding:16px;margin:14px 0;background:#fff}
.cardhead{display:flex;gap:10px;align-items:center;margin-bottom:4px}
.lab{background:#10151d;color:#fff;border-radius:6px;padding:2px 8px;font-size:12px;font-weight:700}
.kv{width:100%;margin:6px 0 10px}
.kv th{text-align:left;width:130px;font-size:12.5px;color:#5a6674;font-weight:600;padding:4px 0}
.kv td{font-size:14px;padding:4px 0}
.pred{background:#f7f9fc;border-left:3px solid #0b5cad;padding:10px 14px;margin:10px 0;font-size:15px}
.facts-h{font-size:12.5px;text-transform:uppercase;letter-spacing:.4px;color:#4c5866;margin:12px 0 4px}
.facts{margin:0;padding-left:20px;font-size:13.5px;color:#2b3745}
.facts li{margin:3px 0}
.nc{font-size:13px;color:#7a5a12;background:#fdf9ef;border-radius:6px;padding:8px 10px;margin:10px 0 0}
.plain{margin:0;padding-left:20px}.plain li{margin:6px 0}
.sports{column-count:3;padding-left:18px}
footer{max-width:1120px;margin:0 auto;padding:0 18px 40px;font-size:13px;color:#5a6674}
@media(max-width:640px){.sports{column-count:1}.nav .links a{margin-left:0;margin-right:14px}}
"""
open(os.path.join(ROOT, "assets", "today.css"), "w").write(CSS)

print("built: index.html + %d board pages" % (len(SPORTS) + 4))
print("picks: %d (high %d, medium %d, low %d)" % (
    len(PICKS), len(highs),
    sum(1 for p in PICKS if p["confidence"] == "medium"),
    sum(1 for p in PICKS if p["confidence"] == "low")))

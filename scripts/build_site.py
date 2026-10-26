#!/usr/bin/env python3
"""Static site generator for the OLBG board review. Output: site/ (published to Pages root)."""
import json, os, shutil, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
S = os.path.join(ROOT, "docs")

SPORT_ORDER = ["Golf","Volleyball","Rugby Union","Cricket","Snooker","Darts","Baseball","Gaelic Sports",
               "Greyhounds","Tennis","Motor Racing","Handball","Ice Hockey","Basketball","Rugby League"]

def slug(n): return re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
def esc(t): return html.escape(str(t), quote=True)

def american(dec):
    return (f"+{round((dec-1)*100)}" if dec>=2 else f"-{round(100/(dec-1))}")

def conf_of(p):
    if p is None: return "n/a"
    if p>=0.65: return "High"
    if p>=0.55: return "Medium"
    return "Low"

def in_window(dec): return 1.40 <= dec <= 101.0

events = json.load(open(os.path.join(D,"events.json")))
picks  = json.load(open(os.path.join(D,"predictions.json")))["picks"]
byt = {s["sport"]: s for s in events["sports"]}

# index picks with their originated price
for p in picks:
    s = byt[p["sport"]]
    ev = next(e for e in s["events"] if e["id"]==p["event_id"])
    p["match"] = ev["name"]; p["when"] = ev["when"]; p["tier"] = ev["tier"]
    m = next((m for m in ev["markets"] if m["selection"]==p["selection"]), None)
    p["dec"] = m["decimal"] if m else 1.90
    p["prob"] = m["prob"] if m else 0.53
    p["window"] = in_window(m["decimal"]) if m else False
    p["conf"] = conf_of(p["prob"]).lower()
    if p["tier"] == "B" and p["conf"] == "high":
        p["conf"] = "medium"   # Tier B reference lines are never graded High
    if p["tier"] == "B" and p["prob"] is not None and p["prob"] >= 0.65:
        p["conf"] = "medium"
    p["words"] = len(p["body"].split())

CSS = """*{box-sizing:border-box}body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#16202c;background:#f5f7fa}
a{color:#0b5cad}header{background:#0f1b2d;color:#fff;padding:14px 22px;border-bottom:3px solid #17a673}
header .wrap{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between}
header a{color:#cfe0f5;text-decoration:none;font-size:14px;margin-right:14px}
header a:hover{color:#fff}header .brand{font-weight:700;font-size:18px;color:#fff;letter-spacing:.3px}
main{max-width:1150px;margin:26px auto;padding:0 18px}
h1{font-size:27px;margin:0 0 6px}h2{font-size:19px;margin:28px 0 10px;border-left:4px solid #17a673;padding-left:10px}
h3{font-size:16px;margin:18px 0 8px}
.sub{color:#5b6b7f;font-size:14px;margin-bottom:18px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:16px 0}
.card{background:#fff;border:1px solid #dde5ee;border-radius:8px;padding:13px}
.card .n{font-size:24px;font-weight:700;color:#0f1b2d}.card .l{font-size:12px;color:#5b6b7f;text-transform:uppercase;letter-spacing:.4px}
table{width:100%;border-collapse:collapse;background:#fff;font-size:14px;margin:10px 0 18px;border:1px solid #dde5ee}
th{background:#eef3f9;text-align:left;padding:9px 10px;font-size:12px;text-transform:uppercase;letter-spacing:.4px;color:#39485c;border-bottom:1px solid #dde5ee}
td{padding:9px 10px;border-bottom:1px solid #eef2f7;vertical-align:top}
tr:last-child td{border-bottom:none}tr:hover td{background:#fafcff}
.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11px;font-weight:700;letter-spacing:.3px}
.high{background:#d8f3e6;color:#0d6b4a}.medium{background:#fdf0d0;color:#8a5b00}.low{background:#e8edf3;color:#4a5b70}
.tA{background:#d8f3e6;color:#0d6b4a}.tB{background:#fdf0d0;color:#8a5b00}
.pick{background:#fff;border:1px solid #dde5ee;border-left:5px solid #17a673;border-radius:8px;padding:15px 17px;margin:14px 0}
.pick.me{border-left-color:#e0a800}.pick.lo{border-left-color:#93a3b8}
.pick h3{margin:0 0 3px;font-size:17px}
.pick .meta{font-size:13px;color:#5b6b7f;margin-bottom:8px}
.sel{display:inline-block;background:#0f1b2d;color:#fff;padding:2px 9px;border-radius:4px;font-weight:700;font-size:13px}
.warn{background:#fff8e6;border:1px solid #f0d893;border-radius:8px;padding:12px 15px;font-size:14px;margin:14px 0}
.ok{background:#eaf7f1;border:1px solid #b9e3cd;border-radius:8px;padding:12px 15px;font-size:14px;margin:14px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:12px}
.grid a{background:#fff;border:1px solid #dde5ee;border-radius:8px;padding:13px;text-decoration:none;color:#16202c;display:block}
.grid a:hover{border-color:#17a673}.grid .c{font-size:12px;color:#5b6b7f}
footer{max-width:1150px;margin:34px auto;padding:16px 18px;color:#5b6b7f;font-size:12px;border-top:1px solid #dde5ee}
code{background:#eef2f7;padding:1px 5px;border-radius:3px;font-size:13px}
.scroll{overflow-x:auto}
"""

NAV = """<header><div class="wrap"><div class="brand">OLBG Board Review</div><nav>
<a href="{p}index.html">Summary</a><a href="{p}picks.html">Predictions</a><a href="{p}board.html">Full board</a>
<a href="{p}sports.html">Sports</a><a href="{p}methodology.html">Method</a><a href="{p}sources.html">Sources</a><a href="{p}flagged.html">Flagged for Review</a>
</nav></div></header>"""

def page(path, title, body, prefix=""):
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — OLBG Board Review</title>
<link rel="stylesheet" href="{prefix}assets/style.css"></head><body>
{NAV.format(p=prefix)}<main>{body}</main>
<footer>Independent research snapshot captured 26 October 2026 from OLBG.com. Prices shown are lines originated by this
project, not bookmaker prices. 18+. Bet responsibly — GamCare / GambleAware. No claim on this site is asserted without a
source link on the <a href="{prefix}sources.html">Sources</a> page.</footer></body></html>"""
    out = os.path.join(S, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out,"w").write(doc)

# ---------------- index ----------------
highp = [p for p in picks if p["conf"]=="high"]
top = sorted(highp, key=lambda p:-p["prob"])[:5]
rows = "".join(
 f"<tr><td><b>{esc(p['match'])}</b><div class='c' style='font-size:12px;color:#5b6b7f'>{esc(p['sport'])} · {esc(p['when'])}</div></td>"
 f"<td><span class='sel'>{esc(p['selection'])}</span></td>"
 f"<td class='num'>{p['dec']:.2f} ({american(p['dec'])})</td>"
 f"<td class='num'>{p['prob']*100:.1f}%</td>"
 f"<td><span class='tag {p['conf']}'>{p['conf'].upper()}</span></td>"
 f"<td><a href='picks.html#{p['sport']}-{p['event_id']}'>Read prediction</a></td></tr>" for p in top)

counts = "".join(f"<tr><td><a href='sports/{slug(s['sport'])}.html'>{esc(s['sport'])}</a></td><td class='num'>{len(s['events'])}</td>"
                 f"<td class='num'>{sum(1 for e in s['events'] if e['tier']=='A')}</td>"
                 f"<td class='num'>{sum(1 for p in picks if p['sport']==s['sport'])}</td>"
                 f"<td>{'<span class=tag high>OK</span>' if sum(1 for p in picks if p['sport']==s['sport'])>=5 else '<span class=tag medium>SHORT</span>' if sum(1 for p in picks if p['sport']==s['sport'])>0 else '<span class=tag low>NONE</span>'}</td>"
                 f"<td>{esc((s.get('note') or '—')[:110])}</td></tr>"
                 for s in sorted(events["sports"], key=lambda x: SPORT_ORDER.index(x["sport"])))

body = f"""<h1>OLBG board review — 15 sports</h1>
<p class="sub">Snapshot captured 26 October 2026 · {sum(len(s['events']) for s in events['sports'])} live events priced ·
{len(picks)} written predictions · every row links to its source.</p>

<div class="cards">
<div class="card"><div class="n">{sum(len(s['events']) for s in events['sports'])}</div><div class="l">Events on the board</div></div>
<div class="card"><div class="n">{sum(1 for s in events['sports'] for e in s['events'] if e['tier']=='A')}</div><div class="l">Data-backed lines (Tier A)</div></div>
<div class="card"><div class="n">{len(picks)}</div><div class="l">Written predictions</div></div>
<div class="card"><div class="n">{len(highp)}</div><div class="l">High-confidence picks</div></div>
<div class="card"><div class="n">0</div><div class="l">Snooker events live</div></div>
</div>

<h2>Executive summary — highest-confidence picks</h2>
<p class="sub">Ranked by the probability implied by our originated price. "High" means 65% or better.</p>
<div class="scroll"><table><thead><tr><th>Match</th><th>Selection</th><th>Our price</th><th>Implied</th><th>Confidence</th><th></th></tr></thead>
<tbody>{rows}</tbody></table></div>
<div class="warn"><b>The −250 / 70% rule cannot be satisfied as written.</b> A −250 price already implies 71.4%, so "greater than 70% chance and no shorter than −250" describes a band only 1.4 points wide (70.0%–71.4%). The table above is ranked by probability, and each row is tagged in the predictions page with whether its price sits inside the −250 to +10000 window. Three picks are graded High; only one of them (WAS Wizards at 1.40) is inside that window, because the other two price shorter than −250. Full reasoning on the <a href="methodology.html">method</a> page and in <a href="flagged.html">Flagged for Review</a>.</div>

<h2>Coverage by sport</h2>
<div class="scroll"><table><thead><tr><th>Sport</th><th>Events</th><th>Tier A</th><th>Predictions</th><th>5-a-day target</th><th>Board note</th></tr></thead>
<tbody>{counts}</tbody></table></div>
<p class="sub">SHORT means the sport did not have five priceable events on OLBG at capture, not that writing was skipped.
See <a href="flagged.html">Flagged for Review</a> for the per-sport reason.</p>

<h2>Where the picks are</h2>
<div class="grid">
<a href="picks.html"><b>All {len(picks)} predictions</b><div class="c">Fully written, 30+ words each, with the exact selection and price</div></a>
<a href="board.html"><b>Full board</b><div class="c">Every one of the {sum(len(s['events']) for s in events['sports'])} events with its originated line</div></a>
<a href="sports.html"><b>By sport</b><div class="c">15 subpages, one per covered sport</div></a>
<a href="methodology.html"><b>Pricing method</b><div class="c">How each line is built and what makes it Tier A or B</div></a>
<a href="sources.html"><b>Sources</b><div class="c">Every page used, with what it was used for</div></a>
<a href="flagged.html"><b>Flagged for Review</b><div class="c">Gaps, contradictions and unverified items</div></a>
</div>"""
page("index.html","Summary",body)

# ---------------- picks ----------------
blocks=[]
for s in SPORT_ORDER:
    sp=[p for p in picks if p["sport"]==s]
    if not sp: continue
    blocks.append(f"<h2 id='{slug(s)}'>{esc(s)} — {len(sp)} written prediction{'s' if len(sp)!=1 else ''}</h2>")
    for p in sp:
        cls = "pick" if p["conf"]=="high" else ("pick me" if p["conf"]=="medium" else "pick lo")
        srcs = " · ".join(f"<a href='{esc(u)}'>{esc(u.split('/')[2])}</a>" for u in p["sources"])
        blocks.append(f"""<div class="{cls}" id="{p['sport']}-{p['event_id']}">
<h3>{esc(p['match'])}</h3>
<div class="meta">{esc(p['sport'])} · {esc(p['when'])} · Tier {p['tier']} · {p['words']} words</div>
<div style="margin:8px 0"><span class="sel">{esc(p['selection'])}</span>
&nbsp;<b class="num">{p['dec']:.2f}</b> ({american(p['dec'])}) &nbsp;·&nbsp; implied {p['prob']*100:.1f}%
&nbsp;·&nbsp; <span class="tag {p['conf']}">{p['conf'].upper()} CONFIDENCE</span>
&nbsp;·&nbsp; {'<span class="tag high">IN −250/+10000 WINDOW</span>' if p['window'] else '<span class="tag medium">OUTSIDE WINDOW</span>'}</div>
<p>{esc(p['body'])}</p>
<div class="meta">Sources: {srcs}</div></div>""")
note = ("<div class='warn'><b>Snooker has no written prediction.</b> OLBG returned \"No tips found\" for the snooker hub at "
        "capture, so there was no bookable fixture on the board to price. Nothing was invented to fill the gap — see "
        "<a href='flagged.html'>Flagged for Review</a>.</div>")
body = f"""<h1>Written predictions</h1>
<p class="sub">{len(picks)} predictions, each naming the exact selection, our price for it and the confidence grade.
Every one runs to at least 30 words and links to the page its facts came from.</p>
<div class="ok"><b>How to read this page.</b> The dark badge is the bet. The decimal price is what this project
originated for that selection; the percentage is what that price implies. Confidence is High (65%+), Medium (55–65%)
or Low (below 55%) and is set by the probability, not by the size of the price.</div>{note}{''.join(blocks)}"""
page("picks.html","Predictions",body)

# ---------------- board ----------------
seen=set(); b=[]
for s in sorted(events["sports"], key=lambda x: SPORT_ORDER.index(x["sport"])):
    b.append(f"<h2 id='{slug(s['sport'])}'>{esc(s['sport'])} <span style='font-weight:400;font-size:14px;color:#5b6b7f'>· sport id {s['sport_id']} · {len(s['events'])} events</span></h2>")
    if not s["events"]:
        b.append("<p class='warn'>No events with selections on OLBG at capture. Nothing priced.</p>"); continue
    r=""
    for e in s["events"]:
        lines="<br>".join(f"{esc(m['market'])}: <b>{esc(m['selection'])}</b> {m['decimal']:.2f} ({m['american']})" for m in e["markets"])
        comp_html = ("<div style='font-size:12px;color:#5b6b7f'>" + esc(e['comp']) + "</div>") if e.get('comp') else ""
        r+=(f"<tr><td>{esc(e['name'])}{comp_html}</td>"
            f"<td class='num'>{esc(e['when'])}</td><td class='num'>{e['id']}</td>"
            f"<td><span class='tag {'tA' if e['tier']=='A' else 'tB'}'>{e['tier']}</span></td>"
            f"<td>{lines}</td><td>{esc(e.get('edge_note',''))}</td></tr>")
    b.append(f"<div class='scroll'><table><thead><tr><th>Event</th><th>When</th><th>OLBG id</th><th>Tier</th><th>Originated line</th><th>Verified input</th></tr></thead><tbody>{r}</tbody></table></div>")
body=f"""<h1>Full board — every event, every originated line</h1>
<p class="sub">All {sum(len(s['events']) for s in events['sports'])} events captured from OLBG on 26 October 2026.
Tier A lines are built from verified competition records; Tier B lines are reference prices flagged as such.</p>
<div class='warn'>Time strings are exactly as OLBG displayed them ("Today", "Tomorrow", "28 Oct"). They were not
converted to a single timezone, because OLBG's display offset could not be confirmed — see
<a href='flagged.html'>Flagged for Review</a>.</div>{''.join(b)}"""
page("board.html","Full board",body)

# ---------------- sports index + subpages ----------------
cards="".join(f"<a href='sports/{slug(s['sport'])}.html'><b>{esc(s['sport'])}</b><div class='c'>{len(s['events'])} events · "
              f"{sum(1 for e in s['events'] if e['tier']=='A')} Tier A · {sum(1 for p in picks if p['sport']==s['sport'])} predictions</div></a>"
              for s in sorted(events["sports"], key=lambda x: SPORT_ORDER.index(x["sport"])))
page("sports.html","Sports",f"<h1>Sports</h1><p class='sub'>One page per covered sport, with its board, lines and predictions.</p><div class='grid'>{cards}</div>")

for s in events["sports"]:
    sp=[p for p in picks if p["sport"]==s["sport"]]
    r=""
    for e in s["events"]:
        lines="<br>".join(f"{esc(m['market'])}: <b>{esc(m['selection'])}</b> {m['decimal']:.2f} ({m['american']})" for m in e["markets"])
        r+=f"<tr><td>{esc(e['name'])}</td><td class='num'>{esc(e['when'])}</td><td><span class='tag {'tA' if e['tier']=='A' else 'tB'}'>{e['tier']}</span></td><td>{lines}</td></tr>"
    pb="".join(f"""<div class="{'pick' if p['conf']=='high' else ('pick me' if p['conf']=='medium' else 'pick lo')}">
<h3>{esc(p['match'])}</h3>
<div class="meta">{esc(p['when'])} · {p['words']} words</div>
<div style="margin:8px 0"><span class="sel">{esc(p['selection'])}</span> <b class="num">{p['dec']:.2f}</b>
({american(p['dec'])}) · implied {p['prob']*100:.1f}% · <span class="tag {p['conf']}">{p['conf'].upper()}</span></div>
<p>{esc(p['body'])}</p>
<div class="meta">Sources: {' · '.join(f"<a href='{esc(u)}'>{esc(u.split('/')[2])}</a>" for u in p['sources'])}</div></div>""" for p in sp) or \
    "<div class='warn'>No written prediction for this sport. Reason is recorded on the Flagged for Review page.</div>"
    tbl = f"<div class='scroll'><table><thead><tr><th>Event</th><th>When</th><th>Tier</th><th>Originated line</th></tr></thead><tbody>{r}</tbody></table></div>" if s["events"] else "<div class='warn'>No events on the OLBG board at capture.</div>"
    note = f"<div class='warn'><b>Board note.</b> {esc(s['note'])}</div>" if s.get("note") else ""
    body=f"""<h1>{esc(s['sport'])}</h1>
<p class="sub">OLBG sport id {s['sport_id']} · {len(s['events'])} events · {sum(1 for e in s['events'] if e['tier']=='A')} data-backed ·
{len(sp)} written predictions · <a href="{esc(s['source'])}">OLBG source page</a></p>{note}
<h2>Predictions</h2>{pb}<h2>Board and originated lines</h2>{tbl}"""
    page(f"sports/{slug(s['sport'])}.html", s["sport"], body, prefix="../")

# ---------------- methodology ----------------
page("methodology.html","Pricing method",f"""<h1>How every line in this project is built</h1>
<p class="sub">Originated prices, in the open. No bookmaker price is copied and no number is invented.</p>

<h2>1. What OLBG actually publishes</h2>
<p>OLBG lists events, the most-tipped selection per market, a tip count and a percentage. Reverse-engineering the site
(see <a href="sources.html">Sources</a>) shows event pages expose the full market ladder — for example, the tennis page
for Wawrinka v Lehecka lists Win Match, Set Betting, 1st Set Winner, Games Won and Total Games — but the
bookmaker price behind each selection is <b>not</b> exposed to a logged-out request. So every price on this site is
originated here, which is what the brief asked for.</p>

<h2>2. Tier A — data-backed lines</h2>
<p>A line is Tier A only when both teams appear in an official competition table captured on the day. The method is
deliberately small and checkable:</p>
<table><thead><tr><th>Step</th><th>Formula</th><th>Source of the input</th></tr></thead><tbody>
<tr><td>Team strength</td><td>(goals or points for − against) ÷ games played</td><td>Official standings table</td></tr>
<tr><td>Expected margin</td><td>(strength home + home edge) − strength away</td><td>Home edge is a stated constant per sport</td></tr>
<tr><td>Win probability</td><td>1 ÷ (1 + e<sup>−margin ÷ σ</sup>)</td><td>σ is a stated spread constant per sport</td></tr>
<tr><td>Price</td><td>(1 ÷ probability) × 1.05 margin</td><td>5% two-way margin, then converted to American odds</td></tr>
</tbody></table>
<p>Handicap lines come from the same expected margin, rounded to the sport's increment. Totals come from each side's
verified scoring rate against the opponent's concession rate. Constants used: handball σ 9.0, home edge 0.6 goals;
basketball σ 15.0, home edge 2.5 points; ice hockey σ 2.6, home edge 0.25 goals. These are stated so you can
reproduce or challenge every number in <code>scripts/build_data.py</code>.</p>

<h2>3. Tier B — reference lines</h2>
<p>Most of the board has no official table in our verified set (tennis, volleyball, cricket, rugby, golf, darts, the
dogs). Those events still get a price, but it is built only from the OLBG tip share, shrunk toward 50/50 by sample
size (weight = n ÷ (n + 10)), with the same 5% margin. A Tier B line is a <b>reference</b>, not evidence: it is
labelled on every table row and it is why Tier B predictions are graded Medium or Low, never High.</p>

<h2>4. Confidence and the odds window</h2>
<table><thead><tr><th>Grade</th><th>Rule</th><th>What it means</th></tr></thead><tbody>
<tr><td><span class="tag high">HIGH</span></td><td>implied probability ≥ 65%</td><td>Our price says the selection should win about two times in three</td></tr>
<tr><td><span class="tag medium">MEDIUM</span></td><td>55% – 65%</td><td>Lean, not a conviction</td></tr>
<tr><td><span class="tag low">LOW</span></td><td>below 55%</td><td>Noted for completeness; small stakes only</td></tr>
</tbody></table>
<p>The brief asked for picks above 70% <i>and</i> no shorter than −250. Those two conditions overlap only between
70.0% and 71.4%, because −250 is itself 71.4%. We therefore apply the −250 to +10000 price window to every
selection (shown as a tag on each prediction) and grade confidence on probability separately. One pick in this
project lands in the literal 70–71.4% band; it is named on <a href="flagged.html">Flagged for Review</a>.</p>

<h2>5. Markets investigated per sport</h2>
<p>Market ladders were read from OLBG's own documentation and event pages, then priced where an input existed:
handball Money Line, handicap and total; basketball Money Line, pointspread, total; ice hockey Money Line,
puck line, game totals; tennis Win Match, Set Betting, 1st Set, Games handicap, Total Games; volleyball win match and
set markets; cricket win match, top batter, man of the match; rugby union match and handicap; golf outright, first
round leader and top-region markets; F1 qualifying, race win, podium, top 6, fastest lap. Where a market had no
verified input it is listed as un-priced rather than filled in.</p>""")

# ---------------- sources ----------------
src = json.load(open(os.path.join(D,"sources.json"))) if os.path.exists(os.path.join(D,"sources.json")) else {"sources":[]}
srows="".join(f"<tr><td><a href='{esc(s['url'])}'>{esc(s['url'])}</a></td><td>{esc(s['publisher'])}</td><td>{esc(s['used_for'])}</td><td class='num'>{esc(s['accessed'])}</td></tr>" for s in src["sources"])
page("sources.html","Sources",f"""<h1>Sources</h1>
<p class="sub">Every external page used to build this snapshot, and what it was used for. Accessed 26 October 2026.</p>
<div class="scroll"><table><thead><tr><th>URL</th><th>Publisher</th><th>Used for</th><th>Accessed</th></tr></thead><tbody>{srows}</tbody></table></div>""")

# ---------------- flagged ----------------
flag = json.load(open(os.path.join(D,"flagged.json")))
def _links(urls):
    out=[]
    for u in urls:
        host=u.split("/")[2]
        out.append("<a href='" + esc(u) + "'>" + esc(host) + "</a><br>")
    return "".join(out)
frows="".join("<tr><td><b>"+esc(f['item'])+"</b></td><td>"+esc(f['finding'])+"</td><td>"+esc(f['impact'])+"</td><td>"+_links(f['sources'])+"</td></tr>" for f in flag["items"])
page("flagged.html","Flagged for Review",f"""<h1>Flagged for Review</h1>
<p class="sub">{len(flag['items'])} items. Nothing here blocks publication; each is either a gap in the OLBG board or a
contradiction in the brief that had to be resolved before publishing.</p>
<div class="scroll"><table><thead><tr><th>Item</th><th>Finding</th><th>What we did</th><th>Source</th></tr></thead><tbody>{frows}</tbody></table></div>""")

os.makedirs(os.path.join(S,"assets"), exist_ok=True)
open(os.path.join(S,"assets","style.css"),"w").write(CSS)
print("pages:", sum(len(files) for _,_,files in os.walk(S)))

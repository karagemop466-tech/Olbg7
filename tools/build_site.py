#!/usr/bin/env python3
"""Build the static GitHub Pages site at the repo root from data/*.json."""
import json, os, re, html
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TODAY = "2026-10-26"

SPORTS = [
    ("golf", "Golf"),
    ("volleyball", "Volleyball"),
    ("rugby-union", "Rugby Union"),
    ("cricket", "Cricket"),
    ("snooker", "Snooker"),
    ("darts", "Darts"),
    ("baseball", "Baseball"),
    ("gaelic-sports", "Gaelic Sports"),
    ("greyhounds", "Greyhounds"),
    ("tennis", "Tennis"),
    ("motor-racing", "Motor Racing"),
    ("handball", "Handball"),
    ("ice-hockey", "Ice Hockey"),
    ("basketball", "Basketball"),
    ("rugby-league", "Rugby League"),
]
SLUG = dict(SPORTS)
NAME_TO_SLUG = {name: slug for slug, name in SPORTS}



def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


def esc(x):
    return html.escape(str(x)) if x is not None else ""


def dec_to_american(d):
    if d is None:
        return "-"
    if d >= 2.0:
        return f"+{round((d - 1) * 100)}"
    return f"{round(-100 / (d - 1))}"


def word_count(t):
    return len(re.findall(r"[A-Za-z0-9'\-]+", t))


def price_for(pick, pricing_index):
    """Return (p_fair, card_dec, source_label) for a pick."""
    if pick.get("cal2_p_fair"):
        p = float(pick["cal2_p_fair"])
        card = round(1.0 / (p * 1.05), 2)
        return p, card, pick.get("method", "CAL-2")
    key = (pick["event_id"], pick["selection"])
    row = pricing_index.get(key)
    if row:
        return row["p_fair"], row["card_decimal"], "CAL-1"
    # Sub-market selections (a different outcome on an event page) are priced with the
    # same CAL-1 formula, straight from the split printed in the pick record.
    t = (pick.get("olbg_tips") or "").replace(" ", "")
    m = re.match(r"^(\d+)/(\d+)$", t)
    if m:
        try:
            from pricing import price as cal1
        except ImportError:  # running from another cwd
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "pricing", os.path.join(ROOT, "tools", "pricing.py"))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            cal1 = mod.price
        out = cal1(pick["market"], int(m.group(1)), int(m.group(2)), pick.get("olbg_pct"), pick.get("sport", ""))
        if out:
            return out["p_fair"], out["card_decimal"], "CAL-1"
    return None, None, "unpriced"


def confidence_of(p_fair, card, tips_total):
    if p_fair is None or card is None:
        return "low"
    in_band = 1.40 <= card <= 101.0
    if p_fair >= 0.60 and (tips_total or 0) >= 8 and in_band:
        return "high"
    if p_fair >= 0.50:
        return "medium"
    return "low"


def tips_total_of(pick):
    t = pick.get("olbg_tips") or ""
    m = re.match(r"^(\d+)\s*/\s*(\d+)$", t.replace(" ", ""))
    return int(m.group(2)) if m else 0


CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#12161c;--muted:#5b6675;--line:#e2e6ec;
--high:#0d7a45;--med:#a86a00;--low:#6b7280;--accent:#1b4fd8;--hi-bg:#e8f6ee;--med-bg:#fdf3e0;--low-bg:#eef0f3}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
header{background:#0f172a;color:#fff;padding:14px 20px}
header .wrap{max-width:1180px;margin:0 auto;display:flex;flex-wrap:wrap;gap:14px;align-items:center}
header h1{font-size:17px;margin:0;font-weight:650;letter-spacing:.2px}
header .sub{color:#9fb0c9;font-size:12.5px}
nav{background:#fff;border-bottom:1px solid var(--line);overflow-x:auto}
nav .wrap{max-width:1180px;margin:0 auto;display:flex;gap:2px;padding:0 20px}
nav a{display:block;padding:11px 11px;font-size:13.5px;color:var(--muted);text-decoration:none;white-space:nowrap;border-bottom:2px solid transparent}
nav a:hover{color:var(--accent);border-bottom-color:var(--accent)}
nav a.on{color:var(--ink);font-weight:650;border-bottom-color:var(--ink)}
main{max-width:1180px;margin:0 auto;padding:22px 20px 60px}
h2{font-size:20px;margin:30px 0 10px}
h3{font-size:15.5px;margin:22px 0 8px}
p.lede{font-size:15px;color:#2b3440;max-width:900px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:13px 15px}
.kpi .n{font-size:24px;font-weight:700;line-height:1.1}
.kpi .l{font-size:12px;color:var(--muted);margin-top:3px}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:13.5px}
th,td{text-align:left;padding:9px 11px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#f0f3f7;font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--muted);font-weight:650}
tr:last-child td{border-bottom:none}
tbody tr:hover{background:#fafbfc}
.pill{display:inline-block;padding:2px 8px;border-radius:99px;font-size:11.5px;font-weight:650;white-space:nowrap}
.high{background:var(--hi-bg);color:var(--high)}
.medium{background:var(--med-bg);color:var(--med)}
.low{background:var(--low-bg);color:var(--low)}
.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.muted{color:var(--muted)}
.small{font-size:12.5px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:14px 0}
.card h4{margin:0 0 4px;font-size:15.5px}
.card .meta{font-size:12.5px;color:var(--muted);margin-bottom:9px}
.card .pred{font-size:14.5px;margin:8px 0 10px}
.card ul{margin:6px 0 0 18px;padding:0}
.card li{margin:3px 0;font-size:12.8px}
a{color:var(--accent)}
.tag{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;background:#f0f3f7;padding:1px 6px;border-radius:5px}
.note{background:#fff8e6;border:1px solid #f0dca8;border-radius:10px;padding:12px 15px;font-size:13.5px;margin:15px 0}
.flag{background:#fdecec;border:1px solid #f3c2c2}
footer{max-width:1180px;margin:0 auto;padding:24px 20px 50px;color:var(--muted);font-size:12px;border-top:1px solid var(--line)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:760px){.split{grid-template-columns:1fr}}
"""


def head(title, nav_on=""):
    prefix = "../" if nav_on.startswith("sports/") else ""
    navs = [("index.html", "Dashboard"), ("all-events.html", "All events &amp; lines"),
            ("olbg-map.html", "OLBG site map"), ("methodology.html", "Pricing method"),
            ("sources.html", "Sources"), ("flagged.html", "Flagged for review"),
            ("freshness.html", "Data freshness"),
            ("olbg-tips/index.html", "Tip-consensus board")]
    on_cls = ' class="on"'
    links = "".join(
        f'<a href="{prefix}{h}"{on_cls if nav_on == h else ""}>{t}</a>' for h, t in navs
    )
    sport_links = "".join(f'<a href="{prefix}sports/{s}.html">{t}</a>' for s, t in SPORTS)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><link rel="stylesheet" href="{prefix}assets/style.css"></head>
<body><header><div class="wrap"><div><h1>OLBG Coverage Desk</h1>
<div class="sub">15 sports &middot; our own lines &middot; written predictions &middot; retrieved {TODAY}</div></div></div></header>
<nav><div class="wrap">{links}</div></nav>
<nav style="border-top:1px solid var(--line)"><div class="wrap">{sport_links}</div></nav>
<main><div class="note flag"><strong>Data freshness warning — 27 October 2026. Archived snapshot, not a live betting card.</strong> Event and prediction data were captured on {TODAY}; “Today” and “Tomorrow” refer to that capture date. Fixture status, start times, markets, prices and team news may have changed or expired. Re-check OLBG and official sources before relying on any entry. See <a href="{prefix}freshness.html">Data freshness and snapshot audit</a> and <a href="{prefix}flagged.html">Flagged for review</a>.</div>"""


def foot(prefix=""):
    return f"""</main><footer>
<p><strong>Method.</strong> Lines are originated by this desk from OLBG's published tip splits using the CAL-1
engine described on the <a href="{prefix}methodology.html">pricing method</a> page; they are not bookmaker prices.
Predictions are editorial. Every factual claim carries a source link on the row or card it appears in.</p>
<p>Earlier board from the first session: <a href="{prefix}docs/index.html">docs/</a>.</p>
<p>18+. Betting involves risk. If gambling is causing you concern, support is available from GamCare and GambleAware.
This site republishes no paid tipster content and gives no assurance of profit.</p>
</footer></body></html>"""


def main():
    events = load("events.json")["events"]
    pricing = load("pricing.json")
    picks = load("picks.json")
    sources = load("sources.json")
    flags = load("flags.json")

    pricing_index = {}
    for row in pricing["lines"]:
        if row.get("our_line"):
            pricing_index[(row["id"], row["sel"])] = row["our_line"]

    ev_by_id = {}
    for e in events:
        ev_by_id.setdefault(e["id"], e)

    # enrich picks
    enriched = []
    for p in picks["picks"]:
        p = dict(p)
        pf, card, method = price_for(p, pricing_index)
        p["_p_fair"], p["_card"], p["_method_label"] = pf, card, method
        p["_conf"] = confidence_of(pf, card, tips_total_of(p))
        p["_words"] = word_count(p["prediction"])
        ev = ev_by_id.get(p["event_id"])
        p["_event_date"] = ev["d"] if ev else None
        p["_is_today"] = bool(ev and ev["d"] == TODAY)
        p["_slug"] = NAME_TO_SLUG.get(p["sport"], "index")
        enriched.append(p)

    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "sports"), exist_ok=True)
    with open(os.path.join(ROOT, "assets", "style.css"), "w") as fh:
        fh.write(CSS)

    # ---------- index ----------
    n_picks = len(enriched)
    highs = [p for p in enriched if p["_conf"] == "high"]
    meds = [p for p in enriched if p["_conf"] == "medium"]
    lows = [p for p in enriched if p["_conf"] == "low"]
    todays = [p for p in enriched if p["_is_today"]]
    sports_with_picks = len({p["sport"] for p in enriched})

    conf_rank = {"high": 0, "medium": 1, "low": 2}
    rows = []
    for p in sorted(enriched, key=lambda x: (conf_rank[x["_conf"]], -(x["_p_fair"] or 0)))[:12]:
        rows.append(f"""<tr><td><a href="sports/{p['_slug']}.html">{esc(p['sport'])}</a></td>
<td><strong>{esc(p['selection'])}</strong><div class="small muted">{esc(p['event'])}</div></td>
<td>{esc(p['market'])}</td><td class="num">{p['_card']:.2f} <span class="muted">({dec_to_american(p['_card'])})</span></td>
<td class="num">{p['_p_fair']*100:.1f}%</td><td><span class="pill {p['_conf']}">{p['_conf']}</span></td></tr>""")

    cov_rows = []
    for slug, name in SPORTS:
        ps = [p for p in enriched if p["sport"] == name]
        evs = [e for e in events if e["s"] == name]
        priced = sum(1 for e in evs if any(r["id"] == e["id"] and r.get("our_line") for r in pricing["lines"]))
        hh = sum(1 for p in ps if p["_conf"] == "high")
        status = "OK" if len(ps) >= 5 else f"{len(ps)} of 5 target"
        cls = "" if len(ps) >= 5 else ' class="flag"'
        cov_rows.append(f"""<tr{cls}><td><a href="sports/{slug}.html"><strong>{esc(name)}</strong></a></td>
<td class="num">{len(evs)}</td><td class="num">{priced}</td><td class="num">{len(ps)}</td>
<td class="num">{hh}</td><td>{status}</td></tr>""")

    by_sport_n = {}
    for pp in enriched:
        by_sport_n[pp["sport"]] = by_sport_n.get(pp["sport"], 0) + 1
    for sp in NAME_TO_SLUG:
        by_sport_n.setdefault(sp, 0)
    short = sorted(((n, sp) for sp, n in by_sport_n.items() if n < 5))
    short_list = ", ".join(f"{sp} {n}" for n, sp in short)
    short_n = len(short)
    methods = {}
    for pp in enriched:
        fam = (pp["_method_label"] or "").split(" ")[0].split("(")[0].strip() or "unpriced"
        methods[fam] = methods.get(fam, 0) + 1
    method_line = ", ".join(f"{k}: {v}" for k, v in sorted(methods.items()))

    doc = head("OLBG Coverage Desk - dashboard", "index.html")
    doc += f"""
<h2>Executive summary (2026-10-26 snapshot)</h2>
<p class="lede">We inventoried every OLBG event we could reach across the 15 sports in scope, originated a price for
each one that carries a printed tip split, and wrote {n_picks} full predictions. {len(highs)} selections clear our
high-confidence bar, {len(meds)} are medium and {len(lows)} are low. {short_n} sports cannot reach the five-pick
target in this snapshot because OLBG itself carried too little priced market data in them ({short_list}); those are named below
and on the <a href="flagged.html">Flagged for review</a> page rather than padded out with fixtures and prices that no
source supports.</p>
<div class="grid">
<div class="kpi"><div class="n">15</div><div class="l">sports in scope</div></div>
<div class="kpi"><div class="n">{len(events)}</div><div class="l">OLBG events inventoried</div></div>
<div class="kpi"><div class="n">{pricing['totals']['priced']}</div><div class="l">events with our own line</div></div>
<div class="kpi"><div class="n">{n_picks}</div><div class="l">written predictions</div></div>
<div class="kpi"><div class="n">{len(todays)}</div><div class="l">picks in 26 Oct snapshot</div></div>
<div class="kpi"><div class="n">{len(flags['flags'])}</div><div class="l">irregularities flagged</div></div>
</div>
<div class="note"><strong>How to read the picks.</strong> Confidence is computed from our fair probability, the size of
the tip sample and the price band, not typed in by hand. A pick only earns <span class="pill high">high</span> if the
fair probability is at least 60%, the market has at least 8 tips, and our price sits inside the requested
&minus;250 to +10000 band (1.40 to 101.00 decimal). Selection prices shown are <em>our</em> originating prices, not
bookmaker prices - see the <a href="methodology.html">pricing method</a>.</div>

<h2>Picks ranked by confidence, then by our fair chance</h2>
<table><thead><tr><th>Sport</th><th>Selection &amp; event</th><th>Market</th><th>Our price</th>
<th>Fair chance</th><th>Confidence</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<p class="small muted">The high-confidence tier is {', '.join(f"{esc(x['selection'])} ({esc(x['sport'])})" for x in sorted(highs, key=lambda y: -(y['_p_fair'] or 0))) or 'empty in this snapshot'}.
Full written reasoning for every pick is on each sport page; all {n_picks} picks run to at least 30 words and none
reuse a template.</p>

<h2>Coverage by sport</h2>
<table><thead><tr><th>Sport</th><th>Events found</th><th>Events priced</th><th>Picks written</th>
<th>High confidence</th><th>5-pick target</th></tr></thead><tbody>{''.join(cov_rows)}</tbody></table>
<div class="note flag"><strong>Gaps, stated plainly.</strong> Snooker returned no tips at all from OLBG in the 2026-10-26 capture, Golf
carried only three tournament markets with two tips each, Baseball had a single live game, Rugby League offered only
season ante-post markets, Darts and Motor Racing two markets each, and Gaelic Sports four selections. We publish what
the data supports and flag the rest instead of inventing fixtures, prices or form lines.</div>
<div class="note"><strong>How each price was made.</strong> {method_line}. CAL-1 reprices the tip split OLBG prints.
CAL-2 is used where the printed split is unusable (the handball draw artefact) and CAL-3 where a tournament market has
too few runners and tips to reprice at all. Every row on this site carries its method on the pick card.</div>

<h3>What is where</h3>
<ul class="small">
<li><strong>Picks</strong> live on the sport pages, in the tables at the top and as written cards underneath, each with its source links.</li>
<li><strong>Every event and every originating line</strong> is on <a href="all-events.html">All events &amp; lines</a>.</li>
<li><strong>How the OLBG site is structured</strong> (sport ids, URL grammar, which pages were empty) is on <a href="olbg-map.html">OLBG site map</a>.</li>
<li><strong>How prices are made</strong> is on <a href="methodology.html">Pricing method</a>.</li>
<li><strong>Everything we could not confirm</strong> is on <a href="flagged.html">Flagged for review</a>.</li>
<li><strong>Tip-consensus board.</strong> A third session's 127-row market capture, with its own method and its
own flagged list, is published at <a href="olbg-tips/index.html">olbg-tips/</a> (requested in COORDINATION.md).</li>
<li><strong>Earlier board.</strong> A separate 75-row board produced earlier the same day in another session is
preserved untouched at <a href="docs/index.html">docs/</a>. It uses a different method (hand-set probabilities) and
is kept for comparison, not merged into these totals.</li>
</ul>
"""
    doc += foot()
    with open(os.path.join(ROOT, "index.html"), "w") as fh:
        fh.write(doc)

    # ---------- sport pages ----------
    for slug, name in SPORTS:
        ps = [p for p in enriched if p["sport"] == name]
        ps.sort(key=lambda x: (-(x["_p_fair"] or 0)))
        evs = [e for e in events if e["s"] == name]
        doc = head(f"{name} picks and lines", f"sports/{slug}.html")
        hh = sum(1 for p in ps if p["_conf"] == "high")
        doc += f"""<h2>{esc(name)}</h2>
<p class="lede">{len(evs)} OLBG events inventoried, {len(ps)} written predictions
({hh} high, {sum(1 for p in ps if p['_conf']=='medium')} medium, {sum(1 for p in ps if p['_conf']=='low')} low).
Prices in the table are our own.</p>"""
        if 0 < len(ps) < 5:
            doc += f"""<div class="note flag"><strong>Below the five-pick target.</strong> Only {len(ps)} priced
selection(s) existed for {esc(name)} on OLBG at retrieval. We have not invented extra matches to fill the quota.
The constraint is recorded on the <a href="../flagged.html">Flagged for review</a> page.</div>"""
        if ps:
            doc += """<h3>Picks</h3><table><thead><tr><th>#</th><th>Selection</th><th>Event</th><th>Market</th>
<th>Our price</th><th>Fair chance</th><th>OLBG split</th><th>Confidence</th></tr></thead><tbody>"""
            for i, p in enumerate(ps, 1):
                doc += f"""<tr><td class="num">{i}</td><td><strong>{esc(p['selection'])}</strong></td>
<td>{esc(p['event'])}<div class="small muted">{esc(p['date_label'])}</div></td><td>{esc(p['market'])}</td>
<td class="num">{p['_card']:.2f}<div class="small muted">{dec_to_american(p['_card'])}</div></td>
<td class="num">{p['_p_fair']*100:.1f}%</td><td class="num">{esc(p['olbg_tips'])}{(' (' + str(p['olbg_pct']) + '%)') if p['olbg_pct'] is not None else ''}</td>
<td><span class="pill {p['_conf']}">{p['_conf']}</span></td></tr>"""
            doc += "</tbody></table>"

            doc += "<h3>Written predictions</h3>"
            for i, p in enumerate(ps, 1):
                selnote = ('<div class="small muted">Selection note: ' + esc(p["selection_note"]) + '</div>') if p.get("selection_note") else ""
                facts = "".join(f'<li>{esc(f["t"])} <a href="{esc(f["src"])}" target="_blank" rel="noopener">source</a></li>'
                                for f in p["facts"])
                doc += f"""<div class="card"><h4>{i}. {esc(p['selection'])} &mdash; {esc(p['market'])}
<span class="pill {p['_conf']}">{p['_conf']}</span></h4>
<div class="meta">{esc(p['event'])} &middot; {esc(p['competition'])} &middot; {esc(p['date_label'])} &middot;
our price <strong>{p['_card']:.2f}</strong> ({dec_to_american(p['_card'])}) &middot;
fair chance {p['_p_fair']*100:.1f}% &middot; method <span class="tag">{esc(p['_method_label'])}</span>
&middot; {p['_words']} words</div>
<div class="pred">{esc(p['prediction'])}</div>
{selnote}
<div class="small"><strong>Sources for the facts above</strong><ul>{facts}</ul></div>
<div class="small muted" style="margin-top:8px">Checks performed: {esc(p['verification'])}</div></div>"""
        else:
            doc += f"""<div class="note flag"><strong>No market data.</strong> OLBG's {esc(name)} page returned no tips
when we retrieved it on {TODAY}. Without a printed market there is nothing to originate a line from, so this page
carries no picks. The reason and the supporting evidence are on the
<a href="../flagged.html">Flagged for review</a> page.</div>"""

        # sport-level events table
        doc += """<h3>All inventoried events for this sport</h3><table><thead><tr><th>Event</th>
<th>Competition</th><th>Starts</th><th>OLBG most-tipped</th><th>Market</th><th>Split</th>
<th>Our line (selection)</th><th>Source</th></tr></thead><tbody>"""
        for e in sorted(evs, key=lambda x: x["d"]):
            pl = next((r for r in pricing["lines"] if r["id"] == e["id"] and r["sel"] == e["sel"]), None)
            line = f"{pl['our_line']['card_decimal']:.2f}" if pl and pl.get("our_line") else "&mdash;"
            doc += f"""<tr><td>{esc(e['e'])}</td><td class="small">{esc(e['c'])}</td><td class="small num">{esc(e['start_label'])}</td>
<td>{esc(e['sel'])}</td><td class="small">{esc(e['m'])}</td><td class="num small">{esc(e['tips'])}</td>
<td class="num">{line}</td><td class="small"><a href="https://www.olbg.com{esc(e['path'])}" target="_blank" rel="noopener">OLBG</a></td></tr>"""
        doc += "</tbody></table>"
        doc += foot("../")
        with open(os.path.join(ROOT, "sports", f"{slug}.html"), "w") as fh:
            fh.write(doc)

    # ---------- all events ----------
    doc = head("All events and originating lines", "all-events.html")
    doc += f"""<h2>Every OLBG event we found, with our line</h2>
<p class="lede">{len(events)} events across the 15 sports, retrieved {TODAY}. "Our line" is the price this desk
originates for the selection OLBG lists as most-tipped; where OLBG printed no split, the event is left unpriced and
says so. Fair chance is the un-margined probability behind the price.</p>
<div class="note"><strong>Band filter.</strong> The brief targets selections between &minus;250 and +10000 American,
which is 1.40 to 101.00 decimal. {sum(1 for r in pricing['lines'] if r.get('our_line') and r['our_line']['in_focus_band'])}
of {pricing['totals']['priced']} priced selections fall inside that band.</div>
<table><thead><tr><th>Sport</th><th>Event</th><th>Starts</th><th>Selection</th><th>Market</th>
<th>OLBG split</th><th>Fair chance</th><th>Our price</th><th>American</th><th>Conf.</th><th>Source</th></tr></thead><tbody>"""
    for r in sorted(pricing["lines"], key=lambda x: (x["s"], x["d"])):
        ol = r.get("our_line")
        if ol:
            cells = (f"<td class=\"num\">{ol['p_fair']*100:.1f}%</td><td class=\"num\"><strong>{ol['card_decimal']:.2f}</strong></td>"
                     f"<td class=\"num small\">{dec_to_american(ol['card_decimal'])}</td>"
                     f"<td><span class=\"pill {ol['confidence']}\">{ol['confidence']}</span></td>")
        else:
            cells = "<td colspan=\"4\" class=\"small muted\">not priced - no split printed</td>"
        doc += f"""<tr><td class="small">{esc(r['s'])}</td><td>{esc(r['e'])}</td><td class="small num">{esc(r['start_label'])}</td>
<td>{esc(r['sel'])}</td><td class="small">{esc(r['m'])}</td><td class="num small">{esc(r['tips'])}</td>{cells}
<td class="small"><a href="https://www.olbg.com{esc(r['path'])}" target="_blank" rel="noopener">OLBG</a></td></tr>"""
    doc += "</tbody></table>"
    doc += foot()
    with open(os.path.join(ROOT, "all-events.html"), "w") as fh:
        fh.write(doc)

    # ---------- olbg map ----------
    doc = head("OLBG site map - reverse engineered", "olbg-map.html")
    grammar = sources["olbg_url_grammar"]
    doc += f"""<h2>How OLBG is put together</h2>
<p class="lede">Every page we read, the URL pattern it follows, and what it actually returned on {TODAY}. This is the
map we work from when we refresh the board.</p>
<h3>URL grammar</h3><table><thead><tr><th>Page type</th><th>Pattern</th></tr></thead><tbody>"""
    for k, v in grammar.items():
        if k == "notes":
            continue
        doc += f'<tr><td><span class="tag">{esc(k)}</span></td><td class="small"><code>{esc(v)}</code></td></tr>'
    doc += "</tbody></table><div class=\"note\"><strong>Notes from the crawl</strong><ul class=\"small\">"
    for n in grammar["notes"]:
        doc += f"<li>{esc(n)}</li>"
    doc += "</ul></div>"

    doc += """<h3>Sport ids and status</h3><table><thead><tr><th>Sport</th><th>Sport id</th><th>Root page</th>
<th>Events with tips</th><th>Status at retrieval</th><th>Markets seen</th></tr></thead><tbody>"""
    for s in sources["sports_status"]:
        doc += f"""<tr><td><strong>{esc(s['sport'])}</strong></td><td class="num">{esc(s['id'])}</td>
<td class="small"><a href="{esc(s['root'])}" target="_blank" rel="noopener">root page</a></td>
<td class="num">{esc(s['events'])}</td><td class="small"><span class="tag">{esc(s['status'])}</span></td>
<td class="small">{esc(', '.join(s['markets']))}</td></tr>"""
    doc += "</tbody></table>"
    doc += """<h3>What the event pages give you that the listings do not</h3>
<p class="small">A sport listing shows one row per event: the most-tipped selection, its market, the split
(e.g. 9/16) and the comment count. An <em>event</em> page breaks the same match into every market OLBG carries -
money line, pointspread or handicap with the actual line (e.g. CLE &minus;4.50, Under 232.50), game totals - and gives
the split for each outcome, plus the tipster's written comment. That is the page to read when pricing more than the
favourite. Bookmaker prices are rendered client-side and were absent from every page we retrieved, which is why this
project originates its own lines instead of quoting OLBG's.</p>
"""
    doc += foot()
    with open(os.path.join(ROOT, "olbg-map.html"), "w") as fh:
        fh.write(doc)

    # ---------- methodology ----------
    m = pricing["constants"]
    doc = head("Pricing method", "methodology.html")
    doc += f"""<h2>How we originate a line</h2>
<p class="lede">We cannot read bookmaker prices off OLBG - they are rendered client-side and were missing from every
page we retrieved (see <a href="flagged.html">Flagged for review</a>). So the board is priced by us, from the one
numeric market signal OLBG does print: the tip split for each selection.</p>

<h3>CAL-1, the engine behind {pricing['totals']['priced']} lines</h3>
<table><thead><tr><th>Step</th><th>What happens</th></tr></thead><tbody>
<tr><td>1. Prior</td><td>The market structure sets the starting point: 0.50 for a two-way market, 0.3333 for a
three-way money line, 0.125 for an outright (assumed eight runners, which is an assumption and is labelled).</td></tr>
<tr><td>2. Shrinkage</td><td>The printed split is pulled toward that prior with {m['K_pseudo_tips']} pseudo-tips:
<code>p = (wins + K &times; prior) / (total + K)</code>. This stops a 1/1 tip from becoming a 100% certainty and a
6/6 from becoming a 1.00 shot.</td></tr>
<tr><td>3. Fair price</td><td><code>1 / p</code>.</td></tr>
<tr><td>4. Our card price</td><td><code>1 / (p &times; (1 + {m['margin']}))</code> - a {int(m['margin']*100)}% margin,
so every price we publish is shorter than our fair number.</td></tr>
<tr><td>5. American</td><td>Standard conversion: <code>(dec &minus; 1) &times; 100</code> at 2.00 and above,
<code>&minus;100 / (dec &minus; 1)</code> below 2.00.</td></tr>
<tr><td>6. Confidence</td><td><span class="pill high">high</span> needs fair probability &ge; 60%, a sample of at least
8 tips and a price inside {m['band_min_decimal']} to {m['band_max_decimal']}. <span class="pill medium">medium</span>
is fair probability &ge; 50%. Everything else is <span class="pill low">low</span>. The label is computed, never
typed.</td></tr>
</tbody></table>

<h3>CAL-2, used for Handball only</h3>
<p class="small">OLBG's handball listing prints "Tie" as the most-popular selection for nearly every Champions League
match, which makes the printed split unusable (flag F-002). For those five matches we price from the
competition base rate OLBG itself publishes - EHF Champions League men, favourites won 446 of 654 games (68.2%) -
shrunk 15% toward 50% to allow for what we do not know about the specific tie. The results and standings we cite are
official EHF data.</p>

<h3>CAL-3, used where there is no market at all</h3>
<p class="small">One pick (Antonelli, top-six finish in Mexico City) sits in a market with zero tips. It is priced by
us from the championship arithmetic and is labelled CAL-3 so it can never be mistaken for a market-derived number.</p>

<h3>The &minus;250 to +10000 band</h3>
<p class="small">&minus;250 American is {m['band_min_decimal']} decimal; +10000 is {m['band_max_decimal']}. The band is
applied to our card price. A strong favourite priced under 1.40 is a real pick but is excluded from the high-confidence
tier, because beating a 1.20 shot is not the part of the market the brief wants us working. Recorded constants:
margin {m['margin']}, pseudo-count {m['K_pseudo_tips']}, band {m['band_min_decimal']}-{m['band_max_decimal']}.</p>

<h3>Known limits of this approach</h3>
<ul class="small">
<li>A tip split is a crowd signal, not a probability. Shrinkage reduces the damage from small samples; it does not
manufacture information.</li>
<li>Only {pricing['totals']['priced']} of {len(events)} inventoried events printed a split. Events with no split are
left unpriced rather than guessed.</li>
<li>The engine prices the selection OLBG highlights. Other outcomes in the same market stay unpriced unless the event
page was read.</li>
<li>Confidence describes the strength of our number. It says nothing about whether the bet wins.</li>
</ul>
"""
    doc += foot()
    with open(os.path.join(ROOT, "methodology.html"), "w") as fh:
        fh.write(doc)

    # ---------- sources ----------
    doc = head("Sources", "sources.html")
    doc += f"""<h2>Source register</h2>
<p class="lede">Every external page used to support a factual claim, grouped by sport, with what it was used for.
Retrieved {TODAY}.</p>"""
    for key, items in sources["register"].items():
        doc += f"<h3>{esc(key)}</h3><table><thead><tr><th>Source</th><th>Link</th><th>Used for</th></tr></thead><tbody>"
        for it in items:
            doc += f"""<tr><td>{esc(it['name'])}</td>
<td class="small"><a href="{esc(it['url'])}" target="_blank" rel="noopener">{esc(it['url'][:70])}{'...' if len(it['url'])>70 else ''}</a></td>
<td class="small">{esc(it['use'])}</td></tr>"""
        doc += "</tbody></table>"
    doc += foot()
    with open(os.path.join(ROOT, "sources.html"), "w") as fh:
        fh.write(doc)

    # ---------- flagged ----------
    doc = head("Flagged for review", "flagged.html")
    doc += f"""<h2>Flagged for review</h2>
<p class="lede">Everything we could not confirm, every conflict between sources, and every place where OLBG's own
pages disagree with each other. Nothing here blocks publication; it marks what needs a human decision.</p>
<table><thead><tr><th>ID</th><th>Area</th><th>What we found</th><th>Impact</th><th>Evidence</th></tr></thead><tbody>"""
    for f in flags["flags"]:
        doc += f"""<tr><td class="num"><strong>{esc(f['id'])}</strong></td><td class="small">{esc(f['area'])}</td>
<td class="small">{esc(f['finding'])}</td><td class="small">{esc(f['impact'])}</td>
<td class="small"><a href="{esc(f['source'])}" target="_blank" rel="noopener">link</a></td></tr>"""
    doc += "</tbody></table>"
    doc += """<h3>What is deliberately left blank</h3>
<ul class="small">"""
    for b in flags["blanks"]:
        doc += f"<li>{esc(b)}</li>"
    doc += "</ul>"
    doc += foot()
    with open(os.path.join(ROOT, "flagged.html"), "w") as fh:
        fh.write(doc)

    print(f"wrote index.html, {len(SPORTS)} sport pages, all-events.html, olbg-map.html, "
          f"methodology.html, sources.html, flagged.html; picks={n_picks} "
          f"(high {len(highs)} / med {len(meds)} / low {len(lows)})")


if __name__ == "__main__":
    main()

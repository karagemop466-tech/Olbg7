#!/usr/bin/env python3
"""Build the static dashboard from data/*.json into docs/."""
import html
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "consensus"
# GitHub Pages for this repository is pinned to the repo root of `main`, so the
# generated pages are written there. Set SITE_OUT to build elsewhere.
DOCS = pathlib.Path(os.environ.get("SITE_OUT", ROOT)).resolve()

SLUG = {
    "Golf": "golf",
    "Volleyball": "volleyball",
    "Rugby Union": "rugby-union",
    "Cricket": "cricket",
    "Snooker": "snooker",
    "Darts": "darts",
    "Baseball": "baseball",
    "Gaelic Sports": "gaelic-sports",
    "Greyhounds": "greyhounds",
    "Tennis": "tennis",
    "Motor Racing": "motor-racing",
    "Handball": "handball",
    "Ice Hockey": "ice-hockey",
    "Basketball": "basketball",
    "Rugby League": "rugby-league",
}
SPORT_ORDER = list(SLUG)
CONF_ORDER = {"high": 0, "medium": 1, "low": 2, "none": 3}

CSS = """
:root{--bg:#0f1420;--card:#171e2e;--card2:#1d2637;--line:#2a3548;--txt:#e7ecf5;--dim:#9aa8c0;
--hi:#22c55e;--med:#eab308;--lo:#64748b;--accent:#38bdf8;--warn:#f97316}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
header.top{background:linear-gradient(180deg,#131a28,#101725);border-bottom:1px solid var(--line);padding:18px 20px 10px}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
h1{font-size:26px;margin:0 0 4px}
h2{font-size:19px;margin:34px 0 10px}
h3{font-size:15px;margin:0 0 6px}
.sub{color:var(--dim);font-size:13px}
nav.sports{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 4px}
nav.sports a{background:var(--card2);border:1px solid var(--line);border-radius:999px;padding:4px 11px;font-size:12.5px;color:var(--txt)}
nav.sports a.on{background:#22344d;border-color:#3b5b82;color:#cfe8ff}
nav.sports a.alt{background:transparent;color:var(--accent)}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:13.5px}
th{background:var(--card2);text-align:left;padding:9px 10px;font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--dim);border-bottom:1px solid var(--line);white-space:nowrap}
td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:none}
tbody tr:hover{background:#1b2434}
.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.badge{display:inline-block;padding:1px 8px;border-radius:999px;font-size:11px;font-weight:600;letter-spacing:.03em;text-transform:uppercase}
.b-high{background:rgba(34,197,94,.16);color:var(--hi);border:1px solid rgba(34,197,94,.45)}
.b-medium{background:rgba(234,179,8,.14);color:var(--med);border:1px solid rgba(234,179,8,.45)}
.b-low{background:rgba(100,116,139,.16);color:#a9b7cd;border:1px solid rgba(100,116,139,.5)}
.b-none{background:rgba(249,115,22,.12);color:var(--warn);border:1px solid rgba(249,115,22,.45)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:16px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.kpi .v{font-size:24px;font-weight:700}
.kpi .l{color:var(--dim);font-size:12px;text-transform:uppercase;letter-spacing:.05em}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:12px 0}
.card .pick{font-weight:700;font-size:15px;margin-bottom:4px}
.card p{margin:6px 0}
.meta{color:var(--dim);font-size:12.5px}
ul.facts{margin:8px 0 0;padding-left:18px;font-size:12.5px;color:#c6d2e6}
ul.facts li{margin:2px 0}
.note{border-left:3px solid var(--warn);background:rgba(249,115,22,.07);padding:10px 12px;border-radius:0 8px 8px 0;margin:12px 0;font-size:13.5px}
.ok{border-left:3px solid var(--hi);background:rgba(34,197,94,.07);padding:10px 12px;border-radius:0 8px 8px 0;margin:12px 0;font-size:13.5px}
.scroll{overflow-x:auto;border-radius:10px}
footer{color:var(--dim);font-size:12.5px;border-top:1px solid var(--line);margin-top:40px;padding:18px 0 40px}
.tag{font-size:11px;color:var(--dim);border:1px solid var(--line);border-radius:5px;padding:1px 6px;margin-left:6px}
"""


def esc(x):
    return html.escape("" if x is None else str(x))


def nav(active=""):
    items = [("Executive summary", "index.html", ""), ("All lines", "lines.html", ""),
             ("Method", "method.html", ""), ("Flagged for review", "flagged.html", "alt")]
    out = ['<nav class="sports">']
    for label, href, cls in items:
        on = " on" if href == active else ""
        out.append(f'<a class="{cls}{on}" href="{href}">{label}</a>')
    out.append("</nav>")
    out.append('<nav class="sports">')
    for s in SPORT_ORDER:
        on = " on" if SLUG[s] + ".html" == active else ""
        out.append(f'<a class="{on}" href="{SLUG[s]}.html">{esc(s)}</a>')
    out.append("</nav>")
    return "".join(out)


def page(title, active, body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="Originated prices, picks and written predictions for the sports covered on OLBG. Snapshot 2026-10-26.">
<style>{CSS}</style></head>
<body>
<header class="top"><div class="wrap">
<h1>{esc(title)}</h1>
<div class="sub">Snapshot taken from OLBG on 2026-10-26 &middot; prices are our own originated lines, not quotes from a bookmaker &middot; 18+, please gamble responsibly</div>
{nav(active)}
</div></header>
<main class="wrap">
{body}
</main>
<footer class="wrap">
Every market row links to the OLBG page it came from. Form numbers are only stated where an official league page was read
(<a href="https://www.nhl.com/standings">NHL.com</a>, <a href="https://www.nba.com/standings">NBA.com</a>); everything else is
attributed to OLBG's published tip counts. Unconfirmed fields are left blank and listed on the
<a href="flagged.html">Flagged for review</a> page. This board is the tip-consensus view; the
<a href="../docs/index.html">primary board</a> covers the same sports with tournament-source pricing. Our prices are analytical output, not a bookmaker offer.
</footer>
</body></html>"""


def price_cell(row):
    if row["price_american"] is None:
        return '<span class="meta">not priced</span>'
    p = row["probability"] * 100
    return f'<span class="num">{esc(row["price_american"])}</span><br><span class="meta">{p:.1f}% &middot; {row["price_decimal"]:.2f} dec</span>'


def conf_badge(c):
    return f'<span class="badge b-{c}">{c}</span>'


def tips_cell(row):
    if row["tips"] is None:
        return '<span class="meta">no tip count published</span>'
    return f'<span class="num">{row["tips"]}/{row["total"]}</span><br><span class="meta">{row["pct"]}% share</span>'


def main():
    events = json.loads((DATA / "events.json").read_text())
    lines = json.loads((DATA / "lines.json").read_text())
    picks = json.loads((DATA / "picks.json").read_text())
    preds = json.loads((DATA / "predictions.json").read_text())

    all_picks = picks["picks"]
    pred = preds["picks"]
    status = preds["sport_status"]
    events_per_sport = {}
    for ev in events["events"]:
        events_per_sport[ev["sport"]] = events_per_sport.get(ev["sport"], 0) + 1

    DOCS.mkdir(parents=True, exist_ok=True)
    # remove only pages this script owns - never the repository itself
    owned = ["index.html", "lines.html", "method.html", "flagged.html"] + [SLUG[s] + ".html" for s in SPORT_ORDER]
    for name in owned:
        target = DOCS / name
        if target.exists():
            target.unlink()

    # ---------------- index ----------------
    highs = [p for p in all_picks if p["confidence"] == "high"]
    meds = [p for p in all_picks if p["confidence"] == "medium"]
    b = []
    b.append('<div class="grid">')
    b.append(f'<div class="kpi"><div class="v">{len(events_per_sport)}</div><div class="l">sports covered</div></div>')
    b.append(f'<div class="kpi"><div class="v">{len(events["events"])}</div><div class="l">events captured</div></div>')
    b.append(f'<div class="kpi"><div class="v">{lines["count"]}</div><div class="l">markets priced</div></div>')
    b.append(f'<div class="kpi"><div class="v">{len(all_picks)}</div><div class="l">picks published</div></div>')
    b.append(f'<div class="kpi"><div class="v">{len(highs)}</div><div class="l">high confidence</div></div>')
    b.append('</div>')
    b.append('<div class="note"><b>Historical snapshot — 26 October 2026.</b> This market and fixture capture has not been refreshed for the current date. Do not treat its listed selections, times or availability as current or actionable; events may have started or markets may have changed. See <a href="flagged.html">Flagged for review</a> for known data limitations.</div>')

    b.append('<h2>Executive summary</h2>')
    b.append(f'<div class="ok"><b>Executive summary.</b> {len(highs)} picks meet the strict high-confidence bar '
             '(estimated chance greater than 70%, at least eight market tips, and odds within -250 to +10000). '
             'No picks are promoted to high when the available support falls short. The ranked picks below show the '
             'best-supported available selections; sport-level gaps are stated rather than padded out.</div>')

    b.append('<h2>High-confidence picks (odds between -250 and +10000)</h2>')
    b.append('<p class="sub">Ranked by confidence, then by estimated probability. Every row links to the OLBG event page it came from.</p>')
    b.append('<div class="scroll"><table><thead><tr><th>#</th><th>Sport</th><th>Match / event</th><th>When</th>'
             '<th>Pick</th><th>Market</th><th>Our price</th><th>OLBG tips</th><th>Conf.</th><th>Source</th></tr></thead><tbody>')
    for i, p in enumerate(highs, 1):
        b.append(f'<tr><td class="num">{i}</td><td>{esc(p["sport"])}</td>'
                 f'<td><a href="{SLUG[p["sport"]]}.html">{esc(p["event"])}</a></td><td class="num">{esc(p["start"])}</td>'
                 f'<td><b>{esc(p["selection"])}</b></td><td>{esc(p["market"])}</td><td>{price_cell(p)}</td>'
                 f'<td>{tips_cell(p)}</td><td>{conf_badge(p["confidence"])}</td>'
                 f'<td><a href="{esc(p["url"])}" rel="nofollow">OLBG</a></td></tr>')
    b.append('</tbody></table></div>')

    b.append('<h2>Next tier: medium-confidence picks</h2>')
    b.append('<div class="scroll"><table><thead><tr><th>Sport</th><th>Match / event</th><th>When</th><th>Pick</th>'
             '<th>Market</th><th>Our price</th><th>OLBG tips</th><th>Conf.</th><th>Source</th></tr></thead><tbody>')
    for p in meds:
        b.append(f'<tr><td>{esc(p["sport"])}</td><td><a href="{SLUG[p["sport"]]}.html">{esc(p["event"])}</a></td>'
                 f'<td class="num">{esc(p["start"])}</td><td><b>{esc(p["selection"])}</b></td><td>{esc(p["market"])}</td>'
                 f'<td>{price_cell(p)}</td><td>{tips_cell(p)}</td><td>{conf_badge(p["confidence"])}</td>'
                 f'<td><a href="{esc(p["url"])}" rel="nofollow">OLBG</a></td></tr>')
    b.append('</tbody></table></div>')

    b.append('<h2>Coverage by sport</h2>')
    b.append('<p class="sub">“Events on OLBG” counts the fixtures or markets actually listed on the snapshot date. '
             'Where picks are fewer than five, the reason is stated — no pick was invented to fill a row.</p>')
    b.append('<div class="scroll"><table><thead><tr><th>Sport</th><th>Events on OLBG</th><th>Picks published</th>'
             '<th>High</th><th>Status</th><th>Why the card is short</th></tr></thead><tbody>')
    for s in SPORT_ORDER:
        st = status.get(s, {})
        sp = [p for p in all_picks if p["sport"] == s]
        nh = len([p for p in sp if p["confidence"] == "high"])
        stt = st.get("status", "")
        cls = {"ok": "b-high", "shortfall": "b-medium", "flagged": "b-none", "no_data": "b-none", "no_matches": "b-none"}.get(stt, "b-low")
        b.append(f'<tr><td><a href="{SLUG[s]}.html"><b>{esc(s)}</b></a></td><td class="num">{events_per_sport.get(s,0)}</td>'
                 f'<td class="num">{len(sp)}</td><td class="num">{nh}</td>'
                 f'<td><span class="badge {cls}">{esc(stt.replace("_"," "))}</span></td>'
                 f'<td class="meta">{esc(st.get("reason",""))}</td></tr>')
    b.append('</tbody></table></div>')

    b.append('<h2>How to read this site</h2>')
    b.append('<div class="card"><p><b>1. Picks are the bold selection in each table.</b> The “Pick” column is the bet; '
             'market and price sit next to it. Each sport page repeats its picks at the top, then prints the full '
             'written prediction underneath.</p>'
             '<p><b>2. Prices in this site are ours.</b> OLBG does not publish decimal odds for most of these markets, so '
             'we originate a price from the share of tips on each selection, shrunk towards the market\'s base rate. '
             'The arithmetic is on the <a href="method.html">Method</a> page and in scripts/price_model.py.</p>'
             '<p><b>3. Confidence is a data-quality label, not a promise.</b> High needs at least eight tips on the '
             'market and an estimated chance greater than 70%. Single-tip “100%” selections are never high.</p>'
             '<p><b>4. Everything unresolved is on <a href="flagged.html">Flagged for review</a></b> with source links.</p></div>')

    (DOCS / "index.html").write_text(page(
        "OLBG tip-consensus board — snapshot 26 October 2026", "index.html", "\n".join(b)))

    # ---------------- sport pages ----------------
    lines_by_sport = {}
    for r in lines["lines"]:
        lines_by_sport.setdefault(r["sport"], []).append(r)

    for s in SPORT_ORDER:
        st = status.get(s, {})
        sp = [p for p in all_picks if p["sport"] == s]
        sp.sort(key=lambda r: (CONF_ORDER[r["confidence"]], -r["probability"]))
        b = []
        b.append(f'<p class="sub">OLBG source: <a href="{esc([x for x in events["sports"] if x["name"]==s][0]["olbg_url"])}" rel="nofollow">'
                 f'OLBG {esc(s)} page</a></p>')
        b.append(f'<div class="grid"><div class="kpi"><div class="v">{events_per_sport.get(s,0)}</div><div class="l">events listed on OLBG</div></div>'
                 f'<div class="kpi"><div class="v">{len(sp)}</div><div class="l">picks published</div></div>'
                 f'<div class="kpi"><div class="v">{len([p for p in sp if p["confidence"]=="high"])}</div><div class="l">high confidence</div></div>'
                 f'<div class="kpi"><div class="v">{len(lines_by_sport.get(s,[]))}</div><div class="l">markets priced</div></div></div>')

        if st.get("reason"):
            cls = "ok" if st.get("status") == "ok" else "note"
            extra = ""
            if s in ("Rugby League", "Snooker"):
                extra = (' Fixtures for this sport that OLBG lists without any tip counts are priced on the '
                         f'<a href="../docs/{SLUG[s]}.html">primary board</a>.')
            b.append(f'<div class="{cls}"><b>Coverage note.</b> {esc(st["reason"])}{extra}</div>')

        if not sp:
            b.append('<h2>No picks for this sport</h2>')
            b.append('<div class="note">There is nothing here to price from tip consensus: OLBG returned <b>“No tips found.”</b> '
                     'on its snooker tips page on 2026-10-26, so no tip counts exist to originate a line from. Snooker fixtures '
                     'do exist and are covered on the <a href="../docs/snooker.html">primary board</a>, which prices them from '
                     'tournament sources instead. This gap is logged on the <a href="flagged.html">Flagged for review</a> page.</div>')
        else:
            b.append('<h2>Picks — what to back</h2>')
            b.append('<p class="sub">The <b>Pick</b> column is the selection. Prices are ours, implied chance is shown '
                     'under the price, and the last column opens the OLBG page for that event.</p>')
            b.append('<div class="scroll"><table><thead><tr><th>#</th><th>Match / event</th><th>Competition</th><th>When</th>'
                     '<th>Pick</th><th>Market</th><th>Our price</th><th>OLBG tips</th><th>Conf.</th><th>Source</th></tr></thead><tbody>')
            for i, p in enumerate(sp, 1):
                b.append(f'<tr><td class="num">{i}</td><td><b>{esc(p["event"])}</b></td><td>{esc(p["competition"]) or "<span class=meta>not published</span>"}</td>'
                         f'<td class="num">{esc(p["start"])}</td><td><b>{esc(p["selection"])}</b></td><td>{esc(p["market"])}</td>'
                         f'<td>{price_cell(p)}</td><td>{tips_cell(p)}</td><td>{conf_badge(p["confidence"])}</td>'
                         f'<td><a href="{esc(p["url"])}" rel="nofollow">OLBG</a></td></tr>')
            b.append('</tbody></table></div>')

            b.append('<h2>Written predictions</h2>')
            for i, p in enumerate(sp, 1):
                pr = pred.get(p["event_id"], {})
                b.append('<div class="card">')
                b.append(f'<div class="pick">{i}. {esc(pr.get("headline") or p["selection"])} {conf_badge(p["confidence"])}</div>')
                b.append(f'<div class="meta">{esc(p["event"])} &middot; {esc(p["start"])} &middot; market: {esc(p["market"])} '
                         f'&middot; our price {esc(p["price_american"])} ({p["probability"]*100:.1f}% implied) &middot; '
                         f'OLBG tips {p["tips"]}/{p["total"]} ({p["pct"]}%)</div>')
                b.append(f'<p>{esc(pr.get("text",""))}</p>')
                facts = pr.get("facts", [])
                if facts:
                    b.append('<ul class="facts">')
                    for f in facts:
                        b.append(f'<li>{esc(f["claim"])} — <a href="{esc(f["source"])}" rel="nofollow">{esc(f["source"].split("//")[-1][:64])}</a></li>')
                    b.append('</ul>')
                if pr.get("not_checked"):
                    b.append(f'<p class="meta"><b>Not checked:</b> {esc(pr["not_checked"])}</p>')
                if pr.get("evidence") == "form-checked":
                    b.append('<p class="meta">Form figures in this prediction were read from the official league standings listed above.</p>')
                b.append('</div>')

        rows = sorted(lines_by_sport.get(s, []), key=lambda r: (r["event"], -r["probability"] if r["probability"] else 0))
        if rows:
            b.append('<h2>Every market we priced for this sport</h2>')
            b.append('<p class="sub">Including rows that were priced but rejected — outside the -250/+10000 band, no published '
                     'tip count, or a flagged market anomaly. Nothing is hidden.</p>')
            b.append('<div class="scroll"><table><thead><tr><th>Match / event</th><th>When</th><th>Market</th><th>Selection</th>'
                     '<th>OLBG tips</th><th>Our price</th><th>Implied</th><th>Conf.</th><th>Status</th><th>Source</th></tr></thead><tbody>')
            for r in rows:
                if r["price_american"]:
                    imp = f'{r["probability"]*100:.1f}%'
                else:
                    imp = '<span class="meta">—</span>'
                stat = ('<span class="badge b-none">flagged</span>' if (r["excluded"] and "anomaly" in (r["excluded"] or "")) else
                        ('<span class="badge b-low">not in band</span>' if r["excluded"] else '<span class="badge b-high">eligible</span>'))
                b.append(f'<tr><td>{esc(r["event"])}</td><td class="num">{esc(r["start"])}</td><td>{esc(r["market"])}</td>'
                         f'<td>{esc(r["selection"])}</td><td>{tips_cell(r)}</td><td>{price_cell(r)}</td>'
                         f'<td class="num">{imp}</td><td>{conf_badge(r["confidence"])}</td>'
                         f'<td>{stat}<br><span class="meta">{esc(r["excluded"] or "")}</span></td>'
                         f'<td><a href="{esc(r["url"])}" rel="nofollow">OLBG</a></td></tr>')
            b.append('</tbody></table></div>')

        (DOCS / (SLUG[s] + ".html")).write_text(page(f"{s} — picks and predictions", SLUG[s] + ".html", "\n".join(b)))

    # ---------------- all lines ----------------
    b = ['<p class="sub">All 127 market rows captured, priced with the same method. Sorted by sport, then event.</p>',
         '<div class="scroll"><table><thead><tr><th>Sport</th><th>Match / event</th><th>When</th><th>Market</th>'
         '<th>Selection</th><th>OLBG tips</th><th>Our price</th><th>Implied</th><th>Conf.</th><th>Status</th><th>Source</th></tr></thead><tbody>']
    for r in sorted(lines["lines"], key=lambda x: (SPORT_ORDER.index(x["sport"]), x["event"])):
        imp = f'{r["probability"]*100:.1f}%' if r["probability"] else '<span class="meta">—</span>'
        stat = ('<span class="badge b-none">flagged</span>' if (r["excluded"] and "anomaly" in (r["excluded"] or "")) else
                ('<span class="badge b-low">not in band</span>' if r["excluded"] else '<span class="badge b-high">eligible</span>'))
        b.append(f'<tr><td>{esc(r["sport"])}</td><td>{esc(r["event"])}</td><td class="num">{esc(r["start"])}</td>'
                 f'<td>{esc(r["market"])}</td><td>{esc(r["selection"])}</td><td>{tips_cell(r)}</td><td>{price_cell(r)}</td>'
                 f'<td class="num">{imp}</td><td>{conf_badge(r["confidence"])}</td>'
                 f'<td>{stat}<br><span class="meta">{esc(r["excluded"] or "")}</span></td>'
                 f'<td><a href="{esc(r["url"])}" rel="nofollow">OLBG</a></td></tr>')
    b.append('</tbody></table></div>')
    (DOCS / "lines.html").write_text(page("All originated lines", "lines.html", "\n".join(b)))

    # ---------------- method ----------------
    m = lines["method"]
    b = [f'''<h2>What this site does</h2>
<div class="card"><p>We read OLBG's own tip pages for fifteen sports, record every selection that carries tips, and then
originate our own price for each selection. A price is turned into a pick, a confidence label and — for every pick — a
written prediction of at least thirty words.</p>
<p>OLBG does not publish decimal odds for most of these markets. It publishes how many tipsters backed a selection out of
all tips on that market. That share is the only market input we have, so the method below is built around it.</p></div>

<h2>Pricing method</h2>
<div class="card">
<p><b>Step 1 — tip share.</b> <code>s = tips / total</code>. A share is not a probability: 1 of 1 is a 100% share and
nowhere near a 100% chance.</p>
<p><b>Step 2 — shrink to the base rate.</b> Each market has a number of possible outcomes <code>n_out</code>, so the base
rate is <code>b = 1 / n_out</code>. With <code>n</code> tips on the market and <code>K = {m["pseudo_tips_K"]}</code>:</p>
<p style="text-align:center"><code>w = n / (n + K)</code> &nbsp;&nbsp; <code>p = w·s + (1 − w)·b</code></p>
<p>One tip moves the price by roughly a tenth of the way to the base rate; forty tips move it by four fifths.</p>
<p><b>Step 3 — price with a margin.</b> We quote a decimal price of <code>{1 - m["overround"]/2:.3f} / p</code>, i.e. a
{m["overround"]*100:.0f}% theoretical overround split between the two sides. American odds are derived from that.</p>
<p><b>Step 4 — odds band.</b> Picks must price between <b>−250</b> (decimal 1.40) and <b>+10000</b> (decimal 101). Rows
outside the band are still priced and shown, marked “not in band”.</p>
<p><b>Step 5 — confidence.</b> <span class="badge b-high">high</span> needs {m["confidence_rules"]["high"]};
<span class="badge b-medium">medium</span> needs {m["confidence_rules"]["medium"]};
<span class="badge b-low">low</span> is everything else. A single tipster on a 100% share can never be high.</p>
<p><b>Step 6 — one pick per event.</b> The eligible row with the highest modelled probability wins the event, breaking ties
on tip count and then on market type (match winner, then handicap, then total). Each sport's card is the five
highest-confidence events; where fewer than five exist, the site says so.</p>
</div>

<h2>Model inputs that are assumptions, not facts</h2>
<div class="card"><p>The number of outcomes in a market is an input we set. For two-team markets it is two; for a
ninety-minute handball line three; for a Test match three (two sides plus the draw). For outright markets we use the size
of the field: 32 for the All-Ireland football, 12 for hurling, 12 for Super League, 17 for the NRL, 2 for State of Origin,
6 for the Six Nations, 96 for the PDC World Championship, 128 for a Players Championship, 21 for the F1 drivers' title,
14 for the cricket World Cup, 8 for the WBBL, and 70 for each golf tournament (the Mexico Open page listed more than
eighty golfers; the other two fields were not published, so 70 is an assumption and is flagged).
Greyhound races are treated as six-dog races.</p></div>

<h2>What was checked, and what was not</h2>
<div class="card"><p><b>Checked against an official source:</b> NHL standings for every hockey pick
(<a href="https://www.nhl.com/standings">NHL.com</a>, page dated 26 October 2026) and NBA standings for every basketball
pick (<a href="https://www.nba.com/standings">NBA.com</a>, 2026-27 regular season). Those are the only official form
numbers in the output.</p>
<p><b>Not checked, therefore never claimed:</b> injuries, line-ups, team news, weather, travel, rest days, head-to-head
records, player rankings and cricket series context. The ATP rankings page and the ICC team rankings page were both
requested and both rendered without a data table, and the European league sites could not be read from here, so those
fields stay empty rather than guess. Each prediction names what it could not check.</p>
<p><b>Tipster comments are opinions.</b> We do not repeat them as fact — one captured comment on the Dallas/Miami game
credits Miami with Giannis Antetokounmpo, who plays for Milwaukee. That error is logged on the flagged page.</p></div>

<h2>Files</h2>
<div class="card"><p><code>data/events.json</code> — every captured market row with its OLBG link.<br>
<code>data/lines.json</code> — the same rows after pricing.<br>
<code>data/picks.json</code> — one pick per event, five per sport where available.<br>
<code>data/predictions.json</code> — the written predictions and their fact links.<br>
<code>scripts/price_model.py</code> — the model above, in code.<br>
<code>scripts/build_site.py</code> — this site.<br>
<code>COORDINATION.md</code> — task board, sources, verification log.</p></div>''']
    (DOCS / "method.html").write_text(page("Method — how the lines and labels are built", "method.html", "\n".join(b)))

    # ---------------- flagged ----------------
    flags = [
        ("Snooker has no tips at all", "The snooker page returned “No tips found.” on 2026-10-26: no fixtures, no markets, no tips. Zero lines and zero picks follow from that, and no substitute was invented.",
         "https://www.olbg.com/betting-tips/Snooker/8"),
        ("Rugby league has no matches", "Only three 2027 outrights are listed — State of Origin, Super League Grand Final and NRL Grand Final. There is no match market anywhere on the page, so the three picks are all ante-post.",
         "https://www.olbg.com/betting-tips/Rugby_League/10"),
        ("Baseball: one game", "A single MLB game carries tips (Milwaukee @ Tampa Bay). Its money line prices inside -250, so the run line is the only quotable selection in band.",
         "https://www.olbg.com/betting-tips/Baseball/12"),
        ("Golf: four selections, three events", "Maybank Championship, Mexico Open and Simmons Bank Championship each show a two-tip outright market. A five-pick card is impossible without inventing support.",
         "https://www.olbg.com/betting-tips/Golf/5"),
        ("Darts: outrights only", "Two events, both tournament winner markets. No match markets exist for the Players Championship or the Worlds.",
         "https://www.olbg.com/betting-tips/Darts/15"),
        ("Handball: every top selection is “Tie”", "Fourteen of fifteen matches show “Tie” as the most popular money-line pick, which is a market-mapping fault rather than genuine support. Those rows are priced for transparency and excluded from picks.",
         "https://www.olbg.com/betting-tips/Handball/20"),
        ("Start times disagree between pages", "The all-sports page and the sport pages print different kick-off times for the same fixtures (MIN @ CLE 23:00 vs 19:00; NZ v IND 07:00 vs 03:00; TOR @ CGY 00:37 vs 20:37). Both values are recorded; neither is asserted as correct.",
         "https://www.olbg.com/betting-tips"),
        ("Greyhounds: clock labels do not match start times", "Race titles use a 12-hour label (8:24 Towcester) while the listed start time renders as 16:24, and one race is already marked Expired. Exact post times are unverified.",
         "https://www.olbg.com/betting-tips/Greyhounds/28"),
        ("Greyhounds: single-tip races", "Six of the eight races carry exactly one tip, shown as “1/1, 100%”. That is one person's opinion, not a probability, and all such picks are labelled Low.",
         "https://www.olbg.com/betting-tips/Greyhounds/28"),
        ("Spread label mismatch on Dallas @ Miami", "The selection is published as “DAL Mavericks +7.50”, but the tipping comment and the page summary both discuss +8.50. We priced the published 7.50 and left the conflict visible.",
         "https://www.olbg.com/betting-tips/Basketball/NBA/NBA/DAL_Mavericks_@_MIA_Heat/4?event_id=536200"),
        ("A tipster comment contains a factual error", "The same Dallas/Miami page credits Miami with Giannis Antetokounmpo, who plays for Milwaukee. Comments are not used as fact anywhere in this output, and form numbers come from NBA.com instead.",
         "https://www.olbg.com/betting-tips/Basketball/NBA/NBA/DAL_Mavericks_@_MIA_Heat/4?event_id=536200"),
        ("Hockey comment contradicted by the official table", "An OLBG comment describes the Kings as “0-3-2 on the road”; NHL.com shows a 2-2-2 road record. The officially published figure is the one used in our prediction.",
         "https://www.nhl.com/standings"),
        ("Tennis: no tournament names", "OLBG's tennis list publishes player names and times but not the tournament. Competition is left blank on every tennis row rather than guessed.",
         "https://www.olbg.com/betting-tips/Tennis/3"),
        ("Rugby union: competition unlabelled, tips thin", "Most Pro D2 and URC fixtures are printed without a competition label, and nearly every match carries one or two tips. All five rugby picks are therefore Low.",
         "https://www.olbg.com/betting-tips/Rugby_Union/9"),
        ("Gaelic football market names missing", "Both club fixtures are listed with a handicap selection but no market name, and no competition round. The market column says so explicitly.",
         "https://www.olbg.com/betting-tips/Gaelic_Football/25"),
        ("Gaelic champions claim left unchecked", "OLBG's Gaelic page states that Mayo won the 2026 All-Ireland, ending a 75-year wait. No official GAA results page could be read here, so the claim is not used anywhere in our output.",
         "https://www.olbg.com/betting-tips/Gaelic_Football/25"),
        ("Motor racing: no tip count on the Grand Prix market", "The Mexico City GP top-six market shows a selection with no tip count, so it cannot be priced and is excluded.",
         "https://www.olbg.com/betting-tips/Motor_Racing/14"),
        ("No injury or team-news verification", "Official injury and team-news feeds were unreachable in this session. No prediction claims an injury, a suspension or a line-up change; each one states what it could not check.",
         "https://www.olbg.com/betting-tips"),
        ("Naming typos reproduced, not corrected", "“Central Districts”, “Nissa v Aurillac” and “Pakistan vs Sri Lanka One Day Match” appear exactly as OLBG publishes them.",
         "https://www.olbg.com/betting-tips/Cricket/7"),
    ]
    b = ['<p class="sub">Anything that could not be confirmed from an official source is here, with the link that shows the problem. These items do not block publication; they are listed so they can be checked by hand.</p>']
    b.append('<div class="scroll"><table><thead><tr><th>#</th><th>Issue</th><th>What we found</th><th>Source</th></tr></thead><tbody>')
    for i, (t, d, u) in enumerate(flags, 1):
        b.append(f'<tr><td class="num">{i}</td><td><b>{esc(t)}</b></td><td>{esc(d)}</td>'
                 f'<td><a href="{esc(u)}" rel="nofollow">open</a><br><span class="meta">{esc(u.split("//")[-1][:52])}</span></td></tr>')
    b.append('</tbody></table></div>')
    b.append('<h2>Unverified fields left blank</h2>')
    b.append('<div class="card"><p>Competition (all tennis rows), venue and series context (cricket), exact post times '
             '(greyhounds), injuries and line-ups (all sports), golf field sizes for two of three tournaments, and prize-money '
             'or rankings detail for ante-post markets. Blank means unknown here, not zero.</p></div>')
    (DOCS / "flagged.html").write_text(page("Flagged for review", "flagged.html", "\n".join(b)))

    print("built", len(list(DOCS.glob('*.html'))), "pages")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Static GitHub Pages dashboard builder for 2026-10-27 (T34).

Generates:
  - /index.html (root Executive Summary landing page)
  - /oct27/all-markets.html
  - /oct27/flagged.html
  - /oct27/repo-audit.html
  - /oct27/methodology.html
  - /oct27/sources.html
  - /oct27/sports/<slug>.html (all 15 covered OLBG sports)
"""
import html
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(ROOT, "data", "oct27")
OCT_DIR = os.path.join(ROOT, "oct27")
SPORTS_DIR = os.path.join(OCT_DIR, "sports")
os.makedirs(SPORTS_DIR, exist_ok=True)

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
NAME_TO_SLUG = {name: slug for slug, name in SPORTS}


def esc(val) -> str:
    return html.escape(str(val)) if val is not None else ""


def load_json(name: str):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def badge_html(conf: str) -> str:
    c = (conf or "low").lower()
    cls = "badge-high" if c == "high" else ("badge-medium" if c == "medium" else "badge-low")
    return f'<span class="badge {cls}">{esc(c.capitalize())}</span>'


def render_shell(title: str, active_nav: str, active_sport: str, prefix: str, body_html: str, pick_counts: dict, flag_count: int) -> str:
    nav_items = [
        ("summary", "Executive Summary", f"{prefix}index.html"),
        ("markets", "All 180 Markets", f"{prefix}oct27/all-markets.html"),
        ("flagged", f"Flagged for Review ({flag_count})", f"{prefix}oct27/flagged.html"),
        ("audit", "Repo Audit", f"{prefix}oct27/repo-audit.html"),
        ("method", "How We Price", f"{prefix}oct27/methodology.html"),
        ("sources", "Official Sources", f"{prefix}oct27/sources.html"),
        # Added by session arena/254c7925: the v3 board lives in its own namespace
        # and links back here. Additive only - no existing nav item was changed.
        ("v3", "v3 Written Picks", f"{prefix}v3/index.html"),
    ]
    nav_links = "".join(
        f'<a href="{href}" class="{"active" if key == active_nav else ""}">{esc(lbl)}</a>'
        for key, lbl, href in nav_items
    )
    sport_pills = "".join(
        f'<a href="{prefix}oct27/sports/{slug}.html" class="sport-pill {"active" if name == active_sport else ""}">'
        f'{esc(name)} <span class="cnt">({pick_counts.get(name, 0)})</span></a>'
        for slug, name in SPORTS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} — OLBG 15-Sport Origination Desk (27 Oct 2026)</title>
  <link rel="stylesheet" href="{prefix}assets/oct27.css">
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="{prefix}index.html">
        OLBG 15-Sport Origination Desk
        <span class="brand-badge">27 Oct 2026 · UTC</span>
      </a>
      <nav class="primary-nav">{nav_links}</nav>
    </div>
  </header>
  <div class="sportbar">
    <div class="sportbar-inner">{sport_pills}</div>
  </div>
  <main>
{body_html}
  </main>
  <footer>
    <strong>OLBG 15-Sport Origination Desk (27 October 2026 UTC)</strong> · Every betting price on this site is originated in-house and every table row links to both its OLBG market page and an official governing-body or primary statistical source. Unconfirmed fields remain blank and appear on <a href="{prefix}oct27/flagged.html">Flagged for Review</a>.<br>
    Preserved repository snapshots:
    <a href="{prefix}cycle-board.html">27 Oct Tip-Split Cycle Board</a> ·
    <a href="{prefix}desk/index.html">27 Oct Coverage Desk</a> ·
    <a href="{prefix}picks.html">27 Oct CAL-4 Picks</a> ·
    <a href="{prefix}legacy-cal4/index.html">27 Oct CAL-4 Archive</a> ·
    <a href="{prefix}board/all-markets.html">Early 27 Oct Hub Board</a> ·
    <a href="{prefix}olbg-tips/index.html">26 Oct Tip-Consensus Board</a> ·
    <a href="{prefix}docs/index.html">26 Oct Docs Snapshot</a> ·
    <a href="{prefix}docs/board-review/index.html">26 Oct Board Review</a>
  </footer>
</body>
</html>
"""


def render_pick_card(p: dict, flag_href: str) -> str:
    inj = (
        f'<span><strong>Team / Entry Note:</strong> {esc(p["injury_news"])}</span>'
        if p.get("injury_news")
        else f'<span class="blank-tag">Injury sheet unconfirmed — left blank (<a href="{flag_href}">flagged</a>)</span>'
    )
    return f"""<article class="pick-card" id="{esc(p['pick_id'])}">
  <div class="pick-card-top">
    <div>
      <div class="pick-sport">{esc(p['sport'])} · {esc(p['comp'])}</div>
      <h3 class="pick-title">{esc(p['headline'])}</h3>
    </div>
    {badge_html(p['confidence'])}
  </div>
  <div class="pick-meta">
    <span><strong>Event:</strong> {esc(p['event'])} ({esc(p['start'])})</span>
    <span><strong>Selection:</strong> {esc(p['sel'])} ({esc(p['market'])})</span>
    <span><strong>Our Line:</strong> {esc(p['price_am_str'])} ({p['price_dec']:.2f})</span>
    <span><strong>Fair Chance:</strong> {p['fair_pct']:.1f}%</span>
  </div>
  <p class="pick-body">{esc(p['prediction'])}</p>
  <div class="pick-foot">
    {inj}
    <span class="src-links">
      <a class="src-chip" href="{esc(p['olbg_url'])}" target="_blank" rel="noopener">OLBG ({esc(p['olbg_tips'])}) ↗</a>
      <a class="src-chip" href="{esc(p['official_url'])}" target="_blank" rel="noopener">{esc(p['official_source'])} ↗</a>
    </span>
  </div>
</article>"""


def render_lines_table(rows: list, flag_href: str, table_id: str = "linesTable") -> str:
    body = []
    for r in rows:
        inj_cell = (
            esc(r["injury_news"])
            if r.get("injury_news")
            else f'<span class="blank-tag">— blank (<a href="{flag_href}">flagged</a>)</span>'
        )
        band_note = "" if r["in_band"] else ' <span class="badge badge-flag" title="Shorter than -250 floor">Chalk &lt;-250</span>'
        early_note = ' <span class="badge badge-flag">Started early</span>' if r.get("started_early") else ""
        body.append(
            f'<tr data-sport="{esc(r["sport"])}" data-conf="{esc(r["confidence"])}">'
            f'<td>{esc(r["sport"])}</td>'
            f'<td><strong>{esc(r["event"])}</strong><br><span style="color:#64748b;font-size:12px">{esc(r["comp"])} · {esc(r["start"])}</span>{early_note}</td>'
            f'<td>{esc(r["market"])}</td>'
            f'<td><strong>{esc(r["sel"])}</strong>{band_note}</td>'
            f'<td class="num">{esc(r["olbg_tips"])}</td>'
            f'<td class="num">{r["fair_pct"]:.1f}%</td>'
            f'<td class="num"><strong>{esc(r["price_am_str"])}</strong><br><span style="color:#64748b;font-size:11.5px">{r["price_dec"]:.2f}</span></td>'
            f'<td>{badge_html(r["confidence"])}</td>'
            f'<td style="max-width:250px;font-size:12.3px">{inj_cell}</td>'
            f'<td><span class="src-links">'
            f'<a class="src-chip" href="{esc(r["olbg_url"])}" target="_blank" rel="noopener">OLBG ↗</a>'
            f'<a class="src-chip" href="{esc(r["official_url"])}" target="_blank" rel="noopener">{esc(r["official_source"])} ↗</a>'
            f'</span></td>'
            f'</tr>'
        )
    return f"""<div class="table-wrap">
<table class="data" id="{esc(table_id)}">
  <thead>
    <tr>
      <th>Sport</th>
      <th>Event &amp; Competition</th>
      <th>Market</th>
      <th>Originated Selection</th>
      <th class="num">OLBG Tips</th>
      <th class="num">Fair %</th>
      <th class="num">Our Price</th>
      <th>Confidence</th>
      <th>Team / Injury Status</th>
      <th>Row Sources</th>
    </tr>
  </thead>
  <tbody>
    {''.join(body)}
  </tbody>
</table>
</div>"""


def build_index(events, lines, picks, flags, sources, pick_counts):
    high_picks = [p for p in picks if p["confidence"] == "high"]
    med_picks = [p for p in picks if p["confidence"] == "medium"]
    low_picks = [p for p in picks if p["confidence"] == "low"]

    ev_by_sport = Counter(e["sport"] for e in events)
    ln_by_sport = Counter(l["sport"] for l in lines)
    hi_by_sport = Counter(p["sport"] for p in high_picks)

    # Coverage matrix rows across all 15 sports
    cov_rows = []
    sport_hub_map = sources["sport_hubs"]
    default_off = {s["sport"]: (s["org"], s["url"]) for s in reversed(sources["official_sources"])}
    for slug, sname in SPORTS:
        ne = ev_by_sport[sname]
        nl = ln_by_sport[sname]
        npk = pick_counts[sname]
        nhi = hi_by_sport[sname]
        org, ourl = default_off.get(sname, ("Official Feed", sport_hub_map[sname]))
        if npk >= 5:
            status = '<span class="badge badge-high">5–10 Target Met</span>'
        elif sname == "Baseball":
            status = '<span class="badge badge-medium">3/3 WS Game 4 Markets</span>'
        else:
            status = '<span class="badge badge-flag">0 on OLBG (Flagged)</span>'
        cov_rows.append(
            f'<tr>'
            f'<td><a href="oct27/sports/{slug}.html"><strong>{esc(sname)}</strong></a></td>'
            f'<td class="num">{ne}</td>'
            f'<td class="num">{nl}</td>'
            f'<td class="num"><strong>{npk}</strong></td>'
            f'<td class="num">{nhi}</td>'
            f'<td>{status}</td>'
            f'<td><span class="src-links">'
            f'<a class="src-chip" href="{esc(sport_hub_map[sname])}" target="_blank" rel="noopener">OLBG Hub ↗</a>'
            f'<a class="src-chip" href="{esc(ourl)}" target="_blank" rel="noopener">{esc(org[:26])} ↗</a>'
            f'</span></td>'
            f'</tr>'
        )

    # Executive Summary High-Confidence Picks Table
    hi_rows = []
    for p in high_picks:
        slug = NAME_TO_SLUG[p["sport"]]
        inj_short = esc(p["injury_news"][:72] + ("…" if len(p["injury_news"]) > 72 else "")) if p.get("injury_news") else '<span class="blank-tag">— blank (<a href="oct27/flagged.html">flagged</a>)</span>'
        hi_rows.append(
            f'<tr data-sport="{esc(p["sport"])}">'
            f'<td><a href="oct27/sports/{slug}.html"><strong>{esc(p["sport"])}</strong></a></td>'
            f'<td><a href="oct27/sports/{slug}.html#{esc(p["pick_id"])}"><strong>{esc(p["sel"])}</strong></a>'
            f'<br><span style="color:#64748b;font-size:12px">{esc(p["event"])} · {esc(p["start"])}</span></td>'
            f'<td>{esc(p["market"])}</td>'
            f'<td class="num"><strong>{esc(p["price_am_str"])}</strong> <span style="color:#64748b;font-size:11.5px">({p["price_dec"]:.2f})</span></td>'
            f'<td class="num">{p["fair_pct"]:.1f}%</td>'
            f'<td>{badge_html(p["confidence"])}</td>'
            f'<td style="font-size:12px;max-width:230px">{inj_short}</td>'
            f'<td><span class="src-links">'
            f'<a class="src-chip" href="{esc(p["olbg_url"])}" target="_blank" rel="noopener">OLBG ↗</a>'
            f'<a class="src-chip" href="{esc(p["official_url"])}" target="_blank" rel="noopener">{esc(p["official_source"])} ↗</a>'
            f'</span></td>'
            f'</tr>'
        )

    # One spotlight card per active sport (13 cards) for instant executive reading
    seen_sp = set()
    spotlight_cards = []
    for p in picks:
        if p["sport"] not in seen_sp:
            seen_sp.add(p["sport"])
            spotlight_cards.append(render_pick_card(p, "oct27/flagged.html"))

    # Heavy chalk conversion table (lines shorter than -250 -> how we priced in-band alternatives)
    chalk_lines = [l for l in lines if not l["in_band"] and l["price_dec"] < 1.40]
    chalk_rows = []
    for cl in chalk_lines:
        slug = NAME_TO_SLUG[cl["sport"]]
        chalk_rows.append(
            f'<tr>'
            f'<td>{esc(cl["sport"])}</td>'
            f'<td>{esc(cl["event"])}</td>'
            f'<td>{esc(cl["sel"])} ({esc(cl["market"])})</td>'
            f'<td class="num">{cl["fair_pct"]:.1f}%</td>'
            f'<td class="num">{esc(cl["price_am_str"])} ({cl["price_dec"]:.2f})</td>'
            f'<td><a href="oct27/sports/{slug}.html">View in-band Spread / Set / Prop alternative →</a></td>'
            f'<td><span class="src-links">'
            f'<a class="src-chip" href="{esc(cl["olbg_url"])}" target="_blank" rel="noopener">OLBG ↗</a>'
            f'<a class="src-chip" href="{esc(cl["official_url"])}" target="_blank" rel="noopener">{esc(cl["official_source"])} ↗</a>'
            f'</span></td>'
            f'</tr>'
        )

    sport_opts = '<option value="">All 13 Active Sports</option>' + "".join(
        f'<option value="{esc(name)}">{esc(name)}</option>' for _, name in SPORTS if pick_counts[name] > 0
    )

    body = f"""
<section class="hero">
  <h1>Executive Summary — Today&rsquo;s &amp; Upcoming Originated Lines &amp; High-Confidence Picks</h1>
  <p>Live inventory across all <strong>15 OLBG sports</strong> for <strong>Tuesday 27 October 2026 (UTC)</strong>.
  We originated our own fair probabilities and betting lines across <strong>{len(lines)} markets</strong> on
  <strong>{len(events)} active OLBG events</strong>, cross-checked standings, recent results, probable starters and
  official injury/absence lists from governing bodies, and wrote <strong>{len(picks)} unique predictions</strong>.
  Every single High-Confidence selection sits strictly inside the <strong>&minus;250 to +10000</strong>
  (<code>1.40</code> to <code>101.00</code> decimal) odds window.</p>
  <div class="kpi-grid">
    <div class="kpi"><div class="val">15</div><div class="lbl">OLBG Sports Covered (13 Active, 2 Empty)</div></div>
    <div class="kpi"><div class="val">{len(events)}</div><div class="lbl">Upcoming OLBG Events Inventoried</div></div>
    <div class="kpi"><div class="val">{len(lines)}</div><div class="lbl">Markets Priced (100% Originated)</div></div>
    <div class="kpi"><div class="val">{len(picks)}</div><div class="lbl">Unique Written Predictions (&ge;30w)</div></div>
    <div class="kpi"><div class="val">{len(high_picks)}</div><div class="lbl">High-Confidence Picks (&minus;250..+10000)</div></div>
    <div class="kpi"><div class="val">{len(flags)}</div><div class="lbl"><a href="oct27/flagged.html">Items Flagged for Review</a></div></div>
  </div>
</section>

<section class="panel" style="border-left:5px solid #0f8b8d;background:#f2fbfa">
  <h2>Looking for the full pick list? Open the Value Desk</h2>
  <p>The additive <a href="value-desk/index.html"><strong>OLBG Value Desk &rarr;</strong></a> puts
  <strong>85 sourced written predictions</strong> (5-6 per sport, including Snooker and Greyhounds,
  which OLBG left empty today), <strong>193 originated lines</strong>, an executive summary,
  <strong>29 plus-money picks</strong> inside &minus;250 to +10000, and all
  <strong>221 flagged items</strong> on one clearly labelled board. Every table row carries an
  official source link; blank values stay blank and are flagged rather than filled.</p>
</section>

<section class="panel">
  <h2>1. Highest-Confidence Picks (&minus;250 to +10000 Odds Band)</h2>
  <p class="sub">All {len(high_picks)} High-Confidence selections ({len(med_picks)} Medium and {len(low_picks)} Low picks are on the sport subpages). Heavy &gt;71% money-line chalk shorter than &minus;250 is excluded here and routed to pointspread, handicap, set-betting or player-award markets.</p>
  <div class="filter-bar">
    <label for="hiSportFilter"><strong>Filter by Sport:</strong></label>
    <select id="hiSportFilter" onchange="filterHiTable()">{sport_opts}</select>
    <input type="search" id="hiSearch" placeholder="Search team, player, market…" oninput="filterHiTable()">
  </div>
  <div class="table-wrap">
    <table class="data" id="hiPicksTable">
      <thead>
        <tr>
          <th>Sport</th>
          <th>Selection &amp; Event</th>
          <th>Market</th>
          <th class="num">Our Price</th>
          <th class="num">Fair %</th>
          <th>Confidence</th>
          <th>Confirmed Team / Entry Note</th>
          <th>Row Sources</th>
        </tr>
      </thead>
      <tbody>
        {''.join(hi_rows)}
      </tbody>
    </table>
  </div>
</section>

<section class="panel">
  <h2>2. Lead Written Pick per Active Sport (13-Sport Executive Digest)</h2>
  <p class="sub">One flagship selection from each active OLBG sport today. Click any sport pill above for all 5–8 written predictions and the complete multi-market price board for that sport.</p>
  <div class="picks-grid">
    {''.join(spotlight_cards)}
  </div>
</section>

<section class="panel">
  <h2>3. 15-Sport Coverage &amp; Source Summary</h2>
  <p class="sub">12 active sports meet the 5–10 prediction target. Baseball has 1 active event worldwide on OLBG today (World Series Game 4, all 3 published markets priced and written up), while Snooker and Greyhounds published zero OLBG events at capture and are documented on <a href="oct27/flagged.html">Flagged for Review</a>.</p>
  <div class="table-wrap">
    <table class="data">
      <thead>
        <tr>
          <th>Sport Subpage</th>
          <th class="num">OLBG Events</th>
          <th class="num">Markets Originated</th>
          <th class="num">Written Picks</th>
          <th class="num">High Confidence</th>
          <th>5–10 Pick Target</th>
          <th>Hub &amp; Official Source</th>
        </tr>
      </thead>
      <tbody>
        {''.join(cov_rows)}
      </tbody>
    </table>
  </div>
</section>

<section class="panel">
  <h2>4. Heavy Chalk (&lt;&minus;250 / &gt;71% Raw Chance) Routed to In-Band Markets</h2>
  <p class="sub">Rather than padding High-Confidence picks with &minus;400 to &minus;2000 money-line favourites, every heavy favourite below was re-expressed via its OLBG spread, handicap, straight-sets, or Man-of-the-Match market inside &minus;250 to +10000.</p>
  <div class="table-wrap">
    <table class="data">
      <thead>
        <tr>
          <th>Sport</th>
          <th>Event</th>
          <th>Heavy Chalk Side</th>
          <th class="num">Fair %</th>
          <th class="num">Chalk Price</th>
          <th>Actionable In-Band Route</th>
          <th>Sources</th>
        </tr>
      </thead>
      <tbody>
        {''.join(chalk_rows)}
      </tbody>
    </table>
  </div>
</section>

<script>
function filterHiTable() {{
  var sp = document.getElementById('hiSportFilter').value.toLowerCase();
  var q = document.getElementById('hiSearch').value.toLowerCase();
  var rows = document.querySelectorAll('#hiPicksTable tbody tr');
  rows.forEach(function(r) {{
    var rsp = (r.getAttribute('data-sport') || '').toLowerCase();
    var txt = r.textContent.toLowerCase();
    var okSp = !sp || rsp === sp;
    var okQ = !q || txt.indexOf(q) !== -1;
    r.style.display = (okSp && okQ) ? '' : 'none';
  }});
}}
</script>
"""
    html_out = render_shell("Executive Summary", "summary", "", "", body, pick_counts, len(flags))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_out)


def build_sport_pages(events, lines, picks, flags, sources, pick_counts):
    hub_map = sources["sport_hubs"]
    for slug, sname in SPORTS:
        sp_events = [e for e in events if e["sport"] == sname]
        sp_lines = [l for l in lines if l["sport"] == sname]
        sp_picks = [p for p in picks if p["sport"] == sname]
        sp_flags = [fl for fl in flags if sname in fl["sport"] or fl["sport"] == "All Sports"]
        sp_sources = [s for s in sources["official_sources"] if s["sport"] == sname]

        src_chips = " ".join(
            f'<a class="src-chip" href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["org"])} ↗</a>'
            for s in sp_sources
        )

        if not sp_lines:
            # Snooker or Greyhounds empty OLBG feed explanation
            fl = sp_flags[0]
            body = f"""
<section class="hero">
  <h1>{esc(sname)} — OLBG Market Inventory &amp; Official Schedule Check</h1>
  <p>OLBG&rsquo;s <a href="{esc(hub_map[sname])}" target="_blank" rel="noopener">{esc(sname)} hub ↗</a> published
  <strong>0 active events and 0 tips</strong> on 27 October 2026. Per desk rules, zero matches, runners or prices were fabricated.</p>
  <div class="kpi-grid">
    <div class="kpi"><div class="val">0</div><div class="lbl">Active OLBG Events</div></div>
    <div class="kpi"><div class="val">0</div><div class="lbl">Markets Originated</div></div>
    <div class="kpi"><div class="val">0</div><div class="lbl">Written Predictions</div></div>
    <div class="kpi"><div class="val">1</div><div class="lbl">Flagged Feed Notice</div></div>
  </div>
</section>
<section class="panel">
  <h2>Official Governing-Body Explanation ({esc(fl['id'])})</h2>
  <div class="callout warn">
    <strong>{esc(fl['title'])}</strong><br>
    {esc(fl['detail'])}
  </div>
  <p><strong>Direct Links Checked:</strong>
    <a class="src-chip" href="{esc(fl['olbg_url'])}" target="_blank" rel="noopener">OLBG {esc(sname)} Hub ↗</a>
    {src_chips}
  </p>
</section>
"""
        else:
            cards_html = "".join(render_pick_card(p, "../flagged.html") for p in sp_picks)
            flag_banner = ""
            specific_flags = [fl for fl in flags if sname in fl["sport"]]
            if specific_flags:
                items = "".join(
                    f'<li><strong>{esc(fl["id"])} — {esc(fl["title"])}:</strong> {esc(fl["detail"])} '
                    f'(<a href="{esc(fl["official_url"])}" target="_blank" rel="noopener">Official Source ↗</a>)</li>'
                    for fl in specific_flags
                )
                flag_banner = f'<div class="callout warn"><strong>{esc(sname)} Audit Notes &amp; Blanks:</strong><ul style="margin:6px 0 0;padding-left:20px">{items}</ul></div>'

            body = f"""
<section class="hero">
  <h1>{esc(sname)} — Originated Lines &amp; Written Predictions</h1>
  <p>Inventoried <strong>{len(sp_events)} upcoming OLBG events</strong> and originated prices across
  <strong>{len(sp_lines)} betting markets</strong>, with <strong>{len(sp_picks)} written predictions</strong>
  inside the &minus;250 to +10000 odds window.</p>
  <p style="margin-top:10px"><strong>Official Sources:</strong>
    <a class="src-chip" href="{esc(hub_map[sname])}" target="_blank" rel="noopener">OLBG {esc(sname)} Hub ↗</a>
    {src_chips}
  </p>
</section>
{flag_banner}
<section class="panel">
  <h2>Written Predictions ({len(sp_picks)})</h2>
  <p class="sub">Every selection states the exact market and originated price, incorporates official standings, recent results and confirmed team/entry news, and runs at least 30 words.</p>
  <div class="picks-grid">
    {cards_html}
  </div>
</section>

<section class="panel">
  <h2>All Originated {esc(sname)} Lines ({len(sp_lines)} Markets)</h2>
  <p class="sub">Every row links directly to both its OLBG market page and the official governing-body source. Unconfirmed injury fields are left blank and flagged.</p>
  {render_lines_table(sp_lines, "../flagged.html")}
</section>
"""
        out_html = render_shell(f"{sname} Picks & Originated Lines", "", sname, "../../", body, pick_counts, len(flags))
        with open(os.path.join(SPORTS_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(out_html)


def build_all_markets(lines, flags, pick_counts):
    sport_opts = '<option value="">All Sports</option>' + "".join(
        f'<option value="{esc(name)}">{esc(name)}</option>' for _, name in SPORTS
    )
    body = f"""
<section class="hero">
  <h1>All {len(lines)} Originated Betting Markets (27 October 2026)</h1>
  <p>Complete multi-market price board across Win Match / Money Line / 3-Way 1X2, Pointspread / Handicap / Run Line / Puck Line,
  Game Totals / Points Total, Set Betting, Podium / Points Finish, and Tournament Outrights. Every row carries direct links to
  both OLBG and the official competition source.</p>
</section>
<section class="panel">
  <div class="filter-bar">
    <select id="mkSport" onchange="filterMk()">{sport_opts}</select>
    <select id="mkConf" onchange="filterMk()">
      <option value="">All Confidence Tiers</option>
      <option value="high">High Confidence</option>
      <option value="medium">Medium Confidence</option>
      <option value="low">Low Confidence</option>
    </select>
    <input type="search" id="mkQuery" placeholder="Search event, team, player or market…" oninput="filterMk()">
  </div>
  {render_lines_table(lines, "flagged.html", "allMarketsTable")}
</section>
<script>
function filterMk() {{
  var sp = document.getElementById('mkSport').value.toLowerCase();
  var cf = document.getElementById('mkConf').value.toLowerCase();
  var q = document.getElementById('mkQuery').value.toLowerCase();
  document.querySelectorAll('#allMarketsTable tbody tr').forEach(function(r) {{
    var okSp = !sp || (r.getAttribute('data-sport') || '').toLowerCase() === sp;
    var okCf = !cf || (r.getAttribute('data-conf') || '').toLowerCase() === cf;
    var okQ = !q || r.textContent.toLowerCase().indexOf(q) !== -1;
    r.style.display = (okSp && okCf && okQ) ? '' : 'none';
  }});
}}
</script>
"""
    out_html = render_shell("All 180 Originated Markets", "markets", "", "../", body, pick_counts, len(flags))
    with open(os.path.join(OCT_DIR, "all-markets.html"), "w", encoding="utf-8") as f:
        f.write(out_html)


def build_flagged(lines, flags, pick_counts):
    flag_rows = []
    for fl in flags:
        flag_rows.append(
            f'<tr>'
            f'<td><strong>{esc(fl["id"])}</strong></td>'
            f'<td>{esc(fl["sport"])}</td>'
            f'<td><span class="badge badge-flag">{esc(fl["severity"])}</span></td>'
            f'<td><strong>{esc(fl["title"])}</strong><br><span style="color:#334155">{esc(fl["detail"])}</span></td>'
            f'<td><span class="src-links">'
            f'<a class="src-chip" href="{esc(fl["olbg_url"])}" target="_blank" rel="noopener">OLBG ↗</a>'
            f'<a class="src-chip" href="{esc(fl["official_url"])}" target="_blank" rel="noopener">Official ↗</a>'
            f'</span></td>'
            f'</tr>'
        )

    blank_rows = [l for l in lines if not l.get("injury_news") or l.get("started_early")]
    b_html = []
    for r in blank_rows:
        reason = "Match started 07:00–08:00 UTC on 27 Oct (excluded from pre-match picks)" if r.get("started_early") else "Pre-match official injury sheet not centrally published — left blank"
        b_html.append(
            f'<tr>'
            f'<td>{esc(r["id"])}</td>'
            f'<td>{esc(r["sport"])}</td>'
            f'<td>{esc(r["event"])} ({esc(r["market"])})</td>'
            f'<td class="blank-tag">{esc(reason)}</td>'
            f'<td><span class="src-links">'
            f'<a class="src-chip" href="{esc(r["olbg_url"])}" target="_blank" rel="noopener">OLBG ↗</a>'
            f'<a class="src-chip" href="{esc(r["official_url"])}" target="_blank" rel="noopener">{esc(r["official_source"])} ↗</a>'
            f'</span></td>'
            f'</tr>'
        )

    body = f"""
<section class="hero">
  <h1>Flagged for Review — Data Irregularities &amp; Deliberate Blanks</h1>
  <p>Every discrepancy discovered while cross-checking OLBG against official governing-body calendars, standings,
  entry lists and injury reports, followed by every market row where an unconfirmed pre-match injury sheet was
  intentionally left blank rather than guessed.</p>
</section>
<section class="panel">
  <h2>1. Active Irregularities, Stale OLBG Figures &amp; Empty Sport Hubs ({len(flags)})</h2>
  <div class="table-wrap">
    <table class="data">
      <thead>
        <tr><th>ID</th><th>Sport</th><th>Category</th><th>Finding &amp; Handling</th><th>Evidence Links</th></tr>
      </thead>
      <tbody>{''.join(flag_rows)}</tbody>
    </table>
  </div>
</section>
<section class="panel">
  <h2>2. Market Rows with Deliberate Unconfirmed Blanks or In-Play Exclusions ({len(blank_rows)})</h2>
  <p class="sub">Centralized daily injury reports are published for NBA, NHL, MLB, PDC PC31 and LPGA/PGA fields; domestic European basketball, hockey, volleyball and cricket fixtures without centralized official team-news feeds remain explicitly blank.</p>
  <div class="table-wrap">
    <table class="data">
      <thead>
        <tr><th>Line ID</th><th>Sport</th><th>Event &amp; Market</th><th>Blank / Exclusion Reason</th><th>Row Sources</th></tr>
      </thead>
      <tbody>{''.join(b_html)}</tbody>
    </table>
  </div>
</section>
"""
    out_html = render_shell("Flagged for Review", "flagged", "", "../", body, pick_counts, len(flags))
    with open(os.path.join(OCT_DIR, "flagged.html"), "w", encoding="utf-8") as f:
        f.write(out_html)


def build_repo_audit(audit, flags, pick_counts):
    r26 = audit["root_26oct_audit"]
    r27 = audit["today_early_hub_audit"]

    d26_rows = "".join(
        f'<tr><td><strong>{esc(d["code"])}</strong></td><td><code>{esc(d["file"])}</code></td>'
        f'<td>{esc(d["issue"])}</td>'
        f'<td><a class="src-chip" href="{esc(d["official_source"])}" target="_blank" rel="noopener">Official Source ↗</a></td></tr>'
        for d in r26["structural_defects"]
    )
    d27_rows = "".join(
        f'<tr><td><strong>{esc(d["code"])}</strong></td><td>{esc(d["issue"])}</td>'
        f'<td>{esc(d["resolution"])}</td>'
        f'<td><a class="src-chip" href="{esc(d["official_source"])}" target="_blank" rel="noopener">Official Source ↗</a></td></tr>'
        for d in r27["gaps_resolved_in_oct27"]
    )
    cyc_rows = "".join(
        f'<tr><td><strong>{esc(d["code"])}</strong></td><td>{esc(d["issue"])}</td>'
        f'<td>{esc(d["resolution"])}</td>'
        f'<td><a class="src-chip" href="{esc(d["official_source"])}" target="_blank" rel="noopener">Official Source ↗</a></td></tr>'
        for d in audit.get("concurrent_oct27_audit", [])
    )
    rollover_rows = "".join(
        f'<tr><td><code>{esc(x["id"])}</code></td><td>{esc(x["sport"])}</td><td>{esc(x["event"])}</td>'
        f'<td>{esc(x["label"])}</td><td><code>{esc(x["recorded_date"])}</code> (actually 2026-10-27 UTC)</td></tr>'
        for x in r26["edt_utc_date_rollover_examples"]
    )

    body = f"""
<section class="hero">
  <h1>Line-by-Line Audit of Prior Repository Snapshots</h1>
  <p>Before originating our 27 October 2026 multi-market board, we audited every dataset and pricing script already
  in <code>karagemop466-tech/Olbg7</code> without overwriting or deleting any prior session&rsquo;s files.</p>
</section>

<section class="panel">
  <h2>1. Audit of 26 October Dataset (<code>data/*.json</code> &amp; <code>tools/pricing.py</code>)</h2>
  <p class="sub">Checked {r26['events_count']} events, {r26['priced_count']} priced rows and {r26['picks_count']} picks: found {r26['expired_oct26_events_count']} settled 26 Oct fixtures and {r26['edt_utc_date_rollover_count']} EDT-to-UTC date rollover errors.</p>
  <div class="table-wrap">
    <table class="data">
      <thead><tr><th>Audit ID</th><th>Files</th><th>Finding</th><th>Reference</th></tr></thead>
      <tbody>{d26_rows}</tbody>
    </table>
  </div>
  <h3 style="margin-top:18px;font-size:15px">Sample Unlabeled UTC&minus;4 (EDT) Rollover Rows in <code>data/events.json</code></h3>
  <div class="table-wrap">
    <table class="data">
      <thead><tr><th>Event ID</th><th>Sport</th><th>Event</th><th>OLBG Clock (EDT)</th><th>Recorded vs True UTC Date</th></tr></thead>
      <tbody>{rollover_rows}</tbody>
    </table>
  </div>
</section>

<section class="panel">
  <h2>2. Audit of Early 27 October Hub Capture (<code>data/today/*.json</code>) &amp; What We Upgraded</h2>
  <p class="sub">Checked {r27['captured_rows']} hub rows and {r27['lines_count']} lines ({r27['lines_from_tips_only']} priced from OLBG tip splits alone with no official table or injury feed).</p>
  <div class="table-wrap">
    <table class="data">
      <thead><tr><th>Audit ID</th><th>Gap in Earlier Capture</th><th>How Our 27 Oct Multi-Market Build Resolves It</th><th>Official Source</th></tr></thead>
      <tbody>{d27_rows}{cyc_rows}</tbody>
    </table>
  </div>
</section>
"""
    out_html = render_shell("Line-by-Line Repo Audit", "audit", "", "../", body, pick_counts, len(flags))
    with open(os.path.join(OCT_DIR, "repo-audit.html"), "w", encoding="utf-8") as f:
        f.write(out_html)


def build_methodology(flags, pick_counts):
    body = """
<section class="hero">
  <h1>How We Originate Betting Lines Across All 15 Sports</h1>
  <p>OLBG&rsquo;s server-rendered HTML exposes event IDs, market types, handicap/total lines and community tip counts,
  but omits bookmaker odds. Every price on this site is computed by our own four-family mathematical origination suite.</p>
</section>
<section class="panel">
  <h2>1. Four Sport-Specific Probability Engines</h2>
  <div class="table-wrap">
    <table class="data">
      <thead><tr><th>Engine Family</th><th>Sports Covered</th><th>Inputs &amp; Distribution</th><th>Markets Consistent Simultaneously</th></tr></thead>
      <tbody>
        <tr>
          <td><strong>Gaussian Margin &amp; Total</strong></td>
          <td>Basketball (NBA, EuroLeague, EuroCup, BCL), Rugby Union, Gaelic Handicap</td>
          <td>Official net rating / points differential + home-court edge + confirmed absentee adjustment &rarr; Normal CDF <code>&Phi;((&mu; + h)/&sigma;)</code> and <code>&Phi;((&tau; &minus; T)/&sigma;_T)</code>.</td>
          <td>Money Line, Pointspread / Handicap, and Game Totals</td>
        </tr>
        <tr>
          <td><strong>Poisson &ndash; Skellam Goal/Run Matrix</strong></td>
          <td>Baseball (MLB), Ice Hockey (NHL, Liiga, DEL, SHL), Handball (EHF CL)</td>
          <td>Attack/defense scoring rates <code>(&lambda;_H, &lambda;_A)</code> from official goals/runs per game + goalie/starter/IR adjustments &rarr; exact bivariate goal grid.</td>
          <td>Regulation 3-Way 1X2 (curing OLBG&rsquo;s Handball Tie bug), OT Money Line, Run/Puck Line (&plusmn;1.5), and Over/Under Totals</td>
        </tr>
        <tr>
          <td><strong>Markov Set &amp; Game Chain</strong></td>
          <td>Tennis (ATP/WTA), Volleyball (Best-of-5)</td>
          <td>Per-set win probability <code>p_s</code> from live ATP/WTA ranking, surface hold/break profile, and league set ratios &rarr; exact <code>2-0</code>, <code>2-1</code>, <code>3-0..3-2</code> chains.</td>
          <td>Win Match, Straight-Sets (2-0), and Games Handicap</td>
        </tr>
        <tr>
          <td><strong>Plackett&ndash;Luce Field Engine</strong></td>
          <td>Golf (N=54, 78, 132), Darts (N=96, 128), Motor Racing (N=6, 22), Rugby League (N=2, 14, 18), GAA &amp; Cricket Outrights</td>
          <td>True entrant count <code>N</code> (replacing the legacy 1/8 constant prior), official World Ranking / Order of Merit / post-Austin WDC points, with confirmed absentees zeroed out.</td>
          <td>Win Tournament, Grand Final Winner, Podium Finish, Points Finish</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
<section class="panel">
  <h2>2. Origination Margin &amp; Objective Confidence Rules (&minus;250 to +10000)</h2>
  <div class="callout">
    <strong>Why heavy &gt;71% chalk is never labelled High Confidence here:</strong> A raw win chance above 71.4% converts
    to fair odds shorter than &minus;250 (<code>1.40</code> decimal). Rather than listing &minus;500 to &minus;2000 money-line
    favourites as High Confidence, our engine caps out-of-band chalk and routes conviction plays through pointspreads,
    handicaps, set betting, or tournament markets priced strictly inside <strong>&minus;250 to +10000</strong>
    (<code>1.40 &le; price_dec &le; 101.00</code>).
  </div>
  <ul>
    <li><strong>Origination Overround:</strong> <code>4.5%</code> on 2-way match/spread/total lines, <code>5.5%</code> on 3-way 1X2 lines, and <code>8.0%</code> on multi-runner outrights: <code>price_dec = round(1 / (p_fair &times; overround), 2)</code>.</li>
    <li><strong>High Confidence:</strong> Requires price strictly inside <code>[1.40, 101.00]</code> (<code>&minus;250..+10000</code>), official governing-body form/table/entry support, and either <code>p_fair &ge; 61.5%</code> (<code>&ge;59.5%</code> with confirmed injury/standings edge) on match/spread/total markets or <code>&ge;3.5&times;</code> uniform field share with <code>p_fair &ge; 14.5%</code> on outrights/podiums.</li>
    <li><strong>Medium Confidence:</strong> <code>p_fair &ge; 53.5%</code> on head-to-head/spread/total markets or <code>&ge;1.7&times;</code> uniform field share on outrights (plus heavy chalk shorter than &minus;250).</li>
    <li><strong>Low Confidence:</strong> Marginal edges (<code>p_fair &lt; 53.5%</code>), tip-shrinkage-only domestic lines without official league differentials, or earlier-morning in-play exclusions.</li>
  </ul>
</section>
"""
    out_html = render_shell("How We Price", "method", "", "../", body, pick_counts, len(flags))
    with open(os.path.join(OCT_DIR, "methodology.html"), "w", encoding="utf-8") as f:
        f.write(out_html)


def build_sources(sources, flags, pick_counts):
    hub_rows = "".join(
        f'<tr><td><strong>{esc(name)}</strong></td><td><a href="{esc(sources["sport_hubs"][name])}" target="_blank" rel="noopener">{esc(sources["sport_hubs"][name])} ↗</a></td></tr>'
        for _, name in SPORTS
    )
    off_rows = "".join(
        f'<tr><td><code>{esc(s["id"])}</code></td><td><strong>{esc(s["sport"])}</strong></td>'
        f'<td>{esc(s["org"])}</td><td>{esc(s["used_for"])}</td>'
        f'<td><a class="src-chip" href="{esc(s["url"])}" target="_blank" rel="noopener">Open Source ↗</a></td></tr>'
        for s in sources["official_sources"]
    )
    body = f"""
<section class="hero">
  <h1>Official Governing-Body &amp; OLBG Source Directory</h1>
  <p>Every source consulted on 27 October 2026 to cross-check fixtures, kickoff clocks, league standings, rankings,
  probable starters, and confirmed injury/absence lists across all 15 sports.</p>
</section>
<section class="panel">
  <h2>1. Official Governing-Body &amp; Primary Statistical Sources ({len(sources['official_sources'])})</h2>
  <div class="table-wrap">
    <table class="data">
      <thead><tr><th>ID</th><th>Sport</th><th>Authority / Database</th><th>Data Retrieved</th><th>Link</th></tr></thead>
      <tbody>{off_rows}</tbody>
    </table>
  </div>
</section>
<section class="panel">
  <h2>2. Reverse-Engineered OLBG Sport Hubs (15 Sports)</h2>
  <div class="table-wrap">
    <table class="data">
      <thead><tr><th>Sport</th><th>OLBG Hub URL</th></tr></thead>
      <tbody>{hub_rows}</tbody>
    </table>
  </div>
</section>
"""
    out_html = render_shell("Official Sources", "sources", "", "../", body, pick_counts, len(flags))
    with open(os.path.join(OCT_DIR, "sources.html"), "w", encoding="utf-8") as f:
        f.write(out_html)


def main():
    events = load_json("events.json")["events"]
    lines = load_json("lines.json")["lines"]
    picks = load_json("picks.json")["picks"]
    flags = load_json("flags.json")["flags"]
    sources = load_json("sources.json")
    audit = load_json("repo_audit.json")

    pick_counts = Counter(p["sport"] for p in picks)
    build_index(events, lines, picks, flags, sources, pick_counts)
    build_sport_pages(events, lines, picks, flags, sources, pick_counts)
    build_all_markets(lines, flags, pick_counts)
    build_flagged(lines, flags, pick_counts)
    build_repo_audit(audit, flags, pick_counts)
    build_methodology(flags, pick_counts)
    build_sources(sources, flags, pick_counts)
    print("Built root index.html + 20 pages under oct27/ (15 sport subpages + 5 reference pages).")


if __name__ == "__main__":
    main()

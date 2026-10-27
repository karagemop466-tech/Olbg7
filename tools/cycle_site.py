#!/usr/bin/env python3
"""Build the 2026-10-27 unified board at the repo root (the GitHub Pages root).

Pages written: index.html, all-events.html, sports/<15 slugs>.html, flagged.html,
sources.html, methodology.html  +  assets/cycle.css
Everything is generated from data/cycle-20261027/{events_raw,lines,predictions,sources,flags}.json.
"""
import html
import json
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/cycle-20261027")
CYCLE = "2026-10-27"

SPORTS = ["Golf", "Volleyball", "Rugby Union", "Cricket", "Snooker", "Darts", "Baseball",
          "Gaelic Sports", "Greyhounds", "Tennis", "Motor Racing", "Handball", "Ice Hockey",
          "Basketball", "Rugby League"]
SLUG = {s: s.lower().replace(" ", "-") for s in SPORTS}

# Governing-body pages that were actually read during this capture window. Rows in these
# sports get an official link; rows outside this map get the OLBG row only, plus the words
# "not confirmed against an official source at capture".
OFFICIAL_BY_SPORT = {
    "Baseball": ("https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule", "MLB.com"),
    "Basketball": ("https://www.euroleaguebasketball.net/en/euroleague/?pcode=005009", "EuroLeague (official)"),
    "Cricket": ("https://www.cricinfo.com/series/pakistan-odi-tri-series-2026-27-1550706/match-schedule-fixtures-and-results", "ESPNcricinfo"),
    "Darts": ("https://www.pdc.tv/news/2026/october/26/2026-players-championships-31-32-entries-confirmed", "PDC (official)"),
    "Gaelic Sports": ("https://www.gaa.ie/", "GAA (official)"),
    "Golf": ("https://www.lpga.com/tournaments/maybank-championship", "LPGA (official)"),
    "Handball": ("https://ehfcl.eurohandball.com/men/2026-27/standings/", "EHF (official)"),
    "Ice Hockey": ("https://www.nhl.com/standings", "NHL.com"),
    "Motor Racing": ("https://www.formula1.com/en/results/2026/drivers", "Formula1.com (official)"),
    "Rugby Union": ("https://www.unitedrugby.com/latest/news/2026-27-fixtures-in-full/", "United Rugby Championship (official)"),
    "Tennis": ("https://www.atptour.com/en/news/djokovic-basel-2026-first-match", "ATP Tour (official)"),
    "Volleyball": ("https://tvf.org.tr/icerik/efeler-liginde-birinci-hafta-sona-erdi", "Turkish Volleyball Federation"),
    "Rugby League": ("https://www.olbg.com/betting-tips/", "OLBG (no official league page read at capture)"),
}
OFFICIAL_BY_COMP = {
    "Finland SM Liiga": ("https://www.liiga.fi/en/schedule?kausi=2026-2027&sarja=runkosarja", "Liiga.fi (official)"),
    "Swedish Hockey League": ("https://stats.swehockey.se/ScheduleAndResults/Overview/20961", "SweHockey (official SHL stats)"),
    "NHL": ("https://www.nhl.com/standings", "NHL.com"),
    "Pro D2": ("https://prod2.lnr.fr/club/provence-rugby", "LNR Pro D2 (official)"),
    "URC": ("https://www.bbc.com/sport/rugby-union/pro-tournament/table", "BBC Sport (URC table)"),
    "Six Nations": ("https://www.olbg.com/betting-tips/", "OLBG (ante-post; no official table read)"),
    "DP World Tour": ("https://www.lpga.com/tournaments/maybank-championship", "LPGA (official - OLBG label says DP World Tour, see flag GOLF-001)"),
    "PGA Tour": ("https://www.olbg.com/betting-tips/", "OLBG (event not confirmable - flag GOLF-001)"),
    "Korn Ferry Tour": ("https://www.olbg.com/betting-tips/", "OLBG (event not confirmable - flag GOLF-001)"),
}


def esc(x):
    return html.escape(str(x if x is not None else ""), quote=True)


def price(dec):
    return "&mdash;" if dec in (None, "") else f"{dec:.2f}"


def american(a):
    if a is None:
        return "&mdash;"
    return f"+{a}" if a > 0 else f"{a}"


def pill(kind, text=None):
    t = text or kind
    return f'<span class="pill pill-{esc(kind.lower())}">{esc(t)}</span>'


def src_link(url, label, cls="srclink"):
    if not url:
        return '<span class="noblank" title="No official source was retrievable for this value at capture time">left blank</span>'
    return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'


def main():
    raw = json.load(open(os.path.join(OUT, "events_raw.json")))
    lines = json.load(open(os.path.join(OUT, "lines.json")))
    picks = json.load(open(os.path.join(OUT, "predictions.json")))["picks"]
    flags = json.load(open(os.path.join(OUT, "flags.json")))["flags"]
    sources = json.load(open(os.path.join(OUT, "sources.json")))["sources"]

    by_sport_rows = defaultdict(list)
    for r in lines["lines"]:
        by_sport_rows[r["sport"]].append(r)
    picks_by_sport = defaultdict(list)
    for p in picks:
        picks_by_sport[p["sport"]].append(p)
    flags_by_sport = defaultdict(list)
    for f in flags:
        flags_by_sport[f["sport"]].append(f)

    priced = [r for r in lines["lines"] if r.get("our_line")]
    unpriced = [r for r in lines["lines"] if not r.get("our_line")]
    hi = [p for p in picks if p["confidence"] == "high"]
    band_med = [p for p in picks if p["confidence"] == "medium" and p.get("our_line") and 1.40 <= p["our_line"] <= 101.0
                and p["grade"] in ("A", "B")]
    outside = [p for p in picks if p.get("our_line") and p["our_line"] < 1.40]

    # ---------------------------------------------------------------- index --
    nav = nav_html("index")
    t = [head(""), nav, f"""
<div class="hero">
  <div class="hero-kicker">Cycle {CYCLE} &middot; captured from olbg.com between 05:30 and 06:10 UTC</div>
  <h1>OLBG reverse-engineered: {lines['totals']['markets']} markets captured, {lines['totals']['priced']} lines originated, {len(picks)} written picks across {len(picks_by_sport)} of 15 sports</h1>
  <p class="hero-sub">Every line on this board is <strong>ours</strong>, originated from OLBG's printed tip votes.
  OLBG does not publish bookmaker prices in the HTML that can be read, so nothing here is a book quote.</p>
</div>

<div class="callout">
  <h2>Read this first &mdash; the four things that decide how to use this board</h2>
  <ol>
    <li><strong>Where the picks are:</strong> the executive table below lists all {len(picks)} written picks; each row
      links straight to the full write-up on that sport's page (<a href="#per-sport">per-sport summary</a>).</li>
    <li><strong>{len(hi)} pick{'s' if len(hi)!=1 else ''} cleared high confidence today</strong> &mdash; both in cricket.
      A line only earns that label with 8+ tips counted, a price inside &minus;250 to +10,000, and no structural defect
      in the market it came from.</li>
    <li><strong>The near-certainties are deliberately not sold as picks.</strong> The heaviest votes on this card
      (Afghanistan 15/16, Fernandez 10/12, KalPa 5/5, Ziraat 4/4, Antonelli 17/18) price between 1.15 and 1.36 &mdash;
      all shorter than the &minus;250 floor. They are shown in their own table so the reasoning is visible.</li>
    <li><strong>Two sports produced nothing</strong> (Snooker, Greyhounds: OLBG printed "No tips found."), and
      {len([f for f in flags])} items are flagged &mdash; including a handball market whose tip vote sits on the draw,
      a stale F1 comment thread and two contradictory French rugby tables. See
      <a href="flagged.html">Flagged for review</a>.</li>
  </ol>
</div>

<section id="picks">
  <h2>Today's picks &mdash; the whole set</h2>
  <p class="lede">Sorted high confidence first, then by how far our line sits from evens.
  "Our line" is decimal (American); "Tips" is what OLBG printed on that market; grade A/B/C is the reliability of the
  market structure, not of the prediction.</p>
  {exec_table(picks)}
</section>

<section id="high">
  <h2>Highest-confidence picks ({len(hi)})</h2>
  {''.join(pick_card(p, full=True) for p in hi) or '<p class="lede">None cleared the rule today.</p>'}
</section>

<section id="band">
  <h2>Actionable inside the focus band &mdash; medium confidence, grade A/B ({len(band_med)})</h2>
  <p class="lede">These are the lines where the brief's &minus;250 to +10,000 range and a usable sample both hold.
  Ranked by our own probability estimate.</p>
  {exec_table(sorted(band_med, key=lambda x: -(x['p_fair'] or 0)))}
</section>

<section id="outside">
  <h2>Strong, but priced short of the band &mdash; we decline these ({len(outside)})</h2>
  <p class="lede">The consensus is one-sided and our originated price is below &minus;250, so there is nothing to take.
  Published so the decision is auditable rather than hidden.</p>
  {exec_table(sorted(outside, key=lambda x: x['our_line'] or 99))}
</section>

<section id="per-sport">
  <h2>Per-sport summary</h2>
  <table class="tbl">
    <thead><tr><th>Sport</th><th>OLBG markets</th><th>Priced by us</th><th>Not priced</th>
      <th>Written picks</th><th>high / med / low</th><th>Grade A / B / C</th><th>Flags</th><th>Page</th></tr></thead>
    <tbody>"""]
    for s in SPORTS:
        rows = by_sport_rows.get(s, [])
        pr = [r for r in rows if r.get("our_line")]
        pk = picks_by_sport.get(s, [])
        cnt = {"high": 0, "medium": 0, "low": 0}
        for p in pk:
            cnt[p["confidence"]] = cnt.get(p["confidence"], 0) + 1
        gc = {"A": 0, "B": 0, "C": 0}
        for r in pr:
            gc[r["our_line"]["grade"]] = gc.get(r["our_line"]["grade"], 0) + 1
        fl = flags_by_sport.get(s, []) + flags_by_sport.get("All", []) + flags_by_sport.get("All outrights", [])
        t.append(f"""<tr><td><a class="sportlink" href="sports/{SLUG[s]}.html">{esc(s)}</a></td>
        <td class="num">{len(rows)}</td><td class="num">{len(pr)}</td>
        <td class="num">{len(rows)-len(pr)}</td><td class="num">{len(pk)}</td>
        <td class="num">{cnt.get('high',0)} / {cnt.get('medium',0)} / {cnt.get('low',0)}</td>
        <td class="num">{gc['A']} / {gc['B']} / {gc['C']}</td>
        <td class="num">{len(fl)}</td><td><a href="sports/{SLUG[s]}.html">open &rarr;</a></td></tr>""")
    t.append("""</tbody></table>
  <p class="lede">Snooker and Greyhounds show zero markets because the OLBG pages returned
  "No tips found." at capture &mdash; the empty slate is the finding, not a scrape failure.</p>
</section>

<section id="coverage">
  <h2>Coverage of the 15 sports in scope</h2>
  <table class="tbl">
    <thead><tr><th>#</th><th>Sport</th><th>OLBG page</th><th>Markets captured</th><th>Result</th></tr></thead>
    <tbody>""")
    for i, s in enumerate(SPORTS, 1):
        rows = by_sport_rows.get(s, [])
        note = (f"{len([r for r in rows if r.get('our_line')])} priced, {len(picks_by_sport.get(s, []))} written picks"
                if rows else "page rendered, no markets")
        if s in ("Snooker", "Greyhounds"):
            note = '<span class="flagged">empty slate &mdash; flagged SN-001 / G-001</span>'
        t.append(f"""<tr><td class="num">{i}</td><td>{esc(s)}</td>
        <td><a href="https://www.olbg.com/betting-tips/{esc(s.replace(' ','_'))}" target="_blank" rel="noopener">olbg.com &rsaquo; {esc(s)}</a></td>
        <td class="num">{len(rows)}</td><td>{note}</td></tr>""")
    t.append(f"""</tbody></table>
</section>

<section id="context">
  <h2>This board in context &mdash; every other board, still live and untouched</h2>
  <p class="lede">Four parallel sessions have published boards into this repository. None of them was overwritten by
  this cycle; they are listed here so the site has one front door instead of five.</p>
  <table class="tbl">
    <thead><tr><th>Board</th><th>What it is</th><th>Coverage</th><th>Status</th></tr></thead><tbody>
    <tr><td><a href="picks.html">picks.html</a> &middot; <a href="lines.html">lines.html</a> &middot;
      <a href="method.html">method.html</a> &middot; <a href="archive.html">archive.html</a></td>
      <td>The "Coverage Desk" snapshot of the 05:23 UTC manual capture. It is deliberately <em>fail-closed</em>: its
      script hides scheduled rows and notes after 28 October 2026 05:23 UTC, so those pages show less with time, not
      more. Its own summary states that no priced high-confidence pick was established there.</td>
      <td>54 listings with official schedule references, 71 listings flagged for time/fixture checks, 38 written leans</td>
      <td>Live and unchanged; intentionally expiring</td></tr>
    <tr><td><a href="board/all-markets.html">board/</a></td>
      <td>Session 81a54336's 27 October board: its own executive summary, all-markets table and flagged page</td>
      <td>Its full 27 Oct board exactly as published</td><td>Live, byte-for-byte as shipped</td></tr>
    <tr><td><a href="olbg-map.html">olbg-map.html</a> &middot; <a href="legacy-cal4/index.html">legacy-cal4/</a></td>
      <td>The reverse-engineered OLBG structure (URL grammar, sport ids, what each page returns) and the archived
      CAL-4 board kept behind historical warnings</td>
      <td>Structure reference + archived 26 October board</td><td>Live, preserved</td></tr>
    <tr><td><a href="olbg-tips/index.html">olbg-tips/</a> &middot; <a href="docs/index.html">docs/</a> &middot;
      <a href="docs/board-review/index.html">docs/board-review/</a></td>
      <td>The tip-consensus board, the first session's board and an independent board review with its own tiered
      rating method</td><td>127 market rows / 51 picks; 119 events / 44 predictions</td>
      <td>Live, preserved</td></tr>
    </tbody></table>
  <p class="lede">What is new on this front page is the 27 October re-capture itself: two-sided coverage read off
  OLBG's event pages (152 markets rather than the single most-tipped selection per event), the A/B/C reliability grade
  that blocks draw-clustered and 1-2-tip lines from high confidence, and 52 written predictions with a source link on
  every fact. The previous day's board is kept as the comparison baseline in
  <span class="mono">data/events.json</span> and <span class="mono">data/picks.json</span>.</p>
</section>

<section id="method">
  <h2>How the numbers were made</h2>
  <div class="grid2">
    <div class="boxcard">
      <h3>One formula, applied to every market</h3>
      <p class="mono">p_fair = (tips_on_pick + K &times; prior) / (tips_total + K), K = 6<br>
      our line = 1 / (p_fair &times; 1.05)</p>
      <p>prior is 1/2 for two-way markets, 1/3 where a draw is a listed outcome, 1/8 for outrights
      (field size is not printed &mdash; flagged U-004). A 0%/100% split can never earn high confidence, and grade C
      lines are blocked from it.</p>
      <p><a href="methodology.html">Full methodology &rarr;</a></p>
    </div>
    <div class="boxcard">
      <h3>What we refuse to do</h3>
      <ul>
        <li>No bookmaker price is quoted, because OLBG does not expose one in the retrievable page (flag U-001).</li>
        <li>No field is filled by inference. Anything unconfirmable is printed as
          {src_link('', '')} with the reason attached &mdash; {len(unpriced)} markets are unpriced for exactly that reason.</li>
        <li>No handball draw line is sold as a prediction, even though 11 of 15 handball markets vote for it (flag U-002).</li>
      </ul>
      <p><a href="flagged.html">Flagged for review ({len(flags)}) &rarr;</a> &middot;
         <a href="sources.html">Sources ({len(sources)}) &rarr;</a> &middot;
         <a href="all-events.html">Full market inventory ({len(lines['lines'])}) &rarr;</a></p>
    </div>
  </div>
</section>
{FOOT}""")
    write("index.html", "\n".join(t))

    # ------------------------------------------------------- per-sport pages --
    for s in SPORTS:
        rows = by_sport_rows.get(s, [])
        pr = [r for r in rows if r.get("our_line")]
        unp = [r for r in rows if not r.get("our_line")]
        pk = picks_by_sport.get(s, [])
        fl = flags_by_sport.get(s, [])
        off_url, off_lab = OFFICIAL_BY_SPORT[s] if s in OFFICIAL_BY_SPORT else ("", "")
        t = [head("../"), nav_slug(s), f"""
<div class="hero hero-sm">
  <div class="hero-kicker"><a href="../index.html">&larr; Executive summary</a> &middot; Sport page &middot; <a href="../all-events.html">all markets</a> &middot; <a href="../flagged.html">flagged</a></div>
  <h1>{esc(s)}</h1>
  <p class="hero-sub">{len(rows)} OLBG markets captured &middot; {len(pr)} priced by us &middot;
  {len(pk)} written pick{'s' if len(pk)!=1 else ''} &middot; {len(fl)} flag{'s' if len(fl)!=1 else ''}</p>
</div>"""]
        if not rows:
            t.append(f"""<div class="callout"><h2>No markets were printed for this sport at capture</h2>
<p>The OLBG {esc(s)} page rendered normally at 05:42&ndash;05:45 UTC on {CYCLE} and its entire body was the text
"No tips found." There is therefore nothing to price, no event to summarise and no pick to write. The empty slate is
recorded as a finding, not repaired by guessing.</p>
<ul><li>OLBG page: <a href="https://www.olbg.com/betting-tips/{esc(s.replace(' ','_'))}" target="_blank" rel="noopener">olbg.com &rsaquo; {esc(s)}</a></li>
<li>Related flag: <a href="../flagged.html">{'SN-001' if s=='Snooker' else 'G-001'}</a> &middot; <a href="../index.html">back to the executive summary</a></li></ul></div>""")
        if len(pk) < 5 and rows:
            events = len({r["event"] for r in rows})
            reasons = []
            if unp:
                reasons.append(f"{len(unp)} of those printed no tip split on either side, so they are listed unpriced "
                               f"rather than filled in")
            if events < 5:
                reasons.append(f"the card only carries {events} distinct event{'s' if events!=1 else ''} for this sport, "
                               f"so a fifth pick would mean inventing a fixture")
            if len(pr) < 5:
                reasons.append(f"only {len(pr)} market{'s' if len(pr)!=1 else ''} produced a priceable vote")
            thin = [x for x in pk if x["grade"] == "C"]
            if thin:
                reasons.append(f"{len(thin)} of the written picks sit on markets with 1-2 tips and are graded C, "
                               f"which the method will not promote")
            t.append(f"""<div class="callout"><h2>Why this page has {len(pk)} written pick{'s' if len(pk)!=1 else ''} and not five</h2>
<p class="small">OLBG printed {len(rows)} market{'s' if len(rows)!=1 else ''} for {esc(s)} in the {CYCLE} capture.
{'&nbsp;'.join(esc(r) for r in reasons).rstrip('. ').capitalize()}.</p>
<p class="small">Shortfalls are reported here and on <a href="../flagged.html">Flagged for review</a> instead of being
padded with extra selections from a single event.</p></div>""")
        if pk:
            t.append(f"""<section id="picks-{SLUG[s]}"><h2>The picks &mdash; {esc(s)}</h2>
<p class="lede">Each card is one written prediction: the selection, our originated price, the tip vote it came from,
the facts behind it with their sources, and the way it loses.</p>""")
            t += [pick_card(p, full=True) for p in pk]
            t.append("</section>")
            t.append(f"""<section id="summary-{SLUG[s]}"><h2>Pick table &mdash; {esc(s)}</h2>
{exec_table(pk, same_page=True)}</section>""")
        if pr:
            t.append(f"""<section id="markets-{SLUG[s]}"><h2>Every market we priced &mdash; {esc(s)}</h2>
<p class="lede">Two-sided wherever OLBG printed both sides. The 'Official source' column is the governing body we read
for that fixture family; where no official page could be read, the cell says so instead of linking something plausible.</p>
<table class="tbl tbl-wide"><thead><tr><th>Event</th><th>Market</th><th>Selection</th><th>Tips</th><th>Share</th>
<th>Structure</th><th>Our line</th><th>Am.</th><th>Implied</th><th>Conf.</th><th>Grade</th><th>OLBG row</th>
<th>Official source</th><th>Notes</th></tr></thead><tbody>""")
            for r in sorted(pr, key=lambda x: (-(x["our_line"]["p_fair"]), x["event"])):
                o = r["our_line"]
                ou, ol = official_for(r)
                t.append(f"""<tr>
<td>{esc(r['event'])}</td><td>{esc(r['market'])}</td><td><strong>{esc(r['selection'])}</strong></td>
<td class="num">{r['tips_on_pick']}/{r['tips_total']}</td>
<td class="num">{('&nbsp;' if r['pct'] is None else str(r['pct'])+'%')}</td>
<td class="small">{esc(o['structure'])}</td>
<td class="num strong">{price(o['card_decimal'])}</td><td class="num">{american(o['card_american'])}</td>
<td class="num">{o['implied_pct']}%</td>
<td>{pill(o['confidence'])}</td><td>{pill('grade'+o['grade'], o['grade'])}</td>
<td>{src_link(r['url'],'row')}</td><td>{src_link(ou, ol) if ou else '<span class="noblank">not confirmed at capture</span>'}</td>
<td class="small">{esc('; '.join(o['notes'])) or '&mdash;'}</td></tr>""")
            t.append("</tbody></table></section>")
        if unp:
            t.append(f"""<section id="unpriced-{SLUG[s]}"><h2>Markets we could not price &mdash; {esc(s)}</h2>
<p class="lede">These are real OLBG markets with no numeric signal in the retrievable page. The row is kept and the
reason is stated; nothing is filled in to make the table look complete.</p>
<table class="tbl"><thead><tr><th>Event</th><th>Market</th><th>Selection</th><th>Why there is no line</th><th>OLBG row</th></tr></thead><tbody>""")
            for r in unp:
                t.append(f"""<tr><td>{esc(r['event'])}</td><td>{esc(r['market'])}</td><td>{esc(r['selection'])}</td>
<td class="small">{esc(r.get('unpriced_reason') or 'no tip split printed')}</td><td>{src_link(r['url'],'row')}</td></tr>""")
            t.append("</tbody></table></section>")
        if fl:
            t.append(f"""<section id="flags-{SLUG[s]}"><h2>Flags touching {esc(s)}</h2>
{''.join(flag_block(f) for f in fl)}</section>""")
        t.append(FOOT)
        write(f"sports/{SLUG[s]}.html", "\n".join(t))

    # ----------------------------------------------------------- all-events --
    t = [head(""), nav, f"""<div class="hero hero-sm"><div class="hero-kicker"><a href="index.html">&larr; Executive summary</a></div>
<h1>Full market inventory &mdash; every OLBG row captured on {CYCLE}</h1>
<p class="hero-sub">{len(lines['lines'])} unique markets across 13 sports ({lines['duplicate_rows_removed']} duplicate
rows removed where the sport listing and the event page carried the same market). {len(pr_all(priced))} priced by us,
{len(unpriced)} left unpriced with the reason attached.</p></div>
<table class="tbl tbl-wide"><thead><tr><th>Sport</th><th>Competition</th><th>Event</th><th>Market</th><th>Selection</th>
<th>Tips</th><th>Our line</th><th>Conf.</th><th>Grade</th><th>OLBG row</th><th>Official source</th></tr></thead><tbody>"""]
    for r in sorted(lines["lines"], key=lambda x: (x["sport"], x["event"], str(x["market"]))):
        o = r.get("our_line") or {}
        ou, ol = official_for(r)
        t.append(f"""<tr><td><a href="sports/{SLUG[r['sport']]}.html">{esc(r['sport'])}</a></td>
<td class="small">{esc(r.get('competition') or '') or '<span class="noblank">not printed</span>'}</td>
<td>{esc(r['event'])}</td><td>{esc(r['market'])}</td><td>{esc(r['selection'])}</td>
<td class="num">{('%s/%s' % (r['tips_on_pick'], r['tips_total'])) if r['tips_total'] else '<span class="noblank">no split</span>'}</td>
<td class="num strong">{price(o.get('card_decimal')) if o else '<span class="noblank">not priced</span>'}</td>
<td>{pill(o['confidence']) if o else '&mdash;'}</td><td>{pill('grade'+o['grade'], o['grade']) if o else '&mdash;'}</td>
<td>{src_link(r['url'],'row')}</td>
<td>{src_link(ou, ol) if ou else '<span class="noblank">not confirmed at capture</span>'}</td></tr>""")
    t.append(f"""</tbody></table>
<p class="lede">Capture notes per batch: {esc(raw[0].get('capture_note',''))} (and the 06:10 UTC event-page batch for
handball, ice hockey, cricket and motor racing, which is where both sides of each market came from).</p>{FOOT}""")
    write("all-events.html", "\n".join(t))

    # -------------------------------------------------------------- flagged --
    blanks = []
    for r in lines["lines"]:
        if not r.get("competition"):
            blanks.append((r["sport"], r["event"], "Competition / league", r["url"]))
        if not r.get("our_line"):
            mk = r.get("market") or "market"
            sel = r.get("selection") or "selection"
            blanks.append((r["sport"], r["event"], f"Price for {mk} ({sel}) - {r.get('unpriced_reason') or 'no tip split printed'}", r["url"]))
    t = [head(""), nav, f"""<div class="hero hero-sm"><div class="hero-kicker"><a href="index.html">&larr; Executive summary</a></div>
<h1>Flagged for review</h1>
<p class="hero-sub">{len(flags)} flags raised on the {CYCLE} cycle, plus every field we deliberately left blank.
Nothing on this page is a hidden problem &mdash; each item says what we found, what we did about it and what the reader
should not rely on.</p></div>
<h2>Structural defects and conflicts</h2>
{''.join(flag_block(f, full=True) for f in flags)}
<h2>Register of blank cells</h2>
<p class="lede">A blank means "we could not confirm this from a source we could read", never "there is nothing here".
{len(blanks)} cells are blank on this cycle.</p>
<table class="tbl"><thead><tr><th>Sport</th><th>Event</th><th>Field left blank</th><th>Evidence row</th></tr></thead><tbody>"""]
    for b in blanks[:200]:
        t.append(f"<tr><td>{esc(b[0])}</td><td>{esc(b[1])}</td><td>{esc(b[2])}</td><td>{src_link(b[3],'OLBG row')}</td></tr>")
    t.append(f"""</tbody></table>
<p class="lede">Showing the first {min(200,len(blanks))} of {len(blanks)}. Most are the competition label OLBG omits on
its tennis, volleyball and cricket pages, or markets printed with no tip votes on either side.</p>{FOOT}""")
    write("flagged.html", "\n".join(t))

    # -------------------------------------------------------------- sources --
    by_dom = defaultdict(list)
    for s in sources:
        by_dom[s["url"].split("/")[2].replace("www.", "")].append(s)
    t = [head(""), nav, f"""<div class="hero hero-sm"><div class="hero-kicker"><a href="index.html">&larr; Executive summary</a></div>
<h1>Sources</h1>
<p class="hero-sub">{len(sources)} distinct sources behind the {CYCLE} cycle: the OLBG rows every price is built from,
plus the governing-body and news pages every fact in the write-ups came from. Grouped by domain so it is obvious which
claims rest on an official site and which do not.</p></div>"""]
    for dom in sorted(by_dom):
        group = by_dom[dom]
        t.append(f"""<h2>{esc(dom)} <span class="cnt">({len(group)})</span></h2>
<table class="tbl"><thead><tr><th>Page</th><th>Used for</th><th>Picks</th></tr></thead><tbody>""")
        for s in group:
            used = "<br>".join(esc(u) for u in s["used_for"][:6])
            extra_u = len(s["used_for"]) - 6
            if extra_u > 0:
                used += "<br><em>+" + str(extra_u) + " more</em>"
            pk_shown = ", ".join(s["picks"][:6])
            extra_p = len(s["picks"]) - 6
            if extra_p > 0:
                pk_shown += " +" + str(extra_p) + " more"
            t.append(f"""<tr><td><a href="{esc(s['url'])}" target="_blank" rel="noopener">{esc(s['site'] or s['url'])}</a>
<div class="small mono">{esc(s['url'])}</div></td><td class="small">{used}</td>
<td class="small mono">{esc(pk_shown)}</td></tr>""")
        t.append("</tbody></table>")
    t.append(FOOT)
    write("sources.html", "\n".join(t))

    # ---------------------------------------------------------- methodology --
    c = lines["constants"]
    t = [head(""), nav, f"""<div class="hero hero-sm"><div class="hero-kicker"><a href="index.html">&larr; Executive summary</a></div>
<h1>Methodology, and the rules we did not bend</h1></div>
<h2>1. What was captured</h2>
<p>Twelve OLBG tip pages were fetched on {CYCLE} between 05:30 and 05:50 UTC (Basketball 4, Ice Hockey 13, Tennis 3,
Rugby Union 9, Cricket 7, Volleyball 21, Baseball 12, Handball 20, Greyhounds 28, Snooker 8, Golf 5, plus Gaelic,
Motor Racing and Rugby League listings), and six OLBG event pages were then opened to read the <em>other</em> side of
each market: MIL @ TB (160799), BOS @ CAR (200104), PSG v Aalborg (12134), Wisla Plock v Nantes (12138),
South Africa v Australia (188835) and the F1 outright (912). That produced {len(lines['lines'])} unique market rows
after de-duplication, of which {len(priced)} carry a tip split we can price.</p>
<p>OLBG prints, for each market: the selection, "X / Y Win Tips", the share, a comment count and an event link. It does
<strong>not</strong> print a bookmaker price in the retrievable HTML &mdash; the odds widget is rendered client-side.
So the tip split is the only numeric market signal available, and every price on this board is derived from it
(flag U-001).</p>
<h2>2. How a line is originated</h2>
<p class="mono big">p_fair = (tips_on_pick + K &times; prior) / (tips_total + K) &nbsp;&nbsp;&nbsp; K = {c['K_pseudo_tips']}<br>
decimal line = 1 / (p_fair &times; (1 + {c['margin']})) &nbsp;&nbsp;&nbsp; margin = 5%<br>
American = (d&minus;1)&times;100 if d&ge;2 else &minus;100/(d&minus;1)</p>
<p>The K pseudo-tips are the whole trick: a market with 2 tips and 2 tips on one side would otherwise read as a 100%
probability, so it is pulled back to 0.625 with a 2-way prior and capped at medium confidence. Priors are
1/2 for two-way markets, 1/3 where OLBG lists a draw or tie as an outcome (all EHF handball money lines, and the
cricket Test, where a "Win Match" market and a "Draw" row both appear &mdash; a limited-overs match does not get a
1/3 prior because it cannot be drawn), and 1/8 for outrights because OLBG does not print the field size (U-004).</p>
<h2>3. Grades, confidence and the focus band</h2>
<table class="tbl"><thead><tr><th>Grade</th><th>Meaning</th><th>Effect</th></tr></thead><tbody>
<tr><td>{pill('gradeA','A')}</td><td>{c['min_tips_for_high']}+ tips counted on the market and no structural anomaly</td><td>eligible for high confidence</td></tr>
<tr><td>{pill('gradeB','B')}</td><td>3 to 7 tips</td><td>eligible for medium only</td></tr>
<tr><td>{pill('gradeC','C')}</td><td>under 3 tips, a degenerate 0%/100% split, or a 3-way draw cluster</td>
<td>high confidence blocked; shown with the defect named</td></tr></tbody></table>
<p>High confidence additionally requires a price inside the brief's &minus;250 to +10,000
focus band ({c['band_min_decimal']}&ndash;{c['band_max_decimal']} decimal) and a post-shrinkage probability of at least
60%. That is why the one-sided favourites are not the headline: a 94% vote prices at 1.16, which is outside the band by
construction, and the brief asks for high-confidence work <em>inside</em> the band rather than a list of 1.10s.</p>
<h2>4. Where we intervened in the data</h2>
<ul>
<li><strong>Handball.</strong> Eleven of fifteen priced handball markets are voted onto the "Tie" selection
(PSG v Aalborg 7/9, Plock v Nantes 8/11, Magdeburg 9/14&hellip;). The EHF's own group tables show a single drawn match
in thirty played in these groups, so those selections are graded C, capped at low confidence, and the team-side prices
are published instead. Flag U-002.</li>
<li><strong>Cricket.</strong> The Test match market is priced 3-way because OLBG prints a Draw row alongside it; the
Draw is quoted at 2.67 rather than being folded into a coin flip.</li>
<li><strong>Motor racing.</strong> The Antonelli "Top 6 finish" split is carried forward from the 26 October capture
and labelled as such; the OLBG comment thread on the outright quotes points totals that contradict the official
Formula&nbsp;1 timing sheet, and we used the official one. Flags U-006, U-007.</li>
<li><strong>Times.</strong> OLBG's printed card times are on a US-Eastern clock and are wrong for North American
fixtures in this capture (Game 4 printed 21:00 for an 8:00pm ET first pitch; NHL printed 20:07 for a 20:00 puck drop).
Every time in the copy comes from the governing body instead. Flag U-010.</li>
</ul>
<h2>5. Reproducing this cycle</h2>
<p class="mono big">python3 tools/unify_price.py &nbsp;# prices all {len(lines['lines'])} captured markets<br>
python3 tools/cycle_picks.py &nbsp;# attaches the {len(picks)} written picks, validates 30+ words, banned words, https sources<br>
python3 tools/cycle_site.py &nbsp;&nbsp;# rebuilds every page in this board<br>
python3 tools/check_cycle.py &nbsp;# link, coverage and field checks on the built site</p>
<p>Data files: <span class="mono">data/cycle-20261027/{{events_raw,lines,predictions,sources,flags}}.json</span></p>
{FOOT}"""]
    write("methodology.html", "\n".join(t))

    write("assets/cycle.css", CSS)
    print(f"index + {len(SPORTS)} sport pages + all-events + flagged + sources + methodology")


def voteinline(p):
    return "" if p.get("pct") is None else " (" + str(p["pct"]) + "%)"


def votepct(p):
    return "" if p.get("pct") is None else "<div class='small'>" + str(p["pct"]) + "%</div>"


def pr_all(x):
    return x


def official_for(r):
    comp = r.get("competition") or ""
    for key, val in OFFICIAL_BY_COMP.items():
        if key.lower() in comp.lower():
            return val
    return OFFICIAL_BY_SPORT.get(r["sport"], ("", ""))


def head(prefix=""):
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="OLBG reverse-engineered: 152 markets captured, 141 lines originated and 52 written predictions across the 15 OLBG sports, cycle 2026-10-27.">
<title>OLBG reverse-engineered &middot; daily board &middot; {CYCLE}</title>
<link rel="stylesheet" href="{prefix}assets/cycle.css">
</head><body class="cycle"><a class="sr-only" href="#main">Skip to the board</a><main id="main">"""


def exec_table(pk, same_page=False):
    if not pk:
        return '<p class="lede">No written picks for this slice.</p>'
    out = ["""<table class="tbl"><thead><tr><th>#</th><th>Sport</th><th>Event</th><th>Market</th>
<th>Our selection</th><th>Our line</th><th>Implied</th><th>OLBG tips</th><th>Conf.</th><th>Grade</th>
<th>Full write-up</th><th>Source</th></tr></thead><tbody>"""]
    for p in pk:
        off_url, off_lab = official_for({"sport": p["sport"], "competition": p.get("competition")})
        srcu, srcl = (p["facts"][0]["url"] or off_url, p["facts"][0]["site"] or off_lab) if p["facts"] else (off_url, off_lab)
        link = ("#" + p["id"]) if same_page else ("" if same_page else f"sports/{SLUG[p['sport']]}.html#{p['id']}")
        out.append(f"""<tr>
<td class="mono small">{esc(p['id'].split('-')[-1])}</td><td>{esc(p['sport'])}</td>
<td>{esc(p['event'])}</td><td class="small">{esc(p['market'])}</td>
<td><strong>{esc(p['selection'])}</strong><div class="small">{esc(p['pick_label'])}</div></td>
<td class="num strong">{price(p['our_line'])}<div class="small">{american(p['our_line_american'])}</div></td>
<td class="num">{p['implied_pct']}%</td>
<td class="num">{p['tips_on_pick']}/{p['tips_total']}{votepct(p)}</td>
<td>{pill(p['confidence'])}</td><td>{pill('grade'+p['grade'], p['grade'])}</td>
<td><a href="{link}">read &rarr;</a></td>
<td>{src_link(srcu, srcl)}</td></tr>""")
    out.append("</tbody></table>")
    return "\n".join(out)


def pick_card(p, full=False):
    notes = "".join(f'<li class="notechip">{esc(n)}</li>' for n in p.get("notes", []))
    facts = "".join(
        f'<li>{esc(f["text"])} {src_link(f["url"], f["site"] or "source")}</li>' if True else ""
        for f in p["facts"])
    off_url, off_lab = official_for({"sport": p["sport"], "competition": p.get("competition")})
    return f"""<article class="pickcard" id="{esc(p['id'])}">
<header>
  <div class="pick-sport">{esc(p['sport'])} &middot; {esc(p['competition'] or 'competition not printed on the card')}</div>
  <h3>{esc(p['pick_label'])}</h3>
  <div class="chips">
    {pill(p['confidence'])} {pill('grade'+p['grade'], 'grade '+p['grade'])}
    <span class="chip chip-price">our line {price(p['our_line'])} / {american(p['our_line_american'])}</span>
    <span class="chip">implied {p['implied_pct']}%</span>
    <span class="chip">OLBG vote {p['tips_on_pick']}/{p['tips_total']}{voteinline(p)}</span>
    <span class="chip">{esc(p['structure'])}</span>
  </div>
</header>
<p class="prediction">{esc(p['prediction'])}</p>
<div class="grid2">
  <div><h4>Why this is a lean</h4><p class="small">{esc(p['angle'])}</p></div>
  <div><h4>Where it can miss</h4><p class="small">{esc(p['risk'])}</p></div>
</div>
<h4>Facts behind this pick, each with its own source</h4>
<ul class="facts">{facts}</ul>
{f'<ul class="notes">{notes}</ul>' if notes else ''}
<p class="rowlinks">Event: <strong>{esc(p['event'])}</strong> &middot; market: <strong>{esc(p['market'])}</strong>
 &middot; <a href="{esc(p['olbg_url'])}" target="_blank" rel="noopener">OLBG row</a>
 &middot; {src_link(off_url, off_lab + ' (fixture family)') if off_url else src_link('','')}</p>
</article>"""


def flag_block(f, full=False):
    extra = f'<p class="small">{esc(f["action"])}</p>'
    src = src_link(f["source"][0], f["source"][1]) if f["source"][0] else ""
    return f"""<div class="flagcard sev-{esc(f['severity'])}">
<h3>{esc(f['id'])} &middot; {esc(f['title'])}</h3>
<p class="small"><span class="chip">{esc(f['sport'])}</span> {pill('sev'+f['severity'][:1].upper(), f['severity'])}</p>
<p>{esc(f['detail'])}</p>{extra}{f'<p class="rowlinks">{src}</p>' if src else ''}</div>"""


def nav_html(active="index", prefix=""):
    items = [(prefix + "index.html", "Executive summary"), (prefix + "all-events.html", "All markets"),
             (prefix + "flagged.html", "Flagged"), (prefix + "sources.html", "Sources"),
             (prefix + "methodology.html", "Methodology")]
    sport_links = "".join(f'<a href="{prefix}sports/{SLUG[s]}.html">{esc(s)}</a>' for s in SPORTS)
    return f"""<nav class="topnav"><div class="navin">
<span class="brand"><a href="{prefix}index.html">OLBG&nbsp;Board</a> <em>{CYCLE}</em></span>
<span class="navlinks">{''.join(f'<a href="{h}"{" class=on" if h.startswith("index") and active=="index" else ""}>{esc(t)}</a>' for h,t in items)}</span>
</div><div class="navsports">{sport_links}</div></nav>"""


def nav_slug(s):
    return nav_html(s, prefix="../")


write_cache = {}


def write(rel, body):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(body)
    write_cache[rel] = len(body)


HEAD = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>OLBG reverse-engineered &middot; daily board &middot; 2026-10-27</title>
<link rel="stylesheet" href="assets/cycle.css">
</head><body class="cycle">"""

FOOT = """</main><footer class="foot">
<p>Built from olbg.com captures of 27 October 2026 (05:30&ndash;06:10 UTC) by tools/unify_price.py,
tools/cycle_picks.py and tools/cycle_site.py. Prices on this site are originated lines, not bookmaker quotes;
unconfirmable values are printed blank and flagged. Data: <span class="mono">data/cycle-20261027/</span>.</p>
</footer></body></html>"""

CSS = """
body.cycle{font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
 color:#16181d;background:#f6f7f9;margin:0}
body.cycle .wrap,body.cycle main{max-width:1180px}
body.cycle{padding:0 18px 60px}
body.cycle h1{font-size:31px;line-height:1.18;margin:.35em 0 .25em;letter-spacing:-.4px}
body.cycle h2{font-size:21px;margin:1.7em 0 .5em;letter-spacing:-.2px}
body.cycle h3{font-size:17px;margin:.2em 0 .35em}
body.cycle h4{font-size:12.5px;text-transform:uppercase;letter-spacing:.7px;color:#5a6070;margin:1.1em 0 .3em}
body.cycle p.lede{color:#4a5162;max-width:78ch}
.topnav{position:sticky;top:0;z-index:20;background:#101828;color:#e9edf5;padding:8px 18px 0;
 box-shadow:0 1px 0 rgba(255,255,255,.08) inset}
.navin{max-width:1180px;margin:0 auto;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.brand{font-weight:700;letter-spacing:-.2px}
.brand a{color:#fff;text-decoration:none}
.brand em{font-style:normal;color:#9fb0cc;font-weight:500;font-size:12.5px;margin-left:6px}
.navlinks{display:flex;gap:14px;margin-left:auto;flex-wrap:wrap}
.navlinks a{color:#c9d5ea;text-decoration:none;font-size:13.5px;padding:6px 2px;border-bottom:2px solid transparent}
.navlinks a:hover,.navlinks a.on{color:#fff;border-color:#4c8dff}
.navsports{max-width:1180px;margin:6px auto 0;display:flex;flex-wrap:wrap;gap:4px;padding-bottom:8px}
.navsports a{font-size:12px;color:#aebbd4;text-decoration:none;background:#1b2637;border:1px solid #26344c;
 border-radius:999px;padding:2px 9px}
.navsports a:hover{background:#2a3b56;color:#fff}
.hero,.hero-sm{max-width:1180px;margin:26px auto 8px}
.hero-kicker{font-size:12.5px;color:#68708a;text-transform:uppercase;letter-spacing:.8px}
.hero-sub{color:#454d61;max-width:82ch;font-size:15.5px}
.hero-sm h1{font-size:26px}
.callout{max-width:1180px;margin:20px auto;background:#fff;border:1px solid #dfe3ea;border-left:4px solid #1f5eff;
 border-radius:10px;padding:16px 20px;box-shadow:0 1px 2px rgba(16,24,40,.05)}
.callout h2{margin:0 0 .4em;font-size:17px}
.callout ol{margin:0;padding-left:1.2em}
.callout li{margin:.45em 0;color:#2a3040}
section{max-width:1180px;margin:0 auto}
.tbl{width:100%;border-collapse:collapse;background:#fff;border:1px solid #dfe3ea;border-radius:10px;
 overflow:hidden;font-size:13.5px}
.tbl th{background:#eef1f6;text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.55px;
 color:#515a6d;padding:7px 9px;border-bottom:1px solid #dfe3ea;position:sticky;top:0}
.tbl td{padding:8px 9px;border-bottom:1px solid #eef0f4;vertical-align:top}
.tbl tr:nth-child(even) td{background:#fbfcfd}
.tbl .num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tbl .strong{font-weight:650}
.tbl .small,.small{font-size:12px;color:#5f6779}
.tbl-wide{font-size:12.5px}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12px}
.mono.big{font-size:13px;background:#0f1729;color:#dfe7f6;padding:12px 14px;border-radius:8px;display:inline-block}
.pill{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;
 padding:2px 8px;border-radius:999px;white-space:nowrap}
.pill-high{background:#dcfce7;color:#14532d}.pill-medium{background:#fef3c7;color:#78350f}
.pill-low{background:#fde3e3;color:#7f1d1d}
.pill-gradeA{background:#e0e9ff;color:#1e3a8a}.pill-gradeB{background:#eef1f6;color:#3d4557}
.pill-gradeC{background:#f3e0e6;color:#7d2043}
.pill-S{background:#fff7e6;color:#8a5a00}.pill-M{background:#eef1f6;color:#3d4557}.pill-L{background:#f3e0e6;color:#7d2043}
.pill-sevS{background:#ffe4e6;color:#881337}.pill-sevD{background:#fff2d9;color:#7c4a03}.pill-sevM{background:#e6f0ff;color:#1e3a8a}
.pill-sevB{background:#eaf2ff;color:#243b6b}.pill-sevC{background:#f0ecff;color:#3f3391}
.pill-sevE{background:#eceff5;color:#3f4757}
.chip{display:inline-block;font-size:11.5px;color:#38415a;background:#eef1f6;border-radius:999px;padding:2px 9px;margin:1px 2px 1px 0}
.chip-price{background:#101828;color:#fff;font-weight:650}
.pickcard{background:#fff;border:1px solid #dfe3ea;border-radius:12px;padding:16px 20px 18px;margin:14px 0;
 box-shadow:0 1px 2px rgba(16,24,40,.05)}
.pickcard header{border-bottom:1px solid #eef0f4;padding-bottom:10px;margin-bottom:10px}
.pick-sport{font-size:11.5px;text-transform:uppercase;letter-spacing:.7px;color:#6a7288}
.prediction{font-size:15.5px;color:#12161f;background:#f7f9ff;border-left:3px solid #1f5eff;padding:10px 14px;border-radius:0 8px 8px 0}
.facts{margin:.3em 0 0;padding-left:1.1em}
.facts li{margin:.35em 0;color:#2b3242;font-size:13.5px}
.notes{margin:.6em 0 0;padding-left:0;list-style:none}
.notechip{display:inline-block;font-size:11.5px;background:#fff6e6;color:#7a4b00;border:1px solid #f3e0bb;
 border-radius:6px;padding:2px 7px;margin:2px 4px 0 0}
.rowlinks{font-size:12.5px;color:#5f6779;margin:.9em 0 0}
.srclink{color:#1f4fd8;text-decoration:none;border-bottom:1px dotted #9db8f0;white-space:nowrap}
.srclink:hover{border-bottom-style:solid}
.noblank{color:#8b93a7;font-style:italic;font-size:12px;border-bottom:1px dotted #c3c9d6}
.flagged{color:#881337;font-weight:650}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.boxcard{background:#fff;border:1px solid #dfe3ea;border-radius:12px;padding:14px 18px;margin:12px 0}
.flagcard{background:#fff;border:1px solid #dfe3ea;border-left:4px solid #b30021;border-radius:10px;padding:12px 18px 14px;margin:12px 0}
.flagcard h3{font-size:15.5px}
.flagcard p{color:#333b4d;font-size:13.8px}
.sev-conflict{border-left-color:#c2410c}.sev-defect{border-left-color:#b30021}.sev-empty{border-left-color:#6b7280}
.sev-method{border-left-color:#1f5eff}.sev-data,.sev-blank{border-left-color:#a16207}
.cnt{font-size:12px;color:#6a7288;font-weight:500}
.sportlink{color:#101828;font-weight:650;text-decoration:none;border-bottom:1px solid #cdd6e6}
.sr-only{position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden}
.sr-only:focus{left:8px;top:8px;width:auto;height:auto;background:#fff;padding:6px 10px;z-index:60;border-radius:6px}
.foot{max-width:1180px;margin:36px auto 0;border-top:1px solid #dfe3ea;padding-top:12px;color:#66708a;font-size:12.5px}
a{color:#1f4fd8}
@media (max-width:900px){.grid2{grid-template-columns:1fr}.tbl{font-size:12.5px}.navsports{display:none}}
"""

if __name__ == "__main__":
    main()

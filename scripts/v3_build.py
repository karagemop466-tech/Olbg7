#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3 build - turn data/v3/{events,lines,picks,flags}.json into the site.

The complaint about the four boards that were live was that it is not obvious
what the matches are or where the picks are. This build answers that directly:

  index.html      executive summary, the highest-confidence picks written out
  picks.html      all 65 written predictions, five per sport
  sports/<s>.html one page per sport: the 5 picks, then every market we swept
  lines.html      all 115 markets and the price we originated for each
  flagged.html    every irregularity, with sources
  method.html     how the two tracks work and what the gates are
  sources.html    every official source used, deduplicated
  archive.html    the four boards this one replaces

No price here is a bookmaker price. OLBG renders those client-side, so they are
absent from retrievable HTML and every number is originated by us.
"""
import html, json, os, re, shutil, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "v3")   # our own namespace; the repo root is shared output
DATA = os.path.join(ROOT, "data", "v3")

SLUG = {
    "Baseball": "baseball", "Basketball": "basketball", "Cricket": "cricket",
    "Darts": "darts", "Gaelic Sports": "gaelic-sports", "Golf": "golf",
    "Greyhounds": "greyhounds", "Handball": "handball", "Ice Hockey": "ice-hockey",
    "Motor Racing": "motor-racing", "Rugby League": "rugby-league",
    "Rugby Union": "rugby-union", "Snooker": "snooker", "Tennis": "tennis",
    "Volleyball": "volleyball",
}
SPORTS = ["Cricket", "Basketball", "Ice Hockey", "Rugby Union", "Handball", "Tennis",
          "Volleyball", "Golf", "Darts", "Baseball", "Motor Racing", "Rugby League",
          "Gaelic Sports", "Snooker", "Greyhounds"]
SPORT_NOTE = {
    "Snooker": ("OLBG's Snooker board prints the literal string 'No tips found.' on both the "
                "sport root and the All_Events listing. There is no fixture and no tip data to "
                "price, so no picks are published for this sport. We do not pad an empty board "
                "with invented matches."),
    "Greyhounds": ("OLBG's Greyhounds board carried 8 tip-able events on 26 October and 0 on "
                   "27 October; both the root board and the All_Events listing print 'No tips "
                   "found.' The sweep was repeated and the empty state is what OLBG serves. No "
                   "picks are published for this sport."),
}
TIER_LABEL = {"A": "A \u00b7 20+ tips", "B": "B \u00b7 8-19 tips",
              "C": "C \u00b7 4-7 tips", "D": "D \u00b7 under 4 tips",
              "R": "R \u00b7 our own origination"}


def e(x):
    return html.escape(str(x if x is not None else ""))


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def tag_picks(picks):
    """Give every pick a stable per-sport id, used for anchors across the site."""
    seen = collections.Counter()
    for p in picks:
        seen[p["sport"]] += 1
        # the full slug, not a truncation of it: "rugby-union" and "rugby-league"
        # both start with "rug" and would collide.
        p["id"] = "%s-%02d" % (SLUG[p["sport"]], seen[p["sport"]])
        # the pick files store sources as [label, url] pairs; normalise to dicts
        p["sources"] = [{"label": s[0], "url": s[1]} if isinstance(s, (list, tuple))
                        else s for s in p["sources"]]
    return picks


def counts(lines):
    L = lines["lines"]
    tier = collections.Counter(r.get("tier") or "?" for r in L)
    return {
        "total": len(L),
        "priced": sum(1 for r in L if r.get("fair_american") or rlines(r)),
        "blank": sum(1 for r in L if not (r.get("fair_american") or rlines(r))),
        "in_band": sum(1 for r in L if r.get("in_band") or (
            rlines(r) and -250 <= min(abs(int(v[1])) for v in rlines(r).values()) <= 10000)),
        "track_T": sum(1 for r in L if r.get("track") == "T"),
        "track_R": sum(1 for r in L if r.get("track") == "R"),
        "defective": sum(1 for r in L if r.get("olbg_defect")),
        "sports": sorted({r["sport"] for r in L}),
        "tier": {k: tier.get(k, 0) for k in "ABCDR"},
    }


CSS = """
.bet{display:flex;flex-wrap:wrap;gap:0;margin:10px 0 4px;border:1px solid var(--line);
border-radius:9px;overflow:hidden;background:#fbfcfd}
.bet>div{flex:1 1 140px;padding:8px 12px;border-right:1px solid var(--line)}
.bet>div:last-child{border-right:none}
.bet .l{display:block;font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);font-weight:650}
.bet .v{display:block;font-size:16px;font-weight:700;font-variant-numeric:tabular-nums;margin-top:1px}
.bet .thebet .v{color:var(--accent);font-size:14.5px;font-weight:700;line-height:1.3}
.card.pick{border-left:4px solid var(--line)}
.card.pick.HIGH{border-left-color:var(--high)}
.card.pick.MEDIUM{border-left-color:var(--med)}
.card.pick.LOW{border-left-color:var(--low)}
.card .hd{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:3px}
.card .hd h4{margin:0;font-size:16px}
.srcs{font-size:12.2px;color:var(--muted);margin-top:8px;border-top:1px dashed var(--line);padding-top:7px}
.srcs a{margin-right:2px}
.pill.tr{background:#eef3ff;color:#1b4fd8}
.pill.band{background:#e8f6ee;color:#0d7a45}
.pill.noband{background:#fdecec;color:#a12626}
.pill.blank{background:#f0f3f7;color:#5b6675}
.sports{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px;margin:14px 0}
.sportcard{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;
text-decoration:none;color:inherit;display:block}
.sportcard:hover{border-color:var(--accent)}
.sportcard .nm{font-weight:650;font-size:14.5px}
.sportcard .ct{font-size:12px;color:var(--muted);margin-top:2px}
.sportcard .hg{margin-top:7px}
details.sum{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:11px 14px;margin:10px 0}
details.sum summary{cursor:pointer;font-weight:650;font-size:14px}
.jump{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.jump a{font-size:12.5px;padding:4px 10px;border:1px solid var(--line);border-radius:99px;
text-decoration:none;color:var(--muted);background:var(--card)}
.jump a:hover{border-color:var(--accent);color:var(--accent)}
h2.anchor{scroll-margin-top:14px}
.tnote{font-size:12.8px;color:#3d4756;margin:4px 0 12px;max-width:960px}
.origbox{background:#f7f9fc;border:1px solid var(--line);border-radius:9px;padding:9px 12px;margin:7px 0;font-size:12.5px}
.origbox b{font-variant-numeric:tabular-nums}
code{background:#f0f3f7;padding:1px 5px;border-radius:4px;font-size:12.5px}
@media(max-width:620px){.bet>div{flex:1 1 100%;border-right:none;border-bottom:1px solid var(--line)}}
"""


def page(title, crumb, body, depth=0, on=None):
    p = "../" * depth
    nav = [('Main dashboard', p + '../index.html', 'root'),
           ('This board', p + 'index.html', 'home'),
           ('The picks', p + 'picks.html', 'picks'),
           ('Every line', p + 'lines.html', 'lines')]
    for s in SPORTS:
        nav.append((s, p + 'sports/' + SLUG[s] + '.html', 'sport-' + SLUG[s]))
    nav += [('Flagged for review', p + 'flagged.html', 'flagged'),
            ('Method', p + 'method.html', 'method'),
            ('Sources', p + 'sources.html', 'sources'),
            ('Archive', p + 'archive.html', 'archive')]
    links = "".join('<a href="%s"%s>%s</a>' % (e(u), ' class="on"' if k == on else '', e(t))
                    for t, u, k in nav)
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<link rel="stylesheet" href="%sassets/style.css">
<link rel="stylesheet" href="%sassets/v3.css">
</head><body>
<header><div class="wrap"><div>
<h1>OLBG reverse-engineered &mdash; 27 October 2026</h1>
<div class="sub">%s &nbsp;&middot;&nbsp; 15 sports &middot; 115 markets swept &middot; 65 written picks &middot; every price originated by us</div>
</div></div></header>
<nav><div class="wrap">%s</div></nav>
<main>
%s
</main>
<footer>
<p>Swept from <a href="https://www.olbg.com/betting-tips/">olbg.com/betting-tips</a> on 27 October 2026.
No price on this site is a bookmaker price: OLBG renders those client-side and they are absent from
retrievable HTML, so every number here is originated by us, either from the tip share OLBG prints
(Track&nbsp;T) or from an official competition table, ranking or points record (Track&nbsp;R).
Values that could not be confirmed from an official source are left blank and listed on the
<a href="%sflagged.html">Flagged for Review</a> page &mdash; they are never inferred.
See <a href="%smethod.html">Method</a> and <a href="%ssources.html">Sources</a>.</p>
</footer></body></html>
""" % (e(title), p, p, e(crumb), links, body, p, p, p)


def pill(conf):
    return '<span class="pill %s">%s</span>' % (conf.lower(), conf.title())


def band_pill(p):
    if not p["line"]:
        return '<span class="pill blank">no price</span>'
    return ('<span class="pill band">in band</span>' if p["in_band"]
            else '<span class="pill noband">outside band</span>')


def pick_card(p, show_sport=False):
    sp = ('<span class="pill tr">%s</span>' % e(p["sport"])) if show_sport else ''
    prob = ('%.1f%%' % (p["probability"] * 100)) if p["probability"] is not None else '&mdash;'
    meta = " &middot; ".join(x for x in [
        e(p["competition"]) if p["competition"] else '<span class="muted">competition not confirmed</span>',
        e(p["when"]), e(p["venue"]), e(p["market"])] if x)
    srcs = " &middot; ".join('<a href="%s">%s</a>' % (e(s["url"]), e(s["label"])) for s in p["sources"])
    flag = ('<div class="note flag small"><b>Flagged:</b> %s</div>' % e(p["flag"])) if p.get("flag") else ''
    return """<div class="card pick %s" id="%s">
<div class="hd">%s<span class="pill tr">Track %s</span>%s%s</div>
<h4>%s</h4>
<div class="meta">%s</div>
<div class="bet">
<div class="thebet"><span class="l">The bet</span><span class="v">%s</span></div>
<div><span class="l">Our line</span><span class="v">%s</span></div>
<div><span class="l">Implied chance</span><span class="v">%s</span></div>
<div><span class="l">OLBG tips</span><span class="v" style="font-size:12.5px;font-weight:600">%s</span></div>
</div>
<p class="pred">%s</p>
%s
<div class="srcs"><b>Sources</b> &nbsp;%s</div>
</div>""" % (p["confidence"], e(p["id"]), pill(p["confidence"]), e(p["track"]),
             band_pill(p), sp, e(p["event"]), meta, e(p["selection"]),
             e(p["line"]) if p["line"] else "blank", prob, e(p["olbg"]),
             e(p["text"]), flag, srcs)


def kpi(n, label):
    return '<div class="kpi"><div class="n">%s</div><div class="l">%s</div></div>' % (n, e(label))


def jumpbar(picks, depth=0):
    p = "../" * depth
    out = []
    for s in SPORTS:
        n = sum(1 for x in picks if x["sport"] == s)
        h = sum(1 for x in picks if x["sport"] == s and x["confidence"] == "HIGH")
        out.append('<a href="%ssports/%s.html">%s &middot; %d pick%s%s</a>'
                   % (p, SLUG[s], e(s), n, "" if n == 1 else "s",
                      (" &middot; %d high" % h) if h else ""))
    return '<div class="jump">%s</div>' % "".join(out)


def orig_box(r):
    """Render a Track R row's own line map, which is where the real story lives."""
    lm = rlines(r)
    if not lm:
        return ""
    bits = []
    for k, v in lm.items():
        bits.append('<span>%s <b>%s</b> <span class="muted">(%.1f%%)</span></span>'
                    % (e(k), e(v[1]), v[0] * 100))
    defect = ('<div class="small" style="margin-top:5px;color:#a12626"><b>OLBG defect:</b> %s</div>'
              % e(r["olbg_defect"])) if r.get("olbg_defect") else ""
    return '<div class="origbox"><b>Our own line for this market:</b> %s%s</div>' % (
        " &nbsp;&middot;&nbsp; ".join(bits), defect)


# ------------------------------------------------------------------- page: home
def build_index(picks, lines, flags, C):
    hi = [p for p in picks if p["confidence"] == "HIGH"]
    per = {s: [p for p in picks if p["sport"] == s] for s in SPORTS}
    rows = []
    for p in hi:
        rows.append("<tr><td>%s</td><td><a href=\"sports/%s.html#%s\">%s</a>"
                    "<div class=\"small muted\">%s</div></td><td><b>%s</b></td>"
                    "<td class=\"num\"><b>%s</b></td><td><span class=\"pill tr\">Track %s</span></td>"
                    "<td class=\"small muted\">%s</td></tr>"
                    % (e(p["sport"]), SLUG[p["sport"]], e(p["id"]), e(p["event"]),
                       e(p["competition"]), e(p["selection"]), e(p["line"]),
                       e(p["track"]), e(p["olbg"])))
    cards = []
    for p in hi:
        cards.append('<h3 class="anchor" id="hi-%s">%s &middot; %s</h3>' % (
            e(p["id"]), e(p["sport"]), e(p["selection"])) + pick_card(p))
    sc = []
    for s in SPORTS:
        n = len(per[s]); h = sum(1 for x in per[s] if x["confidence"] == "HIGH")
        sc.append('<a class="sportcard" href="sports/%s.html"><div class="nm">%s</div>'
                  '<div class="ct">%d written pick%s &middot; %d market%s swept</div>'
                  '<div class="hg">%s</div></a>'
                  % (SLUG[s], e(s), n, "" if n == 1 else "s",
                     sum(1 for r in lines["lines"] if r["sport"] == s),
                     "" if sum(1 for r in lines["lines"] if r["sport"] == s) == 1 else "s",
                     (pill("HIGH") + " %d" % h) if h else '<span class="pill blank">no OLBG tips</span>'))
    body = """
<p class="lede"><b>What this is.</b> We swept every tip-able market OLBG publishes across fifteen
sports on 27 October 2026 &mdash; %d markets in total &mdash; originated our own betting line for
every one we could source, picked a side in each match we could price, and wrote a prediction for
each pick. Five written picks per sport. Nothing below is a bookmaker price.</p>
<div class="grid">%s%s%s%s%s%s</div>

<h2>Where the picks are</h2>
<p class="tnote"><a href="picks.html"><b>All %d written predictions &rarr;</b></a> &nbsp;
<a href="lines.html">every one of the %d markets and our price for each &rarr;</a> &nbsp;
<a href="flagged.html">the %d irregularities &rarr;</a> &nbsp;
<a href="method.html">how each price was built &rarr;</a> &nbsp;
<a href="sources.html">every official source &rarr;</a></p>
%s

<h2>The %d highest-confidence picks</h2>
<p class="tnote">A pick is graded high only when all five gates hold: our fair price sits between
-250 and +10000; at least one official source corroborates the direction; the row is not hit by a
known OLBG display defect; the sample is eight or more tips, or a Track&nbsp;R line built from an
official competition table; and the implied chance clears 0.55 on match markets, or 0.40 on
outrights with five or fewer live contenders. Full wording on <a href="method.html">Method</a>.</p>
<table><thead><tr><th>Sport</th><th>Match</th><th>The bet</th><th>Our line</th><th>Track</th>
<th>OLBG tips</th></tr></thead><tbody>%s</tbody></table>

<h2>Every sport</h2>
<div class="sports">%s</div>

<h2>The high-confidence picks, written out in full</h2>
%s
""" % (C["total"],
       kpi(len(picks), "written picks, five per sport"),
       kpi(len(hi), "high confidence"),
       kpi(C["priced"], "of %d markets priced" % C["total"]),
       kpi(C["in_band"], "prices inside -250 to +10000"),
       kpi(flags["counts"]["total"], "irregularities flagged"),
       kpi(2, "sports where OLBG carries no tips"),
       len(picks), C["total"], flags["counts"]["total"],
       jumpbar(picks), len(hi), "".join(rows), "".join(sc), "".join(cards))
    return page("OLBG reverse-engineered - executive summary", "Executive summary", body, 0, "home")


# ------------------------------------------------------------------ page: picks
def build_picks(picks):
    out = ['<p class="lede">All %d written predictions, five per sport. Each one names the side we '
           'are backing, the market it is backed in, the price we originated for it, the OLBG tip '
           'count behind it, and at least one official source for every factual claim in the text. '
           'The shortest is 91 words. Snooker and Greyhounds carry none because OLBG publishes no '
           'events for either on this date &mdash; that is reported, not padded out.</p>' % len(picks),
           jumpbar(picks)]
    for s in SPORTS:
        rows = [p for p in picks if p["sport"] == s]
        out.append('<h2 class="anchor" id="%s">%s</h2>' % (SLUG[s], e(s)))
        out.append('<p class="tnote">%d written pick%s &middot; <a href="sports/%s.html">full %s '
                   'page, including every market we swept &rarr;</a></p>'
                   % (len(rows), "" if len(rows) == 1 else "s", SLUG[s], e(s)))
        if not rows:
            out.append('<div class="note flag">%s</div>' % e(SPORT_NOTE[s]))
        for p in rows:
            out.append(pick_card(p))
    return page("Every pick", "All %d written predictions" % len(picks), "".join(out), 0, "picks")


# --------------------------------------------------------------- page: per sport
def rlines(r):
    """The Track R line map. The engine writes it as orig_lines; lines is the older key."""
    return r.get("orig_lines") or r.get("lines") or {}


def priced(r):
    """A row counts as priced if it carries a headline price or a Track R line map.

    Golf and the F1 outrights publish Track R as primary, so fair_american is
    blank even though we originated a real price. Counting only fair_american
    made the Golf page claim '0 priced by us' while showing +481 for Clark.
    """
    return bool(r.get("fair_american")) or bool(rlines(r))


def headline(r):
    """The price to show in the Our-line column, Track R included."""
    if r.get("fair_american"):
        return r["fair_american"], bool(r.get("in_band"))
    lm = rlines(r)
    if lm:
        # the shortest price we originate is the side we are actually pointing at
        best = min(lm.items(), key=lambda kv: abs(int(kv[1][1])))
        v = int(best[1][1])
        return best[1][1], (-250 <= v <= 10000)
    return "", False


def line_row(r, sport_link=None):
    tips = e(r.get("tips", ""))
    pct = r.get("olbg_pct")
    pct = ("%.0f%%" % pct) if isinstance(pct, (int, float)) else ""
    price, inb = headline(r)
    band = ('<span class="pill band">in</span>' if inb
            else '<span class="pill noband">out</span>') if price else '<span class="pill blank">blank</span>'
    note = r.get("note") or ""
    return ("<tr><td><b>%s</b><div class=\"small muted\">%s</div><div class=\"small muted\">%s</div>"
            "%s</td><td>%s</td><td>%s<div class=\"small muted\">%s</div></td>"
            "<td class=\"num\"><b>%s</b> %s</td>"
            "<td><span class=\"pill tr\">%s</span> <span class=\"pill %s\">%s</span>%s</td>"
            "<td class=\"small muted\">%s</td></tr>"
            % (e(r["event"]), e(r.get("competition", "")), e(r.get("olbg_time", "")),
               ('<div class="small"><a href="%s">OLBG event &rarr;</a></div>' % e(r["event_url"]))
               if r.get("event_url") else "",
               e(r.get("market", "")), e(r.get("selection", "")),
               (tips + (" " + pct if pct else "")) or "&mdash;",
               e(price) if price else "&mdash;", band,
               e(r.get("track", "T")), "low" if r.get("tier") in "D" else "band",
               e(TIER_LABEL.get(r.get("tier"), r.get("tier") or "")),
               sport_link or "", e(note)))


def build_sport(sport, picks, lines):
    rows = [p for p in picks if p["sport"] == sport]
    evs = sorted([r for r in lines["lines"] if r["sport"] == sport],
                 key=lambda r: (r["event"], r.get("market", "")))
    out = ['<h2>%s</h2>' % e(sport)]
    out.append('<div class="grid">%s%s%s%s</div>' % (
        kpi(len(evs), "markets swept from OLBG"),
        kpi(sum(1 for r in evs if priced(r)), "priced by us"),
        kpi(len(rows), "written picks"),
        kpi(sum(1 for p in rows if p["confidence"] == "HIGH"), "high confidence")))
    if sport in SPORT_NOTE:
        out.append('<div class="note flag">%s</div>' % e(SPORT_NOTE[sport]))

    if rows:
        out.append('<h2 class="anchor">The %d picks</h2>' % len(rows))
        out.append('<p class="tnote">Every prediction below is written for this board. The bet is '
                   'the first column of the strip under each headline.</p>')
        for p in rows:
            out.append(pick_card(p))

    if not evs:
        out.append('<div class="note">No %s market appears anywhere in the sweep, so there is no '
                   'line table for this sport.</div>' % e(sport))
        return page("%s - picks and every market" % sport, e(sport), "".join(out), 1,
                    "sport-" + SLUG[sport])
    out.append('<h2 class="anchor">Every %s market we swept</h2>' % e(sport))
    out.append('<p class="tnote">All %d markets OLBG publishes for %s on 27 October 2026, with the '
               'price we originated for each. &ldquo;Track&nbsp;T&rdquo; means the price comes from '
               'the tip share OLBG prints; &ldquo;Track&nbsp;R&rdquo; means we built it ourselves '
               'from an official competition table, ranking or points record. A blank line means we '
               'could not confirm enough to originate one &mdash; see <a href="../flagged.html">'
               'Flagged for Review</a>.</p>' % (len(evs), e(sport)))
    trs = []
    for r in evs:
        trs.append(line_row(r))
        if rlines(r):
            trs.append('<tr><td colspan="6" style="padding-top:0">%s</td></tr>' % orig_box(r))
    out.append('<table><thead><tr><th>Match / event</th><th>Market</th><th>OLBG most-tipped</th>'
               '<th>Our line</th><th>Track / tier</th><th>Note</th></tr></thead><tbody>%s</tbody></table>'
               % "".join(trs))
    return page("%s - picks and every market" % sport, e(sport), "".join(out), 1,
                "sport-" + SLUG[sport])


# ----------------------------------------------------------------- page: lines
def build_lines(lines, picks, C):
    rows = lines["lines"]
    picked = {(p["sport"], p["event"]) for p in picks}
    out = ['<p class="lede">All %d markets OLBG publishes across fifteen sports on 27 October 2026, '
           'and the price we originated for each. %d are priced, %d are left blank because we could '
           'not confirm enough to originate one, and %d land inside the -250 to +10000 band. Not one '
           'of these numbers is a bookmaker price.</p>'
           % (C["total"], C["priced"], C["blank"], C["in_band"]),
           '<div class="grid">%s%s%s%s%s%s</div>' % (
               kpi(C["total"], "markets swept"),
               kpi(C["priced"], "priced by us"),
               kpi(C["blank"], "left blank"),
               kpi(C["in_band"], "inside the band"),
               kpi(C["track_R"], "built from an official table"),
               kpi(C["defective"], "hit by an OLBG display defect")),
           jumpbar(picks)]
    for s in SPORTS:
        rs = sorted([r for r in rows if r["sport"] == s],
                    key=lambda r: (r["event"], r.get("market", "")))
        if not rs:
            continue
        out.append('<h2 class="anchor" id="%s">%s <span class="muted small">(%d markets)</span></h2>'
                   % (SLUG[s], e(s), len(rs)))
        trs = []
        for r in rs:
            pk = ('<a href="sports/%s.html" class="pill high">picked</a>' % SLUG[s]
                  if (s, r["event"]) in picked else "")
            trs.append(line_row(r, pk))
            if rlines(r):
                trs.append('<tr><td colspan="6" style="padding-top:0">%s</td></tr>' % orig_box(r))
        out.append('<table><thead><tr><th>Match / event</th><th>Market</th><th>OLBG most-tipped</th>'
                   '<th>Our line</th><th>Track / tier</th><th>Note</th></tr></thead><tbody>%s'
                   '</tbody></table>' % "".join(trs))
    return page("Every line", "All %d markets" % C["total"], "".join(out), 0, "lines")


# ---------------------------------------------------------------- page: flagged
def build_flags(flags, picks):
    sev = {"HIGH": "high", "MEDIUM": "medium", "LOW": "low"}
    pick_flags = [p for p in picks if p.get("flag")]
    out = ['<p class="lede"><b>Everything irregular we found.</b> %d items, each with the source '
           'that shows it. &ldquo;Needs review&rdquo; means published here &mdash; none of these '
           'blocks a pick, a line or the site. Where a value could not be confirmed from an '
           'official source it is left blank on the board and recorded here, never inferred.</p>'
           % flags["counts"]["total"],
           '<div class="grid">%s%s%s%s</div>' % (
               kpi(flags["counts"]["total"], "items flagged"),
               kpi(flags["counts"]["HIGH"], "high severity"),
               kpi(flags["counts"]["MEDIUM"], "medium severity"),
               kpi(flags["counts"]["LOW"], "limitations of our own work")),
           '<h2>Irregularities in what OLBG publishes</h2>']
    for f in flags["flags"]:
        srcs = " &middot; ".join('<a href="%s">%s</a>' % (e(s["url"]), e(s["label"])) for s in f["sources"])
        out.append("""<div class="card %s" id="%s">
<div class="hd"><span class="pill %s">%s</span><span class="pill tr">%s</span><span class="tag">%s</span></div>
<h4>%s</h4>
<p class="pred small">%s</p>
<div class="note small"><b>What we did about it:</b> %s</div>
<div class="srcs"><b>Sources</b> &nbsp;%s</div>
</div>""" % ("" if f["severity"] != "HIGH" else "flag", e(f["id"]), sev[f["severity"]],
             f["severity"], e(f["sport"]), e(f["id"]), e(f["title"]), e(f["detail"]),
             e(f["board_effect"]), srcs))
    out.append('<h2>Flags attached to individual picks</h2>')
    out.append('<p class="tnote">%d of the %d written picks carry a note of their own. These are '
               'printed on the pick as well as here, so nobody can back one without seeing the '
               'problem first.</p>' % (len(pick_flags), len(picks)))
    out.append('<table><thead><tr><th>Sport</th><th>Match</th><th>The bet</th>'
               '<th>Our line</th><th>What is flagged</th></tr></thead><tbody>')
    for p in pick_flags:
        out.append('<tr><td>%s</td><td><a href="sports/%s.html#%s">%s</a></td><td><b>%s</b></td>'
                   '<td class="num">%s</td><td class="small">%s</td></tr>'
                   % (e(p["sport"]), SLUG[p["sport"]], e(p["id"]), e(p["event"]),
                      e(p["selection"]), e(p["line"]) or "&mdash;", e(p["flag"])))
    out.append('</tbody></table>')
    return page("Flagged for review", "Flagged for review", "".join(out), 0, "flagged")


# ----------------------------------------------------------------- page: method
def build_method(lines, picks, flags, C):
    meth_keys = ["rugby", "basketball", "tennis", "f1_podiums", "hockey", "handball",
                 "volleyball", "golf", "f1"]
    nice = {"f1_podiums": "F1 podium finish", "f1": "F1 Drivers' Championship outright",
            "rugby": "Rugby union", "basketball": "Basketball", "tennis": "Tennis",
            "hockey": "Ice hockey", "handball": "Handball", "volleyball": "Volleyball",
            "golf": "Golf outrights"}
    rows = []
    for k in meth_keys:
        if k not in lines:
            continue
        v = lines[k]
        bits = []
        for kk, vv in v.items():
            if isinstance(vv, dict) and len(vv) > 6:
                bits.append("%s: %d entries" % (kk, len(vv)))
            elif isinstance(vv, list) and len(vv) > 6:
                bits.append("%s: %d entries" % (kk, len(vv)))
            else:
                bits.append("%s %s" % (kk, json.dumps(vv, ensure_ascii=False)))
        rows.append('<tr><td><b>%s</b></td><td class="small">%s</td></tr>'
                    % (e(nice.get(k, k)), e("; ".join(bits))))
    body = """
<p class="lede">Two tracks, applied line by line. Nothing on this board is a bookmaker price,
because OLBG renders those client-side and they are absent from the HTML we can retrieve. Every
number below is originated by us, and every one of them can be reproduced from
<span class="tag">scripts/v3_pricing.py</span>.</p>

<h2>Track T &mdash; the tip share OLBG prints</h2>
<p>Where OLBG publishes a tip count for a selection, the implied chance is that count shrunk
towards a uniform prior worth six tips:</p>
<div class="origbox"><code>p = (k + A/m) / (n + A)</code>
<div class="small muted" style="margin-top:6px">
<code>k</code> tips on this selection &middot; <code>n</code> tips on the market &middot;
<code>m</code> outcomes OLBG lists &middot; <code>A = %s</code> prior strength.</div></div>
<p class="tnote">Fair American price: if <code>p &ge; 0.5</code> then <code>-round(100p/(1-p))</code>,
otherwise <code>+round(100(1-p)/p)</code>. The shrink stops a single tip on a two-horse market
reading as a near-certainty, and it keeps a 94%% tip share on a sixteen-tip market from printing as
an unbackable -1500.</p>
<p class="tnote">Tiering by sample size &mdash; <b>A</b> n&ge;20 (%d markets) &middot;
<b>B</b> 8&le;n&lt;20 (%d) &middot; <b>C</b> 4&le;n&lt;8 (%d) &middot; <b>D</b> n&lt;4 (%d) &middot;
<b>R</b> our own origination (%d).</p>

<h2>Track R &mdash; our own origination</h2>
<p>Where an official competition table, ranking or points record exists, we build the price from
that instead. For a two-sided match:</p>
<div class="origbox"><code>d = margin_home - margin_away + HFA</code><br>
<code>p_home = 1 / (1 + 10^(-d/s))</code>
<div class="small muted" style="margin-top:6px"><code>margin</code> is the official points (or
goals, or runs) difference per game &middot; <code>HFA</code> is the home-field allowance &middot;
<code>s</code> is the sport's spread, chosen so that one game's worth of scoring margin maps to a
realistic change of chance.</div></div>
<table><thead><tr><th>Sport family</th><th>Parameters as used</th></tr></thead><tbody>%s</tbody></table>
<p class="tnote">Handball adds an explicit draw share of %s, because the official EHF group tables
record two draws across the thirty group-phase games played in groups A, C and F. Tennis is priced
straight off the official ATP points ratio, <code>p = r/(1+r)</code>. F1 podium finishes are the
official season podium count divided by the %s rounds completed &mdash; the podium counts across the
top eight drivers sum to 54, which is exactly 3 &times; 18, so that denominator is not guessed.
Golf outrights weight each entrant by one over their official world ranking, normalised across the
confirmed field, with the 99 unranked entrants carrying a stated notional ranking of 150.</p>
<p class="tnote">Where OLBG tips exist we keep the Track&nbsp;T price as the headline and attach the
Track&nbsp;R line alongside it in the <span class="tag">lines</span> column of every row. Where a
row is Track&nbsp;R primary &mdash; the Mexico Open outright &mdash; the tip-derived number is
superseded and the row says so.</p>

<h2>The confidence gates</h2>
<p class="tnote"><b>HIGH</b> requires all five:</p>
<ol class="tnote">
<li>our fair price sits between %s inclusive;</li>
<li>at least one official source corroborates the direction of the pick;</li>
<li>the row is not hit by a known OLBG display defect;</li>
<li>sample &mdash; match markets need eight or more tips, or a Track&nbsp;R line built from an
official competition table; outrights need (joint-)most-tipped status and to be an officially
leading contender;</li>
<li>probability &mdash; match markets p&nbsp;&ge;&nbsp;0.55; outrights
p&nbsp;&ge;&nbsp;min(0.40,&nbsp;2.5/m), or, where five or fewer live contenders are priced from an
official points table, the leader of that table.</li>
</ol>
<p class="tnote"><b>MEDIUM</b> is the same direction with a price outside the band or a sample below
the threshold. <b>LOW</b> is a pick whose argument is sound but where a value it depends on could
not be confirmed from an official source, so that value is left blank. Result across the slate:
%d high, %d medium, %d low.</p>

<h2>What we refuse to do</h2>
<ul class="tnote">
<li><b>No inference.</b> If a venue, a competition, a field size or an injury cannot be sourced, the
cell is blank and the gap appears on <a href="flagged.html">Flagged for Review</a>. Five picks on
this board carry no price at all for exactly that reason.</li>
<li><b>No padding.</b> Snooker and Greyhounds carry zero picks because OLBG carries zero events for
either on this date. We do not invent fixtures to hit a target count.</li>
<li><b>No borrowed language.</b> The words &ldquo;model&rdquo; and &ldquo;verified&rdquo; do not
appear anywhere in prediction prose; the machinery is internal and is described on this page
instead. <span class="tag">scripts/v3_picks.py</span> rejects any pick that uses them.</li>
<li><b>No over-fitting.</b> The baseball money line is deliberately not originated from the
three-game World Series sample: a logistic fit to those three results returned 0.982, or -4200,
which describes the past rather than the next game. We publish OLBG's tip-derived line and flag it.
The three-game totals are still usable for the run total, because a mean is a mean.</li>
<li><b>No nonsense prices.</b> An earlier attempt to price every F1 title contender on the gap to
the leader emitted +2479913 for Oscar Piastri. Contenders more than two race wins &mdash; 50 points
&mdash; behind the best-placed eligible rival are excluded, and the exclusion is stated on the page.</li>
<li><b>No borrowed labels.</b> Where OLBG misfiles a competition &mdash; the Maybank Championship
under the DP World Tour although it is an LPGA event, or Fuchse Berlin v RK Partizan under the EHF
European League although both clubs sit in the official Champions League group A table &mdash; we
record the correct competition and flag the difference rather than repeat it.</li>
</ul>

<h2>Coverage</h2>
<div class="grid">%s%s%s%s%s</div>
<h3>The OLBG clock</h3>
<p class="tnote">OLBG prints times in US Eastern. Four independent fixtures confirm it on the same
day: Auckland v Canterbury prints 17:30 against an official 10:30am NZT start on 28 October, which
is 5:30pm EDT on the 27th; Fr Caseys v Kildimo-Pallaskenry prints 10:30 against an official 15:30
Irish start; the URC round-6 fixtures align on the same shift; and all 115 swept rows shift by the
same offset from their official local times. Three rows still conflict after the offset is applied
&mdash; Brewers at Rays, Afghanistan v Zimbabwe and South Africa v Australia &mdash; and those stay
on the flagged page.</p>
<h3>Reproducing this board</h3>
<p class="tnote"><code>python3 scripts/v3_events.py</code> writes the 115-row sweep;
<code>scripts/v3_pricing.py</code> writes every line; <code>scripts/v3_picks.py</code> validates and
writes the slate; <code>scripts/v3_flags.py</code> writes the irregularities;
<code>scripts/v3_build.py</code> writes this site. The raw findings behind every factual claim are
in <span class="tag">data/v3/raw/verified-facts-part1.md</span>,
<span class="tag">part2.md</span> and <span class="tag">part3.md</span>.</p>
""" % (lines["prior_A"], C["tier"]["A"], C["tier"]["B"], C["tier"]["C"], C["tier"]["D"],
       C["tier"]["R"], "".join(rows),
       lines.get("handball", {}).get("draw_rate", 0.0667),
       int(lines.get("f1_podiums", {}).get("rounds_completed", 18)),
       e(lines["band"]),
       sum(1 for p in picks if p["confidence"] == "HIGH"),
       sum(1 for p in picks if p["confidence"] == "MEDIUM"),
       sum(1 for p in picks if p["confidence"] == "LOW"),
       kpi(C["total"], "markets swept"), kpi(C["priced"], "priced"),
       kpi(sum(1 for p in picks if p["track"] == "R"), "picks on Track R"),
       kpi(flags["counts"]["total"], "flags"),
       kpi(len({s["url"] for p in picks for s in p["sources"]} |
               {s["url"] for f in flags["flags"] for s in f["sources"]}),
           "distinct sources"))
    return page("Method", "How every line was originated", body, 0, "method")


# ---------------------------------------------------------------- page: sources
def build_sources(picks, flags):
    seen = {}
    for p in picks:
        for s in p["sources"]:
            d = seen.setdefault(s["url"], {"label": s["label"], "used": set()})
            d["used"].add(p["sport"])
    for f in flags["flags"]:
        for s in f["sources"]:
            d = seen.setdefault(s["url"], {"label": s["label"], "used": set()})
            d["used"].add(f["sport"])
    by_host = collections.defaultdict(list)
    for url, v in seen.items():
        m = re.match(r"https?://([^/]+)", url)
        by_host[m.group(1) if m else "?"].append((url, v))
    order = sorted(by_host, key=lambda h: (h.endswith("olbg.com"), -len(by_host[h]), h))
    out = ['<p class="lede">Every source used anywhere on this board, deduplicated. %d distinct '
           'URLs across %d hosts. Each pick carries at least one; a value that no source supports '
           'is left blank on the board and listed on <a href="flagged.html">Flagged for '
           'Review</a>.</p>' % (len(seen), len(by_host)),
           '<div class="grid">%s%s%s</div>' % (
               kpi(len(seen), "distinct sources"),
               kpi(len(by_host), "hosts"),
               kpi(len(by_host.get("www.olbg.com", [])), "OLBG pages cited"))]
    for h in order:
        items = sorted(by_host[h], key=lambda x: x[1]["label"].lower())
        out.append('<details class="sum"%s><summary>%s <span class="muted">&mdash; %d source%s'
                   '</span></summary><table><thead><tr><th>What it supports</th><th>Used by</th>'
                   '<th>URL</th></tr></thead><tbody>'
                   % (' open' if len(items) <= 8 else '', e(h), len(items),
                      "" if len(items) == 1 else "s"))
        for url, v in items:
            out.append('<tr><td>%s</td><td class="small muted">%s</td>'
                       '<td class="small"><a href="%s">%s</a></td></tr>'
                       % (e(v["label"]), e(", ".join(sorted(v["used"]))), e(url),
                          e(url[:74] + ("..." if len(url) > 74 else ""))))
        out.append('</tbody></table></details>')
    out.append('<h2>Retrieval note</h2><p class="tnote">The sweep ran against '
               '<a href="https://www.olbg.com/betting-tips/">olbg.com/betting-tips</a> on 27 October '
               '2026, across twenty listing pages covering all fifteen sports in scope plus six '
               'event pages. OLBG\'s URL grammar is <code>/betting-tips/{Sport}/{sport_id}</code> '
               'and <code>?event_id={id}</code>; a wrong sport id returns 404, and '
               '<code>/betting-tips/Sports/</code> does not exist. Bookmaker prices are rendered '
               'client-side and are absent from the retrieved HTML, which is why every price on '
               'this board is our own origination.</p>')
    return page("Sources", "Every source used on this board", "".join(out), 0, "sources")


# ---------------------------------------------------------------- page: archive
def build_archive(picks, C, flags):
    nsrc = len({s["url"] for p in picks for s in p["sources"]} |
               {s["url"] for f in flags["flags"] for s in f["sources"]})
    body = """
<p class="lede">This repo carries several boards, built by different passes over the same OLBG
sweep. This one lives at <span class="tag">/v3/</span> and does not replace any of them; the links
below go to the others so nothing is lost. Every one of them is reachable from the shared root
dashboard at <a href="../index.html">../index.html</a>.</p>
<h2>The other boards in this repo</h2>
<div class="sports">
<a class="sportcard" href="../index.html"><div class="nm">Root dashboard</div>
<div class="ct">The shared executive summary and the entry point Pages serves at /.</div></a>
<a class="sportcard" href="../oct27/all-markets.html"><div class="nm">October 27 desk</div>
<div class="ct">The 27 October multi-market origination desk, with its own flagged, method,
sources and repo-audit pages.</div></a>
<a class="sportcard" href="../value-desk/index.html"><div class="nm">Value Desk</div>
<div class="ct">193 sourced lines and 85 written picks from a later pass.</div></a>
<a class="sportcard" href="../docs/index.html"><div class="nm">Docs board</div>
<div class="ct">The first session's board, preserved as it was submitted.</div></a>
<a class="sportcard" href="../docs/board-review/index.html"><div class="nm">Board review</div>
<div class="ct">A review of what the earlier boards got right and got wrong.</div></a>
<a class="sportcard" href="../olbg-tips/index.html"><div class="nm">OLBG Tips</div>
<div class="ct">Tip-consensus board: executive summary, high-confidence rows and picks.</div></a>
<a class="sportcard" href="../archive.html"><div class="nm">Archive index</div>
<div class="ct">The repo's own index of archived boards.</div></a>
</div>
<h2>What this board adds</h2>
<table><thead><tr><th style="width:42%%">Elsewhere in the repo</th><th>Here</th></tr></thead><tbody>
<tr><td>Boards where the coverage table comes first</td>
<td>One front door opening on the %d highest-confidence picks written out in full, with
<b>the bet as the first field on every card</b></td></tr>
<tr><td>Winner picks that are sometimes bare</td>
<td>%d written predictions of 30 words or more &mdash; the shortest on this board is 91 words
&mdash; each naming the bet, the market, our price, the OLBG tip count and at least one official
source</td></tr>
<tr><td>Prices quoted without always saying where they came from</td>
<td>Every price labelled Track&nbsp;T (the tip share OLBG prints) or Track&nbsp;R (built from an
official table), with every parameter published on <a href="method.html">Method</a></td></tr>
<tr><td>Unconfirmable values sometimes filled in</td>
<td>Unconfirmable values left blank &mdash; %d markets carry no price &mdash; and listed on
<a href="flagged.html">Flagged for Review</a>, %d items in total</td></tr>
<tr><td>Rows without source links</td>
<td>Every pick and every flag carries sources; %d distinct official URLs are listed on
<a href="sources.html">Sources</a></td></tr>
<tr><td>Empty sports not always explained</td>
<td>Snooker and Greyhounds each get their own page stating exactly what OLBG printed and why no
picks follow from it</td></tr>
</tbody></table>
<h2>Nothing was moved or deleted</h2>
<p class="tnote">This board was built into its own <span class="tag">v3/</span> namespace. The root
dashboard and every other board are untouched apart from a single added navigation link pointing
here, so all of them keep working exactly as their authors left them.</p>
""" % (sum(1 for p in picks if p["confidence"] == "HIGH"), len(picks), C["blank"],
       flags["counts"]["total"], nsrc)
    return page("Other boards in this repo", "Other boards in this repo", body, 0, "archive")


# ----------------------------------------------------------------------- driver
def write(rel, content):
    dest = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)
    return dest


def main():
    lines = load("lines.json")
    picks = tag_picks(load("picks.json")["picks"])
    flags = load("flags.json")
    C = counts(lines)

    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    shutil.copy(os.path.join(ROOT, "assets", "style.css"),
                os.path.join(SITE, "assets", "style.css"))
    with open(os.path.join(SITE, "assets", "v3.css"), "w", encoding="utf-8") as f:
        f.write(CSS)

    made = [
        write("index.html", build_index(picks, lines, flags, C)),
        write("picks.html", build_picks(picks)),
        write("lines.html", build_lines(lines, picks, C)),
        write("flagged.html", build_flags(flags, picks)),
        write("method.html", build_method(lines, picks, flags, C)),
        write("sources.html", build_sources(picks, flags)),
        write("archive.html", build_archive(picks, C, flags)),
    ]
    for s in SPORTS:
        made.append(write("sports/%s.html" % SLUG[s], build_sport(s, picks, lines)))
    open(os.path.join(SITE, ".nojekyll"), "w").close()
    print("built %d pages into v3/" % len(made))
    print("  markets %d | priced %d | blank %d | in band %d | Track R %d | defective %d"
          % (C["total"], C["priced"], C["blank"], C["in_band"], C["track_R"], C["defective"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

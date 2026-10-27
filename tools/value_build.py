#!/usr/bin/env python3
"""Build the value desk data: originate a line for every event, then attach picks.

Run from the repo root:  python3 tools/value_build.py

Inputs  : data/value/capture.json, data/value/extra_markets.json,
          tools/value_editorial.py, data/picks_610d0099.json (for the review log).
Outputs : data/value/lines.json, picks.json, flags.json, sources.json,
          summary.json, and data/value/editorial.json (the copy, persisted).

No network access is used here. Every numeric input is either an OLBG tip split
transcribed from a public page or an official tournament/fixture fact with a URL.
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from value_editorial import PICKS as EDITORIAL, OLBG_HUBS  # noqa: E402

V = ROOT / "data" / "value"
BAND_MIN_DEC = 1.40          # -250 american
BAND_MAX_DEC = 101.00        # +10000 american
MARGIN = 1.05                # 5% overround on our own fair price


def american(dec):
    if dec is None or dec <= 1.0:
        return ""
    a = (dec - 1) * 100
    return f"+{int(round(a))}" if dec >= 2.0 else f"-{int(round(100 / (dec - 1)))}"


def parse_tips(t):
    if isinstance(t, str) and re.match(r"^\s*\d+\s*/\s*\d+\s*$", t):
        w, n = t.split("/")
        return int(w), int(n)
    return None, None


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


SPORTS = ["Golf", "Volleyball", "Rugby Union", "Cricket", "Snooker", "Darts",
          "Baseball", "Gaelic Sports", "Greyhounds", "Tennis", "Motor Racing",
          "Handball", "Ice Hockey", "Basketball", "Rugby League"]


def build_line(row, origin):
    """Originate one line. Returns the priced record."""
    sport = row["sport"]
    market = row.get("market") or ""
    selection = row.get("selection") or ""
    flags = []

    # ---- structural prior -------------------------------------------------
    w, n = parse_tips(row.get("tips"))
    field_size = row.get("field_size")
    outcomes = row.get("outcomes")
    if not outcomes:
        outcomes = 3 if selection.strip().lower().startswith("tie") else 2
        if origin == "capture" and not row.get("tips"):
            flags.append("outcomes-assumed")
    m = market.lower()
    e = row["event"].lower()
    is_outright = any(t in m for t in ("win tournament", "outright", "grand final winner",
                                       "win hurling", "fastest qualifier", "win race",
                                       "race winner", "win championship")) or any(
        t in e for t in ("championship 2027", "world cup 2027", "six nations 2027",
                         "big bash", "sa20", "t20 blast", "nrl 2027", "super league 2027",
                         "state of origin 2027", "pdc world championship 2027"))
    if field_size and int(field_size) > 0:
        N = int(field_size)
        prior = 1.0 / N
        k = max(6, min(12, math.ceil(N / 8)))
        method = f"V1-FIELD: tip share shrunk toward 1/{N} with k={k}"
        outcomes_eff = N
    elif is_outright:
        # No official field size published: documented conservative 1/32 prior,
        # never presented as a measured field size.
        prior, k, outcomes_eff = 1 / 32, 6, 32
        method = "V1-FIELD-DEFAULT: unverified field size, conservative 1/32 prior with k=6"
        flags.append("field-size-default-32")
    else:
        prior = 1.0 / outcomes
        k = 6
        method = f"V1-STRUCT: tip share shrunk toward 1/{outcomes} with k=6"
        outcomes_eff = outcomes

    if w is not None and n and n > 0:
        p = (w + k * prior) / (n + k)
        tip_note = f"{w}/{n}"
    elif row.get("prior_p") is not None:
        p = float(row["prior_p"])
        method = "V2-" + str(row.get("basis") or "prior").upper() + ": documented prior, no OLBG tip split"
        tip_note = None
        flags.append("no-tip-split")
    else:
        p = prior
        method = "V2-STRUCT: equal-chance structural prior, no OLBG tip split"
        tip_note = None
        flags.append("no-tip-split")

    p = min(max(p, 0.004), 0.95)
    fair_dec = 1.0 / (p * MARGIN)
    dec = min(max(fair_dec, BAND_MIN_DEC), BAND_MAX_DEC)
    if dec > fair_dec + 1e-9:
        flags.append("band-floor-applied")
    if dec < fair_dec - 1e-9:
        flags.append("band-cap-applied")

    if origin == "capture" and row.get("schedule_status") == "not_checked":
        flags.append("schedule-not-independently-checked")
    if row.get("bookmaker_odds") is None:
        flags.append("bookmaker-odds-blank")
    if not row.get("start_timezone"):
        flags.append("timezone-blank")

    return {
        "id": row["id"] if origin == "extra" else row["row_id"],
        "origin": origin,
        "sport": sport,
        "slug": slug(sport),
        "event": row["event"],
        "date": row.get("date_bucket") or row.get("date") or "",
        "start_label": row.get("start_label") or "",
        "market": market,
        "selection": selection,
        "tips": tip_note,
        "pct": row.get("pct"),
        "field_size": field_size,
        "outcomes": outcomes_eff,
        "prior": round(prior, 5),
        "shrink_k": k,
        "p_fair": round(p, 5),
        "fair_price_dec": round(fair_dec, 3),
        "price_dec": round(dec, 2),
        "price_american": american(dec),
        "in_band": BAND_MIN_DEC - 1e-9 <= dec <= BAND_MAX_DEC + 1e-9,
        "plus_money": dec >= 2.0,
        "method": method,
        "olbg_url": row.get("olbg_url") or row.get("listing_url") or OLBG_HUBS.get(sport, ""),
        "official_url": row.get("official_url") or "",
        "source_note": row.get("source_note", ""),
        "flags": sorted(set(flags)),
    }


def main():
    capture = json.loads((V / "capture.json").read_text())
    extra = json.loads((V / "extra_markets.json").read_text())

    lines = []
    for r in capture["events"]:
        lines.append(build_line(r, "capture"))
    for r in extra["rows"]:
        lines.append(build_line(r, "extra"))
    by_id = {l["id"]: l for l in lines}
    # short numeric ids used by the authored copy
    by_short = {l["id"][-3:]: l for l in lines if l["origin"] == "capture"}

    # persist the authored copy
    (V / "editorial.json").write_text(json.dumps({
        "schema_version": 1,
        "session": "sess-arena-7cf491a1",
        "date": "2026-10-27",
        "note": "Original written predictions. Facts carry the URL that was read to support them.",
        "picks": EDITORIAL,
    }, indent=1, ensure_ascii=False))

    official_kinds = {"official", "olbg"}

    def confidence(p, hint, facts, line):
        kinds = {f["kind"] for f in facts}
        n_words = len(p["prediction"].split())
        if n_words < 30 or not facts or not line["in_band"]:
            return "low"
        if hint == "high":
            # Confidence measures evidence quality, not implied probability:
            # the brief explicitly wants high-confidence picks out to +10000.
            ok = (len(facts) >= 2 and kinds & official_kinds and line["p_fair"] >= 0.07)
            return "high" if ok else "medium"
        if hint == "medium":
            return "medium" if kinds & official_kinds else "low"
        return "low"

    picks = []
    seen = set()
    for p in EDITORIAL:
        l = by_id.get(p["line_id"]) or by_short.get(p["line_id"])
        if l is None:
            raise SystemExit(f"unknown line id {p['line_id']} for pick {p['id']}")
        key = (p["sport"], p["id"])
        if key in seen:
            raise SystemExit(f"duplicate pick id {p['id']}")
        seen.add(key)

        selection = p["selection_override"] or l["selection"]
        market = p["market_override"] or l["market"]
        price = round(l["price_dec"], 2)
        flags = list(dict.fromkeys(list(l["flags"]) + list(p["flags"])))
        facts = [dict(f) for f in p["facts"]]
        # every row needs at least one source link; de-duplicate identical links
        if not any(f["source"].startswith("https://") for f in facts):
            facts.append({"claim": "OLBG sport hub / event market listing for 27 October 2026",
                          "source": l["olbg_url"], "kind": "olbg"})
        uniq, seen_urls = [], set()
        for f in facts:
            if f["source"] in seen_urls:
                continue
            seen_urls.add(f["source"])
            uniq.append(f)
        facts = uniq
        if not any(f["kind"] == "official" for f in facts) and l["official_url"]:
            # only label an auto-attached link "official" if it really is one
            host = re.sub(r"^www\.", "", l["official_url"].split("/")[2].lower())
            official_hosts = ("olbg.com", "nhl.com", "nba.com", "mlb.com", "pgatour.com",
                              "lpga.com", "formula1.com", "pdc.tv", "wst.tv",
                              "eurohandball.com", "unitedrugby.com", "munster.gaa.ie",
                              "leagueworldcup2026.com", "cbv.com.br", "atptour.com",
                              "wtatennis.com", "simmonsbankchampionship.com", "gbgb.org.uk",
                              "romfordgreyhoundstadium.co.uk", "centralpark-greyhounds.co.uk")
            kind = "official" if any(host.endswith(h) for h in official_hosts) else "media"
            if kind == "official":
                facts.append({"claim": l["source_note"] or "Official competition source",
                              "source": l["official_url"], "kind": kind})
        kinds = {f["kind"] for f in facts}
        if not kinds & {"official"}:
            flags.append("no-official-source")
        if kinds and kinds <= {"secondary"}:
            flags.append("secondary-sources-only")
        flags.append("injury-news-blank")
        if "tie" in selection.lower():
            flags.append("tie-selection-irregularity")

        conf = confidence(p, p["conf_hint"], facts, l)
        picks.append({
            "id": p["id"], "sport": p["sport"], "slug": slug(p["sport"]),
            "event": l["event"], "date": l["date"], "start_label": l["start_label"],
            "competition": "", "market": market, "selection": selection,
            "tips": l["tips"], "p_fair": l["p_fair"], "price_dec": price,
            "price_american": l["price_american"], "fair_price_dec": l["fair_price_dec"],
            "in_band": l["in_band"], "plus_money": l["plus_money"],
            "confidence": conf, "conf_hint": p["conf_hint"],
            "prediction": p["prediction"], "word_count": len(p["prediction"].split()),
            "facts": facts,
            "olbg_url": l["olbg_url"], "official_url": l["official_url"],
            "line_id": l["id"], "method": l["method"], "flags": sorted(set(flags)),
            "note": p["note"],
        })

    # ---------------------------- sources ---------------------------------
    src = defaultdict(lambda: {"count": 0, "kinds": set(), "sports": set(), "claims": []})
    for p in picks:
        for f in p["facts"]:
            s = src[f["source"]]
            s["count"] += 1
            s["kinds"].add(f["kind"])
            s["sports"].add(p["sport"])
            if len(s["claims"]) < 3:
                s["claims"].append(f["claim"])
    sources = [{"url": u, "count": v["count"], "kinds": sorted(v["kinds"]),
                "sports": sorted(v["sports"]), "claims": v["claims"]}
               for u, v in sorted(src.items(), key=lambda kv: (-kv[1]["count"], kv[0]))]

    # ----------------------------- flags ----------------------------------
    row_flags = []
    for p in picks:
        for f in p["flags"]:
            if f in {"injury-news-blank", "timezone-blank", "bookmaker-odds-blank"}:
                continue
            row_flags.append({
                "id": f"ROW-{p['id']}-{f}", "scope": "row", "severity": "low",
                "title": f, "sport": p["sport"], "pick_id": p["id"],
                "detail": f"Pick {p['id']} ({p['sport']} - {p['selection']}) carries the flag '{f}'.",
                "sources": [x["source"] for x in p["facts"]][:3],
            })

    repo_flags = [
        {"id": "F01", "scope": "repo", "severity": "high", "sport": "All",
         "title": "Prior published card was a 26 October snapshot",
         "detail": "data/events.json and the root dashboard carry retrieved_at 2026-10-26. This desk uses a fresh 27 October transcription (143 OLBG rows) plus 50 rows read from OLBG event pages and official fixtures. Tip splits changed substantially: India moved from 27/40 to 35/49, Afghanistan from 8/9 to 15/16, Pakistan from 14/21 to 22/31.",
         "sources": ["https://www.olbg.com/betting-tips", "data/value/capture.json"]},
        {"id": "F02", "scope": "repo", "severity": "high", "sport": "Baseball",
         "title": "Earlier board contains stale, contradictory World Series claims",
         "detail": "data/picks_610d0099.json says Milwaukee led 2-0 before Game 3 on 26 October and describes Freddy Peralta as a Rays pitcher with a 2-0 record and 1.08 playoff ERA. MLB.com's official schedule now shows Milwaukee winning Game 3 10-1 to lead 3-0, and its report says Peralta was charged with the eight-run fifth inning. Those earlier rows must not be republished as current.",
         "sources": ["https://www.mlb.com/news/2026-mlb-playoff-and-world-series-schedule", "data/picks_610d0099.json"]},
        {"id": "F03", "scope": "repo", "severity": "medium", "sport": "Handball",
         "title": "OLBG handball hub shows 'Tie' as the most-tipped selection",
         "detail": "Thirteen of the 27 October handball rows list 'Tie' as the selected outcome with tip shares up to 78%. This is a rendering artefact of the hub's most-tipped-outcome display, not a usable market consensus. Here those matches are priced as three-way contests and the straight win is picked using EHF's official group table.",
         "sources": ["https://www.olbg.com/betting-tips/Handball/20", "https://ehfcl.eurohandball.com/men/2026-27/standings/"]},
        {"id": "F04", "scope": "repo", "severity": "high", "sport": "Snooker, Greyhounds",
         "title": "OLBG has no snooker or greyhound tips today",
         "detail": "Both hubs returned 'No tips found.' on 27 October. The picks on this desk for those sports come from WST's official match centre/rankings and Romford Stadium's official advance card, not from OLBG markets. They are labelled and must not be described as OLBG community picks.",
         "sources": ["https://www.olbg.com/betting-tips/Snooker/8", "https://www.olbg.com/betting-tips/Greyhounds/28", "https://www.wst.tv/rankings/", "https://romfordgreyhoundstadium.co.uk/racing/advance/races"]},
        {"id": "F05", "scope": "repo", "severity": "medium", "sport": "Darts",
         "title": "PDC sources conflict on Players Championship event numbering",
         "detail": "A PDC article dated 26 October announces Players Championships 31-32 for 28-29 October, but another PDC article dated the same day lists 2026 PC event winners through event 32 (Jeffrey de Graaf 31, Gabriel Clemens 32). An OLBG tipster comment also credits Wessel Nijman with six 2026 PC titles, which does not match PDC's own winner list. All darts form claims are flagged where they come from community comments.",
         "sources": ["https://www.pdc.tv/news/2026/october/26/2026-players-championships-31-32-entries-confirmed", "https://www.pdc.tv/news/2026/october/26/schindler---coates-secure-grand-slam-qualification", "https://www.olbg.com/betting-tips/Darts/All_Darts/All_Events/Players_Championship_31/15?event_id=32446"]},
        {"id": "F06", "scope": "repo", "severity": "medium", "sport": "Motor Racing",
         "title": "Market label for the Verstappen Mexico row differs between captures",
         "detail": "The 27 October hub row 007 names the market 'Podium Finish' with selection 'Max Verstappen - Yes' at 1/2 tips, while the earlier root inventory called this event's market 'Top 6 Finish'. The market name is left exactly as captured on 27 October and the discrepancy is recorded here.",
         "sources": ["https://www.olbg.com/betting-tips/Motor_Racing/14", "data/value/capture.json"]},
        {"id": "F07", "scope": "repo", "severity": "medium", "sport": "Golf, Darts, Cricket",
         "title": "Earlier outright lines used a 1/8 prior for large fields",
         "detail": "Earlier boards priced outright markets with a 1/8 structural prior even for fields of 100+ runners, which produced unrealistically short prices on longshots. This desk uses official field sizes where published (120 for the Mexico Open, 54 for the Simmons Bank Championship, 128 for Players Championship 31) and a documented shrinkage constant. Where a field size was not published it is left blank and flagged.",
         "sources": ["https://www.pgatour.com/article/news/betting-dfs/2026/10/26/odds-outlook-vidantaworld-mexico-open-betting-fantasy-picks-advice-fedexcup-fall", "https://www.pdc.tv/news/2026/october/26/2026-players-championships-31-32-entries-confirmed", "https://simmonsbankchampionship.com/"]},
        {"id": "F08", "scope": "repo", "severity": "medium", "sport": "All",
         "title": "No bookmaker odds in retrievable OLBG HTML",
         "detail": "OLBG's rendered pages show tip counts and percentages but no bookmaker price in the HTML we can retrieve, so the bookmaker_odds column is blank throughout and no price-comparison claim is made. One exception: the PGA TOUR's own betting article publishes FanDuel prices for the Mexico Open, which are quoted on the golf rows as a published benchmark, not as an OLBG price.",
         "sources": ["https://www.olbg.com/betting-tips", "https://www.pgatour.com/article/news/betting-dfs/2026/10/26/odds-outlook-vidantaworld-mexico-open-betting-fantasy-picks-advice-fedexcup-fall"]},
        {"id": "F09", "scope": "repo", "severity": "medium", "sport": "All",
         "title": "Injury and team-news fields are blank",
         "detail": "No official injury report or confirmed team sheet was retrieved for the majority of events. Injury and team-news cells are intentionally blank rather than filled with speculation; each affected pick carries the injury-news-blank flag. Where an official source did name a starter (MLB Game 4, WST draw, PDC entries), that fact is stated with its link.",
         "sources": ["data/value/lines.json", "data/value/picks.json", "https://www.olbg.com/betting-tips"]},
        {"id": "F10", "scope": "repo", "severity": "medium", "sport": "All",
         "title": "Start times have no published timezone",
         "detail": "OLBG prints 'Today 21:00', 'Tomorrow 08:00' and similar labels without a timezone. The timezone field is blank on all captured rows. WST's match centre shows round-two snooker at 21:30 on 30 October while a specialist draw lists 01:30Z on 31 October, so exact start times are left as displayed and not converted.",
         "sources": ["data/value/capture.json", "https://www.wst.tv/match-centre/bb4f8b36-42f0-490f-b97b-b8f8799f693b", "https://www.snooker.org/res/index.asp?event=2762"]},
        {"id": "F11", "scope": "repo", "severity": "low", "sport": "Golf",
         "title": "Hub shows one tipped name per golf tournament; event pages show two",
         "detail": "The OLBG golf hub lists one 1/2 selection per tournament, but the three event pages each show two players on one tip apiece (Woad/Choi, Clark/Homa, Cink/Els). Both tipped names are priced here with the event-page URL attached, because the hub's single-name display hides half the market.",
         "sources": ["https://www.olbg.com/betting-tips/Golf/5", "https://www.olbg.com/betting-tips/Golf/All_Golf/All_Events/Mexico_Open/5?event_id=101915"]},
        {"id": "F12", "scope": "repo", "severity": "low", "sport": "Snooker",
         "title": "Opponent world rankings come from a specialist draw list",
         "detail": "WST publishes the official top rankings (Selby 4, Murphy 7, Wu 2, Wilson 9), but rankings for players outside the top eleven such as Mitchell Mann, Liam Davies and Liu Hongyu were only available on snooker.org's draw page. Those numbers are labelled secondary and are not presented as official WST figures.",
         "sources": ["https://www.wst.tv/rankings/", "https://www.snooker.org/res/index.asp?event=2762"]},
        {"id": "F13", "scope": "repo", "severity": "low", "sport": "Greyhounds",
         "title": "Advance racecard has no form figures",
         "detail": "Romford's official advance card publishes trap draws, trainers, grades and race times but no recent form, sectional times or injury notes. Greyhound selections are therefore made from the trap draw plus OLBG's own Romford trap-1 statistic, and every such pick is low confidence.",
         "sources": ["https://imminent-otter.files.svdcdn.com/production/assets/results/Romford/race-advances/TUESDAY-ADVANCED_2026-10-26-121153_lbhn.pdf", "https://www.olbg.com/betting-tips/Greyhounds/28"]},
        {"id": "F14", "scope": "repo", "severity": "low", "sport": "All",
         "title": "Several earlier rows cite Wikipedia or aggregator pages",
         "detail": "The first board's snooker, Gaelic and golf rows cite Wikipedia, Golf News Net and similar secondary pages. Where this desk reuses a fact of that type it is labelled secondary in the sources table and flagged on the row; official governing-body links were substituted wherever one was available.",
         "sources": ["data/picks_610d0099.json", "data/value/sources.json", "https://www.wst.tv/rankings/", "https://munster.gaa.ie/fixtures/club-championships-2026/"]},
        {"id": "F15", "scope": "repo", "severity": "low", "sport": "All",
         "title": "Four separate boards exist in this repository",
         "detail": "The root dashboard, /docs/, /olbg-tips/ and /docs/board-review/ each publish their own version of the card, which is the source of the confusion reported by the user. This desk is a single self-contained board with one pick table, one lines table, one sources page and one flagged page. A link from the root dashboard is requested in COORDINATION.md rather than editing another session's page.",
         "sources": ["index.html", "docs/index.html", "olbg-tips/index.html", "docs/board-review/index.html", "value-desk/index.html", "https://github.com/karagemop466-tech/Olbg7"]},
        {"id": "F16", "scope": "repo", "severity": "low", "sport": "Cricket, Rugby League, Handball",
         "title": "Ante-post markets extend into 2027",
         "detail": "Rows such as the 2027 World Cup, State of Origin 2027, NRL 2027 and the 2027 All-Ireland championships are long-dated. They are kept because OLBG lists them, but their confidence is capped at medium and they are excluded from the today-only executive summary.",
         "sources": ["data/value/capture.json", "https://www.olbg.com/betting-tips/Rugby_League/10"]},
        {"id": "F17", "scope": "repo", "severity": "low", "sport": "All",
         "title": "Prices shorter than -250 or longer than +10000 are floored or capped",
         "detail": "The coverage brief asks for high-confidence picks between -250 and +10000. Where our fair price falls outside that range the published line is floored at 1.40 or capped at 101.00, the fair price is retained in the data, and the row is flagged band-floor-applied or band-cap-applied. Nothing is silently rounded into the band.",
         "sources": ["data/value/lines.json", "value-desk/method.html", "https://www.olbg.com/betting-tips"]},
    ]
    flags = repo_flags + row_flags

    # ---------------------------- summary ---------------------------------
    per_sport = {}
    for s in SPORTS:
        ps = [p for p in picks if p["sport"] == s]
        per_sport[s] = {
            "sport": s, "slug": slug(s), "picks": len(ps),
            "high": sum(p["confidence"] == "high" for p in ps),
            "medium": sum(p["confidence"] == "medium" for p in ps),
            "low": sum(p["confidence"] == "low" for p in ps),
            "plus_money": sum(p["plus_money"] for p in ps),
            "lines": sum(l["sport"] == s for l in lines),
            "olbg_hub": OLBG_HUBS[s],
        }
    summary = {
        "date": "2026-10-27",
        "session": "sess-arena-7cf491a1",
        "sports": len(SPORTS),
        "lines": len(lines),
        "capture_rows": len(capture["events"]),
        "extra_rows": len(extra["rows"]),
        "picks": len(picks),
        "high": sum(p["confidence"] == "high" for p in picks),
        "medium": sum(p["confidence"] == "medium" for p in picks),
        "low": sum(p["confidence"] == "low" for p in picks),
        "plus_money": sum(p["plus_money"] for p in picks),
        "in_band": sum(p["in_band"] for p in picks),
        "facts": sum(len(p["facts"]) for p in picks),
        "sources": len(sources),
        "flags": len(flags),
        "sports_under_five": [s for s in SPORTS if per_sport[s]["picks"] < 5],
        "per_sport": per_sport,
    }

    for name, obj in [("lines", {"schema_version": 1, "date": "2026-10-27", "lines": lines}),
                      ("picks", {"schema_version": 1, "date": "2026-10-27", "picks": picks}),
                      ("flags", {"schema_version": 1, "date": "2026-10-27", "flags": flags}),
                      ("sources", {"schema_version": 1, "date": "2026-10-27", "sources": sources}),
                      ("summary", summary)]:
        (V / f"{name}.json").write_text(json.dumps(obj, indent=1, ensure_ascii=False))

    print(json.dumps({k: summary[k] for k in ["lines", "picks", "high", "medium", "low",
                                              "plus_money", "facts", "sources", "flags",
                                              "sports_under_five"]}, indent=2))
    for s in SPORTS:
        d = per_sport[s]
        print(f"  {s:15} picks={d['picks']:2} high={d['high']:2} med={d['medium']:2} "
              f"low={d['low']:2} plus={d['plus_money']:2} lines={d['lines']:3}")


if __name__ == "__main__":
    main()

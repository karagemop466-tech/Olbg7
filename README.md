# Olbg7 — OLBG 15-Sport Predictions Board

Static dashboard (GitHub Pages, `/docs`) with originated fair lines and unique written predictions
for Golf, Volleyball, Rugby Union, Cricket, Snooker, Darts, Baseball, Gaelic Sports, Greyhounds,
Tennis, Motor Racing, Handball, Ice Hockey, Basketball and Rugby League.

- Landing + executive summary: `docs/index.html`
- One page per sport: `docs/<sport>.html` (5 rows each, 75 total)
- Unconfirmed items: `docs/flagged.html` — selections/prices left blank, never invented
- Pricing method: `docs/method.html` · Machine-readable data: `data/picks.json`
- Rebuild: `python3 tools/build_site.py` · Coordination log: `COORDINATION.md`

Snapshot date: 26 Oct 2026. Lines are originated estimates (fair decimal = 1 / estimated probability),
not bookmaker odds. 18+ Gamble Responsibly. Information only, not financial advice.

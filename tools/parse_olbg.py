import re, json, sys, os

def parse(md):
    md = md.replace('\\|','|')
    # split on list items that start an event block
    blocks = re.split(r'\n- \[', md)
    rows = []
    for b in blocks[1:]:
        m = re.match(r'\*\*(.+?)\*\*\]\((https://www\.olbg\.com/[^)\s"]+)', b)
        if not m: continue
        ev, url = m.group(1).strip(), m.group(2)
        if '/bookmakers/articles' in url: continue
        eid = re.search(r'event_id=(\d+)', url)
        # competition = plain line after the url quote block (first non-empty line not bold)
        comp = None
        mm = re.search(r'""\)\s*\n\s*([A-Za-z0-9][^\n*]+?)\s*\n\s*\n\s*(Today|Tomorrow|Mon|Tue|Wed|Thu|Fri|Sat|Sun)', b)
        if mm: comp = mm.group(1).strip()
        when = None
        mw = re.search(r'\n\s*(Today|Tomorrow|Yesterday)\s+(\d{1,2}:\d{2})', b)
        if not mw:
            mw = re.search(r'\n\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*\s+(\d{1,2}:\d{2})', b)
        if mw: when = mw.group(1) + ' ' + mw.group(2)
        # popular selection + market: selection link appears after the 'when'
        tail = b[mw.end():] if mw else b
        ms = re.search(r'\[?\*\*([^*\]]+?)\*\*\]?\s*\n\s*(Money Line|Pointspread|Game Totals|Puck Line|Win Match|Win Tournament|To Win|Handicap|Outright Winner|Top Team\d Batsman|Man Of The Match|Daily Races|Win Hurling|To Qualify|Total|[A-Z][A-Za-z0-9 ()&\'\-\.]{2,34})\s*\n', tail)
        sel = mkt = None
        if ms: sel, mkt = ms.group(1).strip(), ms.group(2).strip()
        mt = re.search(r'\*\*(\d+)/(\d+) Win Tips\*\*\s*\n\s*(\d+)%', tail)
        tips_t = tips_m = pct = None
        if mt: tips_t, tips_m, pct = int(mt.group(1)), int(mt.group(2)), int(mt.group(3))
        ncom = re.search(r'(\d+) comments?', tail)
        nex = re.search(r'(\d+) expert', tail)
        rows.append(dict(event=ev, url=url.split(' "')[0], event_id=eid.group(1) if eid else None,
            competition=comp, when=when, selection=sel, market=mkt, tips_on_pick=tips_t,
            tips_total=tips_m, pct=pct, comments=int(ncom.group(1)) if ncom else 0,
            experts=int(nex.group(1)) if nex else 0))
    seen=set(); out=[]
    for r in rows:
        k=(r['event'],r['selection'],r['market'])
        if k in seen: continue
        seen.add(k); out.append(r)
    return out

if __name__=='__main__':
    src=sys.argv[1]; sport=sys.argv[2]
    md=open(src).read()
    rows=parse(md)
    p=f'/home/user/Olbg7/data/cycle-20261027/raw_{sport}.json'
    prev = json.load(open(p)) if os.path.exists(p) else []
    seen={x['event'] for x in prev}
    json.dump(prev+[r for r in rows if r['event'] not in seen], open(p,'w'), indent=1)
    print(sport, len(rows), 'parsed;', len(prev)+len([r for r in rows if r['event'] not in seen]), 'total')
    for r in rows[:6]: print('  ', r['event'],'|',r['competition'],'|',r['when'],'|',r['selection'],'|',r['market'],'|',r['tips_on_pick'],'/',r['tips_total'],r['pct'])

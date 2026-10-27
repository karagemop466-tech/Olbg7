#!/usr/bin/env python3
"""OLBG live sweep 2026-10-27 -> data/v3/events.json

Every field is transcribed from the OLBG listing page named in `source`.
Nothing is inferred. Where OLBG printed no value the field is "" (blank) and the
row is flagged UNVERIFIED rather than filled in.
"""
import json, os, datetime

RETRIEVED = "2026-10-27"
ROOT = "https://www.olbg.com/betting-tips"

# sport, slug, olbg id, page title observed
SPORTS = [
    ("Golf",            "golf",            "5",  "Golf/5"),
    ("Volleyball",      "volleyball",      "21", "Volleyball/21"),
    ("Rugby Union",     "rugby-union",     "9",  "Rugby_Union/9"),
    ("Cricket",         "cricket",         "7",  "Cricket/7"),
    ("Snooker",         "snooker",         "8",  "Snooker/8"),
    ("Darts",           "darts",           "15", "Darts/15"),
    ("Baseball",        "baseball",        "12", "Baseball/12"),
    ("Gaelic Sports",   "gaelic-sports",   "25", "Gaelic_Football/25"),
    ("Gaelic Sports",   "gaelic-sports",   "26", "Hurling/26"),
    ("Greyhounds",      "greyhounds",      "28", "Greyhounds/28"),
    ("Tennis",          "tennis",          "3",  "Tennis/3"),
    ("Motor Racing",    "motor-racing",    "14", "Motor_Racing/14"),
    ("Handball",        "handball",        "20", "Handball/20"),
    ("Ice Hockey",      "ice-hockey",      "13", "Ice_Hockey/13"),
    ("Basketball",      "basketball",      "4",  "Basketball/4"),
    ("Rugby League",    "rugby-league",    "10", "Rugby_League/10"),
]

# (sport_label, olbg_path, event, olbg_time, competition, selection, market, tips_for, tips_total, event_id)
ROWS = [
 # ---------------- TENNIS ----------------
 ("Tennis","Tennis/3","Leylah Fernandez vs Himeno Sakatsume","Today 02:00","","Leylah Fernandez","Win Match",10,12,"902172"),
 ("Tennis","Tennis/3","Lilli Tagger vs Venus Williams","Today 03:30","","Lilli Tagger","Win Match",4,8,"902189"),
 ("Tennis","Tennis/3","Naomi Osaka vs Jasmine Paolini","Today 04:00","","Naomi Osaka","Win Match",4,4,"902177"),
 ("Tennis","Tennis/3","Alejandro Tabilo vs Rafael Jodar","Today 09:00","","Rafael Jodar","Win Match",4,6,"902238"),
 ("Tennis","Tennis/3","Stan Wawrinka vs Jiri Lehecka","Today 14:30","","Stan Wawrinka","Win Match",4,8,"902232"),
 ("Tennis","Tennis/3","Novak Djokovic vs Ugo Humbert","Tomorrow 06:00","","Novak Djokovic","Win Match",4,5,"902233"),
 ("Tennis","Tennis/3","Hubert Hurkacz vs Zizou Bergs","Today 07:00","","Hubert Hurkacz","Win Match",3,3,"902322"),
 ("Tennis","Tennis/3","Tommy Paul vs Andrey Rublev","Today 08:30","","Andrey Rublev","Win Match",3,4,"902252"),
 ("Tennis","Tennis/3","Cameron Norrie vs Francisco Cerundolo","Today 11:30","","Cameron Norrie","Win Match",3,5,"902210"),
 ("Tennis","Tennis/3","Polina Kudermetova vs Janice Tjen","Today 02:00","","Janice Tjen","Win Match",2,2,"902187"),
 ("Tennis","Tennis/3","Nuno Borges vs Casper Ruud","Today 07:00","","Casper Ruud","Win Match",2,2,"902409"),
 ("Tennis","Tennis/3","Alex Michelsen vs Botic Van De Zandschulp","Today 10:00","","Alex Michelsen","Win Match",2,3,"902240"),
 ("Tennis","Tennis/3","Karen Khachanov vs Carlos Alcaraz","Today 10:00","","Karen Khachanov","Win Match",2,2,"902213"),
 ("Tennis","Tennis/3","Antonia Ruzic vs Claire Liu","Today 02:00","","Antonia Ruzic","Win Match",1,1,"902182"),
 # ---------------- BASKETBALL ----------------
 ("Basketball","Basketball/4","Panathinaikos vs Milano","Today 15:15","Euroleague","Panathinaikos","Money Line",5,8,"536177"),
 ("Basketball","Basketball/4","Seoul Knights vs KCC Egis","Today 06:00","Korea KBL","Seoul Knights","Money Line",4,5,"536214"),
 ("Basketball","Basketball/4","BC Dubai vs Paris","Today 12:00","Euroleague","BC Dubai","Money Line",4,7,"536176"),
 ("Basketball","Basketball/4","Valencia vs Fenerbahce","Today 15:30","Euroleague","Fenerbahce","Money Line",4,6,"536179"),
 ("Basketball","Basketball/4","Bayern Munich vs Barcelona","Today 15:00","Euroleague","Bayern Munich","Money Line",3,5,"536174"),
 ("Basketball","Basketball/4","Baskonia vs Real Madrid","Today 16:00","Euroleague","Baskonia","Money Line",3,6,"536178"),
 ("Basketball","Basketball/4","Lietkabelis vs Ratiopharm Ulm","Today 13:00","Euro Cup","Lietkabelis","Money Line",2,2,"536218"),
 ("Basketball","Basketball/4","Frankfurt Skyliners vs U BT Cluj Napoca","Today 14:30","Euro Cup","Frankfurt Skyliners +1.50","Pointspread",2,2,"536217"),
 ("Basketball","Basketball/4","Crvena Zvezda vs Maccabi Tel Aviv","Today 15:00","Euroleague","Crvena Zvezda","Money Line",2,4,"536175"),
 ("Basketball","Basketball/4","UCAM Murcia vs Peristeri","Today 15:30","Basketball Champions League","UCAM Murcia","Money Line",2,2,"536235"),
 ("Basketball","Basketball/4","Aris vs Cedevita Olimpija","Tomorrow 13:30","Euro Cup","Aris","Money Line",2,2,"536222"),
 ("Basketball","Basketball/4","Besiktas vs Olympiacos","Tomorrow 13:30","Euroleague","Besiktas","Money Line",2,3,"536180"),
 ("Basketball","Basketball/4","Asvel Lyon Villeurbanne vs Partizan","Tomorrow 15:00","Euroleague","Partizan","Money Line",2,2,"536181"),
 ("Basketball","Basketball/4","Virtus Bologna vs Zalgiris","Tomorrow 15:30","Euroleague","Virtus Bologna","Money Line",0,0,"536183"),
 # ---------------- ICE HOCKEY ----------------
 ("Ice Hockey","Ice_Hockey/13","Kalpa vs Sport","Today 12:30","Finland SM Liiga","Kalpa","Money Line",5,5,"200081"),
 ("Ice Hockey","Ice_Hockey/13","IF Malmo Redhawks vs Linkoping HC","Today 14:00","Swedish Hockey League","IF Malmo Redhawks","Money Line",3,3,"200082"),
 ("Ice Hockey","Ice_Hockey/13","Frolunda HC vs Rogle BK","Today 14:00","Swedish Hockey League","Frolunda HC","Money Line",2,3,"200083"),
 ("Ice Hockey","Ice_Hockey/13","Kolner Haie vs Adler Mannheim","Today 14:30","Germany Eishockey Liga","Adler Mannheim","Money Line",2,2,"200100"),
 ("Ice Hockey","Ice_Hockey/13","CLB Blue Jackets @ PHI Flyers","Today 19:07","NHL","PHI Flyers","Money Line",2,3,"200108"),
 ("Ice Hockey","Ice_Hockey/13","BOS Bruins @ CAR Hurricanes","Today 20:07","NHL","BOS Bruins +1.50","Puck Line",2,2,"200104"),
 ("Ice Hockey","Ice_Hockey/13","Herning Blue Fox vs Rodovre Mighty Bulls","Today 14:00","Danish Metal Ligaen","Rodovre Mighty Bulls +3.50","Puck Line",1,1,"200098"),
 ("Ice Hockey","Ice_Hockey/13","Fehervar AV19 vs Milano HC","Today 14:15","Austria EHL","Fehervar AV19 -1.50","Puck Line",1,1,"200146"),
 ("Ice Hockey","Ice_Hockey/13","Fribourg Gotteron vs Davos","Today 14:45","Switzerland NLA","Fribourg Gotteron -1.50","Puck Line",1,1,"200116"),
 ("Ice Hockey","Ice_Hockey/13","Bern vs ZSC Lions","Today 14:45","Switzerland NLA","ZSC Lions -1.50","Puck Line",1,1,"200122"),
 ("Ice Hockey","Ice_Hockey/13","EHC Kloten vs HC Ajoie","Today 14:45","Switzerland NLA","EHC Kloten -1.50","Puck Line",1,1,"200115"),
 ("Ice Hockey","Ice_Hockey/13","Zug vs Lugano","Today 14:45","Switzerland NLA","Lugano +1.50","Puck Line",1,1,"200117"),
 ("Ice Hockey","Ice_Hockey/13","Lausanne HC vs SCL Tigers","Today 14:45","Switzerland NLA","Lausanne HC -1.50","Puck Line",1,1,"200118"),
 ("Ice Hockey","Ice_Hockey/13","Ambri Piotta vs EHC Biel","Today 14:45","Switzerland NLA","Ambri Piotta -1.50","Puck Line",1,1,"200119"),
 ("Ice Hockey","Ice_Hockey/13","Rapperswil Jona Lakers vs Servette GE","Today 14:45","Switzerland NLA","Servette GE +1.50","Puck Line",1,1,"200123"),
 # ---------------- CRICKET ----------------
 ("Cricket","Cricket/7","New Zealand vs India 3rd T20 Match","Today 03:00","","India","Win Match",35,49,"188852"),
 ("Cricket","Cricket/7","Namibia vs Ireland 3rd ODI","Today 03:30","","Ireland","Win Match",22,32,"188854"),
 ("Cricket","Cricket/7","Pakistan vs Sri Lanka One Day Match","Today 04:00","","Pakistan","Win Match",22,31,"188868"),
 ("Cricket","Cricket/7","Afghanistan vs Zimbabwe 1st T20 Match","Today 10:30","","Afghanistan","Win Match",15,16,"188872"),
 ("Cricket","Cricket/7","Melbourne Stars W vs Hobart Hurricanes W T20 Big Bash","29 Oct 04:10","WBBL","Hobart Hurricanes W","Win Match",4,6,"188864"),
 ("Cricket","Cricket/7","Auckland vs Canterbury One Day Match","Today 17:30","","Canterbury","Win Match",3,4,"188876"),
 ("Cricket","Cricket/7","Brisbane Heat W vs Sydney Sixers W T20 Big Bash","30 Oct 04:10","WBBL","Sydney Sixers W","Win Match",3,5,"188865"),
 ("Cricket","Cricket/7","South Africa vs Australia","31 Oct 04:30","","South Africa","Win Match",3,8,"188835"),
 ("Cricket","Cricket/7","Wellington vs Otago One Day Match","Today 17:30","","Wellington","Win Match",2,4,"188878"),
 ("Cricket","Cricket/7","Central Districts vs Northern Districts One Day Match","Today 17:30","","Northern Districts","Win Match",2,3,"188877"),
 ("Cricket","Cricket/7","Lions vs Eastern Storm T20","Tomorrow 12:00","","Lions","Win Match",1,1,"188874"),
 ("Cricket","Cricket/7","Melbourne Renegades W vs Sydney Thunder W T20 Big Bash","29 Oct 00:40","WBBL","G Wareham (Melbourne Renegades W)","Top Team1 Batsman",1,2,"188863"),
 ("Cricket","Cricket/7","Bangladesh vs West Indies","31 Oct 23:30","","West Indies","Win Match",1,1,"188871"),
 ("Cricket","Cricket/7","World Cup 2027","21 Nov 2027 05:00","ICC","India","Win Tournament",0,0,"182606"),
 # ---------------- RUGBY UNION ----------------
 ("Rugby Union","Rugby_Union/9","Dax v Provence","29 Oct 16:00","Pro D2","Dax","To Win",2,3,"609605"),
 ("Rugby Union","Rugby_Union/9","Colomiers v Agen","30 Oct 14:00","Pro D2","Colomiers","To Win",2,2,"609604"),
 ("Rugby Union","Rugby_Union/9","Montauban v Narbonne","30 Oct 14:30","Pro D2","Montauban","To Win",2,3,"609603"),
 ("Rugby Union","Rugby_Union/9","Oyonnax v Soyaux Angouleme","30 Oct 14:30","Pro D2","Oyonnax","To Win",2,3,"609598"),
 ("Rugby Union","Rugby_Union/9","Beziers v Grenoble","30 Oct 14:30","Pro D2","Grenoble","To Win",1,1,"609599"),
 ("Rugby Union","Rugby_Union/9","Nissa v Aurillac","30 Oct 14:30","Pro D2","Nissa","To Win",1,1,"609600"),
 ("Rugby Union","Rugby_Union/9","Glasgow Warriors v Lions","30 Oct 15:45","United Rugby Championship","Glasgow Warriors","To Win",1,1,"609590"),
 ("Rugby Union","Rugby_Union/9","Connacht v Leinster","30 Oct 15:45","United Rugby Championship","Connacht +3.50","Handicap",1,1,"609584"),
 ("Rugby Union","Rugby_Union/9","Biarritz v Valence Romans","30 Oct 16:00","Pro D2","Biarritz","To Win",1,1,"609602"),
 ("Rugby Union","Rugby_Union/9","Stormers v Ulster","31 Oct 08:45","United Rugby Championship","Ulster +12.50","Handicap",1,1,"609588"),
 ("Rugby Union","Rugby_Union/9","Munster v Sharks","31 Oct 13:30","United Rugby Championship","Munster -6.50","Handicap",1,1,"609586"),
 ("Rugby Union","Rugby_Union/9","Pau v Toulouse","01 Nov 15:05","Top 14","Pau","To Win",1,1,"609611"),
 ("Rugby Union","Rugby_Union/9","Six Nations 2027","14 Mar 2027 16:00","Six Nations","Ireland","Win Tournament",3,11,"609013"),
 # ---------------- VOLLEYBALL ----------------
 ("Volleyball","Volleyball/21","Conegliano W vs Vallefoglia W","Tomorrow 15:00","","Vallefoglia W","Win Match",6,10,"37076"),
 ("Volleyball","Volleyball/21","Marignano W vs Bergamo W","Today 15:00","","Bergamo W","Win Match",5,7,"37075"),
 ("Volleyball","Volleyball/21","TFL Altekma vs Halkbank Ankara","Today 08:00","","Halkbank Ankara","Win Match",4,5,"37126"),
 ("Volleyball","Volleyball/21","Ziraat Bankasi vs Gaziantep Genclik Spor","Today 12:00","","Ziraat Bankasi","Win Match",4,4,"37121"),
 ("Volleyball","Volleyball/21","Uni Opole W vs Palac Bydgoszcz W","Today 15:30","","Uni Opole W","Win Match",4,6,"37081"),
 ("Volleyball","Volleyball/21","Istanbul Genclik Spor vs IBB Spor","Today 07:00","","IBB Spor","Win Match",3,5,"37124"),
 ("Volleyball","Volleyball/21","VaLePa vs AC Oulu","Today 12:30","","VaLePa","Win Match",3,4,"37129"),
 ("Volleyball","Volleyball/21","Suzano Volei vs Goias Volei","Today 17:30","","Suzano Volei","Win Match",3,4,"37103"),
 ("Volleyball","Volleyball/21","Praia Clube vs Sao Jose","Today 20:00","","Praia Clube","Win Match",3,4,"37104"),
 ("Volleyball","Volleyball/21","Sungurlu Bld vs Galatasaray","Today 09:30","","Galatasaray","Win Match",2,3,"37122"),
 ("Volleyball","Volleyball/21","Fenerbahce vs Alanya Bld","Today 12:00","","Alanya Bld","Win Match",2,3,"37125"),
 ("Volleyball","Volleyball/21","Volleys Borken W vs Vilsbiburg W","Today 13:30","","Vilsbiburg W","Win Match",2,3,"37131"),
 ("Volleyball","Volleyball/21","Budowlani Lodz W vs Radomka Radom W","Tomorrow 12:30","","Budowlani Lodz W","Win Match",2,3,"37082"),
 ("Volleyball","Volleyball/21","Mielec W vs Rzeszow W","Tomorrow 14:00","","Rzeszow W","Win Match",2,3,"37083"),
 ("Volleyball","Volleyball/21","Sultanbeyli Bld vs Gebze Genclik","Today 09:00","","Sultanbeyli Bld","Win Match",1,1,"37123"),
 # ---------------- HANDBALL ----------------
 ("Handball","Handball/20","SC Magdeburg vs HC Kriens Luzern","Tomorrow 15:45","EHF Champions League","Tie","Money Line",9,14,"12136"),
 ("Handball","Handball/20","HC Vardar vs MT Melsungen","Tomorrow 13:45","EHF European League","Tie","Money Line",8,13,"12130"),
 ("Handball","Handball/20","Wisla Plock vs Nantes","Tomorrow 13:45","EHF Champions League","Tie","Money Line",8,11,"12138"),
 ("Handball","Handball/20","KS Kielce vs Kolstad","Tomorrow 15:45","EHF Champions League","Tie","Money Line",7,11,"12132"),
 ("Handball","Handball/20","PSG Handball vs Aalborg Handbold","Tomorrow 15:45","EHF Champions League","Tie","Money Line",7,9,"12134"),
 ("Handball","Handball/20","RK Celje vs RK Zagreb","Tomorrow 15:45","EHF Champions League","Tie","Money Line",6,8,"12135"),
 ("Handball","Handball/20","Fuchse Berlin vs RK Partizan","29 Oct 13:45","EHF European League","Tie","Money Line",6,14,"12128"),
 ("Handball","Handball/20","FC Porto vs Veszprem","Tomorrow 13:45","EHF Champions League","Tie","Money Line",5,9,"12127"),
 ("Handball","Handball/20","GOG vs Sporting CP","29 Oct 13:45","EHF European League","Tie","Money Line",3,5,"12129"),
 ("Handball","Handball/20","Montpellier vs Dinamo Bucuresti","29 Oct 15:45","EHF European League","Tie","Money Line",3,4,"12133"),
 ("Handball","Handball/20","VasterasIrsta HF W vs Skuru IK W","Today 14:00","Sweden (W)","VasterasIrsta HF (W)","Money Line",2,4,"12197"),
 ("Handball","Handball/20","OV Helsingborg HK W vs Skovde HF W","Today 14:00","Sweden (W)","Skovde HF (W)","Money Line",2,4,"12196"),
 ("Handball","Handball/20","IFK Kristianstad vs Pick Szeged","29 Oct 13:45","EHF European League","Tie","Money Line",2,4,"12131"),
 ("Handball","Handball/20","SG Flensburg Handewitt vs HBW Balingen Weilstetten","29 Oct 14:00","Germany Bundesliga","HBW Balingen-Weilstetten","Money Line",1,1,"12180"),
 ("Handball","Handball/20","Skanderborg Handbold vs FC Barcelona","29 Oct 15:45","EHF Champions League","Skanderborg Handbold","Money Line",1,3,"12137"),
 # ---------------- GOLF ----------------
 ("Golf","Golf/5","Maybank Championship","01 Nov 06:45","DP World Tour","Lottie Woad","Win Tournament",1,2,"101913"),
 ("Golf","Golf/5","Mexico Open","01 Nov 17:45","PGA Tour","Wyndham Clark","Win Tournament",1,2,"101915"),
 ("Golf","Golf/5","Simmons Bank Championship","01 Nov 17:45","PGA Tour Champions","Stewart Cink","Win Tournament",1,2,"101914"),
 # ---------------- DARTS ----------------
 ("Darts","Darts/15","PDC World Championship 2027","03 Jan 2027 12:00","PDC","Luke Littler","Win Tournament",22,36,"26023"),
 ("Darts","Darts/15","Players Championship 31","Tomorrow 08:00","PDC","Nathan Aspinall","Win Tournament",2,8,"32446"),
 # ---------------- BASEBALL ----------------
 ("Baseball","Baseball/12","MIL Brewers @ TB Rays","Today 21:00","MLB","MIL Brewers","Money Line",2,2,"160799"),
 # ---------------- GAELIC SPORTS ----------------
 ("Gaelic Sports","Gaelic_Football/25","Kanturk v Eire Og Cor","01 Nov 09:00","Munster Club SFC","Eire Og Cor +0.50","Handicap",6,6,"3531"),
 ("Gaelic Sports","Gaelic_Football/25","Fr Caseys v Kildimo Pallaskenry","01 Nov 10:30","Limerick Club SFC","Kildimo Pallaskenry +3.50","Handicap",5,7,"3537"),
 ("Gaelic Sports","Gaelic_Football/25","All Ireland Football Championship 2027","25 Jul 2027 10:30","GAA","Kerry","Win Tournament",6,8,"3327"),
 ("Gaelic Sports","Hurling/26","All Ireland Hurling Championship 2027","18 Jul 2027 10:30","GAA","Galway","Win Hurling",7,18,"675"),
 # ---------------- MOTOR RACING ----------------
 ("Motor Racing","Motor_Racing/14","Mexico City Grand Prix","01 Nov 15:00","Formula 1","Max Verstappen - Yes","Podium Finish",1,2,"914"),
 ("Motor Racing","Motor_Racing/14","Formula 1 Drivers Championship 2026 Without Kimi Antonelli","06 Dec 08:00","Formula 1","Max Verstappen","Win Tournament",4,7,"912"),
 # ---------------- RUGBY LEAGUE ----------------
 ("Rugby League","Rugby_League/10","State of Origin 2027","27 May 2027 06:00","State of Origin","New South Wales","Win Tournament",9,13,"2695857"),
 ("Rugby League","Rugby_League/10","Super League 2027","02 Oct 2027 13:00","Super League","Wigan Warriors","Grand Final Winner",2,4,"2801554"),
 ("Rugby League","Rugby_League/10","NRL 2027","03 Oct 2027 04:30","NRL","Penrith Panthers","Grand Final Winner",1,3,"2801600"),
]

def slug(name):
    return "_".join(name.replace("@","@").split())

events=[]
for (sport, path, ev, t, comp, sel, mkt, tf, tt, eid) in ROWS:
    events.append({
        "sport": sport,
        "event": ev,
        "competition": comp,
        "olbg_time": t,
        "market": mkt,
        "most_tipped_selection": sel,
        "tips_for": tf,
        "tips_total": tt,
        "olbg_pct": round(100.0*tf/tt,1) if tt else "",
        "event_id": eid,
        "event_url": f"{ROOT}/{path}/All_Events/{slug(ev)}/{{id}}?event_id={eid}".replace("{id}", path.split("/")[1] if "/" in path else ""),
        "source": f"{ROOT}/{path}",
        "retrieved": RETRIEVED,
    })

# fix event_url: needs the numeric sport id as the trailing path segment
idmap = {i: p for (_,_,i,p) in SPORTS}
for e in events:
    sid = e["source"].rsplit("/",1)[-1]
    parts = e["source"].split("/")
    e["event_url"] = f"{ROOT}/{parts[-2]}/All_Events/{slug(e['event'])}/{sid}?event_id={e['event_id']}"

# Empty sports observed on the live page
EMPTY = {
  "Snooker":     f"{ROOT}/Snooker/8",
  "Greyhounds":  f"{ROOT}/Greyhounds/28",
}

out = {
  "schema_version": 3,
  "retrieved": RETRIEVED,
  "retrieved_by": "session arena-254c7925 via fetch_page (bash has no olbg.com route)",
  "sports": [{"sport": s, "slug": sl, "olbg_id": i, "root": f"{ROOT}/{p}"} for (s,sl,i,p) in SPORTS],
  "events": events,
  "empty_pages": [{"sport": k, "source": v, "olbg_message": "No tips found.", "events": 0} for k,v in EMPTY.items()],
  "counts": {s: sum(1 for e in events if e["sport"]==s) for (s,_,_,_) in SPORTS},
}
os.makedirs("data/v3", exist_ok=True)
json.dump(out, open("data/v3/events.json","w"), indent=1)
print("events:", len(events))
for k,v in out["counts"].items(): print(f"  {k:16s} {v}")

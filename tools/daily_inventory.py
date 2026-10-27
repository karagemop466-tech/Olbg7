#!/usr/bin/env python3
"""Transcribed 2026-10-27 OLBG listing inventory.

The compact tuples below are manual transcriptions of the retrieved public OLBG
listing pages. No missing tip percentage, market label, bookmaker price, or start
timezone is filled in by inference. Event URLs use the link grammar displayed by
OLBG and the event id/slug in each retrieved link.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "daily" / "2026-10-27" / "inventory.json"
DAY = "2026-10-27"

HUBS = {
    "Golf": "https://www.olbg.com/betting-tips/Golf/5",
    "Volleyball": "https://www.olbg.com/betting-tips/Volleyball/21",
    "Rugby Union": "https://www.olbg.com/betting-tips/Rugby_Union/9",
    "Cricket": "https://www.olbg.com/betting-tips/Cricket/7",
    "Snooker": "https://www.olbg.com/betting-tips/Snooker/8",
    "Darts": "https://www.olbg.com/betting-tips/Darts/15",
    "Baseball": "https://www.olbg.com/betting-tips/Baseball/12",
    "Gaelic Sports": "https://www.olbg.com/betting-tips/Gaelic_Football/25",
    "Greyhounds": "https://www.olbg.com/betting-tips/Greyhounds/28",
    "Tennis": "https://www.olbg.com/betting-tips/Tennis/3",
    "Motor Racing": "https://www.olbg.com/betting-tips/Motor_Racing/14",
    "Handball": "https://www.olbg.com/betting-tips/Handball/20",
    "Ice Hockey": "https://www.olbg.com/betting-tips/Ice_Hockey/13",
    "Basketball": "https://www.olbg.com/betting-tips/Basketball/4",
    "Rugby League": "https://www.olbg.com/betting-tips/Rugby_League/10",
}

SPORT_PATH = {
    "Golf": ("Golf", 5), "Volleyball": ("Volleyball", 21),
    "Rugby Union": ("Rugby_Union", 9), "Cricket": ("Cricket", 7),
    "Darts": ("Darts", 15), "Tennis": ("Tennis", 3),
    "Motor Racing": ("Motor_Racing", 14), "Handball": ("Handball", 20),
    "Rugby League": ("Rugby_League", 10),
}

# sport, competition, event, OLBG event id, start label, most-tipped selection,
# market label (None when absent), win tips/total tips (None when absent),
# displayed percentage (None when absent)
R = []
def add(sport, competition, rows):
    for event, event_id, start, selection, market, tips, pct in rows:
        R.append(dict(sport=sport, competition=competition, event=event,
                      event_id=str(event_id), start_label=start,
                      selection=selection, market=market, tips=tips, pct=pct))

add("Golf", "All Golf", [
    ("Maybank Championship", 101913, "01 Nov 06:45", "Lottie Woad", "Win Tournament", "1/2", 50),
    ("Mexico Open", 101915, "01 Nov 17:45", "Wyndham Clark", "Win Tournament", "1/2", 50),
    ("Simmons Bank Championship", 101914, "01 Nov 17:45", "Stewart Cink", "Win Tournament", "1/2", 50),
])
add("Darts", "All Darts", [
    ("PDC World Championship 2027", 26023, "03 Jan 2027 12:00", "Luke Littler", "Win Tournament", "22/36", 61),
    ("Players Championship 31", 32446, "Tomorrow 08:00", "Nathan Aspinall", "Win Tournament", "2/8", 25),
])
add("Motor Racing", "All Motor Racing", [
    ("Formula 1 Drivers Championship 2026 Without Kimi Antonelli", 912, "06 Dec 08:00", "Max Verstappen", "Win Tournament", "4/7", 57),
    ("Mexico City Grand Prix", 914, "01 Nov 15:00", "Max Verstappen - Yes", "Podium Finish", "1/2", 50),
])
add("Baseball", "MLB", [
    ("MIL Brewers @ TB Rays", 160799, "Today 21:00", "MIL Brewers", "Money Line", "2/2", 100),
])
add("Gaelic Sports", "Gaelic Football", [
    ("Kanturk v Eire Og Cor", 3531, "01 Nov 09:00", "Eire Og Cor +0.50", None, "6/6", 100),
    ("Fr Caseys v Kildimo Pallaskenry", 3537, "01 Nov 10:30", "Kildimo Pallaskenry +3.50", None, "5/7", 71),
    ("All Ireland Football Championship 2027", 3327, "25 Jul 2027 10:30", "Kerry", None, "6/8", 75),
])
add("Gaelic Sports", "Hurling", [
    ("All Ireland Hurling Championship 2027", 675, "18 Jul 2027 10:30", "Galway", "Win Hurling", "7/18", 39),
])
add("Rugby League", "All Rugby League", [
    ("State of Origin 2027", 2695857, "27 May 2027 06:00", "New South Wales", "Win Tournament", "9/13", 69),
    ("Super League 2027", 2801554, "02 Oct 2027 13:00", "Wigan Warriors", "Grand Final Winner", "2/4", 50),
    ("NRL 2027", 2801600, "03 Oct 2027 04:30", "Penrith Panthers", "Grand Final Winner", "1/3", 33),
])
add("Rugby Union", "All Rugby Union", [
    ("Dax v Provence", 609605, "29 Oct 16:00", "Dax", "To Win", "2/3", 67),
    ("Colomiers v Agen", 609604, "30 Oct 14:00", "Colomiers", "To Win", "2/2", 100),
    ("Montauban v Narbonne", 609603, "30 Oct 14:30", "Montauban", "To Win", "2/3", 67),
    ("Oyonnax v Soyaux Angouleme", 609598, "30 Oct 14:30", "Oyonnax", "To Win", "2/3", 67),
    ("Beziers v Grenoble", 609599, "30 Oct 14:30", "Grenoble", "To Win", "1/1", 100),
    ("Nissa v Aurillac", 609600, "30 Oct 14:30", "Nissa", "To Win", "1/1", 100),
    ("Glasgow Warriors v Lions", 609590, "30 Oct 15:45", "Glasgow Warriors", "To Win", "1/1", 100),
    ("Connacht v Leinster", 609584, "30 Oct 15:45", "Connacht +3.50", "Handicap", "1/1", 100),
    ("Biarritz v Valence Romans", 609602, "30 Oct 16:00", "Biarritz", "To Win", "1/1", 100),
    ("Stormers v Ulster", 609588, "31 Oct 08:45", "Ulster +12.50", "Handicap", "1/1", 100),
    ("Munster v Sharks", 609586, "31 Oct 13:30", "Munster -6.50", "Handicap", "1/1", 100),
    ("Pau v Toulouse", 609611, "01 Nov 15:05", "Pau", "To Win", "1/1", 100),
    ("Six Nations 2027", 609013, "14 Mar 2027 16:00", "Ireland", "Win Tournament", "3/11", 27),
])
add("Tennis", "All Tennis", [
    ("Leylah Fernandez vs Himeno Sakatsume", 902172, "Today 02:00", "Leylah Fernandez", "Win Match", "10/12", 83),
    ("Lilli Tagger vs Venus Williams", 902189, "Today 03:30", "Lilli Tagger", "Win Match", "4/8", 50),
    ("Naomi Osaka vs Jasmine Paolini", 902177, "Today 04:00", "Naomi Osaka", "Win Match", "4/4", 100),
    ("Alejandro Tabilo vs Rafael Jodar", 902238, "Today 09:00", "Rafael Jodar", "Win Match", "4/6", 67),
    ("Stan Wawrinka vs Jiri Lehecka", 902232, "Today 14:30", "Stan Wawrinka", "Win Match", "4/8", 50),
    ("Novak Djokovic vs Ugo Humbert", 902233, "Tomorrow 06:00", "Novak Djokovic", "Win Match", "4/5", 80),
    ("Hubert Hurkacz vs Zizou Bergs", 902322, "Today 07:00", "Hubert Hurkacz", "Win Match", "3/3", 100),
    ("Tommy Paul vs Andrey Rublev", 902252, "Today 08:30", "Andrey Rublev", "Win Match", "3/4", 75),
    ("Cameron Norrie vs Francisco Cerundolo", 902210, "Today 11:30", "Cameron Norrie", "Win Match", "3/5", 60),
    ("Polina Kudermetova vs Janice Tjen", 902187, "Today 02:00", "Janice Tjen", "Win Match", "2/2", 100),
    ("Nuno Borges vs Casper Ruud", 902409, "Today 07:00", "Casper Ruud", "Win Match", "2/2", 100),
    ("Alex Michelsen vs Botic Van De Zandschulp", 902240, "Today 10:00", "Alex Michelsen", "Win Match", "2/3", 67),
    ("Karen Khachanov vs Carlos Alcaraz", 902213, "Today 10:00", "Karen Khachanov", "Win Match", "2/2", 100),
    ("Antonia Ruzic vs Claire Liu", 902182, "Today 02:00", "Antonia Ruzic", "Win Match", "1/1", 100),
    ("Tereza Valentova vs Mia Pohankova", 902310, "Today 02:30", "Tereza Valentova", "Win Match", "1/1", 100),
    ("Lucrezia Stefanini vs Isabella Maria Serban", 902372, "Today 06:00", "Lucrezia Stefanini", "Win Match", "1/1", 100),
    ("Danka Kovinic vs Noma Noha Akugue", 902374, "Today 06:00", "Noma Noha Akugue", "Win Match", "1/1", 100),
    ("Xinran Sun vs Mananchaya Sawangkaew", 902183, "Today 07:00", "Mananchaya Sawangkaew", "Win Match", "1/1", 100),
    ("Marina Bassols Ribera vs Victoria Jimenez Kasintseva", 902378, "Today 07:30", "Marina Bassols Ribera", "Win Match", "1/1", 100),
    ("Jerome Kym vs Arthur Rinderknech", 902234, "Today 08:30", "Jerome Kym", "Win Match", "1/2", 50),
])
add("Cricket", "All Cricket", [
    ("New Zealand vs India 3rd T20 Match", 188852, "Today 03:00", "India", "Win Match", "35/49", 71),
    ("Namibia vs Ireland 3rd ODI", 188854, "Today 03:30", "Ireland", "Win Match", "22/32", 69),
    ("Pakistan vs Sri Lanka One Day Match", 188868, "Today 04:00", "Pakistan", "Win Match", "22/31", 71),
    ("Afghanistan vs Zimbabwe 1st T20 Match", 188872, "Today 10:30", "Afghanistan", "Win Match", "15/16", 94),
    ("Melbourne Stars W vs Hobart Hurricanes W T20 Big Bash", 188864, "29 Oct 04:10", "Hobart Hurricanes W", "Win Match", "4/6", 67),
    ("Auckland vs Canterbury One Day Match", 188876, "Today 17:30", "Canterbury", "Win Match", "3/4", 75),
    ("Brisbane Heat W vs Sydney Sixers W T20 Big Bash", 188865, "30 Oct 04:10", "Sydney Sixers W", "Win Match", "3/5", 60),
    ("South Africa vs Australia", 188835, "31 Oct 04:30", "South Africa", "Win Match", "3/8", 38),
    ("Wellington vs Otago One Day Match", 188878, "Today 17:30", "Wellington", "Win Match", "2/4", 50),
    ("Central Districts vs Northern Districts One Day Match", 188877, "Today 17:30", "Northern Districts", "Win Match", "2/3", 67),
    ("Lions vs Eastern Storm T20", 188874, "Tomorrow 12:00", "Lions", "Win Match", "1/1", 100),
    ("Melbourne Renegades W vs Sydney Thunder W T20 Big Bash", 188863, "29 Oct 00:40", "G Wareham (Melbourne Renegades W)", "Top Team1 Batsman", "1/2", 50),
    ("Bangladesh vs West Indies", 188871, "31 Oct 23:30", "West Indies", "Win Match", "1/1", 100),
    ("World Cup 2027", 182606, "21 Nov 2027 05:00", "India", "Outright Winner", "6/12", 50),
    ("Big Bash Women 2026", 187184, "05 Dec 03:10", "Sydney Sixers W", "Outright Winner", "2/2", None),
    ("T20 Big Bash 2026-27", 187503, "12 Dec 03:15", "Adelaide Strikers", "Outright Winner", "1/2", 50),
    ("SA20 2026-27", 187504, "24 Jan 2027 11:30", "Pretoria Capitals", "Outright Winner", "1/1", 100),
    ("T20 Blast 2027", 188350, "18 Jul 2027 11:00", "Derbyshire", "Outright Winner", None, None),
])
add("Volleyball", "All Volleyball", [
    ("Conegliano W vs Vallefoglia W", 37076, "Tomorrow 15:00", "Vallefoglia W", "Win Match", "6/10", 60),
    ("Marignano W vs Bergamo W", 37075, "Today 15:00", "Bergamo W", "Win Match", "5/7", 71),
    ("TFL Altekma vs Halkbank Ankara", 37126, "Today 08:00", "Halkbank Ankara", "Win Match", "4/5", 80),
    ("Ziraat Bankasi vs Gaziantep Genclik Spor", 37121, "Today 12:00", "Ziraat Bankasi", "Win Match", "4/4", 100),
    ("Uni Opole W vs Palac Bydgoszcz W", 37081, "Today 15:30", "Uni Opole W", "Win Match", "4/6", 67),
    ("Istanbul Genclik Spor vs IBB Spor", 37124, "Today 07:00", "IBB Spor", "Win Match", "3/5", 60),
    ("VaLePa vs AC Oulu", 37129, "Today 12:30", "VaLePa", "Win Match", "3/4", 75),
    ("Suzano Volei vs Goias Volei", 37103, "Today 17:30", "Suzano Volei", "Win Match", "3/4", 75),
    ("Praia Clube vs Sao Jose", 37104, "Today 20:00", "Praia Clube", "Win Match", "3/4", 75),
    ("Sungurlu Bld vs Galatasaray", 37122, "Today 09:30", "Galatasaray", "Win Match", "2/3", 67),
    ("Fenerbahce vs Alanya Bld", 37125, "Today 12:00", "Alanya Bld", "Win Match", "2/3", 67),
    ("Volleys Borken W vs Vilsbiburg W", 37131, "Today 13:30", "Vilsbiburg W", "Win Match", "2/3", 67),
    ("Budowlani Lodz W vs Radomka Radom W", 37082, "Tomorrow 12:30", "Budowlani Lodz W", "Win Match", "2/3", 67),
    ("Mielec W vs Rzeszow W", 37083, "Tomorrow 14:00", "Rzeszow W", "Win Match", "2/3", 67),
    ("Sultanbeyli Bld vs Gebze Genclik", 37123, "Today 09:00", "Sultanbeyli Bld", "Win Match", "1/2", 50),
    ("Onikisubat Bld vs Spor Toto SK", 37127, "Today 12:00", "Onikisubat Bld", "Win Match", "1/2", 50),
    ("LP Pihtipudas W vs Nurmon Jymy W", 37134, "Today 12:30", "LP Pihtipudas W", "Win Match", "1/2", 50),
    ("PGE Skra Belchatow vs GKS Katowice", 37132, "Today 12:30", "PGE Skra Belchatow", "Win Match", "1/2", 50),
    ("SV Warnemunde vs VfB Friedrichshafen", 37135, "Today 14:30", "SV Warnemunde", "Win Match", "1/2", 50),
    ("SSC Karlsruhe vs SWD Duren", 37136, "Today 15:00", "SSC Karlsruhe", "Win Match", "1/1", 100),
])
add("Handball", "All Handball", [
    ("SC Magdeburg vs HC Kriens Luzern", 12136, "Tomorrow 15:45", "Tie", "Money Line", "9/14", 64),
    ("HC Vardar vs MT Melsungen", 12130, "Tomorrow 13:45", "Tie", "Money Line", "8/13", 62),
    ("Wisla Plock vs Nantes", 12138, "Tomorrow 13:45", "Tie", "Money Line", "8/11", 73),
    ("KS Kielce vs Kolstad", 12132, "Tomorrow 15:45", "Tie", "Money Line", "7/11", 64),
    ("PSG Handball vs Aalborg Handbold", 12134, "Tomorrow 15:45", "Tie", "Money Line", "7/9", 78),
    ("RK Celje vs RK Zagreb", 12135, "Tomorrow 15:45", "Tie", "Money Line", "6/8", 75),
    ("Fuchse Berlin vs RK Partizan", 12128, "29 Oct 13:45", "Tie", "Money Line", "6/14", 43),
    ("FC Porto vs Veszprem", 12127, "Tomorrow 13:45", "Tie", "Money Line", "5/9", 56),
    ("GOG vs Sporting CP", 12129, "29 Oct 13:45", "Tie", "Money Line", "3/5", 60),
    ("Montpellier vs Dinamo Bucuresti", 12133, "29 Oct 15:45", "Tie", "Money Line", "3/4", 75),
    ("VasterasIrsta HF W vs Skuru IK W", 12197, "Today 14:00", "VasterasIrsta HF (W)", "Money Line", "2/4", 50),
    ("OV Helsingborg HK W vs Skovde HF W", 12196, "Today 14:00", "Skovde HF (W)", "Money Line", "2/4", 50),
    ("IFK Kristianstad vs Pick Szeged", 12131, "29 Oct 13:45", "Tie", "Money Line", "2/4", 50),
    ("SG Flensburg Handewitt vs HBW Balingen Weilstetten", 12180, "29 Oct 14:00", "HBW Balingen-Weilstetten", "Money Line", "1/1", 100),
    ("Skanderborg Handbold vs FC Barcelona", 12137, "29 Oct 15:45", "Skanderborg Handbold", "Money Line", "1/3", 33),
    ("ThSV Eisenach vs Fuchse Berlin", 12169, "01 Nov 10:30", "Tie", "Money Line", "1/1", 100),
    ("Team Tvis Holstebro vs TMS Ringsted", 12163, "01 Nov 12:00", "Tie", "Money Line", "1/1", 100),
    ("BM Granollers vs FC Barcelona", 12185, "01 Nov 12:00", "Tie", "Money Line", "1/1", 100),
    ("Fredericia HK vs Mors Thy Handbold", 12158, "01 Nov 14:00", "Tie", "Money Line", "1/1", 100),
])
add("Ice Hockey", "Finland SM Liiga", [
    ("Kalpa vs Sport", 200081, "Today 12:30", "Kalpa", "Money Line", "5/5", 100),
])
add("Ice Hockey", "Swedish Hockey League", [
    ("IF Malmo Redhawks vs Linkoping HC", 200082, "Today 14:00", "IF Malmo Redhawks", "Money Line", "3/3", 100),
    ("Frolunda HC vs Rogle BK", 200083, "Today 14:00", "Frolunda HC", "Money Line", "2/3", 67),
])
add("Ice Hockey", "Germany Eishockey Liga", [
    ("Kolner Haie vs Adler Mannheim", 200100, "Today 14:30", "Adler Mannheim", "Money Line", "2/2", 100),
])
add("Ice Hockey", "NHL", [
    ("CLB Blue Jackets @ PHI Flyers", 200108, "Today 19:07", "PHI Flyers", "Money Line", "2/3", 67),
    ("BOS Bruins @ CAR Hurricanes", 200104, "Today 20:07", "BOS Bruins +1.50", "Puck Line", "2/2", 100),
    ("FLA Panthers @ WPG Jets", 200105, "Today 20:07", "Under 5.50", "Game Totals", "1/1", 100),
    ("NJ Devils @ DAL Stars", 200111, "Today 20:07", "Under 5.50", "Game Totals", "1/1", 100),
    ("NY Islanders @ NSH Predators", 200112, "Today 20:07", "NY Islanders +1.50", "Puck Line", "1/1", 100),
])
add("Ice Hockey", "Danish Metal Ligaen", [
    ("Herning Blue Fox vs Rodovre Mighty Bulls", 200098, "Today 14:00", "Rodovre Mighty Bulls +3.50", "Puck Line", "1/1", 100),
])
add("Ice Hockey", "Austria EHL", [
    ("Fehervar AV19 vs Milano HC", 200146, "Today 14:15", "Fehervar AV19 -1.50", "Puck Line", "1/1", 100),
])
add("Ice Hockey", "Switzerland NLA", [
    ("Fribourg Gotteron vs Davos", 200116, "Today 14:45", "Fribourg Gotteron -1.50", "Puck Line", "1/1", 100),
    ("Bern vs ZSC Lions", 200122, "Today 14:45", "ZSC Lions -1.50", "Puck Line", "1/1", 100),
    ("EHC Kloten vs HC Ajoie", 200115, "Today 14:45", "EHC Kloten -1.50", "Puck Line", "1/1", 100),
    ("Zug vs Lugano", 200117, "Today 14:45", "Lugano +1.50", "Puck Line", "1/1", 100),
    ("Lausanne HC vs SCL Tigers", 200118, "Today 14:45", "Lausanne HC -1.50", "Puck Line", "1/1", 100),
    ("Ambri Piotta vs EHC Biel", 200119, "Today 14:45", "Ambri Piotta -1.50", "Puck Line", "1/1", 100),
    ("Rapperswil Jona Lakers vs Servette GE", 200123, "Today 14:45", "Servette GE +1.50", "Puck Line", "1/1", 100),
])
add("Basketball", "Euroleague", [
    ("Panathinaikos vs Milano", 536177, "Today 15:15", "Panathinaikos", "Money Line", "5/8", 63),
    ("BC Dubai vs Paris", 536176, "Today 12:00", "BC Dubai", "Money Line", "4/7", 57),
    ("Valencia vs Fenerbahce", 536179, "Today 15:30", "Fenerbahce", "Money Line", "4/6", 67),
    ("Bayern Munich vs Barcelona", 536174, "Today 15:00", "Bayern Munich", "Money Line", "3/5", 60),
    ("Baskonia vs Real Madrid", 536178, "Today 16:00", "Baskonia", "Money Line", "3/6", 50),
    ("Crvena Zvezda vs Maccabi Tel Aviv", 536175, "Today 15:00", "Crvena Zvezda", "Money Line", "2/4", 50),
    ("Besiktas vs Olympiacos", 536180, "Tomorrow 13:30", "Besiktas", "Money Line", "2/3", 67),
    ("Asvel Lyon Villeurbanne vs Partizan", 536181, "Tomorrow 15:00", "Partizan", "Money Line", "2/2", 100),
    ("Virtus Bologna vs Zalgiris", 536183, "Tomorrow 15:30", "Virtus Bologna", "Money Line", "2/2", 100),
])
add("Basketball", "Korea KBL", [
    ("Seoul Knights vs KCC Egis", 536214, "Today 06:00", "Seoul Knights", "Money Line", "4/5", 80),
])
add("Basketball", "Euro Cup", [
    ("Lietkabelis vs Ratiopharm Ulm", 536218, "Today 13:00", "Lietkabelis", "Money Line", "2/2", 100),
    ("Frankfurt Skyliners vs U BT Cluj Napoca", 536217, "Today 14:30", "Frankfurt Skyliners +1.50", "Pointspread", "2/2", 100),
    ("Aris vs Cedevita Olimpija", 536222, "Tomorrow 13:30", "Aris", "Money Line", "2/2", 100),
    ("Balkan Botevgrad vs Manresa", 536215, "Today 13:00", "Balkan Botevgrad", "Money Line", "1/2", 50),
    ("Roma Basketball vs Bosna Sarajevo", 536219, "Today 15:00", "Roma Basketball", "Money Line", "1/1", 100),
])
add("Basketball", "Basketball Champions League", [
    ("UCAM Murcia vs Peristeri", 536235, "Today 15:30", "UCAM Murcia", "Money Line", "2/2", 100),
    ("Baku Sabah vs Nanterre", 536232, "Today 12:00", "Nanterre", "Money Line", "1/1", 100),
])
add("Basketball", "Brazil NBB", [
    ("Cruzeiro vs Brasilia", 536209, "Today 18:30", "Cruzeiro", "Money Line", "1/1", 100),
])
add("Basketball", "NBA", [
    ("BKN Nets @ BOS Celtics", 536253, "Today 19:40", "BOS Celtics", "Money Line", "1/1", 100),
    ("DET Pistons @ NY Knicks", 536251, "Today 20:10", "NY Knicks", "Money Line", "1/1", 100),
])


def date_bucket(label: str) -> str:
    if label.startswith("Today"):
        return DAY
    if label.startswith("Tomorrow"):
        return "2026-10-28"
    # Explicit labels are kept as printed; an ISO bucket is added only where
    # the day and month are unambiguous within this retrieval window.
    months = {"Oct": 10, "Nov": 11, "Dec": 12, "Jan": 1, "Mar": 3,
              "May": 5, "Jul": 7}
    bits = label.split()
    try:
        day = int(bits[0]); month = months[bits[1]]
        if len(bits) >= 3 and bits[2].isdigit() and len(bits[2]) == 4:
            year = int(bits[2]); time_index = 3
        else:
            year = 2026; time_index = 2
        return f"{year:04d}-{month:02d}-{day:02d}"
    except (ValueError, KeyError, IndexError):
        raise ValueError(f"Cannot bucket start label: {label}")


def event_url(row: dict) -> str:
    sport = row["sport"]
    slug = row["event"].replace(" ", "_")
    eid = row["event_id"]
    if sport == "Gaelic Sports":
        base = "Gaelic_Football" if row["competition"] == "Gaelic Football" else "Hurling"
        sid = 25 if base == "Gaelic_Football" else 26
        return f"https://www.olbg.com/betting-tips/{base}/All_{base}/All_Events/{slug}/{sid}?event_id={eid}"
    if sport in SPORT_PATH:
        base, sid = SPORT_PATH[sport]
        return f"https://www.olbg.com/betting-tips/{base}/All_{base}/All_Events/{slug}/{sid}?event_id={eid}"
    if sport == "Baseball":
        return f"https://www.olbg.com/betting-tips/Baseball/MLB/MLB/{slug}/12?event_id={eid}"
    if sport == "Ice Hockey":
        comp = {"NHL": "NHL/NHL", "Finland SM Liiga": "Other/Finland_SM_Liiga",
                "Swedish Hockey League": "Other/Swedish_Hockey_League",
                "Germany Eishockey Liga": "Other/Germany_Eishockey_Liga",
                "Danish Metal Ligaen": "Other/Danish_Metal_Ligaen",
                "Austria EHL": "Other/Austria_EHL",
                "Switzerland NLA": "Other/Switzerland_NLA"}[row["competition"]]
        return f"https://www.olbg.com/betting-tips/Ice_Hockey/{comp}/{slug}/13?event_id={eid}"
    if sport == "Basketball":
        comp = {"NBA": "NBA/NBA", "Euroleague": "European/Euroleague",
                "Euro Cup": "European/Euro_Cup",
                "Basketball Champions League": "European/Basketball_Champions_League",
                "Korea KBL": "Other/Korea_KBL", "Brazil NBB": "Other/Brazil_NBB"}[row["competition"]]
        return f"https://www.olbg.com/betting-tips/Basketball/{comp}/{slug}/4?event_id={eid}"
    raise ValueError(sport)


def main():
    expected = {"Golf": 3, "Volleyball": 20, "Rugby Union": 13, "Cricket": 18,
                "Snooker": 0, "Darts": 2, "Baseball": 1, "Gaelic Sports": 4,
                "Greyhounds": 0, "Tennis": 20, "Motor Racing": 2, "Handball": 19,
                "Ice Hockey": 18, "Basketball": 20, "Rugby League": 3}
    actual = {s: sum(r["sport"] == s for r in R) for s in expected}
    assert actual == expected, (actual, expected)
    assert len({(r["sport"], r["event_id"], r["market"], r["selection"]) for r in R}) == len(R)
    for i, row in enumerate(R, 1):
        row["row_id"] = f"OLBG-20261027-{i:03d}"
        row["date_bucket"] = date_bucket(row["start_label"])
        row["start_timezone"] = None
        row["bookmaker_odds"] = None
        row["olbg_url"] = event_url(row)
        row["listing_url"] = HUBS[row["sport"]]
        row["schedule_status"] = "not_checked"
        row["our_line"] = None
    payload = {
        "schema_version": 1,
        "snapshot_date": DAY,
        "transcribed_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "method": "Manual line-by-line transcription of retrieved OLBG public listing pages; no values imputed.",
        "field_notes": {
            "start_label": "Exactly as displayed. Today=2026-10-27 and Tomorrow=2026-10-28 only for date_bucket.",
            "start_timezone": "Blank: OLBG listing does not state a timezone.",
            "tips": "Tips on displayed selection / total tips in that market, not win probability.",
            "pct": "Displayed OLBG tip share; blank when not displayed.",
            "bookmaker_odds": "Blank throughout: no bookmaker price was retrievable.",
            "our_line": "Populated only after schedule review and transparent independent pricing.",
            "schedule_status": "not_checked until a current official/trusted schedule source is attached."
        },
        "hubs": HUBS,
        "empty_hubs": {"Snooker": "No tips found.", "Greyhounds": "No tips found."},
        "counts": actual,
        "events": R,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(R)} rows to {OUT.relative_to(ROOT)}")
    print(actual)

if __name__ == "__main__":
    main()

# This script fetches historical MLB player statistics for the seasons 2019 to 2024
# and saves them in JSON and CSV formats. It uses the MLB Stats API to get the data.
# scrape_player_stats.py - Pulls current season stats for all MLB players
import os
import json
import csv
import requests
from datetime import datetime
from time import sleep

OUTPUT_DIR = "./data"
TEAM_LIST_URL = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
ROSTER_URL = "https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
PLAYER_STATS_URL = "https://statsapi.mlb.com/api/v1/people/{player_id}?hydrate=stats(group=[hitting],type=[season],season=2024)"

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def fetch_json(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        log(f"❌ Error fetching {url}: {e}")
        return None

def fetch_team_list():
    data = fetch_json(TEAM_LIST_URL)
    if not data:
        return []
    return [(team["id"], team["name"]) for team in data.get("teams", [])]

def fetch_team_roster(team_id):
    data = fetch_json(ROSTER_URL.format(team_id=team_id))
    if not data:
        return []
    return [entry["person"]["id"] for entry in data.get("roster", [])]

def fetch_player_stats(player_id):
    data = fetch_json(PLAYER_STATS_URL.format(player_id=player_id))
    if not data or "people" not in data:
        return None

    person = data["people"][0]
    stat_splits = person.get("stats", [{}])[0].get("splits", [])
    if not stat_splits:
        return None

    stat = stat_splits[0].get("stat", {})
    return {
        "name": person.get("fullName", ""),
        "team": person.get("currentTeam", {}).get("name", ""),
        "AB": stat.get("atBats", 0),
        "R": stat.get("runs", 0),
        "H": stat.get("hits", 0),
        "HR": stat.get("homeRuns", 0),
        "RBI": stat.get("rbi", 0),
        "BB": stat.get("baseOnBalls", 0),
        "K": stat.get("strikeOuts", 0),
        "AVG": stat.get("avg", ""),
        "OBP": stat.get("obp", ""),
        "SLG": stat.get("slg", ""),
        "OPS": stat.get("ops", ""),
        "playerType": "hitter"
    }

def save_to_files(players, date_str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, f"player_stats_{date_str}.json")
    csv_path = os.path.join(OUTPUT_DIR, f"player_stats_{date_str}.csv")

    with open(json_path, "w") as jf:
        json.dump(players, jf, indent=2)

    with open(csv_path, "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=players[0].keys())
        writer.writeheader()
        writer.writerows(players)

    log(f"✅ Saved {len(players)} player stats to {json_path} and {csv_path}")

def main():
    log("📡 Fetching MLB player stats...")
    today = datetime.now().strftime("%Y-%m-%d")
    all_stats = []

    teams = fetch_team_list()
    for team_id, team_name in teams:
        log(f"🔍 Processing team: {team_name}")
        roster = fetch_team_roster(team_id)
        for pid in roster:
            pdata = fetch_player_stats(pid)
            if pdata:
                all_stats.append(pdata)
            sleep(0.3)  # light delay for rate limiting

    if all_stats:
        save_to_files(all_stats, today)
    else:
        log("⚠️ No player stats found.")

    log("🎯 Player stat scrape complete.")

if __name__ == "__main__":
    main()

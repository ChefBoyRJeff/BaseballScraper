# This script fetches historical MLB player statistics for the seasons 2019 to 2024
# and saves them in JSON and CSV formats. It uses the MLB Stats API to get the data.
# scrape_players.py - Pulls all active MLB players and their bio info
import os
import json
import csv
import requests
from datetime import datetime
from time import sleep

OUTPUT_DIR = "./data"
TEAMS_URL = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
ROSTER_URL = "https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
PLAYER_BIO_URL = "https://statsapi.mlb.com/api/v1/people/{player_id}"

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
    data = fetch_json(TEAMS_URL)
    if not data:
        return []
    return [(team["id"], team["name"]) for team in data["teams"]]

def fetch_team_roster(team_id):
    data = fetch_json(ROSTER_URL.format(team_id=team_id))
    if not data:
        return []
    return [entry["person"]["id"] for entry in data.get("roster", [])]

def fetch_player_info(player_id):
    data = fetch_json(PLAYER_BIO_URL.format(player_id=player_id))
    if not data or "people" not in data:
        return None
    return data["people"][0]

def normalize_player(p, team_name):
    return {
        "name": p.get("fullName", ""),
        "team": team_name,
        "jersey": p.get("jerseyNumber", ""),
        "position": p.get("primaryPosition", {}).get("name", ""),
        "age": p.get("currentAge", ""),
        "height": p.get("height", ""),
        "weight": p.get("weight", ""),
        "batSide": p.get("batSide", {}).get("code", ""),
        "throwSide": p.get("pitchHand", {}).get("code", "")
    }

def save_to_files(players, date_str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, f"players_{date_str}.json")
    csv_path = os.path.join(OUTPUT_DIR, f"players_{date_str}.csv")

    with open(json_path, "w") as jf:
        json.dump(players, jf, indent=2)

    with open(csv_path, "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=players[0].keys())
        writer.writeheader()
        writer.writerows(players)

    log(f"✅ Saved {len(players)} players to {json_path} and {csv_path}")

def main():
    log("📡 Fetching MLB player rosters...")
    today = datetime.now().strftime("%Y-%m-%d")
    all_players = []

    teams = fetch_team_list()
    for team_id, team_name in teams:
        log(f"🔍 Processing {team_name}...")
        player_ids = fetch_team_roster(team_id)
        for pid in player_ids:
            pinfo = fetch_player_info(pid)
            if pinfo:
                player = normalize_player(pinfo, team_name)
                all_players.append(player)
            sleep(0.25)

    save_to_files(all_players, today)
    log("🎯 Roster scrape complete.")

if __name__ == "__main__":
    main()

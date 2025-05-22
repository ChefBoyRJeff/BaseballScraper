# This script fetches historical MLB player statistics for the seasons 2019 to 2024
# and saves them in JSON and CSV formats. It uses the MLB Stats API to get the data.
# scrape_standings.py - Pull current MLB standings
import os
import json
import requests
from datetime import datetime

OUTPUT_DIR = "./data"
STANDINGS_URL = "https://site.api.espn.com/apis/v2/sports/baseball/mlb/standings"

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def fetch_standings():
    try:
        res = requests.get(STANDINGS_URL, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        log(f"❌ Failed to fetch standings: {e}")
        return None

def parse_standings(data):
    parsed = []
    for team in data.get("children", []):
        for entry in team.get("standings", {}).get("entries", []):
            try:
                team_info = entry.get("team", {})
                stats = {stat["name"]: stat.get("value", "") for stat in entry.get("stats", [])}
                parsed.append({
                    "team": team_info.get("displayName", ""),
                    "abbreviation": team_info.get("abbreviation", ""),
                    "wins": stats.get("wins", 0),
                    "losses": stats.get("losses", 0),
                    "winPct": stats.get("winPercent", 0.0),
                    "gamesBack": stats.get("gamesBack", ""),
                    "streak": stats.get("streak", ""),
                    "divisionRank": stats.get("divisionRank", ""),
                    "leagueRank": stats.get("playoffSeed", "")
                })
            except Exception as e:
                log(f"⚠️ Error parsing team standings: {e}")
    return parsed

def save_standings(standings, date_str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, f"standings_{date_str}.json")
    with open(file_path, "w") as f:
        json.dump(standings, f, indent=2)
    log(f"✅ Saved standings to {file_path}")

def main():
    log("📡 Fetching MLB standings...")
    today = datetime.now().strftime("%Y-%m-%d")
    data = fetch_standings()
    if data:
        standings = parse_standings(data)
        save_standings(standings, today)
    log("🎯 Standings scrape complete.")

if __name__ == "__main__":
    main()

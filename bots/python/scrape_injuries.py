# This script fetches historical MLB player statistics for the seasons 2019 to 2024
# and saves them in JSON and CSV formats. It uses the MLB Stats API to get the data.
# scrape_injuries.py - Pull current injury data for MLB players from ESPN
import os
import json
import requests
from datetime import datetime

OUTPUT_DIR = "./data"
INJURY_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/injuries"

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def fetch_injuries():
    try:
        res = requests.get(INJURY_URL, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        log(f"❌ Failed to fetch injury data: {e}")
        return None

def parse_injuries(data):
    parsed = []
    for team_entry in data.get("teams", []):
        team_name = team_entry.get("team", {}).get("displayName", "")
        for item in team_entry.get("injuries", []):
            athlete = item.get("athlete", {})
            parsed.append({
                "name": athlete.get("fullName", ""),
                "team": team_name,
                "position": athlete.get("position", {}).get("abbreviation", ""),
                "injury": item.get("details", ""),
                "status": item.get("status", {}).get("description", ""),
                "date": item.get("date", "")
            })
    return parsed

def save_to_file(injuries, date_str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"injuries_{date_str}.json")
    with open(path, "w") as f:
        json.dump(injuries, f, indent=2)
    log(f"✅ Saved injury report to {path}")

def main():
    log("📡 Fetching MLB injury data from ESPN...")
    today = datetime.now().strftime("%Y-%m-%d")
    data = fetch_injuries()
    if data:
        injuries = parse_injuries(data)
        save_to_file(injuries, today)
    log("🎯 Injury scrape complete.")

if __name__ == "__main__":
    main()

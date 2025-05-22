# This script fetches historical MLB player statistics for the seasons 2019 to 2024
# and saves them in JSON and CSV formats. It uses the MLB Stats API to get the data.
# scrape_schedule.py - Pull today's MLB game schedule
import os
import json
import requests
from datetime import datetime

OUTPUT_DIR = "./data"
SCHEDULE_URL = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def fetch_schedule():
    try:
        response = requests.get(SCHEDULE_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log(f"❌ Failed to fetch schedule: {e}")
        return None

def parse_schedule(data):
    games = []
    for date_obj in data.get("dates", []):
        for game in date_obj.get("games", []):
            try:
                games.append({
                    "gamePk": game.get("gamePk"),
                    "gameDate": game.get("gameDate"),
                    "homeTeam": game.get("teams", {}).get("home", {}).get("team", {}).get("name", ""),
                    "awayTeam": game.get("teams", {}).get("away", {}).get("team", {}).get("name", ""),
                    "status": game.get("status", {}).get("detailedState", ""),
                    "venue": game.get("venue", {}).get("name", "")
                })
            except Exception as e:
                log(f"⚠️ Error parsing game: {e}")
    return games

def save_schedule(games, date_str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, f"schedule_{date_str}.json")
    with open(file_path, "w") as f:
        json.dump(games, f, indent=2)
    log(f"✅ Saved schedule to {file_path}")

def main():
    log("📡 Fetching today’s MLB schedule...")
    today_str = datetime.now().strftime("%Y-%m-%d")
    raw = fetch_schedule()
    if raw:
        parsed = parse_schedule(raw)
        save_schedule(parsed, today_str)
    log("🎯 Schedule scrape complete.")

if __name__ == "__main__":
    main()

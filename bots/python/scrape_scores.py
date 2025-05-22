# This script fetches historical MLB player statistics for the seasons 2019 to 2024
# and saves them in JSON and CSV formats. It uses the MLB Stats API to get the data.
# scrape_scores.py - Refactored ESPN scoreboard scraper
import os
import json
import requests
from datetime import datetime

OUTPUT_DIR = "./data"
SCORES_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def fetch_scores():
    try:
        response = requests.get(SCORES_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log(f"❌ Failed to fetch scores: {e}")
        return None

def parse_scores(data):
    games = []
    for event in data.get("events", []):
        try:
            competition = event["competitions"][0]
            competitors = competition.get("competitors", [])
            game = {
                "date": event.get("date"),
                "name": event.get("name"),
                "status": competition.get("status", {}).get("type", {}).get("description", ""),
                "homeTeam": "",
                "awayTeam": "",
                "homeScore": "",
                "awayScore": ""
            }

            for team in competitors:
                if team.get("homeAway") == "home":
                    game["homeTeam"] = team.get("team", {}).get("displayName", "")
                    game["homeScore"] = team.get("score", "0")
                elif team.get("homeAway") == "away":
                    game["awayTeam"] = team.get("team", {}).get("displayName", "")
                    game["awayScore"] = team.get("score", "0")

            games.append(game)
        except Exception as e:
            log(f"⚠️ Error parsing event: {e}")
    return games

def save_scores(games, date_str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, f"scores_{date_str}.json")
    with open(file_path, "w") as f:
        json.dump(games, f, indent=2)
    log(f"✅ Saved {len(games)} games to {file_path}")

def main():
    log("📡 Fetching today’s MLB scores...")
    today = datetime.now().strftime("%Y-%m-%d")
    raw = fetch_scores()
    if raw:
        parsed = parse_scores(raw)
        save_scores(parsed, today)
    log("🎯 Score scrape complete.")

if __name__ == "__main__":
    main()

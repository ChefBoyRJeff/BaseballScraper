# This script scrapes player statistics from ESPN's JSON API for the MLB season.
# It fetches data for batting average, home runs, and RBIs, and saves the results in JSON and CSV formats.    
import os
import json
import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://site.web.api.espn.com/apis/common/v3/sports/baseball/mlb/leaders"

# Categories: batting average, home runs, RBIs
STAT_CATEGORIES = ["avg", "homeRuns", "rbi"]

def fetch_stats(category, season=2024):
    params = {
        "limit": 50,
        "offset": 0,
        "sort": category,
        "season": season,
        "seasontype": 2
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def extract_players(data, category):
    players = []
    for entry in data.get("leaders", [])[0].get("leaders", []):
        athlete = entry.get("athlete", {})
        stats = entry.get("stats", [])

        players.append({
            "name": athlete.get("displayName"),
            "team": athlete.get("team", {}).get("displayName"),
            "position": athlete.get("position", {}).get("abbreviation"),
            category: stats[0] if stats else None
        })
    return players

def scrape_all_stats():
    combined = {}
    for category in STAT_CATEGORIES:
        print(f"Fetching {category} leaders...")
        raw_data = fetch_stats(category)
        players = extract_players(raw_data, category)

        # Merge data by name
        for player in players:
            name = player["name"]
            if name not in combined:
                combined[name] = player
            else:
                combined[name].update(player)
    return list(combined.values())

def save_output(players):
    today = datetime.today().strftime("%Y-%m-%d")
    os.makedirs("data", exist_ok=True)

    with open(f"data/player_stats_{today}.json", "w") as f:
        json.dump(players, f, indent=2)

    pd.DataFrame(players).to_csv(f"data/player_stats_{today}.csv", index=False)

if __name__ == "__main__":
    data = scrape_all_stats()
    save_output(data)
    print("✅ Player stats from ESPN’s JSON API saved.")

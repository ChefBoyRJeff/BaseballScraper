# This script scrapes player statistics from ESPN's JSON API for the MLB season.
# It fetches data for batting average, home runs, and RBIs, and saves the results in JSON and CSV formats.

import requests, json, pandas as pd, os
from datetime import datetime

URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/statistics/players"

def fetch_player_stats():
    res = requests.get(URL)
    data = res.json()

    players = []
    for category in data.get("categories", []):
        stat_category = category.get("name")
        for stat in category.get("leaders", []):
            athlete = stat["athlete"]
            players.append({
                "name": athlete["fullName"],
                "team": athlete["team"]["displayName"],
                "position": athlete.get("position", {}).get("abbreviation"),
                "stat_category": stat_category,
                "value": stat["value"]
            })

    return players

def save(players):
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("data", exist_ok=True)
    with open(f"data/player_stats_{today}.json", "w") as f:
        json.dump(players, f, indent=2)
    pd.DataFrame(players).to_csv(f"data/player_stats_{today}.csv", index=False)
    print("✅ Player stats saved.")

if __name__ == "__main__":
    data = fetch_player_stats()
    save(data)
    print("✅ Player stats fetched.")
    
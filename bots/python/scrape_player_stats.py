# scrape_player_stats.py
# Pulls MLB leader stats for HR, AVG, RBI from statsapi.mlb.com

import requests
import pandas as pd
import json
import os
from datetime import datetime

# Config
STAT_CATEGORIES = ["homeRuns", "battingAverage", "rbi"]
SEASON = datetime.now().year
LIMIT = 50  # You can increase if needed

def fetch_mlb_leaders():
    url = "https://statsapi.mlb.com/api/v1/stats/leaders"
    params = {
        "leaderCategories": ",".join(STAT_CATEGORIES),
        "season": SEASON,
        "sportId": 1,
        "limit": LIMIT
    }

    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json()

def parse_leaders(data):
    parsed = []
    for category in data.get("leagueLeaders", []):
        cat_name = category["leaderCategory"]
        for player in category.get("leaders", []):
            parsed.append({
                "name": player["person"]["fullName"],
                "team": player["team"]["name"],
                "stat": cat_name,
                "value": player["value"]
            })
    return parsed

def save_output(leaders):
    today = datetime.today().strftime("%Y-%m-%d")
    os.makedirs("data", exist_ok=True)

    # JSON
    with open(f"data/player_stats_{today}.json", "w") as f:
        json.dump(leaders, f, indent=2)

    # CSV
    pd.DataFrame(leaders).to_csv(f"data/player_stats_{today}.csv", index=False)
    print(f"✅ Player stats saved to ./data/player_stats_{today}.json and .csv")

if __name__ == "__main__":
    try:
        raw_data = fetch_mlb_leaders()
        parsed_stats = parse_leaders(raw_data)
        save_output(parsed_stats)
    except Exception as e:
        print(f"❌ Error fetching or saving player stats: {e}")

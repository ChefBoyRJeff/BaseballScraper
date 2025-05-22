# This script fetches historical MLB player statistics for the seasons 2019 to 2024
# and saves them in JSON and CSV formats. It uses the MLB Stats API to get the data.

import os
import requests
import json
import pandas as pd
from datetime import datetime

seasons = list(range(2019, 2025))  # 2019–2024
categories = ['homeRuns', 'battingAverage', 'rbi']
base_url = "https://statsapi.mlb.com/api/v1/stats/leaders"
output_dir = "data/archived_data"
os.makedirs(output_dir, exist_ok=True)

all_data = []
for season in seasons:
    url = f"{base_url}?leaderCategories={','.join(categories)}&season={season}&sportId=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        json_path = os.path.join(output_dir, f"leader_stats_{season}.json")
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)
        all_data.append((season, data))
        print(f"✅ Fetched and saved: {json_path}")
    else:
        print(f"❌ Failed to fetch season {season}: {response.status_code}")

# Transform for CSV
rows = []
for season, data in all_data:
    for stat in data.get("stats", []):
        for leader in stat.get("leaders", []):
            rows.append({
                "season": season,
                "category": stat["stat"],
                "player_id": leader["player"]["id"],
                "player_name": leader["player"]["fullName"],
                "team_id": leader["team"]["id"],
                "team_name": leader["team"]["name"],
                "value": leader["value"],
                "rank": leader["rank"]
            })

df = pd.DataFrame(rows)
df.to_csv(os.path.join(output_dir, "leader_stats_2019_2024.csv"), index=False)
print("✅ Combined CSV created.")

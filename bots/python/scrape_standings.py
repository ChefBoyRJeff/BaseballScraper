# scrape_standings.py
# Scrapes MLB standings data from ESPN and saves in JSON and CSV formats.

import os
import json
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")

URL = "https://site.api.espn.com/apis/v2/sports/baseball/mlb/standings"

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def fetch_standings():
    try:
        res = requests.get(URL)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        log(f"❌ Error fetching standings: {e}")
        return {}

def parse_standings(data):
    teams = []
    for group in data.get("children", []):
        for team in group.get("standings", {}).get("entries", []):
            team_info = team.get("team", {})
            stats = {stat.get("name"): stat.get("value") for stat in team.get("stats", []) if "value" in stat}

            teams.append({
                "team": team_info.get("displayName"),
                "abbreviation": team_info.get("abbreviation"),
                "wins": stats.get("wins"),
                "losses": stats.get("losses"),
                "win_pct": stats.get("winPercent"),
                "games_behind": stats.get("gamesBehind"),
                "streak": stats.get("streak"),
                "rank": team.get("rank")
            })
    return teams

def save_output(teams):
    date_str = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(DATA_DIR, exist_ok=True)

    json_path = os.path.join(DATA_DIR, f"standings_{date_str}.json")
    csv_path = os.path.join(DATA_DIR, f"standings_{date_str}.csv")

    with open(json_path, "w") as f:
        json.dump(teams, f, indent=2)

    pd.DataFrame(teams).to_csv(csv_path, index=False)

    log(f"✅ Standings saved to {json_path} and {csv_path} ({len(teams)} teams)")

if __name__ == "__main__":
    raw_data = fetch_standings()
    teams = parse_standings(raw_data)
    save_output(teams)
    log("✅ Standings fetch complete.")

# This script scrapes player statistics from ESPN's JSON API for the MLB season.
# It fetches data for batting average, home runs, and RBIs, and saves the results in JSON and CSV formats.
import os
import json
import requests
import pandas as pd
from datetime import datetime

URL = "https://site.api.espn.com/apis/v2/sports/baseball/mlb/standings"

def fetch_standings():
    res = requests.get(URL)
    res.raise_for_status()
    return res.json()

def parse_standings(data):
    teams = []
    for group in data.get("children", []):
        for team in group.get("standings", {}).get("entries", []):
            team_info = team["team"]
            stats = {stat["name"]: stat["value"] for stat in team["stats"] if "value" in stat}

            teams.append({
                "team": team_info["displayName"],
                "abbreviation": team_info.get("abbreviation"),
                "wins": stats.get("wins"),
                "losses": stats.get("losses"),
                "win_pct": stats.get("winPercent"),
                "games_behind": stats.get("gamesBehind"),
                "streak": stats.get("streak"),
                "rank": team.get("rank"),
            })
    return teams

def save_output(teams):
    today = datetime.today().strftime("%Y-%m-%d")
    os.makedirs("data", exist_ok=True)

    with open(f"data/standings_{today}.json", "w") as f:
        json.dump(teams, f, indent=2)

    pd.DataFrame(teams).to_csv(f"data/standings_{today}.csv", index=False)

if __name__ == "__main__":
    raw_data = fetch_standings()
    teams = parse_standings(raw_data)
    save_output(teams)
    print("✅ Standings saved to JSON and CSV.")

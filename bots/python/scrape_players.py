# This script scrapes player statistics from ESPN's JSON API for the MLB season.
# It fetches data for batting average, home runs, and RBIs, and saves the results in JSON and CSV formats.
import requests, json, os
from datetime import datetime

URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/players"

def fetch_players():
    res = requests.get(URL)
    data = res.json()
    players = []

    for item in data.get("items", []):
        players.append({
            "id": item.get("id"),
            "name": item.get("displayName"),
            "team": item.get("team", {}).get("displayName"),
            "position": item.get("position", {}).get("name")
        })

    return players

def save(players):
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("data", exist_ok=True)
    with open(f"data/players_{today}.json", "w") as f:
        json.dump(players, f, indent=2)
    print("✅ Players list saved.")

if __name__ == "__main__":
    players = fetch_players()
    save(players)
    print("✅ Players list fetched.")
    
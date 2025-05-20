# scrape_players.py
# Scrapes player rosters by iterating through hardcoded ESPN MLB team IDs.

import requests
import json
import os
from datetime import datetime
from time import sleep

TEAM_IDS = {
    1: "Angels", 2: "Diamondbacks", 3: "Braves", 4: "Orioles", 5: "Red Sox",
    6: "Cubs", 7: "White Sox", 8: "Reds", 9: "Guardians", 10: "Rockies",
    11: "Tigers", 12: "Astros", 13: "Royals", 14: "Dodgers", 15: "Marlins",
    16: "Brewers", 17: "Twins", 18: "Yankees", 19: "Mets", 20: "Athletics",
    21: "Phillies", 22: "Pirates", 23: "Padres", 24: "Giants", 25: "Mariners",
    26: "Cardinals", 27: "Rays", 28: "Rangers", 29: "Blue Jays", 30: "Nationals"
}

BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams"

def fetch_players():
    players = []
    failed = []

    for team_id, team_name in TEAM_IDS.items():
        url = f"{BASE_URL}/{team_id}/roster"
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            for group in data.get("athletes", []):
                for player in group.get("items", []):
                    players.append({
                        "team": team_name,
                        "name": player.get("fullName"),
                        "position": player.get("position", {}).get("name", "N/A"),
                        "jersey": player.get("jersey", ""),
                        "height": player.get("displayHeight", ""),
                        "weight": player.get("displayWeight", ""),
                        "age": player.get("age", "")
                    })
        except Exception as e:
            print(f"❌ Failed for team {team_name} ({team_id}): {e}")
            failed.append(team_name)
        sleep(0.2)  # throttle requests

    return players, failed

def save(players):
    today = datetime.today().strftime("%Y-%m-%d")
    os.makedirs("data", exist_ok=True)

    with open(f"data/players_{today}.json", "w") as f:
        json.dump(players, f, indent=2)

    with open(f"data/players_{today}.csv", "w") as f:
        f.write("team,name,position,jersey,height,weight,age\n")
        for p in players:
            f.write(f'"{p["team"]}","{p["name"]}","{p["position"]}","{p["jersey"]}","{p["height"]}","{p["weight"]}","{p["age"]}"\n')

    print(f"✅ Players list saved: {len(players)} total.")

if __name__ == "__main__":
    players, failed = fetch_players()
    save(players)
    if failed:
        print(f"⚠️ Failed teams: {', '.join(failed)}")

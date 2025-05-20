# This script scrapes player statistics from ESPN's JSON API for the MLB season.
# It fetches data for batting average, home runs, and RBIs, and saves the results in JSON and CSV formats.
# Import necessary libraries

import requests
import pandas as pd
from datetime import datetime
import os
import json

# Prepare today's date
today = datetime.today().strftime('%Y-%m-%d')
api_date = datetime.today().strftime('%Y%m%d')
url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={api_date}"

# Make request to ESPN's JSON API
res = requests.get(url)
if res.status_code != 200:
    print(f"❌ Failed to fetch scoreboard: {res.status_code}")
    exit()

data = res.json()
events = data.get("events", [])

games = []
for game in events:
    try:
        competition = game["competitions"][0]
        competitors = competition["competitors"]
        status = game["status"]["type"]["description"]

        # Ensure home and away are identified
        home = next(team for team in competitors if team["homeAway"] == "home")
        away = next(team for team in competitors if team["homeAway"] == "away")

        games.append({
            "date": today,
            "home_team": home["team"]["displayName"],
            "home_score": home.get("score"),
            "away_team": away["team"]["displayName"],
            "away_score": away.get("score"),
            "status": status
        })

    except Exception as e:
        print(f"⚠️ Error parsing game: {e}")

# Ensure output folder exists
os.makedirs("data", exist_ok=True)

# Save JSON
with open(f"data/scores_{today}.json", "w") as f:
    json.dump(games, f, indent=2)

# Save CSV
pd.DataFrame(games).to_csv(f"data/scores_{today}.csv", index=False)

print(f"✅ Scraped and saved {len(games)} game scores for {today}.")

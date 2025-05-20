# scrape_scores.py
# Scrapes daily MLB scores from ESPN and saves as JSON and CSV.

import os
import json
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")

def log(message):
    print(f"[{datetime.now().isoformat()}] {message}")

def fetch_scores():
    today = datetime.today()
    display_date = today.strftime('%Y-%m-%d')
    api_date = today.strftime('%Y%m%d')

    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={api_date}"

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        log(f"❌ Failed to fetch scoreboard data: {e}")
        return [], display_date

    games = []
    for game in data.get("events", []):
        try:
            competition = game.get("competitions", [])[0]
            competitors = competition.get("competitors", [])
            status = game.get("status", {}).get("type", {}).get("description", "Unknown")

            home = next(team for team in competitors if team["homeAway"] == "home")
            away = next(team for team in competitors if team["homeAway"] == "away")

            games.append({
                "date": display_date,
                "home_team": home["team"]["displayName"],
                "home_score": home.get("score"),
                "away_team": away["team"]["displayName"],
                "away_score": away.get("score"),
                "status": status
            })
        except Exception as e:
            log(f"⚠️ Error parsing game: {e}")

    return games, display_date

def save_scores(games, date_str):
    os.makedirs(DATA_DIR, exist_ok=True)

    json_path = os.path.join(DATA_DIR, f"scores_{date_str}.json")
    csv_path = os.path.join(DATA_DIR, f"scores_{date_str}.csv")

    with open(json_path, "w") as f:
        json.dump(games, f, indent=2)

    pd.DataFrame(games).to_csv(csv_path, index=False)

    log(f"✅ Scraped and saved {len(games)} game scores for {date_str}.")

if __name__ == "__main__":
    scores, date_str = fetch_scores()
    if scores:
        save_scores(scores, date_str)

# This script scrapes the latest MLB scores from ESPN and saves them in JSON and CSV formats.
# Import necessary libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# Prepare today's date
today = datetime.today().strftime('%Y-%m-%d')

# Request ESPN scoreboard
url = "https://www.espn.com/mlb/scoreboard"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

# Extract scores (simplified example)
games = []
scoreboards = soup.select('section.Scoreboard')

if not scoreboards:
    print("Could not find scoreboard data.")
else:
    for sb in scoreboards:
        try:
            teams = sb.select('span.sb-team-short')
            scores = sb.select('span.sb-team-score')
            status = sb.select_one('span.sb-meta').text.strip()

            games.append({
                "date": today,
                "home_team": teams[1].text,
                "home_score": scores[1].text,
                "away_team": teams[0].text,
                "away_score": scores[0].text,
                "status": status
            })
        except Exception as e:
            print(f"Error parsing game: {e}")

    # Ensure output folder exists
    output_dir = os.path.join("data")
    os.makedirs(output_dir, exist_ok=True)

    # Save JSON
    json_path = os.path.join(output_dir, f"scores_{today}.json")
    pd.DataFrame(games).to_json(json_path, orient='records', indent=2)

    # Save CSV
    csv_path = os.path.join(output_dir, f"scores_{today}.csv")
    pd.DataFrame(games).to_csv(csv_path, index=False)

    print("Scraped and saved latest scores.")

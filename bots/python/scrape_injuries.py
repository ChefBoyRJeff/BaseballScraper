# scrape_injuries.py
# Scrapes player injury data from ESPN's JSON API for the MLB season.

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")

URL = 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/injuries'

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def fetch_injuries():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        log(f"❌ Error fetching injury data: {e}")
        return []

    injuries = []

    for team in data.get('injuries', []):
        if 'players' not in team:
            continue  # Skip teams with no injuries

        for player in team['players']:
            injuries.append({
                'team': team['team']['displayName'],
                'name': player.get('fullName'),
                'position': player.get('position', {}).get('abbreviation'),
                'status': player.get('status'),
                'injury': player.get('injury'),
                'date': player.get('date')
            })

    return injuries

def save_injuries(injuries):
    date_str = datetime.now().strftime('%Y-%m-%d')
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f'injuries_{date_str}.json')
    with open(filepath, 'w') as f:
        json.dump(injuries, f, indent=2)
    log(f"✅ Injuries data saved: {filepath} ({len(injuries)} players)")

if __name__ == '__main__':
    injuries = fetch_injuries()
    save_injuries(injuries)
    log("✅ Injuries data fetch complete.")

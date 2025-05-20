# scrape_schedule.py
# Scrapes MLB daily game schedule and status from ESPN's JSON API.

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")

URL = 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard'

def log(message):
    print(f"[{datetime.now().isoformat()}] {message}")

def fetch_schedule():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        log(f"❌ Error fetching schedule: {e}")
        return []

    schedule = []

    for event in data.get('events', []):
        game = {
            'date': event.get('date'),
            'name': event.get('name'),
            'shortName': event.get('shortName'),
            'status': event.get('status', {}).get('type', {}).get('description'),
            'competitors': [
                {
                    'name': team.get('team', {}).get('displayName'),
                    'score': team.get('score', '0')
                } for team in event.get('competitions', [{}])[0].get('competitors', [])
            ]
        }
        schedule.append(game)

    return schedule

def save_schedule(schedule):
    date_str = datetime.now().strftime('%Y-%m-%d')
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f'schedule_{date_str}.json')
    with open(filepath, 'w') as f:
        json.dump(schedule, f, indent=2)

    log(f"✅ Schedule data saved to {filepath} ({len(schedule)} games)")

if __name__ == '__main__':
    schedule = fetch_schedule()
    save_schedule(schedule)
    log("✅ Schedule scrape complete.")

# This script scrapes player injury data from ESPN's JSON API for the MLB season.
# It handles teams with no injuries and saves results in JSON format.

import os
import json
import requests
from datetime import datetime

URL = 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/injuries'

def fetch_injuries():
    response = requests.get(URL)
    data = response.json()

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
    date = datetime.now().strftime('%Y-%m-%d')
    os.makedirs('data', exist_ok=True)
    with open(f'data/injuries_{date}.json', 'w') as f:
        json.dump(injuries, f, indent=2)
    print(f'✅ Injuries data saved ({len(injuries)} players).')

if __name__ == '__main__':
    injuries = fetch_injuries()
    save_injuries(injuries)
    print('✅ Injuries data fetched.')
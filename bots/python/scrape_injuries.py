# This script scrapes player statistics from ESPN's JSON API for the MLB season.
# It fetches data for batting average, home runs, and RBIs, and saves the results in JSON and CSV formats.
import os
import json
import requests
from datetime import datetime

URL = 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/injuries'

def fetch_injuries():
    response = requests.get(URL)
    data = response.json()

    injuries = []

    for team in data['injuries']:
        for player in team['players']:
            injuries.append({
                'team': team['team']['displayName'],
                'name': player['fullName'],
                'position': player['position']['abbreviation'],
                'status': player['status'],
                'injury': player['injury'],
                'date': player['date']
            })

    return injuries

def save_injuries(injuries):
    date = datetime.now().strftime('%Y-%m-%d')
    os.makedirs('data', exist_ok=True)
    with open(f'data/injuries_{date}.json', 'w') as f:
        json.dump(injuries, f, indent=2)
    print('✅ Injuries data saved.')

if __name__ == '__main__':
    injuries = fetch_injuries()
    save_injuries(injuries)

# This script scrapes player statistics from ESPN's JSON API for the MLB season.
# It fetches data for batting average, home runs, and RBIs, and saves the results in JSON and CSV formats.
import os
import json
import requests
from datetime import datetime

URL = 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard'

def fetch_schedule():
    response = requests.get(URL)
    data = response.json()

    schedule = []

    for event in data['events']:
        game = {
            'date': event['date'],
            'name': event['name'],
            'shortName': event['shortName'],
            'status': event['status']['type']['description'],
            'competitors': [
                {
                    'name': team['team']['displayName'],
                    'score': team['score']
                } for team in event['competitions'][0]['competitors']
            ]
        }
        schedule.append(game)

    return schedule

def save_schedule(schedule):
    date = datetime.now().strftime('%Y-%m-%d')
    os.makedirs('data', exist_ok=True)
    with open(f'data/schedule_{date}.json', 'w') as f:
        json.dump(schedule, f, indent=2)
    print('✅ Schedule data saved.')

if __name__ == '__main__':
    schedule = fetch_schedule()
    save_schedule(schedule)

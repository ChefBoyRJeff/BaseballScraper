# This script scrapes player statistics from ESPN's JSON API for the MLB season.
# It fetches data for batting average, home runs, and RBIs, and saves the results in JSON and CSV formats.
import os
import json
import requests
from datetime import datetime

teams = [
    'atl', 'bos', 'chc', 'chw', 'cin', 'cle', 'col', 'det', 'hou',
    'kc', 'laa', 'lad', 'mia', 'mil', 'min', 'nym', 'nyy', 'oak',
    'phi', 'pit', 'sd', 'sea', 'sf', 'stl', 'tb', 'tex', 'tor', 'was'
]

def fetch_players():
    all_players = []

    for team in teams:
        url = f'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/{team}/roster'
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()

            for group in data['athletes']:
                for player in group['items']:
                    all_players.append({
                        'team': team,
                        'name': player['fullName'],
                        'position': player['position']['name'],
                        'jersey': player.get('jersey'),
                        'height': player.get('displayHeight'),
                        'weight': player.get('displayWeight'),
                        'age': player.get('age')
                    })
        except Exception as e:
            print(f'❌ Failed for team: {team}', e)

    return all_players

def save_players(players):
    date = datetime.now().strftime('%Y-%m-%d')
    os.makedirs('data', exist_ok=True)
    with open(f'data/players_{date}.json', 'w') as f:
        json.dump(players, f, indent=2)
    print('✅ Player data saved.')

if __name__ == '__main__':
    players = fetch_players()
    save_players(players)

# This script fetches historical MLB player statistics for the seasons 2019 to 2024
# and saves them in JSON and CSV formats. It uses the MLB Stats API to get the data.
# scrape_historical_data.py - Pull historical season stats per player/team
import os
import json
import csv
import requests
from datetime import datetime
from time import sleep

OUTPUT_DIR = "./data/archived_data"
YEARS_BACK = 20  # How many past seasons to pull
SEASON_END_YEAR = datetime.now().year - 1

TEAM_URL = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
ROSTER_URL = "https://statsapi.mlb.com/api/v1/teams/{team_id}/roster?season={year}"
STATS_URL = "https://statsapi.mlb.com/api/v1/people/{player_id}?hydrate=stats(group=[hitting],type=[yearByYear])"

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def fetch_json(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        log(f"❌ Error fetching {url}: {e}")
        return None

def fetch_teams():
    data = fetch_json(TEAM_URL)
    return [(t["id"], t["name"]) for t in data.get("teams", [])]

def fetch_roster(team_id, year):
    url = ROSTER_URL.format(team_id=team_id, year=year)
    data = fetch_json(url)
    return [p["person"]["id"] for p in data.get("roster", [])]

def fetch_player_season_stats(player_id, target_year):
    url = STATS_URL.format(player_id=player_id)
    data = fetch_json(url)
    if not data or "people" not in data:
        return None
    person = data["people"][0]
    stats = person.get("stats", [])
    if not stats:
        return None
    for group in stats:
        for split in group.get("splits", []):
            if str(split.get("season")) == str(target_year):
                stat = split.get("stat", {})
                return {
                    "name": person.get("fullName", ""),
                    "year": target_year,
                    "team": split.get("team", {}).get("name", ""),
                    "AB": stat.get("atBats", 0),
                    "R": stat.get("runs", 0),
                    "H": stat.get("hits", 0),
                    "HR": stat.get("homeRuns", 0),
                    "RBI": stat.get("rbi", 0),
                    "BB": stat.get("baseOnBalls", 0),
                    "K": stat.get("strikeOuts", 0),
                    "AVG": stat.get("avg", ""),
                    "OBP": stat.get("obp", ""),
                    "SLG": stat.get("slg", ""),
                    "OPS": stat.get("ops", ""),
                    "playerType": "hitter"
                }
    return None

def save_to_file(stats, year):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fname = os.path.join(OUTPUT_DIR, f"historical_stats_{year}.csv")
    with open(fname, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=stats[0].keys())
        writer.writeheader()
        writer.writerows(stats)
    log(f"✅ Saved {len(stats)} records to {fname}")

def main():
    log("📦 Starting historical data scrape...")
    teams = fetch_teams()
    for year in range(SEASON_END_YEAR, SEASON_END_YEAR - YEARS_BACK, -1):
        yearly_stats = []
        log(f"📅 Processing season {year}...")
        for team_id, team_name in teams:
            log(f"🏟️ {team_name} ({year})")
            roster = fetch_roster(team_id, year)
            for pid in roster:
                stats = fetch_player_season_stats(pid, year)
                if stats:
                    yearly_stats.append(stats)
                sleep(0.3)
        if yearly_stats:
            save_to_file(yearly_stats, year)
    log("🎯 Historical scrape complete.")

if __name__ == "__main__":
    main()

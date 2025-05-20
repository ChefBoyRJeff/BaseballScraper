// This script scrapes the latest MLB scores from ESPN and saves them in JSON and CSV formats.
// Import necessary libraries
// Note: This script is designed to run in a Node.js environment.
const axios = require("axios");
const fs = require("fs");
const path = require("path");

const BASE_URL = "https://site.web.api.espn.com/apis/common/v3/sports/baseball/mlb/leaders";
const STAT_CATEGORIES = ["avg", "homeRuns", "rbi"];
const SEASON = 2024;

async function fetchStats(category) {
  const res = await axios.get(BASE_URL, {
    params: {
      limit: 50,
      offset: 0,
      sort: category,
      season: SEASON,
      seasontype: 2
    }
  });
  return res.data;
}

function extractPlayers(data, category) {
  return data.leaders[0].leaders.map(entry => {
    const athlete = entry.athlete;
    const stats = entry.stats || [];
    return {
      name: athlete.displayName,
      team: athlete.team?.displayName,
      position: athlete.position?.abbreviation,
      [category]: stats[0]
    };
  });
}

async function scrapeAllStats() {
  const combined = {};

  for (const category of STAT_CATEGORIES) {
    console.log(`Fetching ${category}...`);
    const rawData = await fetchStats(category);
    const players = extractPlayers(rawData, category);

    for (const player of players) {
      if (!combined[player.name]) {
        combined[player.name] = player;
      } else {
        combined[player.name][category] = player[category];
      }
    }
  }

  return Object.values(combined);
}

function saveOutput(players) {
  const date = new Date().toISOString().split("T")[0];
  const dir = path.join(__dirname, "..", "..", "data");
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  fs.writeFileSync(
    path.join(dir, `player_stats_${date}.json`),
    JSON.stringify(players, null, 2)
  );

  // Save to CSV
  const header = ["name", "team", "position", "avg", "homeRuns", "rbi"];
  const csv = [
    header.join(","),
    ...players.map(p =>
      header.map(h => (p[h] !== undefined ? `"${p[h]}"` : "")).join(",")
    )
  ].join("\n");

  fs.writeFileSync(path.join(dir, `player_stats_${date}.csv`), csv);

  console.log("✅ Saved JSON and CSV.");
}

scrapeAllStats().then(saveOutput).catch(console.error);

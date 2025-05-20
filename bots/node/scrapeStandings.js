// This script scrapes the latest MLB scores from ESPN and saves them in JSON and CSV formats.
// Import necessary libraries
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const URL = 'https://site.api.espn.com/apis/v2/sports/baseball/mlb/standings';

async function fetchStandings() {
  try {
    const res = await axios.get(URL);
    const records = res.data.children.flatMap(conference =>
      conference.standings.entries.map(team => ({
        name: team.team.displayName,
        wins: team.stats.find(s => s.name === 'wins')?.value,
        losses: team.stats.find(s => s.name === 'losses')?.value,
        winPct: team.stats.find(s => s.name === 'winPercent')?.value,
        gamesBack: team.stats.find(s => s.name === 'gamesBehind')?.displayValue,
        streak: team.stats.find(s => s.name === 'streak')?.displayValue
      }))
    );

    const date = new Date().toISOString().split('T')[0];
    const dir = path.join(__dirname, '..', '..', 'data');
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    fs.writeFileSync(
      path.join(dir, `standings_${date}.json`),
      JSON.stringify(records, null, 2)
    );

    console.log('✅ Standings data saved.');
  } catch (error) {
    console.error('Error fetching standings:', error);
  }
}

fetchStandings();

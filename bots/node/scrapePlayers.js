// This script scrapes the latest MLB scores from ESPN and saves them in JSON and CSV formats.
// Import necessary libraries
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const teams = [
  'atl', 'bos', 'chc', 'chw', 'cin', 'cle', 'col', 'det', 'hou',
  'kc', 'laa', 'lad', 'mia', 'mil', 'min', 'nym', 'nyy', 'oak',
  'phi', 'pit', 'sd', 'sea', 'sf', 'stl', 'tb', 'tex', 'tor', 'was'
];

async function fetchPlayers() {
  let allPlayers = [];

  for (const team of teams) {
    const url = `https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/${team}/roster`;
    try {
      const res = await axios.get(url);
      const players = res.data.athletes.flatMap(group => group.items.map(player => ({
        team,
        name: player.fullName,
        position: player.position.name,
        jersey: player.jersey,
        height: player.displayHeight,
        weight: player.displayWeight,
        age: player.age
      })));

      allPlayers.push(...players);
    } catch (err) {
      console.error(`❌ Failed for team: ${team}`);
    }
  }

  const date = new Date().toISOString().split('T')[0];
  const dir = path.join(__dirname, '..', '..', 'data');
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  fs.writeFileSync(
    path.join(dir, `players_${date}.json`),
    JSON.stringify(allPlayers, null, 2)
  );

  console.log('✅ Player data saved.');
}

fetchPlayers();

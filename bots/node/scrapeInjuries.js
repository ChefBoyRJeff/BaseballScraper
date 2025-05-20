// This script scrapes the latest MLB scores from ESPN and saves them in JSON and CSV formats.
// Import necessary libraries
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const URL = 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/injuries';

async function fetchInjuries() {
  try {
    const response = await axios.get(URL);
    const data = response.data;

    const injuries = [];

    data.injuries.forEach(team => {
      team.players.forEach(player => {
        injuries.push({
          team: team.team.displayName,
          name: player.fullName,
          position: player.position.abbreviation,
          status: player.status,
          injury: player.injury,
          date: player.date
        });
      });
    });

    const date = new Date().toISOString().split('T')[0];
    const dir = path.join(__dirname, '..', '..', 'data');
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    fs.writeFileSync(
      path.join(dir, `injuries_${date}.json`),
      JSON.stringify(injuries, null, 2)
    );

    console.log('✅ Injuries data saved.');
  } catch (error) {
    console.error('Error fetching injuries:', error);
  }
}

fetchInjuries();

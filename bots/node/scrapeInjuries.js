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

    if (data && Array.isArray(data.injuries)) {
      data.injuries.forEach(team => {
        if (team && Array.isArray(team.players)) {
          team.players.forEach(player => {
            injuries.push({
              team: team.team.displayName,
              name: player.fullName,
              position: player.position?.abbreviation ?? 'N/A',
              status: player.status,
              injury: player.injury,
              date: player.date
            });
          });
        }
      });
    }

    const date = new Date().toISOString().split('T')[0];
    const dir = path.join(__dirname, '..', '..', 'data');
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    fs.writeFileSync(
      path.join(dir, `injuries_${date}.json`),
      JSON.stringify(injuries, null, 2)
    );

    console.log(`✅ Injuries data saved. Total players: ${injuries.length}`);
  } catch (err) {
    console.error('❌ Error fetching injuries:', err.message);
  }
}

fetchInjuries();

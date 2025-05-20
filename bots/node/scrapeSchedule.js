// This script scrapes the latest MLB scores from ESPN and saves them in JSON and CSV formats.
// Import necessary libraries
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const URL = 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard';

async function fetchSchedule() {
  try {
    const response = await axios.get(URL);
    const data = response.data;

    const schedule = data.events.map(event => ({
      date: event.date,
      name: event.name,
      shortName: event.shortName,
      status: event.status.type.description,
      competitors: event.competitions[0].competitors.map(team => ({
        name: team.team.displayName,
        score: team.score
      }))
    }));

    const date = new Date().toISOString().split('T')[0];
    const dir = path.join(__dirname, '..', '..', 'data');
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    fs.writeFileSync(
      path.join(dir, `schedule_${date}.json`),
      JSON.stringify(schedule, null, 2)
    );

    console.log('✅ Schedule data saved.');
  } catch (error) {
    console.error('Error fetching schedule:', error);
  }
}

fetchSchedule();

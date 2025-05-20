// This script scrapes MLB scores from ESPN and saves them in JSON and CSV formats.
// It uses axios for HTTP requests and cheerio for parsing HTML.
// scrapeScores.js — API-based version
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const today = new Date().toISOString().split('T')[0];
const outputDir = path.join(__dirname, '../../data');

(async () => {
  try {
    const res = await axios.get('http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard');
    const events = res.data.events;

    const games = events.map(event => {
      const competition = event.competitions[0];
      const home = competition.competitors.find(c => c.homeAway === 'home');
      const away = competition.competitors.find(c => c.homeAway === 'away');

      return {
        date: today,
        home_team: home.team.abbreviation,
        home_score: home.score,
        away_team: away.team.abbreviation,
        away_score: away.score,
        status: competition.status.type.description
      };
    });

    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

    // Save JSON
    fs.writeFileSync(path.join(outputDir, `scores_${today}.json`), JSON.stringify(games, null, 2));

    // Save CSV
    const csvData = [
      'date,home_team,home_score,away_team,away_score,status',
      ...games.map(g =>
        `${g.date},"${g.home_team}",${g.home_score},"${g.away_team}",${g.away_score},"${g.status}"`
      )
    ].join('\n');

    fs.writeFileSync(path.join(outputDir, `scores_${today}.csv`), csvData);

    console.log("✅ Scraped and saved scores (Node).");
  } catch (err) {
    console.error("❌ Scraping failed:", err.message);
  }
})();


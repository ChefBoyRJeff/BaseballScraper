// This script scrapes MLB scores from ESPN and saves them in JSON and CSV formats.
// It uses axios for HTTP requests and cheerio for parsing HTML.
// scrapeScore.js
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

const today = new Date().toISOString().split('T')[0];
const outputDir = path.join(__dirname, '../../data');

(async () => {
  try {
    const res = await axios.get('https://www.espn.com/mlb/scoreboard');
    const $ = cheerio.load(res.data);
    const games = [];

    $('section.Scoreboard').each((i, el) => {
      const teams = $(el).find('span.sb-team-short').map((i, el) => $(el).text()).get();
      const scores = $(el).find('span.sb-team-score').map((i, el) => $(el).text()).get();
      const status = $(el).find('span.sb-meta').text().trim();

      if (teams.length === 2 && scores.length === 2) {
        games.push({
          date: today,
          home_team: teams[1],
          home_score: scores[1],
          away_team: teams[0],
          away_score: scores[0],
          status: status
        });
      }
    });

    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);

    fs.writeFileSync(path.join(outputDir, `scores_${today}.json`), JSON.stringify(games, null, 2));
    fs.writeFileSync(path.join(outputDir, `scores_${today}.csv`), [
      'date,home_team,home_score,away_team,away_score,status',
      ...games.map(g =>
        `${g.date},"${g.home_team}",${g.home_score},"${g.away_team}",${g.away_score},"${g.status}"`
      )
    ].join('\n'));

    console.log("Scraped and saved scores (Node).");
  } catch (err) {
    console.error("Scraping failed:", err);
  }
})();

// This script scrapes the latest MLB scores from ESPN and saves them in JSON and CSV formats.
// Dynamically fetch MLB player rosters from ESPN
const axios = require("axios");
const fs = require("fs");
const path = require("path");

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchTeamIds() {
  const url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams";
  const res = await axios.get(url);
  return res.data.sports[0].leagues[0].teams.map(t => ({
    id: t.team.id,
    name: t.team.displayName
  }));
}

async function fetchPlayers() {
  const allPlayers = [];
  const failedTeams = [];

  const teams = await fetchTeamIds();

  for (const { id, name } of teams) {
    const url = `https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/${id}/roster`;

    try {
      const res = await axios.get(url);
      const athletes = res.data.athletes || [];

      for (const group of athletes) {
        for (const player of group.items) {
          allPlayers.push({
            team: name,
            name: player.fullName,
            position: player.position?.name ?? "N/A",
            jersey: player.jersey ?? "",
            height: player.displayHeight ?? "",
            weight: player.displayWeight ?? "",
            age: player.age ?? ""
          });
        }
      }
    } catch (err) {
      console.error(`❌ Failed for team ${name} (ID: ${id}): ${err.message}`);
      failedTeams.push(name);
    }

    await sleep(200);
  }

  const date = new Date().toISOString().split("T")[0];
  const dir = path.join(__dirname, "..", "..", "data");
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  fs.writeFileSync(path.join(dir, `players_${date}.json`), JSON.stringify(allPlayers, null, 2));

  const csvHeader = "team,name,position,jersey,height,weight,age";
  const csvRows = allPlayers.map(p =>
    `"${p.team}","${p.name}","${p.position}","${p.jersey}","${p.height}","${p.weight}","${p.age}"`
  );
  fs.writeFileSync(path.join(dir, `players_${date}.csv`), [csvHeader, ...csvRows].join("\n"));

  console.log(`✅ Player data saved. Total players: ${allPlayers.length}`);
  if (failedTeams.length > 0) {
    console.warn(`⚠️  Failed teams: ${failedTeams.join(", ")}`);
  }
}

fetchPlayers();

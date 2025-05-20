# 🧢 Baseball Scraper Project

This project scrapes MLB data from ESPN using Python and Node.js. It pulls **live scores**, **player stats**, **standings**, **rosters**, **schedules**, and **injuries**, and saves the results in both `.json` and `.csv` formats.

## 📦 Features

- ✅ Python + Node.js scrapers
- ✅ Live scores via ESPN's hidden JSON API
- ✅ Full roster scraping for all teams
- ✅ Player stats, standings, and injury reports
- ✅ Output in JSON & CSV
- ✅ PowerShell automation support
- ✅ Daily run via Task Scheduler

---

## ⚙️ How to Set Up

### 🐧 Ubuntu / WSL (Linux-based setup)

```bash
# Update system
sudo apt update && sudo apt upgrade

# Install Python and Git
sudo apt install git python3.12-venv -y

# Clone the repo
git clone https://github.com/ChefBoyRJeff/BaseballProject.git
cd BaseballProject/BaseballScraper

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install requests beautifulsoup4 pandas


🪟 Windows (PowerShell & GitHub Desktop)

1. Clone using GitHub Desktop

2. Open in Visual Studio Code

3. In terminal:
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install requests beautifulsoup4 pandas
    cd bots/node
    npm install

🚀 Running the Scraper
✅ Manual (One-Off)
Activate your environment and run:
    .\venv\Scripts\Activate.ps1
    python bots/python/scrape_scores.py
    node bots/node/scrapeScores.js

Or to run everything:
    .\run_scrapers.ps1

🕒 Automated (Task Scheduler)

1. Open Task Scheduler

2. Create new task → Trigger daily

3. Action:

    Program: powershell.exe

    Arguments:
        -ExecutionPolicy Bypass -File "$env:USERPROFILE\Desktop\BaseballProject\BaseballScraper\run_scrapers.ps1"

📁 Output

All data is saved in the /data folder:
   - scores_YYYY-MM-DD.json
   - players_YYYY-MM-DD.csv
   - standings_YYYY-MM-DD.csv
   - injuries_YYYY-MM-DD.json
   - and more!

🤝 Contributing

Pull requests welcome!

Ideas:
   - Add betting odds scraper
   - Add news/event feed
   - Add error logs or retry wrappers
   - Add Linux/macOS cron support

🧠 Author

Name: Jeff Jones
📧 jcode3026@gmail.com
🔗 github.com/ChefBoyRJeff
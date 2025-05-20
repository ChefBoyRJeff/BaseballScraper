# 🍙 Baseball Scraper 

This project scrapes MLB data from ESPN using **Python** and **Node.js**. It pulls **live scores**, **player stats**, **standings**, **rosters**, **schedules**, and **injuries**, and saves the results in both `.json` and `.csv` formats.

---

## 📆 Features

* ✅ Python + Node.js scrapers
* ✅ Live scores via ESPN's hidden JSON API
* ✅ Full roster scraping for all teams
* ✅ Player stats, standings, and injury reports
* ✅ Output in JSON & CSV
* ✅ PowerShell automation support
* ✅ Daily execution via Task Scheduler

---

## ⚙️ Setup Instructions

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
```

---

### 🪠 Windows (PowerShell + GitHub Desktop)

1. **Clone** using GitHub Desktop
2. **Open** the folder in Visual Studio Code
3. **Run in terminal:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install requests beautifulsoup4 pandas
cd bots\node
npm install
```

---

## 🚀 Running the Scraper

### ✅ Manual Run

Activate your environment and run scrapers manually:

```powershell
.\venv\Scripts\Activate.ps1
python bots/python/scrape_scores.py
node bots/node/scrapeScores.js
```

Run the full pipeline:

```powershell
.\run_scrapers.ps1
```

---

### 🕒 Automated Run (Windows Task Scheduler)

1. Open **Task Scheduler**
2. Create a new task → Set to trigger **daily**
3. Set the action to:

```text
Program: powershell.exe
Arguments: -ExecutionPolicy Bypass -File "$env:USERPROFILE\Desktop\BaseballProject\BaseballScraper\run_scrapers.ps1"
```

---

## 📁 Output

All files are saved to the `data/` directory in both `.csv` and `.json` formats:

* `scores_YYYY-MM-DD.json`
* `players_YYYY-MM-DD.csv`
* `standings_YYYY-MM-DD.csv`
* `injuries_YYYY-MM-DD.json`
* ...and more!

---

## 🤝 Contributing

Pull requests welcome!

### Suggestions:

* Add betting odds scraper
* Add news and event feeds
* Add retry + error logging
* Support Linux/macOS cron automation

---

## 🧐 Author

**Jeff Jones**
📧 [jcode3026@gmail.com](mailto:jcode3026@gmail.com)
🔗 [github.com/ChefBoyRJeff](https://github.com/ChefBoyRJeff)

---

## 📄 License

MIT License

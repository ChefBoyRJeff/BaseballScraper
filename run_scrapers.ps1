# Activate the Python virtual environment
$venvPath = "C:\Users\jjone\OneDrive\Desktop\BaseballProject\BaseballScraper\venv\Scripts\Activate.ps1"
& $venvPath

# Define base path
$basePath = "C:\Users\jjone\OneDrive\Desktop\BaseballProject\BaseballScraper"

# Run Python scrapers only
Write-Host "Running Python scrapers..."
python "$basePath\bots\python\scrape_scores.py"
python "$basePath\bots\python\scrape_standings.py"
python "$basePath\bots\python\scrape_player_stats.py"
python "$basePath\bots\python\scrape_players.py"
python "$basePath\bots\python\scrape_injuries.py"
python "$basePath\bots\python\scrape_schedule.py"
python "$basePath\bots\python\scrape_historical_data.py"

Write-Host "✅ All scrapers finished."

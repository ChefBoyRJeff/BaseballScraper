# run_scraper.ps1

# Navigate to the scraper directory
cd "C:\Users\jjone\OneDrive\Desktop\BaseballProject\BaseballScraper"

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Run the Python scraper
python bots/python/scrape_scores.py

# Deactivate the virtual environment
deactivate
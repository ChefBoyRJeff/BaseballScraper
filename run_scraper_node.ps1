# run_scraper_node.ps1

cd "C:\Users\jjone\OneDrive\Desktop\BaseballProject\BaseballScraper"

# Run the Node.js scraper
node bots/node/scrapeScore.js

# Check if the Node.js scraper ran successfully
if ($LASTEXITCODE -eq 0) {
    Write-Host "Node.js scraper ran successfully."
} else {
    Write-Host "Node.js scraper failed with exit code $LASTEXITCODE."
}
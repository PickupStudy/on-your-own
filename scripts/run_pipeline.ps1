param(
  [string]$ProjectRoot = "D:\Develop-project\agentLearning\pkb-core"
)

Set-Location $ProjectRoot

if (!(Test-Path ".env")) {
  Write-Host "Missing .env file. Copy .env.example to .env first." -ForegroundColor Yellow
  exit 1
}

node ".\node\src\main.js" pipeline

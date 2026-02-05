param(
  [Parameter(Mandatory=$true)][string]$Query,
  [string]$Log = "C:\Users\bainz\clawd\data\chatlog\discord_enami_1466296030181199933.ndjson",
  [int]$Max = 40
)

$ErrorActionPreference = 'Stop'
if(!(Test-Path $Log)){
  Write-Host "Log not found: $Log" -ForegroundColor Yellow
  exit 1
}

# Fast keyword search (ripgrep if available; fallback to Select-String)
$rg = Get-Command rg -ErrorAction SilentlyContinue
if($rg){
  rg --no-heading --line-number --max-count $Max $Query $Log
} else {
  Select-String -Path $Log -Pattern $Query -SimpleMatch | Select-Object -First $Max
}

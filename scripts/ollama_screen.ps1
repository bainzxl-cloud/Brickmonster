param(
  [Parameter(Mandatory=$true)][string]$Query,
  [string]$Log = "C:\Users\bainz\clawd\data\chatlog\discord_enami_1466296030181199933.ndjson",
  [int]$MaxLines = 60,
  [string]$Model = "gpt-oss:20b"
)

$ErrorActionPreference = 'Stop'

# 1) Pull relevant raw lines quickly
$recall = Join-Path $PSScriptRoot 'recall.ps1'
if(!(Test-Path $recall)){
  throw "Missing recall.ps1 at $recall"
}

$lines = & $recall -Query $Query -Log $Log -Max $MaxLines | Out-String
$lines = $lines.Trim()
if(!$lines){
  Write-Output "(no matching raw log lines found)"
  exit 0
}

# 2) Ask local Ollama to screen/summarize into a tiny memory snippet
$system = @'
You are a fast memory screener. You will be given raw chat log lines.
Return ONLY:
- up to 8 short bullet points of relevant facts/preferences/decisions
- include message ids or dates if present
- do not add new info
- keep it concise
'@

$prompt = "Query: $Query`n`nRaw log lines:`n$lines"

$body = @{ 
  model = $Model
  messages = @(
    @{ role = 'system'; content = $system },
    @{ role = 'user'; content = $prompt }
  )
  stream = $false
  options = @{ temperature = 0.1 }
} | ConvertTo-Json -Depth 6

$resp = Invoke-RestMethod -Method Post -Uri 'http://localhost:11434/api/chat' -ContentType 'application/json' -Body $body
$resp.message.content

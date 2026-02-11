param(
  [Parameter(Mandatory=$true)][string]$InputFile,
  [Parameter(Mandatory=$true)][string]$State,
  [Parameter(Mandatory=$true)][string]$MemoryFile,
  [string]$Model = "llama3.2:3b",
  [int]$MaxLines = 120,
  [int]$OllamaTimeoutSec = 60,
  [int]$TotalTimeoutSec = 120
)

$ErrorActionPreference = 'Stop'

function Write-State([string]$now, [string]$status = $null, [string]$error = $null){
  $obj = @{ lastRun = $now }
  if($status){ $obj.status = $status }
  if($error){ $obj.error = $error }
  $obj | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $State -Encoding UTF8
}

if(!(Test-Path -LiteralPath $InputFile)){
  throw "Input file not found: $InputFile"
}

$stateDir = Split-Path -Parent $State
New-Item -ItemType Directory -Force -Path $stateDir | Out-Null

$rawAll = Get-Content -LiteralPath $InputFile -Raw
$rawAll = ($rawAll + '').Trim()

if(-not $rawAll){
  $now = (Get-Date).ToString('o')
  Write-State -now $now -status 'ok'
  Write-Output "memory-digest ok (0 lines)"
  exit 0
}

# Keep it bounded
$lines = $rawAll -split "`r?`n"
if($lines.Count -gt $MaxLines){
  $lines = $lines | Select-Object -Last $MaxLines
}
$raw = ($lines -join "`n").Trim()

$system = @'
You are a memory filter.
You will be given raw chat lines from ONE user.
Return ONLY 5 to 12 bullet points.
Rules:
- Keep ONLY important, durable memories: preferences, facts, plans, decisions, ongoing projects, important emotions, open loops.
- Do NOT include small talk unless it reveals an enduring preference or goal.
- Do NOT invent anything.
- Keep each bullet short.
- No headings, no intro text; bullets only.
'@

$body = @{
  model = $Model
  messages = @(
    @{ role = 'system'; content = $system },
    @{ role = 'user'; content = "Filter these messages into durable memories:\n\n$raw" }
  )
  stream = $false
  options = @{ temperature = 0.1 }
} | ConvertTo-Json -Depth 8

$now = (Get-Date).ToString('o')

# Call Ollama with a hard timeout so the cron job never hangs.
$summary = $null
$errText = $null

$job = Start-Job -ScriptBlock {
  param($bodyJson, $timeoutSec)
  $ErrorActionPreference = 'Stop'
  # gpt-oss:20b has been observed to 500 on /api/chat; /api/generate is more stable.
  $payload = $bodyJson | ConvertFrom-Json
  $prompt = ($payload.messages | ForEach-Object { ($_.role + ': ' + $_.content) }) -join "`n"
  $genBody = @{ model = $payload.model; prompt = $prompt; stream = $false; options = $payload.options } | ConvertTo-Json -Depth 8
  $r = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:11434/api/generate' -ContentType 'application/json' -Body $genBody -TimeoutSec $timeoutSec
  return ($r.response + '').Trim()
} -ArgumentList $body, $OllamaTimeoutSec

$completed = Wait-Job -Job $job -Timeout $TotalTimeoutSec
if(-not $completed){
  try { Stop-Job -Job $job -Force | Out-Null } catch {}
  try { Remove-Job -Job $job -Force | Out-Null } catch {}

  $errText = "ollama timeout (>${TotalTimeoutSec}s)"
  Write-State -now $now -status 'error' -error $errText
  Write-Output "memory-digest error: $errText"
  exit 1
}

try {
  $summary = Receive-Job -Job $job -ErrorAction Stop
} catch {
  $errText = (($_.Exception.Message + '') -replace "\s+"," ").Trim()
  Write-State -now $now -status 'error' -error $errText
  Write-Output "memory-digest error: $errText"
  exit 1
} finally {
  try { Remove-Job -Job $job -Force | Out-Null } catch {}
}

if(-not $summary){
  $errText = 'empty summary returned'
  Write-State -now $now -status 'error' -error $errText
  Write-Output "memory-digest error: $errText"
  exit 1
}

# Append to memory file
$memDir = Split-Path -Parent $MemoryFile
New-Item -ItemType Directory -Force -Path $memDir | Out-Null

if(!(Test-Path -LiteralPath $MemoryFile)){
  Set-Content -LiteralPath $MemoryFile -Encoding UTF8 -Value ("# " + (Get-Date -Format 'yyyy-MM-dd') + "`n")
}

$block = @(
  "",
  "## Discord hourly memory digest",
  "- Ran: $now",
  "",
  $summary,
  ""
) -join "`n"

Add-Content -LiteralPath $MemoryFile -Encoding UTF8 -Value $block

Write-State -now $now -status 'ok'

Write-Output "memory-digest ok"

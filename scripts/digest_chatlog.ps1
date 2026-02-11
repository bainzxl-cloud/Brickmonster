param(
  [string]$Log = "C:\Users\bainz\clawd\data\chatlog\discord_enami_1466296030181199933.ndjson",
  [string]$State = "C:\Users\bainz\clawd\memory\digests\enami-state.json",
  [string]$Out = "C:\Users\bainz\clawd\memory\digests\enami-latest.md",
  [string]$Model = "gpt-oss:20b",
  [int]$MaxMessages = 60,
  [string]$Author = "Bainzxl"
)

$ErrorActionPreference = 'Stop'

if(!(Test-Path -LiteralPath $Log)){
  throw "Log not found: $Log"
}

$stateDir = Split-Path -Parent $State
New-Item -ItemType Directory -Force -Path $stateDir | Out-Null

$lastId = $null
if(Test-Path -LiteralPath $State){
  try {
    $st = Get-Content -LiteralPath $State -Raw | ConvertFrom-Json
    $lastId = $st.lastMessageId
  } catch {
    $lastId = $null
  }
}

# Read new entries after lastId (author-filtered)
$collect = @()
$pastLast = if($lastId){ $false } else { $true }

Get-Content -LiteralPath $Log | ForEach-Object {
  $line = $_
  if(-not $line.Trim()) { return }

  try { $o = $line | ConvertFrom-Json } catch { return }

  if(-not $o.messageId){ return }

  if(-not $pastLast){
    if($o.messageId -eq $lastId){ $pastLast = $true }
    return
  }

  if($o.author -ne $Author){ return }

  $collect += $o
}

if($collect.Count -eq 0){
  # Still update a heartbeat file so we can see it ran.
  $now = (Get-Date).ToString('o')
  Set-Content -LiteralPath $Out -Encoding UTF8 -Value "# Enami digest\n\n- Ran: $now\n- No new messages\n"
  @{ lastMessageId = $lastId; lastRun = $now } | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $State -Encoding UTF8
  Write-Output "digest ok (0 new)"
  exit 0
}

# Keep only the most recent MaxMessages
if($collect.Count -gt $MaxMessages){
  $collect = $collect | Select-Object -Last $MaxMessages
}

# Ensure chronological order
$collect = $collect | Sort-Object { try { [DateTime]$_.ts } catch { [DateTime]::MinValue } }

$raw = ($collect | ForEach-Object { "[$($_.ts)] ($($_.messageId)) $($_.text)" }) -join "`n"

$system = @'
You are a fast memory summarizer.
You will be given raw chat lines from ONE user.
Return ONLY:
- 6 to 10 short bullet points
- capture preferences, important facts, decisions, emotions, open loops
- do not invent anything
- keep it casual and compact
'@

$body = @{
  model = $Model
  messages = @(
    @{ role = 'system'; content = $system },
    @{ role = 'user'; content = "Summarize these new messages:\n\n$raw" }
  )
  stream = $false
  options = @{ temperature = 0.1 }
} | ConvertTo-Json -Depth 8

# Use 127.0.0.1 instead of localhost to avoid IPv6 (::1) connection hangs on some Windows setups
$resp = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:11434/api/chat' -ContentType 'application/json' -Body $body
$summary = ($resp.message.content + '').Trim()

$now = (Get-Date).ToString('o')
$lastProcessed = $collect[-1].messageId

$md = @(
  '# Enami digest',
  '',
  "- Ran: $now",
  "- Messages summarized: $($collect.Count)",
  "- Last messageId: $lastProcessed",
  '',
  $summary,
  ''
) -join "`n"

$outDir = Split-Path -Parent $Out
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
Set-Content -LiteralPath $Out -Encoding UTF8 -Value $md

@{ lastMessageId = $lastProcessed; lastRun = $now; count = $collect.Count } | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $State -Encoding UTF8

Write-Output "digest ok ($($collect.Count) new)"
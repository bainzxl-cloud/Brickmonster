param(
  [Parameter(Mandatory=$true)][string]$Channel,
  [Parameter(Mandatory=$true)][string]$Author,
  [Parameter(Mandatory=$true)][string]$MessageId,
  [Parameter(Mandatory=$true)][string]$Text,
  [string]$Ts,
  [string]$Out = "C:\Users\bainz\clawd\data\chatlog\discord_enami_1466296030181199933.ndjson"
)

$ErrorActionPreference = 'Stop'

$tsIso = if ($Ts -and $Ts.Trim().Length -gt 0) {
  # Accept either ISO 8601 string or anything PowerShell can parse.
  try {
    (Get-Date $Ts).ToString('o')
  } catch {
    # Fall back to raw input if parsing fails.
    $Ts
  }
} else {
  (Get-Date).ToString('o')
}

$entry = [pscustomobject]@{
  ts = $tsIso
  channel = $Channel
  author = $Author
  messageId = $MessageId
  text = $Text
}

$dir = Split-Path $Out
New-Item -ItemType Directory -Force -Path $dir | Out-Null
($entry | ConvertTo-Json -Compress -Depth 5) + "`n" | Add-Content -Encoding UTF8 -Path $Out

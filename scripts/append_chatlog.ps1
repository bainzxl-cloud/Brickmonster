param(
  [Parameter(Mandatory=$true)][string]$Channel,
  [Parameter(Mandatory=$true)][string]$Author,
  [Parameter(Mandatory=$true)][string]$MessageId,
  [Parameter(Mandatory=$true)][string]$Text,
  [string]$Out = "C:\Users\bainz\clawd\data\chatlog\discord_enami_1466296030181199933.ndjson"
)

$ErrorActionPreference = 'Stop'

$entry = [pscustomobject]@{
  ts = (Get-Date).ToString('o')
  channel = $Channel
  author = $Author
  messageId = $MessageId
  text = $Text
}

$dir = Split-Path $Out
New-Item -ItemType Directory -Force -Path $dir | Out-Null
($entry | ConvertTo-Json -Compress -Depth 5) + "`n" | Add-Content -Encoding UTF8 -Path $Out

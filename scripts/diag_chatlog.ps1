$p = 'C:\Users\bainz\clawd\data\chatlog\discord_enami_1466296030181199933.ndjson'
if (!(Test-Path -LiteralPath $p)) {
  [pscustomobject]@{ exists = $false; path = $p } | ConvertTo-Json
  exit 0
}

$i = Get-Item -LiteralPath $p
$tail = Get-Content -LiteralPath $p -Tail 12

[pscustomobject]@{
  exists = $true
  path = $p
  bytes = $i.Length
  lastWrite = $i.LastWriteTime
  tail = $tail
} | ConvertTo-Json -Depth 4

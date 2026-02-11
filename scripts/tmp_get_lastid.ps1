$path = 'C:\Users\bainz\clawd\data\chatlog\discord_enami_1466296030181199933.ndjson'
$lastId = $null
if (Test-Path -LiteralPath $path) {
  $lines = Get-Content -LiteralPath $path -Tail 200
  $line = $lines | Where-Object { $_.Trim() -ne '' } | Select-Object -Last 1
  if ($null -ne $line) {
    try {
      $obj = $line | ConvertFrom-Json -ErrorAction Stop
      if ($obj.messageId) { $lastId = [string]$obj.messageId }
    } catch {}
  }
}
if ($lastId) { Write-Output $lastId }

$ErrorActionPreference = 'SilentlyContinue'
$p = 'C:\Users\bainz\clawd\data\chatlog\discord_enami_1466296030181199933.ndjson'
$lastId = $null
if (Test-Path $p) {
  $lines = Get-Content $p -Tail 50 | Where-Object { $_ -and $_.Trim() -ne '' }
  if ($lines.Count -gt 0) {
    $l = $lines[-1]
    try {
      $o = $l | ConvertFrom-Json
      if ($null -ne $o.messageId) { $lastId = [string]$o.messageId }
      elseif ($null -ne $o.MessageId) { $lastId = [string]$o.MessageId }
    } catch { $lastId = $null }
  }
}
if ($lastId) { Write-Output $lastId }

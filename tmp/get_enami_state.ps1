$statePath = 'C:\Users\bainz\clawd\memory\digests\enami-filter-state.json'
if (Test-Path $statePath) {
  $j = Get-Content $statePath -Raw | ConvertFrom-Json
} else {
  $dir = Split-Path $statePath -Parent
  if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
  $j = [pscustomobject]@{ lastMessageId = $null; lastRun = $null }
  $j | ConvertTo-Json | Set-Content -Path $statePath -Encoding UTF8
}
if ($null -eq $j.lastMessageId) { '' } else { [string]$j.lastMessageId }

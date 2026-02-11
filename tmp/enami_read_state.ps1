$statePath = 'C:\Users\bainz\clawd\memory\digests\enami-filter-state.json'
if (Test-Path $statePath) {
  $j = Get-Content $statePath -Raw | ConvertFrom-Json
  if ($null -ne $j.lastMessageId) { Write-Output $j.lastMessageId }
} else {
  # no output
}

$ErrorActionPreference = "SilentlyContinue"
$state = Get-Content 'C:\Users\bainz\clawd\memory\digests\enami-filter-state.json' | ConvertFrom-Json
if ($state.lastMessageId) { Write-Output $state.lastMessageId } else { Write-Output "null" }

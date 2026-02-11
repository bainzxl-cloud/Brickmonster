$ErrorActionPreference='Stop'
$statePath='C:\Users\bainz\clawd\memory\digests\enami-filter-state.json'
$tempPath='C:\Users\bainz\clawd\tmp\enami-hourly-raw.txt'

if(Test-Path $tempPath){ Remove-Item -Force $tempPath }

$now=(Get-Date).ToString('o')
if(Test-Path $statePath){ $st=Get-Content $statePath -Raw | ConvertFrom-Json } else { $st=[pscustomobject]@{} }

$st | Add-Member -NotePropertyName lastMessageId -NotePropertyValue $null -Force
$st | Add-Member -NotePropertyName lastRun -NotePropertyValue $now -Force
$st | Add-Member -NotePropertyName status -NotePropertyValue 'error' -Force

$st | ConvertTo-Json | Out-File -FilePath $statePath -Encoding utf8

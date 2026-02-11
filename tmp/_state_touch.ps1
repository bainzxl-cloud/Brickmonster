param($StatePath,$TempFile)
$j = Get-Content $StatePath -Raw | ConvertFrom-Json
$j.lastRun = (Get-Date).ToString('o')
($j | ConvertTo-Json) | Set-Content -Path $StatePath -Encoding UTF8
if ($TempFile -and (Test-Path $TempFile)) { Remove-Item -Force $TempFile }

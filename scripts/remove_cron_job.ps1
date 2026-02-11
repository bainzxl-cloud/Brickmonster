$p = 'C:\Users\bainz\.clawdbot\cron\jobs.json'
$j = Get-Content $p -Raw | ConvertFrom-Json
$before = $j.jobs.Count
$j.jobs = @($j.jobs | Where-Object { $_.id -ne '5e7f1abd-7c4d-41b7-abca-ac78ec5f8d3c' })
$after = $j.jobs.Count
($j | ConvertTo-Json -Depth 80) | Set-Content -Encoding UTF8 $p
Write-Output ("removed={0} remaining={1}" -f ($before-$after), $after)

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\Users\bainz\clawd\scripts\create_memory_daily.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 12am
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "CreateDailyMemoryFile" -Action $action -Trigger $trigger -Settings $settings -User "SYSTEM" -RunLevel Highest
Write-Host "Scheduled task created!"

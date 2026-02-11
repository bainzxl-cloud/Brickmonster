$ErrorActionPreference = 'Stop'

$os = Get-CimInstance Win32_OperatingSystem
$cs = Get-CimInstance Win32_ComputerSystem
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1

$memTotalGB = [math]::Round($cs.TotalPhysicalMemory / 1GB, 1)
$memFreeGB  = [math]::Round($os.FreePhysicalMemory / 1MB, 1) # KB -> MB
$memUsedGB  = [math]::Round($memTotalGB - $memFreeGB, 1)

$uptime = (Get-Date) - $os.LastBootUpTime

$drives = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" |
  Select-Object DeviceID,
    @{n='FreeGB';e={[math]::Round($_.FreeSpace/1GB,1)}},
    @{n='SizeGB';e={[math]::Round($_.Size/1GB,1)}}

$top = Get-Process |
  Sort-Object CPU -Descending |
  Select-Object -First 8 |
  Select-Object ProcessName,Id,CPU,@{n='WorkingSetMB';e={[math]::Round($_.WorkingSet64/1MB,0)}}

[pscustomobject]@{
  CpuLoadPct     = $cpu.LoadPercentage
  MemoryUsedGB   = $memUsedGB
  MemoryTotalGB  = $memTotalGB
  Uptime         = ('{0:%d}d {0:hh}h {0:mm}m' -f $uptime)
  Drives         = $drives
  TopCpuProcesses= $top
} | ConvertTo-Json -Depth 4

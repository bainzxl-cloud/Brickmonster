param(
  [Parameter(Mandatory=$true)][string]$JsonPath,
  [Parameter(Mandatory=$true)][string]$Channel,
  [Parameter(Mandatory=$true)][string]$Author
)
$ErrorActionPreference = 'Stop'
$append = 'C:\Users\bainz\clawd\scripts\append_chatlog.ps1'
$msgs = Get-Content -Raw -Path $JsonPath | ConvertFrom-Json
$msgs = $msgs | Sort-Object { [datetime]$_.ts }
$n = 0
foreach ($m in $msgs) {
  & $append -Channel $Channel -Author $Author -MessageId ([string]$m.id) -Ts ([string]$m.ts) -Text ([string]$m.text)
  $n++
}
Write-Output $n

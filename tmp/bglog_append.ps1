param(
  [Parameter(Mandatory=$true)][string]$Channel,
  [Parameter(Mandatory=$true)][string]$Author,
  [Parameter(Mandatory=$true)][string]$AppendScript,
  [Parameter(Mandatory=$true)][string]$JsonPath
)

$json = Get-Content -Raw -Path $JsonPath
$items = $json | ConvertFrom-Json
foreach($m in $items){
  & $AppendScript -Channel $Channel -Author $Author -MessageId $m.id -Ts $m.ts -Text $m.text
  if(-not $?) { throw "append failed for $($m.id)" }
}

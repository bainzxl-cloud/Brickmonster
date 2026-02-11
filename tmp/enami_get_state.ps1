param([string]$StatePath)
if(Test-Path $StatePath){
  $j = Get-Content $StatePath -Raw | ConvertFrom-Json
} else {
  $j = [pscustomobject]@{ lastMessageId = $null; lastRun = $null }
}
$j.lastMessageId

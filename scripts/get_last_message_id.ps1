param(
  [Parameter(Mandatory=$true)][string]$Path
)
if(!(Test-Path -LiteralPath $Path)){
  exit 0
}
$line = Get-Content -LiteralPath $Path -Tail 200 | Where-Object { $_.Trim().Length -gt 0 } | Select-Object -Last 1
if([string]::IsNullOrWhiteSpace($line)){
  exit 0
}
try {
  $obj = $line | ConvertFrom-Json
  if($null -ne $obj -and $obj.messageId){
    Write-Output $obj.messageId
  }
} catch {
  exit 0
}

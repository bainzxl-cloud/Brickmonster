param(
  [Parameter(Mandatory=$true)][string]$Path
)
if(!(Test-Path -LiteralPath $Path)){
  ''
  exit 0
}
$line = Get-Content -LiteralPath $Path -Tail 200 | Where-Object { $_ -and $_.Trim() -ne '' } | Select-Object -Last 1
if(-not $line){
  ''
  exit 0
}
try {
  ( $line | ConvertFrom-Json -ErrorAction Stop ).messageId
} catch {
  ''
}

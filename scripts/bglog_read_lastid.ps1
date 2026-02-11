param(
  [Parameter(Mandatory=$true)][string]$Path
)
if (!(Test-Path $Path)) { return }
$line = Get-Content -Path $Path -Tail 50 | Where-Object { $_.Trim() -ne '' } | Select-Object -Last 1
if (-not $line) { return }
try {
  $obj = $line | ConvertFrom-Json
  if ($null -ne $obj.messageId) { $obj.messageId }
} catch {
  return
}

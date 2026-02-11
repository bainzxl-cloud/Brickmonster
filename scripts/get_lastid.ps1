param(
  [Parameter(Mandatory=$true)][string]$Path
)

if (!(Test-Path -LiteralPath $Path)) { exit 0 }

$line = Get-Content -LiteralPath $Path -Tail 200 | Where-Object { $_ -match '\S' } | Select-Object -Last 1
if ($null -eq $line -or $line -eq '') { exit 0 }

try {
  $obj = $line | ConvertFrom-Json
  if ($null -ne $obj -and $null -ne $obj.messageId) {
    Write-Output $obj.messageId
  }
} catch {
  exit 0
}

param(
  [Parameter(Mandatory=$true)][string]$Path
)

if (-not (Test-Path -LiteralPath $Path)) { exit 0 }

$last = Get-Content -LiteralPath $Path -ErrorAction SilentlyContinue |
  Where-Object { $_ -and $_.Trim() -ne '' } |
  Select-Object -Last 1

if (-not $last) { exit 0 }

try {
  $obj = $last | ConvertFrom-Json
  if ($null -ne $obj.messageId) { Write-Output $obj.messageId }
} catch {
  # ignore
}

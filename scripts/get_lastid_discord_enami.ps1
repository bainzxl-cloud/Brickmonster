param(
  [string]$Path
)

if (-not (Test-Path -LiteralPath $Path)) { exit 0 }

# Read a tail window; find last non-empty line; parse JSON; print messageId
$lines = Get-Content -LiteralPath $Path -Tail 400 -ErrorAction SilentlyContinue
if (-not $lines) { exit 0 }

$last = ($lines | Where-Object { $_ -and $_.Trim() -ne '' } | Select-Object -Last 1)
if (-not $last) { exit 0 }

try {
  $obj = $last | ConvertFrom-Json -ErrorAction Stop
  if ($obj -and $obj.messageId) { Write-Output $obj.messageId }
} catch {
  exit 0
}

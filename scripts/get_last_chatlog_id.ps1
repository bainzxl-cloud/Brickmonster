param(
  [Parameter(Mandatory=$true)][string]$Path
)

if (!(Test-Path -LiteralPath $Path)) { exit 0 }

$lines = Get-Content -LiteralPath $Path -Tail 200 -ErrorAction SilentlyContinue
if (-not $lines) { exit 0 }

$line = $null
for ($i = $lines.Count - 1; $i -ge 0; $i--) {
  if ($lines[$i] -and $lines[$i].Trim().Length -gt 0) { $line = $lines[$i]; break }
}
if (-not $line) { exit 0 }

try {
  $o = $line | ConvertFrom-Json -ErrorAction Stop
  if ($null -ne $o.messageId -and ("$($o.messageId)".Trim().Length -gt 0)) {
    Write-Output $o.messageId
  }
} catch {
  exit 0
}

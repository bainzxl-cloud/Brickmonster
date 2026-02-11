param(
  [Parameter(Mandatory=$true)][string]$Path
)

$lastId = $null

if (Test-Path $Path) {
  # Read a tail chunk for speed; then pick last non-empty line
  $lines = Get-Content -Path $Path -Tail 500 -ErrorAction SilentlyContinue | Where-Object { $_ -and $_.Trim() -ne '' }
  if ($lines -and $lines.Count -gt 0) {
    $line = $lines[-1]
    try {
      $obj = $line | ConvertFrom-Json -ErrorAction Stop
      if ($obj -and $obj.messageId) { $lastId = [string]$obj.messageId }
    } catch {
      $lastId = $null
    }
  }
}

if ($null -ne $lastId) { Write-Output $lastId }

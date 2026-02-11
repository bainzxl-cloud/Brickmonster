param(
  [string]$Path
)

$lastId = $null
try {
  if (Test-Path -LiteralPath $Path) {
    $line = Get-Content -LiteralPath $Path -Tail 200 | Where-Object { $_ -and $_.Trim() -ne '' } | Select-Object -Last 1
    if ($line) {
      try {
        $obj = $line | ConvertFrom-Json
        if ($obj -and $obj.messageId) { $lastId = [string]$obj.messageId }
      } catch {
        $lastId = $null
      }
    }
  }
} catch {
  $lastId = $null
}

if ($lastId) { Write-Output $lastId }

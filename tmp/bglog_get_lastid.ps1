param(
  [string]$Path
)
$lastId = $null
if (Test-Path $Path) {
  $lines = Get-Content -Path $Path -Tail 200 | Where-Object { $_ -ne $null -and $_.Trim().Length -gt 0 }
  if ($lines.Count -gt 0) {
    $last = $lines[-1]
    try {
      $obj = $last | ConvertFrom-Json -ErrorAction Stop
      if ($null -ne $obj.messageId -and [string]$obj.messageId -ne '') {
        $lastId = [string]$obj.messageId
      }
    } catch {
      $lastId = $null
    }
  }
}
$lastId

param(
  [Parameter(Mandatory=$true)][string]$Path
)

$lastId = $null
if (Test-Path $Path) {
  $line = Get-Content -Path $Path -Tail 50 | Where-Object { $_ -and $_.Trim() -ne '' } | Select-Object -Last 1
  if ($line) {
    try {
      $obj = $line | ConvertFrom-Json -ErrorAction Stop
      if ($null -ne $obj.messageId -and [string]$obj.messageId) {
        $lastId = [string]$obj.messageId
      }
    } catch {
      # ignore
    }
  }
}

if ($lastId) { Write-Output $lastId }

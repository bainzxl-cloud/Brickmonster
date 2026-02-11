param(
  [Parameter(Mandatory=$true)][string]$Path
)

$lastId = $null
if (Test-Path $Path) {
  $lastNonEmpty = Get-Content -Path $Path -ErrorAction SilentlyContinue |
    Where-Object { $_ -and $_.Trim() -ne '' } |
    Select-Object -Last 1

  if ($lastNonEmpty) {
    try {
      $obj = $lastNonEmpty | ConvertFrom-Json -ErrorAction Stop
      if ($null -ne $obj.messageId -and [string]$obj.messageId -ne '') {
        $lastId = [string]$obj.messageId
      }
    } catch {
      # ignore
    }
  }
}

$lastId

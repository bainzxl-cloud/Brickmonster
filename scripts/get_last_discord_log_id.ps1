param(
  [Parameter(Mandatory=$true)][string]$Path
)

$lastId = $null

if (Test-Path $Path) {
  $line = Get-Content -Path $Path -Tail 200 |
    Where-Object { $_ -and $_.Trim() -ne '' } |
    Select-Object -Last 1

  if ($line) {
    try {
      $obj = $line | ConvertFrom-Json -ErrorAction Stop
      if ($obj.messageId) { $lastId = [string]$obj.messageId }
    } catch {
      # ignore parse errors
    }
  }
}

if ($lastId) { Write-Output $lastId } else { Write-Output '__NULL__' }

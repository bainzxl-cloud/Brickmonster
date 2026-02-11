param([string]$Path)
try {
  $raw = Get-Content -LiteralPath $Path -Raw
  $d = $raw | ConvertFrom-Json
  Write-Output "JSON_OK items=$($d.items.Count)"
} catch {
  Write-Output ("JSON_ERR " + $_.Exception.Message)
  exit 1
}

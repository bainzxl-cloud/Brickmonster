param($StatePath)
$dir = Split-Path -Parent $StatePath
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
$j = $null
if (Test-Path $StatePath) {
  try {
    $raw = Get-Content $StatePath -Raw
    $j = $raw | ConvertFrom-Json
  } catch {
    $j = $null
  }
}
if ($null -eq $j) {
  $j = [pscustomobject]@{ lastMessageId = $null; lastRun = $null }
  ($j | ConvertTo-Json) | Set-Content -Path $StatePath -Encoding UTF8
}
$j | ConvertTo-Json -Compress

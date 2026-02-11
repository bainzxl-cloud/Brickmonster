param([string]$StatePath,[string]$LastMessageId,[string]$LastRun)
if (Test-Path $StatePath) { $s = Get-Content $StatePath -Raw | ConvertFrom-Json } else { $s = [pscustomobject]@{} }
if ($PSBoundParameters.ContainsKey('LastMessageId')) { $s.lastMessageId = $LastMessageId }
$s.lastRun = $LastRun
$s | ConvertTo-Json -Depth 10 | Set-Content -Path $StatePath -Encoding utf8

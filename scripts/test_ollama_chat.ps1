param(
  [string]$Model = 'gpt-oss:20b'
)

$ErrorActionPreference = 'Stop'

$body = @{ 
  model = $Model
  messages = @(
    @{ role = 'system'; content = 'Reply with the single word OK.' },
    @{ role = 'user'; content = 'OK' }
  )
  stream = $false
} | ConvertTo-Json -Depth 8

try {
  $r = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:11434/api/chat' -ContentType 'application/json' -Body $body -TimeoutSec 60
  $r | ConvertTo-Json -Depth 6
  exit 0
} catch {
  Write-Output ("ERROR: " + $_.Exception.Message)
  try {
    $resp = $_.Exception.Response
    if($resp){
      $sr = New-Object System.IO.StreamReader($resp.GetResponseStream())
      $txt = $sr.ReadToEnd()
      $sr.Close()
      Write-Output "RESPONSE_BODY:"
      Write-Output $txt
    }
  } catch {}
  exit 1
}

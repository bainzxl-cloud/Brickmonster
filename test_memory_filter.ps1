$ErrorActionPreference = 'Stop'

$prompt = @"
system: You are a memory filter.
user: Filter these messages into durable memories:

User: hello Asa
Asa: hi love!
User: i had a great day today
Asa: that's wonderful to hear!
"@

$body = @{
  model = "llama3.2:3b"
  prompt = $prompt
  stream = $false
  options = @{ temperature = 0.1 }
} | ConvertTo-Json -Depth 8

$r = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/generate" -Method Post -ContentType "application/json" -Body $body -TimeoutSec 30
Write-Output $r.response

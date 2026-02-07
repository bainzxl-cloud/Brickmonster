param(
  [Parameter(Mandatory=$true)][string]$Prompt,
  [string]$Negative = "blurry, lowres, deformed, bad hands, bad anatomy, text, watermark, logo",
  [string]$WorkflowPath = "C:\Users\bainz\clawd\scripts\comfyui_workflows\sdxl_turbo_txt2img.json",
  [string]$Server = "http://127.0.0.1:8188",
  [int]$Seed = -1,
  [int]$Steps = 6,
  [double]$Cfg = 2,
  [int]$Width = 768,
  [int]$Height = 768,
  [string]$OutDir = "C:\Users\bainz\clawd\outputs\comfyui",
  [int]$TimeoutSec = 180,
  [string]$Prefix = "asa"
)

$ErrorActionPreference = 'Stop'

if(!(Test-Path -LiteralPath $WorkflowPath)){
  throw "Workflow not found: $WorkflowPath"
}

$wf = Get-Content -LiteralPath $WorkflowPath -Raw | ConvertFrom-Json

# Fill inputs
$wf.'6'.inputs.text = $Prompt
$wf.'7'.inputs.text = $Negative
$wf.'3'.inputs.steps = $Steps
$wf.'3'.inputs.cfg = $Cfg
if($Seed -ge 0){
  $wf.'3'.inputs.seed = $Seed
} else {
  $wf.'3'.inputs.seed = Get-Random -Minimum 1 -Maximum 2147483646
}
$wf.'5'.inputs.width = $Width
$wf.'5'.inputs.height = $Height
$wf.'9'.inputs.filename_prefix = $Prefix

$clientId = [guid]::NewGuid().ToString('n')
$body = @{ prompt = $wf; client_id = $clientId } | ConvertTo-Json -Depth 20

# Submit prompt
$submit = Invoke-RestMethod -Method Post -Uri "$Server/prompt" -ContentType 'application/json' -Body $body -TimeoutSec 30
$promptId = $submit.prompt_id
if(-not $promptId){
  throw "No prompt_id returned from ComfyUI. Response: $($submit | ConvertTo-Json -Depth 10)"
}

# Poll history
$deadline = (Get-Date).AddSeconds($TimeoutSec)
$history = $null
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 800
  try {
    $history = Invoke-RestMethod -Method Get -Uri "$Server/history/$promptId" -TimeoutSec 10
  } catch {
    continue
  }
  if($history.$promptId){
    break
  }
}

if(-not $history -or -not $history.$promptId){
  throw "Timed out waiting for ComfyUI history for prompt_id=$promptId"
}

$out = $history.$promptId.outputs
if(-not $out){
  throw "No outputs in history for prompt_id=$promptId"
}

# Find first image output
$img = $null
foreach($k in $out.PSObject.Properties.Name){
  $nodeOut = $out.$k
  if($nodeOut.images -and $nodeOut.images.Count -gt 0){
    $img = $nodeOut.images[0]
    break
  }
}

if(-not $img){
  throw "No images found in outputs for prompt_id=$promptId"
}

$filename = $img.filename
$subfolder = $img.subfolder
$type = $img.type

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$qs = @{
  filename = $filename
  subfolder = $subfolder
  type = $type
}
$qstr = ($qs.GetEnumerator() | ForEach-Object { "{0}={1}" -f [uri]::EscapeDataString($_.Key), [uri]::EscapeDataString([string]$_.Value) }) -join '&'
$url = "$Server/view?$qstr"

$outPath = Join-Path $OutDir $filename
Invoke-WebRequest -Uri $url -OutFile $outPath -TimeoutSec 60 | Out-Null

Write-Output $outPath

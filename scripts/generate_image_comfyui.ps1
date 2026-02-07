param(
  [Parameter(Mandatory=$true)][string]$Prompt,
  [string]$Negative = "blurry, lowres, deformed, bad hands, bad anatomy, text, watermark, logo",
  [string]$WorkflowPath = "C:\Users\bainz\clawd\scripts\comfyui_workflows\sdxl_turbo_txt2img.json",
  [string]$Server = "http://127.0.0.1:8188",
  [int]$Seed = -1,
  [int]$Steps = 6,
  [double]$Cfg = 2,
  # Output size (final).
  [int]$Width = 2560,
  [int]$Height = 1560,
  # Internal generation size (VRAM-heavy). If set, ComfyUI generates at this size, then we optionally resize to Width/Height.
  [int]$GenWidth = 1080,
  [int]$GenHeight = 1080,
  [string]$OutDir = "C:\Users\bainz\clawd\outputs\comfyui",
  [int]$TimeoutSec = 180,
  [string]$Prefix = "asa"
)

$ErrorActionPreference = 'Stop'

if(!(Test-Path -LiteralPath $WorkflowPath)){
  throw "Workflow not found: $WorkflowPath"
}

function Detect-Mode([string]$p){
  $t = ($p + '').ToLowerInvariant()
  if($t -match '\b(product|listing|ecommerce|catalog|white background|studio lighting)\b'){ return 'product' }
  if($t -match '\b(portrait|headshot|selfie|face|model)\b'){ return 'portrait' }
  if($t -match '\b(logo|icon|sticker|emote|mascot)\b'){ return 'logo' }
  if($t -match '\b(landscape|cinematic|movie|wide shot|scene)\b'){ return 'scene' }
  if($t -match '\b(chart|graph|plot|diagram)\b'){ return 'diagram' }
  return 'general'
}

function Apply-StyleHint([string]$mode, [string]$p){
  switch($mode){
    'product' { return "$p, clean studio product photo, soft diffused lighting, clean background" }
    'portrait' { return "$p, professional portrait photo, natural skin texture, 85mm lens, shallow depth of field" }
    'logo' { return "$p, centered composition, high contrast, minimal background" }
    'scene' { return "$p, cinematic lighting, dramatic atmosphere, high detail" }
    'diagram' { return "$p, clean minimal design, high readability" }
    default { return $p }
  }
}

$wf = Get-Content -LiteralPath $WorkflowPath -Raw | ConvertFrom-Json

# Fill inputs
$mode = Detect-Mode $Prompt
$finalPrompt = Apply-StyleHint $mode $Prompt

$wf.'6'.inputs.text = $finalPrompt
$wf.'7'.inputs.text = $Negative
$wf.'3'.inputs.steps = $Steps
$wf.'3'.inputs.cfg = $Cfg
if($Seed -ge 0){
  $wf.'3'.inputs.seed = $Seed
} else {
  $wf.'3'.inputs.seed = Get-Random -Minimum 1 -Maximum 2147483646
}

# Internal generation resolution
$genW = $GenWidth
$genH = $GenHeight
$wf.'5'.inputs.width = $genW
$wf.'5'.inputs.height = $genH
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

# Optional upscale/resize to requested output size
if(($Width -ne $genW) -or ($Height -ne $genH)){
  try {
    Add-Type -AssemblyName System.Drawing
    $src = [System.Drawing.Image]::FromFile($outPath)
    $bmp = New-Object System.Drawing.Bitmap($Width, $Height)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.DrawImage($src, 0, 0, $Width, $Height)
    $g.Dispose(); $src.Dispose()

    $resized = [System.IO.Path]::Combine($OutDir, ([System.IO.Path]::GetFileNameWithoutExtension($filename) + "_${Width}x${Height}.png"))
    $bmp.Save($resized, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    Write-Output $resized
    exit 0
  } catch {
    # Fall back to original if resizing fails
  }
}

Write-Output $outPath

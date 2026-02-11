param(
  [Parameter(Mandatory=$true)][string]$Name
)

$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$dir = Join-Path $base 'presets'

$mapPath = Join-Path $dir 'presets.json'
if (!(Test-Path $mapPath)) { throw "Missing presets.json at $mapPath" }
$map = Get-Content $mapPath -Raw | ConvertFrom-Json

if ($Name -eq 'list') {
  $map.psobject.Properties.Name | Sort-Object
  exit 0
}

if (-not $map.psobject.Properties.Name.Contains($Name)) {
  throw "Unknown preset '$Name'. Use: -Name list" 
}

$rel = $map.$Name
$path = Join-Path $dir $rel
if (!(Test-Path $path)) { throw "Preset file not found: $path" }

Write-Output "Running preset: $Name ($rel)"
& powershell -NoProfile -ExecutionPolicy Bypass -File $path

param(
  [string]$Workspace = "C:\Users\bainz\clawd",
  [string]$Model = "gpt-oss:20b",
  [int]$MaxDailyFiles = 2,
  [int]$TimeoutSec = 180
)

$ErrorActionPreference = 'Stop'

$memRoot = Join-Path $Workspace 'memory'
$topicsDir = Join-Path $memRoot 'topics'
$digestsDir = Join-Path $memRoot 'digests'
$statePath = Join-Path $digestsDir 'organize-topics-state.json'
$longTerm = Join-Path $Workspace 'MEMORY.md'

New-Item -ItemType Directory -Force -Path $topicsDir | Out-Null
New-Item -ItemType Directory -Force -Path $digestsDir | Out-Null

# Collect source files: MEMORY.md + daily memory logs (exclude digests/topics)
$daily = Get-ChildItem -LiteralPath $memRoot -File -Filter '*.md' -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match '^\d{4}-\d{2}-\d{2}\.md$' } |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First $MaxDailyFiles

$srcFiles = @()
if(Test-Path -LiteralPath $longTerm){ $srcFiles += (Get-Item -LiteralPath $longTerm) }
$srcFiles += $daily

if($srcFiles.Count -eq 0){
  Write-Output 'organize-topics ok (0 sources)'
  exit 0
}

# Compute a simple state hash from file mtimes/sizes to avoid redundant rewrites
$stamp = ($srcFiles | ForEach-Object { "{0}|{1}|{2}" -f $_.FullName, $_.Length, $_.LastWriteTimeUtc.Ticks }) -join "`n"
$stampHash = [BitConverter]::ToString((New-Object Security.Cryptography.SHA256Managed).ComputeHash([Text.Encoding]::UTF8.GetBytes($stamp))).Replace('-','').ToLowerInvariant()

$prevHash = $null
if(Test-Path -LiteralPath $statePath){
  try { $prevHash = ((Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json).hash + '') } catch {}
}

if($prevHash -and $prevHash -eq $stampHash){
  Write-Output 'organize-topics ok (no changes)'
  exit 0
}

# Read content (bounded)
function Read-FileSafe([string]$path, [int]$maxChars = 4000){
  if(!(Test-Path -LiteralPath $path)){ return '' }
  $t = Get-Content -LiteralPath $path -Raw
  if($t.Length -gt $maxChars){
    return $t.Substring($t.Length - $maxChars)
  }
  return $t
}

$chunks = @()
foreach($f in $srcFiles){
  $txt = Read-FileSafe -path $f.FullName
  if($txt){
    $chunks += "FILE: $($f.Name)\n---\n$txt\n---"
  }
}

$corpus = ($chunks -join "\n\n")
# sanitize problematic characters that can break JSON transport/parsing
$corpus = $corpus -replace "\uFEFF", ""
$corpus = $corpus -replace "[\x00-\x08\x0B\x0C\x0E-\x1F]", ""

function Select-Corpus([string]$text, [string[]]$keywords, [int]$maxChars = 6500){
  $lines = $text -split "`r?`n"
  $picked = @()
  foreach($ln in $lines){
    foreach($k in $keywords){
      if($ln -match [Regex]::Escape($k)) { $picked += $ln; break }
    }
  }
  if($picked.Count -eq 0){
    $picked = $lines | Select-Object -Last 200
  }
  $out = ($picked -join "`n").Trim()
  if($out.Length -gt $maxChars){ $out = $out.Substring($out.Length - $maxChars) }
  return $out
}

$prefCorpus = Select-Corpus $corpus @('Tone:','Emojis:','Addressing:','prefers','call the user','short','warm')
$webCorpus  = Select-Corpus $corpus @('brickmonster','lego-shop','GitHub','domain','listing','listings.json','product','store')
$imgCorpus  = Select-Corpus $corpus @('ComfyUI','SDXL','Flux','checkpoint','safetensors','KSampler','VRAM','workflow','prompt')
$persCorpus = Select-Corpus $corpus @('Birthday','name','timezone','likes','interests','feels','values','perfectionism')
$otherCorpus= Select-Corpus $corpus @('TODO','next','reminder','cron','gateway','restart')

function Call-OllamaBullets([string]$topic, [string]$instructions, [string]$corpusText){
  $system = "You are a memory organizer. Output ONLY markdown bullet lines. 5-20 bullets max. If nothing: - (none). Keep ONLY durable info; dedupe; prefer newest."
  $user = "Topic: $topic\n\n$instructions\n\nSource notes:\n$corpusText"
  $prompt = "system: $system`nuser: $user"

  $genObj = @{ model = $Model; prompt = $prompt; stream = $false; options = @{ temperature = 0.0; num_predict = 220; num_ctx = 4096 } }
  $genBody = $genObj | ConvertTo-Json -Depth 8
  $null = $genBody | ConvertFrom-Json
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($genBody)

  $r = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:11434/api/generate' -ContentType 'application/json' -Body $bytes -TimeoutSec $TimeoutSec
  $out = ($r.response + '').Trim()
  if(-not $out){
    return "- (none)"
  }
  return $out
}

# Split organization into separate calls to avoid filling context window.
$preferences = Call-OllamaBullets -topic 'preferences' -instructions 'Extract stable chat/style preferences, how the assistant should behave, and formatting preferences.' -corpusText $prefCorpus
$web = Call-OllamaBullets -topic 'web_creation' -instructions 'Extract ongoing web creation projects, repos, domains, procedures, decisions, and next steps.' -corpusText $webCorpus
$image = Call-OllamaBullets -topic 'image_generation' -instructions 'Extract ComfyUI/SDXL/Flux setup notes, model names, settings that worked, and troubleshooting tips.' -corpusText $imgCorpus
$personal = Call-OllamaBullets -topic 'personal' -instructions 'Extract personal preferences/interests/goals that the user wants remembered.' -corpusText $persCorpus
$other = Call-OllamaBullets -topic 'other' -instructions 'Anything durable that does not fit the above.' -corpusText $otherCorpus

function Write-Topic([string]$name, [string]$title, [string]$bullets){
  $path = Join-Path $topicsDir $name
  $now = (Get-Date).ToString('o')
  $content = @(
    "# $title",
    "",
    "- Updated: $now",
    "",
    ($bullets + '').Trim(),
    ""
  ) -join "`n"
  Set-Content -LiteralPath $path -Encoding UTF8 -Value $content
}

Write-Topic -name 'preferences.md' -title 'Preferences (chat style + behavior)' -bullets $preferences
Write-Topic -name 'web-creation.md' -title 'Web creation (sites, scripts, projects)' -bullets $web
Write-Topic -name 'image-generation.md' -title 'Image generation (ComfyUI/SDXL/Flux)' -bullets $image
Write-Topic -name 'personal.md' -title 'Personal (interests, facts, goals)' -bullets $personal
Write-Topic -name 'other.md' -title 'Other durable memories' -bullets $other

# Update state
$state = @{ lastRun = (Get-Date).ToString('o'); hash = $stampHash; sources = $srcFiles.Count }
$state | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $statePath -Encoding UTF8

Write-Output ('organize-topics ok (' + $srcFiles.Count + ' sources)')

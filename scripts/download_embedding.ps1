param(
  [string]$Url = 'https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q4_K_M.gguf',
  [string]$OutDir = "$env:USERPROFILE\.clawdbot\models\embeddings",
  [string]$FileName = 'nomic-embed-text-v1.5.Q4_K_M.gguf'
)
$ErrorActionPreference='Stop'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$outPath = Join-Path $OutDir $FileName
if(!(Test-Path -LiteralPath $outPath)){
  Write-Host "Downloading: $Url"
  Invoke-WebRequest -Uri $Url -OutFile $outPath
} else {
  Write-Host "Already exists: $outPath"
}
Get-Item -LiteralPath $outPath | Select-Object FullName,Length,LastWriteTime

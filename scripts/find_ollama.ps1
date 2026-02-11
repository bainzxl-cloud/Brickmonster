$ErrorActionPreference = 'SilentlyContinue'
$pf86 = ${env:ProgramFiles(x86)}
$candidates = @(
  "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe",
  "$env:ProgramFiles\Ollama\ollama.exe",
  "$pf86\Ollama\ollama.exe"
)
foreach($c in $candidates){
  if($c -and (Test-Path -LiteralPath $c)){
    Write-Output $c
    exit 0
  }
}

# fallback: quick search (limited)
$roots = @($env:LOCALAPPDATA, $env:ProgramFiles, $pf86) | Where-Object { $_ -and (Test-Path $_) }
foreach($r in $roots){
  Get-ChildItem -Path $r -Filter 'ollama.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
  if($LASTEXITCODE -eq 0){ }
}

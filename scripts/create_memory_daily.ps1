# Automated Daily Memory File Creator
# Runs at midnight each day to create memory/YYYY-MM-DD.md

$ErrorActionPreference = 'Stop'

$Today = Get-Date -Format 'yyyy-MM-dd'
$MemoryDir = Join-Path $PSScriptRoot "..\memory"
$MemoryFile = Join-Path $MemoryDir "${Today}.md"

# Create memory directory if it doesn't exist
if(!(Test-Path $MemoryDir)){
    New-Item -ItemType Directory -Path $MemoryDir -Force | Out-Null
}

# Create today's memory file if it doesn't exist
if(!(Test-Path $MemoryFile)){
    $header = "# ${Today}`n`n## Daily Notes`n- `n`n"
    Set-Content -Path $MemoryFile -Value $header -Encoding UTF8
    Write-Host "Created memory file: ${Today}.md"
    exit 0
} else {
    Write-Host "Memory file already exists: ${Today}.md"
    exit 0
}

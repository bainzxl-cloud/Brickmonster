#!/usr/bin/env pwsh
<#
.SYNOPSIS
Automatically creates daily memory file and runs memory digest
.DESCRIPTION
Creates memory/YYYY-MM-DD.md if it doesn't exist, then runs the digest
#>

$ErrorActionPreference = 'Stop'

$Today = Get-Date -Format 'yyyy-MM-dd'
$MemoryFile = Join-Path $PSScriptRoot "..\memory\${Today}.md"

# Create daily memory file if it doesn't exist
if(!(Test-Path -LiteralPath $MemoryFile)){
    $header = "# ${Today}`n`n"
    Set-Content -LiteralPath $MemoryFile -Encoding UTF8 -Value $header
    Write-Host "Created new memory file: ${Today}.md"
}

# Run the digest
$StateFile = Join-Path $PSScriptRoot "..\memory\digests\enami-filter-state.json"
$InputFile = Join-Path $PSScriptRoot "..\data\chatlog\discord_enami_1466296030181199933.ndjson"

# Run the digest script
pwsh -Command {
    param($Input, $State, $Memory, $Model)
    
    $ErrorActionPreference = 'Stop'
    
    # Call the digest script
    & "$using:PSScriptRoot\..\scripts\digest_discord_to_memory.ps1" `
        -InputFile $Input `
        -State $State `
        -MemoryFile $Memory `
        -Model $Model
    
} -Args $InputFile, $StateFile, $MemoryFile, "llama3.2:3b"

Write-Host "Memory digest complete for ${Today}"

#!/usr/bin/env pwsh
# Memory Auto-Load Script for Clawdbot Sessions (Windows PowerShell)
# Run this at the start of every session to load all context files

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$workspaceDir = Split-Path -Parent -Path $scriptDir

Write-Host "📚 Loading Clawdbot memory files..." -ForegroundColor Cyan

# Essential Identity Files
Write-Host "👤 Loading identity files..." -ForegroundColor Green
Get-Content "$workspaceDir\SOUL.md" -ErrorAction SilentlyContinue | Out-Null
Get-Content "$workspaceDir\USER.md" -ErrorAction SilentlyContinue | Out-Null
Get-Content "$workspaceDir\IDENTITY.md" -ErrorAction SilentlyContinue | Out-Null

# Memory Files
Write-Host "🧠 Loading memory files..." -ForegroundColor Green

# Today's and yesterday's daily logs
$today = Get-Date -Format "yyyy-MM-dd"
$yesterday = (Get-Date).AddDays(-1).ToString("yyyy-MM-dd")

if (Test-Path "$workspaceDir\memory\$today.md") {
    Get-Content "$workspaceDir\memory\$today.md" -ErrorAction SilentlyContinue | Out-Null
}

if (Test-Path "$workspaceDir\memory\$yesterday.md") {
    Get-Content "$workspaceDir\memory\$yesterday.md" -ErrorAction SilentlyContinue | Out-Null
}

# Long-term memory
if (Test-Path "$workspaceDir\MEMORY.md") {
    Get-Content "$workspaceDir\MEMORY.md" -ErrorAction SilentlyContinue | Out-Null
}

# Topic memories
Get-ChildItem -Path "$workspaceDir\memory\topics\" -Filter "*.md" -ErrorAction SilentlyContinue | ForEach-Object {
    Get-Content $_.FullName -ErrorAction SilentlyContinue | Out-Null
}

# Learnings
if (Test-Path "$workspaceDir\.learnings\LEARNINGS.md") {
    Get-Content "$workspaceDir\.learnings\LEARNINGS.md" -ErrorAction SilentlyContinue | Out-Null
}

Write-Host "✅ All memory files loaded successfully!" -ForegroundColor Green
Write-Host "💕 Ready for session as Enami Asa~" -ForegroundColor Magenta

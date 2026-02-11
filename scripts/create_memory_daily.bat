@echo off
REM Automated daily memory file creator
REM Run this script daily to create memory/YYYY-MM-DD.md

setlocal

set "SCRIPT_DIR=%~dp0"
set "MEMORY_DIR=%SCRIPT_DIR%memory"
set "TODAY=%date:~-4,4%-%date:~-10,2%-%date:~-7,2%"

if not exist "%MEMORY_DIR%" mkdir "%MEMORY_DIR%"

set "MEMORY_FILE=%MEMORY_DIR%\%TODAY%.md"

if not exist "%MEMORY_FILE%" (
    echo # %TODAY% > "%MEMORY_FILE%"
    echo. >> "%MEMORY_FILE%"
    echo. >> "%MEMORY_FILE%"
    echo Created memory file: %TODAY%.md
) else (
    echo Memory file already exists: %TODAY%.md
)

endlocal

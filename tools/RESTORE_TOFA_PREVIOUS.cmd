@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-TOFA-Unified.ps1" -Restore
if errorlevel 1 echo TO+FA restore failed. See error above.
pause

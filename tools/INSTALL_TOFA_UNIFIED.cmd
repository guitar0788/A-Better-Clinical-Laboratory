@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-TOFA-Unified.ps1"
if errorlevel 1 echo TO+FA combined test install failed. See error above.
pause

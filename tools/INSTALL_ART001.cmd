@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-ABCL-ART001.ps1"
if errorlevel 1 echo ART-001 installation did NOT complete. Read the message above.
pause

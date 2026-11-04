@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-ABCL-G1.ps1" -NativeLeadTest
if errorlevel 1 echo ABCL G1 R3 installation failed. Read the error above.
pause

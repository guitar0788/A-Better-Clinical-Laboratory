@echo off
setlocal
cd /d "%~dp0.."
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-TO004-Into-G1.ps1" %*
if errorlevel 1 (echo TO-004 installation stopped. No manual copying. & pause & exit /b 1)
echo TO-004 TEST ONLY installation completed.
pause
@echo off
setlocal
cd /d "%~dp0.."
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Uninstall-TO004-From-G1.ps1" %*
if errorlevel 1 (echo TO-004 removal stopped to protect files. & pause & exit /b 1)
echo TO-004 matching test-only files removed.
pause
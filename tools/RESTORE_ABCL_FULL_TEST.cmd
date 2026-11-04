@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-ABCL-Full-Test.ps1" -Restore
set "RC=%ERRORLEVEL%"
echo.
pause
exit /b %RC%

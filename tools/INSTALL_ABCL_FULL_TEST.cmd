@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-ABCL-Full-Test.ps1"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" echo ABCL install did not complete. No gameplay PASS is claimed.
echo.
pause
exit /b %RC%

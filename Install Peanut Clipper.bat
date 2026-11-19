@echo off
setlocal EnableExtensions
title Peanut Clipper - Install
set "ZIPURL=https://github.com/smearframestudios-svg/peanut-clipper/archive/refs/heads/main.zip"

rem Install next to this file if it's inside an existing Peanut Clipper folder, otherwise in Documents.
if exist "%~dp0.venv\Scripts\python.exe" (set "DEST=%~dp0") else if exist "%~dp0clipper\__main__.py" (set "DEST=%~dp0") else (set "DEST=%USERPROFILE%\Documents\PeanutClipper\")

echo.
echo  Peanut Clipper installer
echo  ------------------------
echo  Installing to: %DEST%
echo  Your settings, banners, layout, YouTube login and Shorts are kept.
echo.
if not exist "%DEST%" mkdir "%DEST%"

set "TMPZ=%TEMP%\peanut-clipper.zip"
set "TMPX=%TEMP%\peanut-clipper-x"
if exist "%TMPX%" rmdir /s /q "%TMPX%"
echo  [1/3] Downloading the latest version...
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol='Tls12'; $ProgressPreference='SilentlyContinue'; Invoke-WebRequest '%ZIPURL%' -OutFile '%TMPZ%'; Expand-Archive '%TMPZ%' '%TMPX%' -Force"
if errorlevel 1 (
  echo  [!] Download failed - check your internet connection and try again.
  pause
  exit /b 1
)
set "SRC="
for /d %%D in ("%TMPX%\*") do set "SRC=%%D"
if not defined SRC (
  echo  [!] The download was empty. Try again in a minute.
  pause
  exit /b 1
)
if exist "%DEST%clipper" rmdir /s /q "%DEST%clipper"
robocopy "%SRC%" "%DEST%." /E /NFL /NDL /NJH /NJS /NP >nul
rmdir /s /q "%TMPX%" 2>nul
del "%TMPZ%" 2>nul
if exist "%DEST%Peanut Clipper.bat" del "%DEST%Peanut Clipper.bat"

cd /d "%DEST%"
if exist ".venv\Scripts\python.exe" goto setup
echo  [2/3] Creating the app's Python folder...
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY (
  echo  [!] Python is not installed. Get it from https://www.python.org/downloads/
  echo      and tick "Add python.exe to PATH" on the first installer screen, then run this again.
  pause
  exit /b 1
)
%PY% -m venv .venv
if errorlevel 1 (
  echo  [!] Could not create the app's Python folder.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q --upgrade pip

:setup
echo  [3/3] Installing what the app needs (first time: 10-20 minutes, after that: seconds)...
set "VIRTUAL_ENV="
".venv\Scripts\python.exe" -m clipper install
if errorlevel 1 (
  echo.
  echo  [!] Setup hit a problem - send a screenshot of this window to Claude.
  pause
  exit /b 1
)
echo.
echo  Done! Use the "Peanut Clipper" icon on your Desktop or in the Start menu.
echo  Opening the app now...
start "" ".venv\Scripts\pythonw.exe" -m clipper launch
timeout /t 4 >nul

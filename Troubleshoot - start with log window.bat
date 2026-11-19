@echo off
title Peanut Clipper (log window)
cd /d "%~dp0"
echo Starting Peanut Clipper with a visible log. Close this window to quit.
".venv\Scripts\python.exe" -m clipper app
pause

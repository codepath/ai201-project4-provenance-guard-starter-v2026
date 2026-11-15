@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto local
if exist "..\ai201-project4-provenance-guard-starter-v2026\.venv\Scripts\python.exe" goto shared
if not exist ".venv\Scripts\python.exe" (
  echo First run: creating the Python environment and installing dependencies.
  py -3.13 -m venv .venv
  if errorlevel 1 goto failure
  ".venv\Scripts\python.exe" -m pip install -r requirements-capstone.txt
  if errorlevel 1 goto failure
)
:local
set "CAPSTONE_PYTHON=.venv\Scripts\python.exe"
goto run
:shared
set "CAPSTONE_PYTHON=..\ai201-project4-provenance-guard-starter-v2026\.venv\Scripts\python.exe"
:run
echo Open http://127.0.0.1:5050 in your browser.
start "" "http://127.0.0.1:5050"
"%CAPSTONE_PYTHON%" capstone.py
if errorlevel 1 goto failure
exit /b 0
:failure
echo Setup or startup failed. See RUNNING.md for troubleshooting.
pause
exit /b 1

@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo First run: creating the Python environment and installing dependencies.
  py -3.13 -m venv .venv
  if errorlevel 1 goto failure
  ".venv\Scripts\python.exe" -m pip install -r requirements-capstone.txt
  if errorlevel 1 goto failure
)
echo Open http://127.0.0.1:5050 in your browser.
start "" "http://127.0.0.1:5050"
".venv\Scripts\python.exe" capstone.py
if errorlevel 1 goto failure
exit /b 0
:failure
echo Setup or startup failed. See RUNNING.md for troubleshooting.
pause
exit /b 1

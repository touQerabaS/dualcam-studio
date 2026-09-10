@echo off
cd /d "%~dp0"
if exist "dist-preview\DualCam Studio\DualCam Studio.exe" (
  start "" "dist-preview\DualCam Studio\DualCam Studio.exe"
  exit /b
)
if exist "dist-fixed\DualCam Studio\DualCam Studio.exe" (
  start "" "dist-fixed\DualCam Studio\DualCam Studio.exe"
  exit /b
)
if exist "dist\DualCam Studio\DualCam Studio.exe" (
  start "" "dist\DualCam Studio\DualCam Studio.exe"
  exit /b
)
if exist ".venv\Scripts\pythonw.exe" (
  start "" ".venv\Scripts\pythonw.exe" "app.py"
  exit /b
)
echo Install Python 3.11, 3.12 or 3.13, then follow README.md.
pause

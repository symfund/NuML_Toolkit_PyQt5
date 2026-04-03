@echo off
:: Ensure the script runs from the folder where it is located
set SCRIPT_DIR=%~dp0
cd /d "%~dp0"
setlocal enabledelayedexpansion

:: 1. Find the official Miniforge Shortcut
set "SC_USER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Miniforge3\Miniforge Prompt.lnk"
set "SC_SYSTEM=%ProgramData%\Microsoft\Windows\Start Menu\Programs\Miniforge3\Miniforge Prompt.lnk"

if exist "%SC_USER%" (set "SC=%SC_USER%") else if exist "%SC_SYSTEM%" (set "SC=%SC_SYSTEM%")

if not defined SC (
    echo [ERROR] Miniforge not found. Please install Miniforge3 first.
    pause & exit /b
)

:: 2. Extract the Root Path from the Shortcut's last argument
for /f "delims=" %%A in ('powershell -NoProfile -Command "(New-Object -ComObject WScript.Shell).CreateShortcut('%SC%').Arguments"') do set "ARGS=%%A"
for %%B in (%ARGS%) do set "MINIFORGE_ROOT=%%~B"

:: 3. Setup paths for your specific environment
set "ENV_NAME=numl_toolkit"
set "ENV_PATH=%MINIFORGE_ROOT%/envs/%ENV_NAME%"
set PATH=%ENV_PATH%;%ENV_PATH%/Scripts;%SCRIPT_DIR%;%PATH%
set "PYTHON_EXE=%ENV_PATH%/python.exe"

:: 4. Launch the application
%PYTHON_EXE% numl_toolkit_pyqt5.py

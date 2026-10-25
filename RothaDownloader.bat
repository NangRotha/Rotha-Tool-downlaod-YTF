@echo off
title RothaDownloader - 4K & 1080p Video Downloader
chcp 65001 > nul
cd /d "%~dp0"

:: 1. Detect Python
set "PY_CMD="

:: Test system python
python -c "import sys; sys.exit(0)" >nul 2>nul
if %errorlevel% equ 0 set "PY_CMD=python"

:: Test py launcher
if "%PY_CMD%"=="" (
    py -3 -c "import sys; sys.exit(0)" >nul 2>nul
    if %errorlevel% equ 0 set "PY_CMD=py -3"
)

:: Search known locations
if "%PY_CMD%"=="" (
    for %%P in (
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
        "%ProgramFiles%\Python312\python.exe"
        "%ProgramFiles%\Python311\python.exe"
        "%ProgramFiles%\Python310\python.exe"
        "%ProgramFiles(x86)%\Python311\python.exe"
        "C:\Python312\python.exe"
        "C:\Python311\python.exe"
        "C:\Python310\python.exe"
        "%~dp0python\python.exe"
    ) do (
        if exist "%%~P" (
            "%%~P" -c "import sys; sys.exit(0)" >nul 2>nul
            if %errorlevel% equ 0 (
                set "PY_CMD="%%~P""
                goto :py_ready
            )
        )
    )
)

:py_ready
if "%PY_CMD%"=="" (
    echo ======================================================================
    echo [!] Python is not yet configured on this computer.
    echo កំពុងបើកកម្មវិធី Install_RothaDownloader.bat ដើម្បីរៀបចំដោយស្វ័យប្រវត្តិ...
    echo ======================================================================
    echo.
    call "%~dp0Install_RothaDownloader.bat"
    exit /b
)

:: 2. Check if server is already running on port 5005
curl -s -m 1 http://localhost:5005/api/status >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Starting RothaDownloader Background Server...
    start /b "" %PY_CMD% "%~dp0server.py"
    timeout /t 2 /nobreak >nul
)

set APP_URL=http://localhost:5005
set DATA_DIR=%LOCALAPPDATA%\RothaDownloader\Data

:: 3. Launch in App Window Mode (Chrome or Edge)
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app="%APP_URL%" --user-data-dir="%DATA_DIR%" --window-size=1260,880
) else if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" --app="%APP_URL%" --user-data-dir="%DATA_DIR%" --window-size=1260,880
) else if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" --app="%APP_URL%" --user-data-dir="%DATA_DIR%" --window-size=1260,880
) else if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app="%APP_URL%" --user-data-dir="%DATA_DIR%" --window-size=1260,880
) else (
    start "" "%APP_URL%"
)

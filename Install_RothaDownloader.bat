@echo off
title RothaDownloader - Windows One-Click Installer Wizard
chcp 65001 > nul
cd /d "%~dp0"

echo ======================================================================
echo    👑 ROTHA DOWNLOADER - WINDOWS ONE-CLICK INSTALLER
echo    YouTube, TikTok, Facebook 4K & 1080p Downloader & Video Studio
echo ======================================================================
echo.
echo កំពុងចាប់ផ្ដើមដំឡើង RothaDownloader សម្រាប់ Windows...
echo Installing RothaDownloader on your Windows PC...
echo.

:: 0. Check if user extracted the ZIP file
if not exist "%~dp0server.py" (
    echo [ERROR] រកមិនឃើញ server.py នៅក្នុងថតនេះទេ!
    echo [ERROR] server.py not found in the current folder!
    echo.
    echo ⚠️ សូមប្រាកដថាអ្នកបានពន្លា (Extract / Unzip) File RothaDownloader-Windows.zip
    echo    រួចទើបបើកដំណើរការ Install_RothaDownloader.bat នៅក្នុង Folder ដែលបាន Extract!
    echo.
    pause
    exit /b 1
)

:: 1. Detect or Auto-Install Python
echo [1/4] កំពុងពិនិត្យមើល Python (Checking Python environment)...

set "PY_CMD="

:: Test system python
python -c "import sys; sys.exit(0)" >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_CMD=python"
)

:: Test py launcher
if "%PY_CMD%"=="" (
    py -3 -c "import sys; sys.exit(0)" >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY_CMD=py -3"
    )
)

:: Search known installation directories
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
                goto :found_python
            )
        )
    )
)

:: If Python is still missing, auto-download official Python 3.11 installer silently
if "%PY_CMD%"=="" (
    echo.
    echo [!] រកមិនឃើញ Python នៅលើកុំព្យូទ័ររបស់អ្នកទេ។
    echo [!] Python was not found. Automatically downloading and installing official Python 3.11...
    echo     (ដំណើរការនេះចំណាយពេលប្រហែល 30-60 វិនាទីប៉ុណ្ណោះ សូមរង់ចាំ...)
    echo.
    powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $installer = Join-Path $env:TEMP 'python_setup_311.exe'; Write-Host '  -> Downloading Python 3.11 from python.org...'; (New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe', $installer); Write-Host '  -> Installing Python silently...'; Start-Process $installer -ArgumentList '/quiet InstallAllUsers=0 PrependPath=1 Include_test=0' -Wait; Remove-Item $installer -Force -ErrorAction SilentlyContinue"
    
    if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
        set "PY_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe""
    ) else (
        where winget >nul 2>nul
        if %errorlevel% equ 0 (
            echo   -> Trying winget fallback...
            winget install -e --id Python.Python.3.11 --scope currentuser --accept-package-agreements --accept-source-agreements
            if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
                set "PY_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe""
            )
        )
    )
)

:found_python
if "%PY_CMD%"=="" (
    echo.
    echo ❌ មិនអាចដំឡើង Python ដោយស្វ័យប្រវត្តិបានទេ។
    echo សូមទាញយក និងដំឡើង Python ដោយខ្លួនឯងពី: https://www.python.org/downloads/
    echo ⚠️ សំខាន់បំផុត: សូមប្រាកដថាបានធីក [✓] "Add Python to PATH" នៅពេល Install!
    echo.
    pause
    exit /b 1
)
echo [OK] Python រួចរាល់: %PY_CMD%

:: 2. Ensure standalone yt-dlp binary exists in bin/
echo.
echo [2/4] កំពុងពិនិត្យមើល yt-dlp Engine (Checking yt-dlp Engine)...
if not exist "%~dp0bin" mkdir "%~dp0bin"

if exist "%~dp0bin\yt-dlp.exe" (
    echo [OK] Standalone bin\yt-dlp.exe រួចរាល់!
) else (
    echo [!] កំពុងទាញយក standalone yt-dlp.exe ពី GitHub Releases...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', '%~dp0bin\yt-dlp.exe')"
    if exist "%~dp0bin\yt-dlp.exe" (
        echo [OK] yt-dlp.exe ទាញយកបានជោគជ័យ!
    ) else (
        echo [!] Fallback: Installing yt-dlp via pip...
        %PY_CMD% -m pip install --upgrade yt-dlp
    )
)

:: 3. Ensure FFmpeg exists in bin/ or in system PATH
echo.
echo [3/4] កំពុងពិនិត្យមើល FFmpeg (Checking FFmpeg for 1080p & 4K)...
where ffmpeg >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] FFmpeg រួចរាល់នៅក្នុង System PATH!
) else if exist "%~dp0bin\ffmpeg.exe" (
    echo [OK] Standalone bin\ffmpeg.exe រួចរាល់!
) else (
    echo [!] កំពុងដំឡើង FFmpeg ដោយស្វ័យប្រវត្តិ...
    where winget >nul 2>nul
    if %errorlevel% equ 0 (
        winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements
    )
    where ffmpeg >nul 2>nul
    if %errorlevel% neq 0 (
        if not exist "%~dp0bin\ffmpeg.exe" (
            echo   -> Downloading FFmpeg standalone builds...
            powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ffzip = Join-Path $env:TEMP 'ffmpeg_win.zip'; $ffdest = Join-Path $env:TEMP 'ffmpeg_ext'; (New-Object System.Net.WebClient).DownloadFile('https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip', $ffzip); Expand-Archive -Path $ffzip -DestinationPath $ffdest -Force; Copy-Item (Join-Path $ffdest '*\bin\*.exe') -Destination '%~dp0bin\' -Force; Remove-Item $ffzip, $ffdest -Recurse -Force -ErrorAction SilentlyContinue"
        )
    )
    if exist "%~dp0bin\ffmpeg.exe" (
        echo [OK] FFmpeg ដំឡើងបានជោគជ័យ!
    )
)

:: 4. Create Desktop & Start Menu Shortcuts with RothaDownloader Icon
echo.
echo [4/4] កំពុងបង្កើត Desktop & Start Menu Shortcuts (Creating Shortcuts)...
set "TARGET_BAT=%~dp0RothaDownloader.bat"
set "ICON_FILE=%~dp0RothaDownloader.ico"
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\RothaDownloader.lnk"
set "STARTMENU_SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\RothaDownloader.lnk"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $d = $ws.CreateShortcut('%DESKTOP_SHORTCUT%'); $d.TargetPath = '%TARGET_BAT%'; $d.WorkingDirectory = '%~dp0'; if (Test-Path '%ICON_FILE%') { $d.IconLocation = '%ICON_FILE%' }; $d.Description = 'RothaDownloader - 4K & 1080p Video Downloader'; $d.Save(); $m = $ws.CreateShortcut('%STARTMENU_SHORTCUT%'); $m.TargetPath = '%TARGET_BAT%'; $m.WorkingDirectory = '%~dp0'; if (Test-Path '%ICON_FILE%') { $m.IconLocation = '%ICON_FILE%' }; $m.Description = 'RothaDownloader - 4K & 1080p Video Downloader'; $m.Save()"

echo.
echo ======================================================================
echo 🎉 ✅ ដំឡើងបានជោគជ័យ ១០០%! (Installation Completed Successfully!)
echo ======================================================================
echo.
echo 📍 Shortcut ត្រូវបានបង្កើតនៅលើ Desktop: RothaDownloader
echo 🚀 អ្នកអាចបើកដំណើរការកម្មវិធីដោយគ្រាន់តែ Double-click លើ Desktop Shortcut!
echo.
set /p START_NOW="តើអ្នកចង់បើកកម្មវិធីឥឡូវនេះទេ? / Start RothaDownloader now? (Y/N): "
if /i "%START_NOW%"=="Y" (
    start "" "%TARGET_BAT%"
)

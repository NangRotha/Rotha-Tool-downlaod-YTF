# ==============================================================================
# RothaDownloader - Windows PowerShell Installer
# Run: powershell -ExecutionPolicy Bypass -File .\install_windows.ps1
# ==============================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "    👑 ROTHA DOWNLOADER - WINDOWS INSTALLER (PowerShell)" -ForegroundColor Yellow
Write-Host "    YouTube, TikTok, Facebook 4K & 1080p Downloader" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $CurrentDir

# 1. Check Python
Write-Host "[1/4] កំពុងពិនិត្យមើល Python (Checking Python)..." -ForegroundColor White
$PythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonCmd = "py"
} else {
    Write-Host "[!] រកមិនឃើញ Python ទេ។ កំពុងដំឡើង Python តាមរយៈ WinGet..." -ForegroundColor Yellow
    winget install -e --id Python.Python.3.11 --scope currentuser --accept-package-agreements --accept-source-agreements
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $PythonCmd = "python"
    } else {
        Write-Host "[X] សូមទាញយក និងដំឡើង Python ពី https://www.python.org/downloads/ ដោយធីកយក 'Add Python to PATH'." -ForegroundColor Red
        Read-Host "ចុច Enter ដើម្បីចាកចេញ..."
        exit 1
    }
}
Write-Host "[OK] Python រួចរាល់: $PythonCmd" -ForegroundColor Green

# 2. Upgrade yt-dlp
Write-Host "`n[2/4] កំពុងដំឡើង / អាប់ដេត yt-dlp (Installing yt-dlp)..." -ForegroundColor White
& $PythonCmd -m pip install --upgrade yt-dlp

# 3. Check FFmpeg
Write-Host "`n[3/4] កំពុងពិនិត្យមើល FFmpeg (Checking FFmpeg)..." -ForegroundColor White
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "[!] កំពុងដំឡើង FFmpeg តាមរយៈ WinGet..." -ForegroundColor Yellow
    winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements
} else {
    Write-Host "[OK] FFmpeg រួចរាល់!" -ForegroundColor Green
}

# 4. Create Desktop & Start Menu Shortcuts
Write-Host "`n[4/4] កំពុងបង្កើត Shortcuts (Desktop & Start Menu)..." -ForegroundColor White
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$StartMenuPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('ApplicationData'), "Microsoft\Windows\Start Menu\Programs")
$TargetBat = Join-Path $CurrentDir "RothaDownloader.bat"
$IconFile = Join-Path $CurrentDir "RothaDownloader.ico"

# Desktop Shortcut
$DesktopShortcut = $WshShell.CreateShortcut((Join-Path $DesktopPath "RothaDownloader.lnk"))
$DesktopShortcut.TargetPath = $TargetBat
$DesktopShortcut.WorkingDirectory = $CurrentDir
$DesktopShortcut.Description = "RothaDownloader - 4K & 1080p Downloader"
if (Test-Path $IconFile) {
    $DesktopShortcut.IconLocation = $IconFile
}
$DesktopShortcut.Save()

# Start Menu Shortcut
$StartMenuShortcut = $WshShell.CreateShortcut((Join-Path $StartMenuPath "RothaDownloader.lnk"))
$StartMenuShortcut.TargetPath = $TargetBat
$StartMenuShortcut.WorkingDirectory = $CurrentDir
$StartMenuShortcut.Description = "RothaDownloader - 4K & 1080p Downloader"
if (Test-Path $IconFile) {
    $StartMenuShortcut.IconLocation = $IconFile
}
$StartMenuShortcut.Save()

Write-Host "`n======================================================================" -ForegroundColor Green
Write-Host "🎉 ✅ ដំឡើងបានជោគជ័យ ១០០%! (Installation Completed Successfully!)" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "`n📍 Shortcut ត្រូវបានបង្កើតនៅលើ Desktop: $ShortcutPath"
Write-Host "🚀 អ្នកអាចបើកដំណើរការដោយគ្រាន់តែ Double-click លើ Desktop Shortcut!`n"

$Ans = Read-Host "តើអ្នកចង់បើកកម្មវិធីឥឡូវនេះទេ? / Start RothaDownloader now? (Y/N)"
if ($Ans -eq "Y" -or $Ans -eq "y") {
    Start-Process $TargetBat
}

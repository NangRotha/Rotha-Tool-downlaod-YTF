#!/bin/bash
# ==============================================================================
# RothaDownloader - One-Click Installer for macOS
# Automatically installs RothaDownloader.app into /Applications
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_NAME="RothaDownloader.app"
SOURCE_APP="$DIR/$APP_NAME"
TARGET_DIR="/Applications"
TARGET_APP="$TARGET_DIR/$APP_NAME"

clear
echo "======================================================================"
echo "    👑 ROTHA DOWNLOADER - MAC INSTALLATION WIZARD"
echo "    YouTube, TikTok, Facebook 4K & 1080p Downloader for Mac"
echo "======================================================================"
echo ""
echo "កំពុងដំឡើង RothaDownloader ទៅកាន់ /Applications..."
echo "Installing RothaDownloader to /Applications..."
echo ""

# 1. Close any running instance cleanly
pkill -f "server.py" > /dev/null 2>&1 || true

# 2. Check source
if [ ! -d "$SOURCE_APP" ]; then
    echo "❌ Error: Could not locate $SOURCE_APP."
    echo "សូមប្រាកដថា file RothaDownloader.app ស្ថិតនៅក្នុង folder តែមួយជាមួយ Installer នេះ។"
    read -n 1 -s -r -p "ចុច key ណាមួយដើម្បីចាកចេញ (Press any key to exit)..."
    echo ""
    exit 1
fi

# 3. Copy to /Applications
echo "📦 1/3: កំពុងចម្លងកម្មវិធីទៅកាន់ /Applications..."
rm -rf "$TARGET_APP"
cp -R "$SOURCE_APP" "$TARGET_DIR/"

# 4. Remove macOS Quarantine flag (Gatekeeper protection bypass)
echo "🛡️ 2/3: កែសម្រួលសិទ្ធិ macOS Gatekeeper Security Permissions..."
xattr -cr "$TARGET_APP" 2>/dev/null || true
chmod +x "$TARGET_APP/Contents/MacOS/RothaDownloader"
chmod +x "$TARGET_APP/Contents/Resources/server.py"
chmod +x "$TARGET_APP/Contents/Resources/bin/yt-dlp" 2>/dev/null || true

# 5. Register with macOS LaunchServices to immediately display the golden App Icon in Dock & Launchpad
touch "$TARGET_APP" 2>/dev/null || true
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "$TARGET_APP" 2>/dev/null || true

echo ""
echo "======================================================================"
echo "🎉 ✅ ដំឡើងបានជោគជ័យ 100%! (Installation Completed Successfully!)"
echo "======================================================================"
echo ""
echo "📍 ទីតាំងកម្មវិធី (Location): /Applications/RothaDownloader.app"
echo "🚀 អ្នកអាចបើកកម្មវិធីបានយ៉ាងងាយស្រួលតាមរយៈ:"
echo "   1. Finder > Applications > RothaDownloader"
echo "   2. Launchpad > RothaDownloader"
echo "   3. Spotlight Search (Cmd + Space) > វាយ 'RothaDownloader'"
echo ""
echo "កំពុងបើកកម្មវិធី RothaDownloader ឥឡូវនេះ..."
open "$TARGET_APP"
echo ""

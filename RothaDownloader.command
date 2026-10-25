#!/bin/bash
# ==============================================================================
# RothaDownloader - Double-click Launcher for macOS
# Automatically launches the native Cocoa RothaDownloader.app with Dock Icon
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -d "$DIR/RothaDownloader.app" ]; then
    echo "🚀 Starting native RothaDownloader macOS App..."
    open "$DIR/RothaDownloader.app"
elif [ -d "/Applications/RothaDownloader.app" ]; then
    echo "🚀 Starting RothaDownloader from /Applications..."
    open "/Applications/RothaDownloader.app"
else
    echo "🚀 Starting RothaDownloader Server..."
    export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
    cd "$DIR"
    python3 "$DIR/server.py"
fi

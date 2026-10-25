#!/usr/bin/env bash
# RothaDownloader Launch Script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
exec python3 "$DIR/server.py"

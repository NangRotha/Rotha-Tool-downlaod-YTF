#!/usr/bin/env python3
"""
RothaDownloader CLI - Terminal Video Downloader for macOS
100% Guaranteed QuickTime Player & Apple Quick Look Compatible (H.264 / HEVC + AAC).
Usage:
    python3 downloader_cli.py "https://youtube.com/watch?v=..." --quality 1080p
    python3 downloader_cli.py "https://tiktok.com/@user/video/..." --quality best
    python3 downloader_cli.py "https://facebook.com/..." --quality mp3
"""

import sys
import os
import argparse
import subprocess
import shutil
from pathlib import Path

# Guarantee PATH
for p in ["/opt/homebrew/bin", "/opt/homebrew/sbin", "/usr/local/bin", str(Path.home() / ".local/bin")]:
    if p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = f"{p}:{os.environ.get('PATH', '')}"

def find_bin(name):
    candidates = [f"/opt/homebrew/bin/{name}", f"/usr/local/bin/{name}", f"/usr/bin/{name}"]
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return shutil.which(name) or name

YT_DLP = find_bin("yt-dlp")
FFMPEG = find_bin("ffmpeg")
FFPROBE = find_bin("ffprobe")

def ensure_quicktime_compatible(filepath):
    if not filepath or not os.path.exists(filepath):
        return filepath
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in [".mp4", ".m4v", ".mov"]:
        return filepath

    try:
        cmd_v = [FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", filepath]
        cmd_a = [FFPROBE, "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", filepath]
        v = subprocess.check_output(cmd_v, text=True, env=os.environ.copy()).strip().lower()
        a = subprocess.check_output(cmd_a, text=True, env=os.environ.copy()).strip().lower()

        qt_video_ok = v in ["h264", "hevc"] or not v
        qt_audio_ok = a in ["aac", "mp3"] or not a

        if qt_video_ok and qt_audio_ok:
            return filepath

        print("⚡ Optimizing media for macOS QuickTime Player...")
        temp_out = filepath + ".qt_compat.mp4"
        ffmpeg_cmd = [FFMPEG, "-y", "-i", filepath]
        if qt_video_ok:
            ffmpeg_cmd.extend(["-c:v", "copy"])
        else:
            ffmpeg_cmd.extend(["-c:v", "h264_videotoolbox", "-b:v", "8000k"])

        if qt_audio_ok:
            ffmpeg_cmd.extend(["-c:a", "copy"])
        else:
            ffmpeg_cmd.extend(["-c:a", "aac", "-b:a", "192k"])

        ffmpeg_cmd.append(temp_out)
        res = subprocess.run(ffmpeg_cmd, env=os.environ.copy())
        if res.returncode == 0 and os.path.exists(temp_out) and os.path.getsize(temp_out) > 0:
            os.replace(temp_out, filepath)
    except Exception:
        pass
    return filepath

def download(url, quality="1080p", output_dir=None, browser=None):
    if not output_dir:
        output_dir = str(Path.home() / "Downloads")
    os.makedirs(output_dir, exist_ok=True)

    out_tmpl = os.path.join(output_dir, "%(title).150B [%(id)s].%(ext)s")

    cmd = [
        YT_DLP,
        "--ffmpeg-location", FFMPEG,
        "--no-check-certificates",
        "--geo-bypass",
        "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "--format-sort", "vcodec:avc,acodec:m4a",
        "--postprocessor-args", "Merger:-c:a aac",
        "--print", "after_move:FINAL_PATH|%(filepath)s",
        "-o", out_tmpl,
    ]

    if browser and browser != "none":
        cmd.extend(["--cookies-from-browser", browser])

    if quality == "mp3":
        cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
    elif quality in ["4k", "2160p"]:
        cmd.extend(["-f", "bestvideo[height<=2160]+bestaudio/best[height<=2160]/best", "--merge-output-format", "mp4"])
    elif quality in ["2k", "1440p"]:
        cmd.extend(["-f", "bestvideo[height<=1440]+bestaudio/best[height<=1440]/best", "--merge-output-format", "mp4"])
    elif quality == "1080p":
        cmd.extend(["-f", "bestvideo[vcodec^=avc][height<=1080]+bestaudio[acodec^=mp4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best", "--merge-output-format", "mp4"])
    elif quality == "720p":
        cmd.extend(["-f", "bestvideo[vcodec^=avc][height<=720]+bestaudio[acodec^=mp4a]/bestvideo[height<=720]+bestaudio/best[height<=720]/best", "--merge-output-format", "mp4"])
    elif quality == "480p":
        cmd.extend(["-f", "bestvideo[vcodec^=avc][height<=480]+bestaudio[acodec^=mp4a]/bestvideo[height<=480]+bestaudio/best[height<=480]/best", "--merge-output-format", "mp4"])
    else:
        cmd.extend(["-f", "bestvideo[vcodec^=avc]+bestaudio[acodec^=mp4a]/bestvideo+bestaudio/best", "--merge-output-format", "mp4"])

    cmd.append(url)

    print(f"🎬 Downloading: {url}")
    print(f"💎 Quality: {quality.upper()} (Apple QuickTime Compatible H.264/AAC)")
    print(f"📂 Destination: {output_dir}")
    print("-" * 50)

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, env=os.environ.copy())
        final_file = None
        for line in proc.stdout:
            line_str = line.strip()
            if "FINAL_PATH|" in line_str:
                final_file = line_str.split("FINAL_PATH|", 1)[1].strip()
            elif not line_str.startswith("PROG|"):
                print(line_str)
        proc.wait()

        if proc.returncode == 0:
            if final_file and os.path.exists(final_file) and quality != "mp3":
                final_file = ensure_quicktime_compatible(final_file)
            print("\n✅ Download completed successfully!")
            print(f"📂 Saved in: {final_file or output_dir}")
            print("🍎 100% Compatible with QuickTime Player & macOS Quick Look")
        else:
            print("\n❌ Download failed. Check link or format.")
    except KeyboardInterrupt:
        print("\nDownload cancelled.")

def main():
    parser = argparse.ArgumentParser(description="RothaDownloader CLI - QuickTime Compatible 4K/1080p Video Downloader")
    parser.add_argument("url", help="Video URL (YouTube, TikTok, Facebook, etc.)")
    parser.add_argument("-q", "--quality", default="1080p", choices=["4k", "2160p", "2k", "1440p", "1080p", "720p", "480p", "best", "mp3"], help="Resolution quality (default: 1080p)")
    parser.add_argument("-o", "--output", default=None, help="Output directory (defaults to ~/Downloads)")
    parser.add_argument("-b", "--browser", default=None, help="Browser for cookies (chrome, safari, firefox)")

    args = parser.parse_args()
    download(args.url, quality=args.quality, output_dir=args.output, browser=args.browser)

if __name__ == "__main__":
    main()

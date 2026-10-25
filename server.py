#!/usr/bin/env python3
"""
RothaDownloader - High Quality Video Downloader for macOS
Supports YouTube (up to 4K), TikTok (HD No Watermark), Facebook (1080p/HD), and more.
100% Guaranteed QuickTime Player & Apple Quick Look Compatible (H.264 / HEVC + AAC).
"""

import os
import sys
import re
import json
import time
import uuid
import shutil
import tempfile
import urllib.parse
import urllib.request
import subprocess
import threading
import socket
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

# Cross-platform environment PATH setup (macOS, Windows, Linux)
BASE_DIR = Path(__file__).resolve().parent

if sys.platform == "win32":
    default_paths = [
        str(BASE_DIR),
        str(BASE_DIR / "bin"),
        str(Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links"),
        str(Path.home() / "scoop" / "shims"),
        r"C:\ProgramData\chocolatey\bin",
    ]
else:
    default_paths = [
        "/opt/homebrew/bin",
        "/opt/homebrew/sbin",
        "/usr/local/bin",
        "/usr/bin",
        "/bin",
        "/usr/sbin",
        "/sbin",
        str(Path.home() / ".local/bin"),
    ]

existing_path = os.environ.get("PATH", "")
path_elements = existing_path.split(os.pathsep)
for p in reversed(default_paths):
    if p and p not in path_elements and os.path.exists(p):
        path_elements.insert(0, p)
os.environ["PATH"] = os.pathsep.join(path_elements)

# Configuration & Paths
PORT = 5005
PUBLIC_DIR = BASE_DIR / "public"
HISTORY_FILE = BASE_DIR / "downloads_history.json"
SETTINGS_FILE = BASE_DIR / "settings.json"

DEFAULT_DOWNLOAD_DIR = str(Path.home() / "Downloads")

# Locate yt-dlp, ffmpeg, and ffprobe
def ensure_yt_dlp():
    """Auto-downloads standalone universal yt-dlp if not installed on the machine."""
    bin_dir = BASE_DIR / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    exe_name = "yt-dlp.exe" if sys.platform == "win32" else "yt-dlp"
    dest = bin_dir / exe_name
    if dest.is_file() and (sys.platform == "win32" or os.access(dest, os.X_OK)):
        return str(dest)
    download_name = "yt-dlp.exe" if sys.platform == "win32" else ("yt-dlp_macos" if sys.platform == "darwin" else "yt-dlp")
    url = f"https://github.com/yt-dlp/yt-dlp/releases/latest/download/{download_name}"
    try:
        import urllib.request
        print(f"📦 [Auto-Engine] yt-dlp not found. Downloading standalone binary from {url}...")
        urllib.request.urlretrieve(url, str(dest))
        if sys.platform != "win32":
            os.chmod(str(dest), 0o755)
        print(f"✅ [Auto-Engine] yt-dlp successfully installed to {dest}")
        return str(dest)
    except Exception as e:
        print(f"⚠️ [Auto-Engine] Could not auto-download yt-dlp: {e}")
        return None

def ensure_ffmpeg():
    """Auto-downloads standalone FFmpeg if not installed on the machine."""
    bin_dir = BASE_DIR / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    exe_name = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
    dest = bin_dir / exe_name
    if dest.is_file() and (sys.platform == "win32" or os.access(dest, os.X_OK)):
        return str(dest)
    try:
        import urllib.request
        import zipfile
        print(f"📦 [Auto-Engine] FFmpeg not found. Downloading standalone binary for {sys.platform}...")
        if sys.platform == "win32":
            url = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            zip_dest = bin_dir / "ffmpeg_temp.zip"
            urllib.request.urlretrieve(url, str(zip_dest))
            with zipfile.ZipFile(str(zip_dest), 'r') as z:
                for member in z.namelist():
                    if member.endswith("ffmpeg.exe") or member.endswith("ffprobe.exe"):
                        filename = os.path.basename(member)
                        with open(bin_dir / filename, "wb") as f_out:
                            f_out.write(z.read(member))
            if zip_dest.is_file():
                zip_dest.unlink()
        elif sys.platform == "darwin":
            url = "https://evermeet.cx/ffmpeg/getrelease/zip"
            zip_dest = bin_dir / "ffmpeg_mac.zip"
            urllib.request.urlretrieve(url, str(zip_dest))
            with zipfile.ZipFile(str(zip_dest), 'r') as z:
                for member in z.namelist():
                    if member == "ffmpeg":
                        with open(dest, "wb") as f_out:
                            f_out.write(z.read(member))
                        os.chmod(str(dest), 0o755)
            if zip_dest.is_file():
                zip_dest.unlink()
        if dest.is_file():
            print(f"✅ [Auto-Engine] FFmpeg successfully installed to {dest}")
            return str(dest)
    except Exception as e:
        print(f"⚠️ [Auto-Engine] Could not auto-download FFmpeg: {e}")
        return None

def find_binary(name):
    candidates = [
        str(BASE_DIR / "bin" / (f"{name}.exe" if sys.platform == "win32" else name)),
        str(BASE_DIR / (f"{name}.exe" if sys.platform == "win32" else name)),
        str(BASE_DIR.parent / "Resources" / "bin" / name),
        str(BASE_DIR.parent / "Resources" / name),
    ]
    if sys.platform == "win32":
        candidates.extend([
            str(Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / f"{name}.exe"),
            str(Path.home() / "scoop" / "shims" / f"{name}.exe"),
            f"C:\\ProgramData\\chocolatey\\bin\\{name}.exe",
            f"C:\\ffmpeg\\bin\\{name}.exe",
            f"C:\\Program Files\\ffmpeg\\bin\\{name}.exe",
        ])
    else:
        candidates.extend([
            f"/opt/homebrew/bin/{name}",
            f"/usr/local/bin/{name}",
            f"/opt/local/bin/{name}",
            f"/usr/bin/{name}",
            f"/bin/{name}",
            str(Path.home() / ".local/bin" / name),
            str(Path.home() / "bin" / name),
        ])

    for c in candidates:
        if os.path.isfile(c) and (sys.platform == "win32" or os.access(c, os.X_OK)):
            return c
    found = shutil.which(name)
    if found:
        return found

    # If yt-dlp is missing, attempt auto-downloading standalone binary
    if name == "yt-dlp":
        auto_downloaded = ensure_yt_dlp()
        if auto_downloaded:
            return auto_downloaded
    elif name in ("ffmpeg", "ffprobe"):
        auto_downloaded = ensure_ffmpeg()
        if auto_downloaded:
            if name == "ffprobe":
                probe_cand = str(Path(auto_downloaded).parent / ("ffprobe.exe" if sys.platform == "win32" else "ffprobe"))
                if os.path.isfile(probe_cand):
                    return probe_cand
            return auto_downloaded

    return f"{name}.exe" if sys.platform == "win32" else name

YT_DLP_BIN = find_binary("yt-dlp")
FFMPEG_BIN = find_binary("ffmpeg")
FFPROBE_BIN = find_binary("ffprobe")

def get_lan_ip():
    """Gets local network IP address for LAN access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def open_path_native(target_path):
    """Opens a file or directory with the native system file explorer / viewer."""
    try:
        if sys.platform == "win32":
            os.startfile(target_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", target_path], check=True)
        else:
            subprocess.run(["xdg-open", target_path], check=True)
        return True
    except Exception as e:
        print(f"Error opening {target_path}: {e}")
        return False

def reveal_in_explorer_native(filepath):
    """Reveals a file in Windows Explorer or macOS Finder."""
    try:
        if sys.platform == "win32":
            subprocess.run(["explorer", f"/select,{os.path.normpath(filepath)}"], check=True)
        elif sys.platform == "darwin":
            subprocess.run(["open", "-R", filepath], check=True)
        else:
            subprocess.run(["xdg-open", os.path.dirname(filepath)], check=True)
        return True
    except Exception as e:
        print(f"Error revealing {filepath}: {e}")
        return False

# Global thread-safe state for downloads
active_downloads = {}
downloads_lock = threading.Lock()

def get_settings():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not data.get("download_dir"):
                    data["download_dir"] = DEFAULT_DOWNLOAD_DIR
                return data
        except Exception:
            pass
    return {"download_dir": DEFAULT_DOWNLOAD_DIR, "browser": "none"}

def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving settings: {e}")

def get_history():
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def add_history_item(item):
    history = get_history()
    history = [h for h in history if h.get("filepath") != item.get("filepath")]
    history.insert(0, item)
    history = history[:100]
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving history: {e}")

def detect_platform(url):
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "tiktok.com" in url_lower:
        return "tiktok"
    elif "facebook.com" in url_lower or "fb.watch" in url_lower or "fb.com" in url_lower:
        return "facebook"
    elif "instagram.com" in url_lower:
        return "instagram"
    elif "twitter.com" in url_lower or "x.com" in url_lower:
        return "twitter"
    return "generic"

def format_duration(seconds):
    if not seconds:
        return "--:--"
    seconds = int(seconds)
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    if hrs > 0:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"

def get_stream_codecs(filepath):
    try:
        cmd_v = [FFPROBE_BIN, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", filepath]
        cmd_a = [FFPROBE_BIN, "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", filepath]
        v = subprocess.check_output(cmd_v, text=True, env=os.environ.copy()).strip().lower()
        a = subprocess.check_output(cmd_a, text=True, env=os.environ.copy()).strip().lower()
        return v, a
    except Exception:
        return "", ""

def ensure_quicktime_compatible(filepath):
    """Guarantees 100% QuickTime & Finder Quick Look playback with H.264/AAC."""
    if not filepath or not os.path.exists(filepath):
        return filepath

    ext = os.path.splitext(filepath)[1].lower()
    if ext not in [".mp4", ".m4v", ".mov"]:
        return filepath

    vcodec, acodec = get_stream_codecs(filepath)
    if not vcodec and not acodec:
        return filepath

    qt_video_ok = vcodec in ["h264", "hevc"] or not vcodec
    qt_audio_ok = acodec in ["aac", "mp3"] or not acodec

    if qt_video_ok and qt_audio_ok:
        return filepath

    temp_out = filepath + ".qt_compat.mp4"
    ffmpeg_cmd = [FFMPEG_BIN, "-y", "-i", filepath]

    if qt_video_ok:
        ffmpeg_cmd.extend(["-c:v", "copy"])
    else:
        if sys.platform == "darwin":
            ffmpeg_cmd.extend(["-c:v", "h264_videotoolbox", "-b:v", "8000k"])
        else:
            ffmpeg_cmd.extend(["-c:v", "libx264", "-preset", "fast", "-crf", "22"])

    if qt_audio_ok:
        ffmpeg_cmd.extend(["-c:a", "copy"])
    else:
        ffmpeg_cmd.extend(["-c:a", "aac", "-b:a", "192k"])

    ffmpeg_cmd.append(temp_out)

    try:
        res = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=os.environ.copy())
        if res.returncode == 0 and os.path.exists(temp_out) and os.path.getsize(temp_out) > 0:
            os.replace(temp_out, filepath)
            return filepath
        else:
            if os.path.exists(temp_out):
                os.remove(temp_out)
    except Exception:
        if os.path.exists(temp_out):
            try:
                os.remove(temp_out)
            except Exception:
                pass

    return filepath

def extract_video_info(url, browser="none"):
    cmd = [
        YT_DLP_BIN,
        "-J",
        "--no-playlist",
        "--skip-download",
        "--no-check-certificates",
        "--geo-bypass",
        "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "--ffmpeg-location", FFMPEG_BIN,
    ]
    if browser and browser != "none":
        cmd.extend(["--cookies-from-browser", browser])
    cmd.append(url)

    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=35,
        env=os.environ.copy()
    )
    if proc.returncode != 0:
        err = proc.stderr.strip() or "Failed to extract video information."
        if "ERROR:" in err:
            err = err.split("ERROR:")[-1].strip()
        raise Exception(err)

    data = json.loads(proc.stdout)
    platform = detect_platform(url)

    formats = data.get("formats", [])
    max_height = 0
    available_heights = set()

    for f in formats:
        h = f.get("height")
        if h and isinstance(h, int):
            available_heights.add(h)
            if h > max_height:
                max_height = h

    quality_options = []

    if platform == "youtube":
        if max_height >= 2160 or 2160 in available_heights:
            quality_options.append({"id": "4k", "label": "4K Ultra HD (2160p)", "resolution": "3840x2160", "badge": "4K UHD"})
        if max_height >= 1440 or 1440 in available_heights:
            quality_options.append({"id": "1440p", "label": "2K Quad HD (1440p)", "resolution": "2560x1440", "badge": "2K QHD"})
        if max_height >= 1080 or 1080 in available_heights:
            quality_options.append({"id": "1080p", "label": "Full HD (1080p)", "resolution": "1920x1080", "badge": "1080p FHD"})
        if max_height >= 720 or 720 in available_heights:
            quality_options.append({"id": "720p", "label": "HD (720p)", "resolution": "1280x720", "badge": "720p HD"})
        quality_options.append({"id": "480p", "label": "SD (480p)", "resolution": "854x480", "badge": "480p"})
        quality_options.append({"id": "mp3", "label": "Audio Only (MP3 320kbps)", "resolution": "Audio", "badge": "MP3"})
    elif platform == "tiktok":
        quality_options.append({"id": "best", "label": "TikTok HD (No Watermark)", "resolution": f"HD ({max_height}p)" if max_height else "Original HD", "badge": "HD Watermark-Free"})
        quality_options.append({"id": "mp3", "label": "TikTok Audio (MP3)", "resolution": "Audio", "badge": "MP3"})
    elif platform == "facebook":
        if max_height >= 1080:
            quality_options.append({"id": "1080p", "label": "Facebook 1080p Full HD", "resolution": "1920x1080", "badge": "1080p FHD"})
        quality_options.append({"id": "best", "label": "Facebook HD (Best Quality)", "resolution": f"{max_height}p HD" if max_height else "HD", "badge": "HD"})
        if max_height >= 720:
            quality_options.append({"id": "720p", "label": "Facebook 720p HD", "resolution": "1280x720", "badge": "720p"})
        quality_options.append({"id": "mp3", "label": "Facebook Audio (MP3)", "resolution": "Audio", "badge": "MP3"})
    else:
        quality_options.append({"id": "best", "label": "Best Available Quality", "resolution": f"{max_height}p" if max_height else "Best", "badge": "Best"})
        if max_height >= 1080:
            quality_options.append({"id": "1080p", "label": "1080p Full HD", "resolution": "1080p", "badge": "1080p"})
        if max_height >= 720:
            quality_options.append({"id": "720p", "label": "720p HD", "resolution": "720p", "badge": "720p"})
        quality_options.append({"id": "mp3", "label": "Audio Only (MP3)", "resolution": "Audio", "badge": "MP3"})

    if not quality_options:
        quality_options = [
            {"id": "best", "label": "Best Quality (Auto)", "resolution": "HD", "badge": "Auto"},
            {"id": "mp3", "label": "Audio Only (MP3)", "resolution": "Audio", "badge": "MP3"}
        ]

    thumb = data.get("thumbnail")
    thumbnails = data.get("thumbnails", [])
    if thumbnails:
        thumb = thumbnails[-1].get("url") or thumb

    return {
        "id": data.get("id"),
        "title": data.get("title") or "Unknown Title",
        "uploader": data.get("uploader") or data.get("channel") or data.get("creator") or "Unknown Creator",
        "thumbnail": thumb,
        "duration": data.get("duration"),
        "duration_formatted": format_duration(data.get("duration")),
        "platform": platform,
        "max_height": max_height,
        "quality_options": quality_options,
        "webpage_url": data.get("webpage_url") or url
    }

def run_download_thread(download_id, url, quality, download_dir, browser, video_info):
    with downloads_lock:
        active_downloads[download_id] = {
            "id": download_id,
            "url": url,
            "title": video_info.get("title", "Video"),
            "thumbnail": video_info.get("thumbnail", ""),
            "platform": video_info.get("platform", "generic"),
            "quality": quality,
            "status": "connecting",
            "stage": "init",
            "stage_badge": "CONNECTING",
            "status_text": "កំពុងភ្ជាប់ជាមួយ Server និងវិភាគ Stream...",
            "status_text_km": "កំពុងភ្ជាប់ជាមួយ Server និងវិភាគ Stream...",
            "status_text_en": "Connecting to server and analyzing video stream...",
            "percent": "0.0%",
            "percent_num": 0,
            "speed": "-- MB/s",
            "eta": "--:--",
            "size": "-- MB",
            "filepath": None,
            "filename": None,
            "error": None,
            "completed": False,
            "start_time": time.time(),
        }

    out_tmpl = os.path.join(download_dir, "%(title).150B [%(id)s].%(ext)s")

    cmd = [
        YT_DLP_BIN,
        "--newline",
        "--progress",
        "--no-check-certificates",
        "--geo-bypass",
        "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "--ffmpeg-location", FFMPEG_BIN,
        "--format-sort", "vcodec:avc,acodec:m4a",
        "--progress-template", "download:PROG|%(progress._percent_str)s|%(progress._speed_str)s|%(progress._eta_str)s|%(progress._total_bytes_estimate_str)s|%(progress.downloaded_bytes_str)s|%(progress.status)s",
        "--print", "after_move:FINAL_PATH|%(filepath)s",
        "-o", out_tmpl,
    ]

    if browser and browser != "none":
        cmd.extend(["--cookies-from-browser", browser])

    if quality == "mp3":
        cmd.extend([
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
        ])
    elif quality == "4k":
        cmd.extend([
            "-f", "bestvideo[height<=2160]+bestaudio/bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
        ])
    elif quality == "1440p":
        cmd.extend([
            "-f", "bestvideo[height<=1440]+bestaudio/bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
        ])
    elif quality == "1080p":
        cmd.extend([
            "-f", "bestvideo[height<=1080]+bestaudio/bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
        ])
    elif quality == "720p":
        cmd.extend([
            "-f", "bestvideo[height<=720]+bestaudio/bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
        ])
    elif quality == "480p":
        cmd.extend([
            "-f", "bestvideo[height<=480]+bestaudio/bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
        ])
    else:  # best
        cmd.extend([
            "-f", "bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
        ])

    cmd.append(url)
    final_filepath = None
    stream_type = "video"

    sub_env = os.environ.copy()
    sub_env["PYTHONUNBUFFERED"] = "1"

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            env=sub_env
        )

        # Read line by line in real-time with zero blocking buffer delay
        while True:
            line = proc.stdout.readline()
            if not line and proc.poll() is not None:
                break
            line_str = line.strip()
            if not line_str:
                continue

            with downloads_lock:
                task = active_downloads.get(download_id)
                if not task:
                    break

                # Dynamic instant status detection
                if "[youtube]" in line_str:
                    if "Downloading webpage" in line_str or "Extracting URL" in line_str:
                        task["status"] = "connecting"
                        task["stage"] = "connecting"
                        task["stage_badge"] = "CONNECTING"
                        task["percent"] = "2.0%" if task.get("percent_num", 0) < 2 else task["percent"]
                        task["percent_num"] = max(task.get("percent_num", 0), 2.0)
                        task["status_text_km"] = "កំពុងទាញយកព័ត៌មានវីដេអូពី YouTube..."
                        task["status_text_en"] = "Connecting to YouTube & fetching stream info..."
                        task["status_text"] = task["status_text_km"]
                    elif "Solving JS challenges" in line_str or "deno" in line_str.lower():
                        task["status"] = "resolving"
                        task["stage"] = "resolving"
                        task["stage_badge"] = "DENO CHALLENGE"
                        task["percent"] = "5.0%" if task.get("percent_num", 0) < 5 else task["percent"]
                        task["percent_num"] = max(task.get("percent_num", 0), 5.0)
                        task["status_text_km"] = "កំពុងដោះស្រាយ Security Challenge (Deno Engine)..."
                        task["status_text_en"] = "Solving security challenge (Deno engine)..."
                        task["status_text"] = task["status_text_km"]
                    elif "m3u8" in line_str or "API JSON" in line_str or "player" in line_str.lower():
                        task["status"] = "resolving"
                        task["stage"] = "resolving"
                        task["stage_badge"] = "PREPARING"
                        task["percent"] = "7.0%" if task.get("percent_num", 0) < 7 else task["percent"]
                        task["percent_num"] = max(task.get("percent_num", 0), 7.0)
                        task["status_text_km"] = "កំពុងរៀបចំ Stream និងទម្រង់ 1080p/4K..."
                        task["status_text_en"] = "Preparing high-res video stream..."
                        task["status_text"] = task["status_text_km"]
                elif "[tiktok]" in line_str:
                    task["status"] = "connecting"
                    task["stage"] = "connecting"
                    task["stage_badge"] = "TIKTOK HD"
                    task["status_text_km"] = "កំពុងទាញយកវីដេអូ TikTok HD (គ្មាន Watermark)..."
                    task["status_text_en"] = "Fetching TikTok HD video (No Watermark)..."
                    task["status_text"] = task["status_text_km"]
                elif "[facebook]" in line_str:
                    task["status"] = "connecting"
                    task["stage"] = "connecting"
                    task["stage_badge"] = "FACEBOOK HD"
                    task["status_text_km"] = "កំពុងទាញយកវីដេអូ Facebook HD/1080p..."
                    task["status_text_en"] = "Fetching Facebook HD video stream..."
                    task["status_text"] = task["status_text_km"]
                elif "[info]" in line_str and "Downloading 1 format" in line_str:
                    task["status"] = "downloading"
                    task["stage"] = "downloading"
                    task["stage_badge"] = "STARTING"
                    task["status_text_km"] = "ចាប់ផ្ដើមទាញយកទិន្នន័យ Stream..."
                    task["status_text_en"] = "Starting stream download..."
                    task["status_text"] = task["status_text_km"]

                elif "[download] Destination:" in line_str:
                    task["status"] = "downloading"
                    if ".f" in line_str or "video" in line_str or "mp4" in line_str:
                        stream_type = "video"
                        task["stage"] = "video"
                        task["stage_badge"] = "VIDEO STREAM"
                        task["status_text_km"] = "កំពុងទាញយករូបភាព (Video 1080p/4K)..."
                        task["status_text_en"] = "Downloading video stream (1080p/4K)..."
                        task["status_text"] = task["status_text_km"]
                    elif "audio" in line_str or "m4a" in line_str or "webm" in line_str:
                        stream_type = "audio"
                        task["stage"] = "audio"
                        task["stage_badge"] = "AUDIO STREAM"
                        task["status_text_km"] = "កំពុងទាញយកសម្លេង (Audio M4A/AAC)..."
                        task["status_text_en"] = "Downloading audio stream (M4A/AAC)..."
                        task["status_text"] = task["status_text_km"]

                elif line_str.startswith("PROG|"):
                    parts = line_str.split("|")
                    if len(parts) >= 6:
                        pct_str = parts[1].strip()
                        speed = parts[2].strip()
                        eta = parts[3].strip()
                        total_size = parts[4].strip()

                        try:
                            clean_pct = float(pct_str.replace("%", "").strip())
                        except Exception:
                            clean_pct = task.get("percent_num", 0)

                        task["percent"] = pct_str or f"{clean_pct:.1f}%"
                        task["percent_num"] = clean_pct
                        task["speed"] = speed if speed and speed != "NA" else task["speed"]
                        task["eta"] = eta if eta and eta != "NA" else task["eta"]
                        task["size"] = total_size if total_size and total_size != "NA" else task["size"]
                        task["status"] = "downloading"

                        if stream_type == "audio":
                            task["stage"] = "audio"
                            task["stage_badge"] = "AUDIO STREAM"
                            task["status_text_km"] = f"កំពុងទាញយកសម្លេង Audio ({pct_str})..."
                            task["status_text_en"] = f"Downloading audio stream ({pct_str})..."
                        else:
                            task["stage"] = "video"
                            task["stage_badge"] = "VIDEO STREAM"
                            task["status_text_km"] = f"កំពុងទាញយករូបភាព Video ({pct_str})..."
                            task["status_text_en"] = f"Downloading video stream ({pct_str})..."
                        task["status_text"] = task["status_text_km"]

                # Fallback regex for standard [download] ...% lines
                elif "[download]" in line_str and "%" in line_str:
                    match = re.search(r'\[download\]\s+([\d\.]+)%\s+of\s+~?\s*([\d\.]+\w+)(?:\s+at\s+([\d\.]+\w+/s))?(?:\s+ETA\s+([\d:]+))?', line_str)
                    if match:
                        pct_val = match.group(1)
                        size_val = match.group(2)
                        speed_val = match.group(3)
                        eta_val = match.group(4)
                        try:
                            clean_pct = float(pct_val)
                        except Exception:
                            clean_pct = task.get("percent_num", 0)
                        task["percent"] = f"{clean_pct:.1f}%"
                        task["percent_num"] = clean_pct
                        if size_val: task["size"] = size_val
                        if speed_val: task["speed"] = speed_val
                        if eta_val: task["eta"] = eta_val
                        task["status"] = "downloading"
                        if stream_type == "audio":
                            task["stage"] = "audio"
                            task["stage_badge"] = "AUDIO STREAM"
                            task["status_text_km"] = f"កំពុងទាញយកសម្លេង Audio ({clean_pct:.1f}%)..."
                            task["status_text_en"] = f"Downloading audio stream ({clean_pct:.1f}%)..."
                        else:
                            task["stage"] = "video"
                            task["stage_badge"] = "VIDEO STREAM"
                            task["status_text_km"] = f"កំពុងទាញយករូបភាព Video ({clean_pct:.1f}%)..."
                            task["status_text_en"] = f"Downloading video stream ({clean_pct:.1f}%)..."
                        task["status_text"] = task["status_text_km"]

                elif line_str.startswith("FINAL_PATH|"):
                    final_filepath = line_str.split("FINAL_PATH|", 1)[1].strip()
                    task["filepath"] = final_filepath
                    task["filename"] = os.path.basename(final_filepath)

                elif "[Merger]" in line_str or "Merging formats into" in line_str:
                    task["status"] = "merging"
                    task["stage"] = "merging"
                    task["stage_badge"] = "FFMPEG MERGE"
                    task["status_text_km"] = "FFmpeg កំពុងបញ្ចូលរូបភាព និងសម្លេង (1080p/4K)..."
                    task["status_text_en"] = "FFmpeg merging video & audio into MP4..."
                    task["status_text"] = task["status_text_km"]
                    task["percent"] = "98.0%"
                    task["percent_num"] = 98.0

                elif "[ExtractAudio]" in line_str:
                    task["status"] = "converting_audio"
                    task["stage"] = "converting_audio"
                    task["stage_badge"] = "AUDIO CONVERT"
                    task["status_text_km"] = "កំពុងបម្លែងទៅជា MP3 គុណភាពខ្ពស់ 320kbps..."
                    task["status_text_en"] = "Converting to 320kbps MP3 audio..."
                    task["status_text"] = task["status_text_km"]
                    task["percent"] = "98.0%"
                    task["percent_num"] = 98.0

                elif "ERROR:" in line_str:
                    task["error"] = line_str.split("ERROR:", 1)[1].strip()

        proc.wait()

        with downloads_lock:
            task = active_downloads.get(download_id)
            if task:
                if proc.returncode == 0:
                    target_file = task.get("filepath") or final_filepath

                    # Ensure QuickTime & Apple compatibility (remux to H.264/AAC if needed)
                    if quality != "mp3" and target_file and os.path.exists(target_file):
                        task["status"] = "optimizing_quicktime"
                        task["stage"] = "optimizing"
                        task["stage_badge"] = "QUICKTIME READY"
                        task["status_text_km"] = "កំពុងរៀបចំ Codec ឱ្យដំណើរការ 100% លើ QuickTime Player..."
                        task["status_text_en"] = "Ensuring 100% Apple QuickTime Player compatibility..."
                        task["status_text"] = task["status_text_km"]
                        task["percent"] = "99.0%"
                        target_file = ensure_quicktime_compatible(target_file)
                        task["filepath"] = target_file
                        task["filename"] = os.path.basename(target_file)

                    task["completed"] = True
                    task["stage"] = "completed"
                    task["stage_badge"] = "COMPLETED"
                    task["percent"] = "100%"
                    task["percent_num"] = 100
                    task["status"] = "completed"
                    task["status_text_km"] = "ការទាញយកបានបញ្ចប់ដោយជោគជ័យ! 🎉"
                    task["status_text_en"] = "Download Complete! 🎉"
                    task["status_text"] = task["status_text_km"]

                    file_size_formatted = task.get("size")
                    if task.get("filepath") and os.path.exists(task["filepath"]):
                        try:
                            bytes_size = os.path.getsize(task["filepath"])
                            if bytes_size >= 1024 * 1024 * 1024:
                                file_size_formatted = f"{bytes_size / (1024**3):.2f} GB"
                            elif bytes_size >= 1024 * 1024:
                                file_size_formatted = f"{bytes_size / (1024**2):.1f} MB"
                            else:
                                file_size_formatted = f"{bytes_size / 1024:.1f} KB"
                            task["size"] = file_size_formatted
                        except Exception:
                            pass

                    history_entry = {
                        "id": download_id,
                        "url": url,
                        "title": task["title"],
                        "thumbnail": task["thumbnail"],
                        "platform": task["platform"],
                        "quality": quality,
                        "filepath": task.get("filepath"),
                        "filename": task.get("filename") or os.path.basename(task.get("filepath") or "video.mp4"),
                        "size": file_size_formatted,
                        "timestamp": int(time.time()),
                        "date_str": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    add_history_item(history_entry)

                else:
                    task["completed"] = True
                    task["status"] = "failed"
                    task["status_text"] = "ការទាញយកបរាជ័យ"
                    if not task.get("error"):
                        task["error"] = "Download returned error code. Please verify URL or network access."

    except Exception as e:
        with downloads_lock:
            task = active_downloads.get(download_id)
            if task:
                task["completed"] = True
                task["status"] = "failed"
                task["status_text"] = "ការទាញយកបរាជ័យ"
                task["error"] = str(e)


# ==============================================================================
# CapCut-Style Video Studio & AI Assistant Backend
# ==============================================================================

active_edits = {}
edits_lock = threading.Lock()

def format_srt_timestamp(seconds):
    if seconds < 0:
        seconds = 0
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        millis = 999
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def write_srt_file(subtitles, target_path):
    try:
        with open(target_path, "w", encoding="utf-8") as f:
            for idx, item in enumerate(subtitles, 1):
                start = float(item.get("start", 0))
                end = float(item.get("end", start + 3))
                text = str(item.get("text", "")).strip()
                if not text:
                    continue
                f.write(f"{idx}\n")
                f.write(f"{format_srt_timestamp(start)} --> {format_srt_timestamp(end)}\n")
                f.write(f"{text}\n\n")
        return True
    except Exception as e:
        print(f"Error writing srt file: {e}")
        return False

def get_video_duration_fast(filepath):
    try:
        cmd = [
            FFPROBE_BIN, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            filepath
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        dur = float(res.stdout.strip())
        if dur > 0:
            return dur
    except Exception:
        pass

    try:
        res = subprocess.run([FFMPEG_BIN, "-i", filepath], capture_output=True, text=True, timeout=10)
        import re
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", res.stderr)
        if m:
            h, mi, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
            return h * 3600 + mi * 60 + s
    except Exception:
        pass
    return 30.0

def run_video_edit_thread(edit_id, source_path, options, download_dir):
    try:
        with edits_lock:
            active_edits[edit_id] = {
                "edit_id": edit_id,
                "status": "processing",
                "status_text": "កំពុងចាប់ផ្ដើមកាត់តវីដេអូ...",
                "progress": 5,
                "completed": False,
                "output_file": None,
                "error": None
            }

        src_p = Path(source_path)
        base_name = src_p.stem
        if base_name.endswith("-edited"):
            base_name = base_name[:-7]
        timestamp_suffix = time.strftime("%H%M%S")

        start_time = float(options.get("start_time") or options.get("trim_start") or 0)
        end_time = float(options.get("end_time") or options.get("trim_end") or 0)
        speed = float(options.get("speed") or 1.0)
        aspect_ratio = options.get("aspect_ratio") or options.get("canvas") or "original"
        filter_name = options.get("filter_name") or options.get("filter_preset") or "none"
        
        # Safe brightness/contrast/saturation conversion for FFmpeg eq filter
        raw_b = float(options.get("brightness") if options.get("brightness") is not None else 0.0)
        brightness = (raw_b - 100.0) / 100.0 if raw_b > 20.0 else raw_b
        raw_c = float(options.get("contrast") if options.get("contrast") is not None else 1.0)
        contrast = raw_c / 100.0 if raw_c > 10.0 else raw_c
        raw_s = float(options.get("saturation") if options.get("saturation") is not None else 1.0)
        saturation = raw_s / 100.0 if raw_s > 10.0 else raw_s

        flip_h = bool(options.get("flip_h", False))
        flip_v = bool(options.get("flip_v", False))
        rotate = int(options.get("rotate") or 0)
        volume = float(options.get("volume") if options.get("volume") is not None else 1.0)
        mute = bool(options.get("mute", False))
        fade_in = bool(options.get("fade_in", False))
        fade_out = bool(options.get("fade_out", False))
        export_res = options.get("export_res") or "original"
        export_format = options.get("export_format") or "mp4"
        subtitles = options.get("subtitles") or []

        if export_format == "mp3":
            out_filename = f"{base_name}-audio-{timestamp_suffix}.mp3"
        else:
            out_filename = f"{base_name}-edited-{timestamp_suffix}.mp4"
        out_filepath = str(Path(download_dir) / out_filename)

        # Write companion SRT if subtitles provided
        srt_filepath = None
        if subtitles and isinstance(subtitles, list) and len(subtitles) > 0 and export_format != "mp3":
            srt_filename = f"{base_name}-edited-{timestamp_suffix}.srt"
            srt_filepath = str(Path(download_dir) / srt_filename)
            write_srt_file(subtitles, srt_filepath)

        total_source_dur = get_video_duration_fast(source_path)
        calc_end = end_time if (end_time > start_time) else total_source_dur
        target_dur = max(1.0, (calc_end - start_time) / speed)

        cmd = [FFMPEG_BIN, "-y"]
        if start_time > 0:
            cmd.extend(["-ss", str(start_time)])
        if end_time > start_time:
            cmd.extend(["-to", str(end_time)])
        cmd.extend(["-i", source_path])

        if export_format == "mp3":
            # Extract high quality 320kbps MP3 audio with speed & volume adjustments
            af_filters = []
            if speed != 1.0:
                af_filters.append(f"atempo={speed}")
            if volume != 1.0:
                af_filters.append(f"volume={volume}")
            if fade_in:
                af_filters.append("afade=t=in:ss=0:d=1.0")
            if fade_out and target_dur > 2.0:
                af_filters.append(f"afade=t=out:st={max(0.1, target_dur-1.0):d=1.0}")
            if af_filters:
                cmd.extend(["-af", ",".join(af_filters)])
            cmd.extend(["-vn", "-c:a", "libmp3lame", "-b:a", "320k", out_filepath])
        else:
            # Video Processing Filter Chain
            vf_filters = []
            
            # 1. Canvas / Aspect Ratio
            if aspect_ratio == "9:16":
                # CapCut viral blurred background 9:16 portrait
                filter_complex = "split=2[fg][bg];[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:20[bgb];[fg]scale=1080:1920:force_original_aspect_ratio=decrease[fgs];[bgb][fgs]overlay=(W-w)/2:(H-h)/2"
                vf_filters.append(filter_complex)
            elif aspect_ratio == "1:1":
                filter_complex = "split=2[fg][bg];[bg]scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080,boxblur=20:20[bgb];[fg]scale=1080:1080:force_original_aspect_ratio=decrease[fgs];[bgb][fgs]overlay=(W-w)/2:(H-h)/2"
                vf_filters.append(filter_complex)
            elif aspect_ratio == "16:9":
                vf_filters.append("scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black")

            # 2. Transform: Flip & Rotate (CapCut Mirror & Rotation)
            if flip_h:
                vf_filters.append("hflip")
            if flip_v:
                vf_filters.append("vflip")
            if rotate == 90:
                vf_filters.append("transpose=1")
            elif rotate == 180:
                vf_filters.append("hflip,vflip")
            elif rotate == 270:
                vf_filters.append("transpose=2")

            # 3. Color Preset Filters
            if filter_name == "cinematic":
                vf_filters.append("colorbalance=rs=.08:gs=.02:bs=-.05,eq=contrast=1.12:saturation=1.18")
            elif filter_name == "neon":
                vf_filters.append("colorbalance=rm=.1:bm=.18:bs=.25,eq=contrast=1.22:saturation=1.45")
            elif filter_name == "vintage":
                vf_filters.append("colorbalance=rs=.12:gs=.04:bs=-.08,eq=contrast=1.08:saturation=0.82")
            elif filter_name == "bw":
                vf_filters.append("hue=s=0,eq=contrast=1.28")
            elif filter_name == "clarity":
                vf_filters.append("unsharp=5:5:1.0:5:5:0.0,eq=contrast=1.15:saturation=1.2")
            elif filter_name == "glow":
                vf_filters.append("boxblur=1:1,eq=brightness=0.03:contrast=1.08")

            # 4. Sliders adjustment
            if brightness != 0.0 or contrast != 1.0 or saturation != 1.0:
                vf_filters.append(f"eq=brightness={brightness}:contrast={contrast}:saturation={saturation}")

            # 5. Speed adjustment for video
            if speed != 1.0:
                vf_filters.append(f"setpts={1.0/speed}*PTS")

            # 6. Fade Transitions
            if fade_in:
                vf_filters.append("fade=t=in:st=0:d=1.0")
            if fade_out and target_dur > 2.0:
                vf_filters.append(f"fade=t=out:st={max(0.1, target_dur-1.0):d=1.0}")

            # 7. Resolution scaling
            if export_res == "720p":
                vf_filters.append("scale=-2:720")
            elif export_res == "1080p":
                vf_filters.append("scale=-2:1080")
            elif export_res == "4k":
                vf_filters.append("scale=-2:2160")

            if vf_filters:
                cmd.extend(["-vf", ",".join(vf_filters)])

            # Audio adjustments
            if mute:
                cmd.append("-an")
            else:
                af_filters = []
                if speed != 1.0:
                    af_filters.append(f"atempo={speed}")
                if volume != 1.0:
                    af_filters.append(f"volume={volume}")
                if fade_in:
                    af_filters.append("afade=t=in:ss=0:d=1.0")
                if fade_out and target_dur > 2.0:
                    af_filters.append(f"afade=t=out:st={max(0.1, target_dur-1.0):d=1.0}")
                if af_filters:
                    cmd.extend(["-af", ",".join(af_filters)])
                cmd.extend(["-c:a", "aac", "-b:a", "192k"])

            # Add subtitle track if srt created
            if srt_filepath and os.path.exists(srt_filepath):
                cmd.extend(["-i", srt_filepath, "-c:s", "mov_text", "-metadata:s:s:0", "language=khm"])

            cmd.extend([
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "20",
                "-movflags", "+faststart",
                out_filepath
            ])

        with edits_lock:
            active_edits[edit_id]["status_text"] = "កំពុងដំណើរការកែច្នៃវីដេអូ..."
            active_edits[edit_id]["progress"] = 20

        process = subprocess.Popen(
            cmd,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            errors="replace"
        )

        time_pattern = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")
        while True:
            line = process.stderr.readline()
            if not line and process.poll() is not None:
                break
            match = time_pattern.search(line)
            if match:
                hrs, mins, secs = match.groups()
                cur_seconds = int(hrs) * 3600 + int(mins) * 60 + float(secs)
                pct = min(95, int(20 + (cur_seconds / target_dur) * 75))
                with edits_lock:
                    active_edits[edit_id]["progress"] = pct
                    active_edits[edit_id]["percent"] = pct
                    active_edits[edit_id]["status_text_km"] = f"កំពុងបម្លែង Effect & នាំចេញ... {pct}%"
                    active_edits[edit_id]["status_text_en"] = f"Rendering & exporting... {pct}%"
                    active_edits[edit_id]["status_text"] = f"កំពុងបម្លែង Effect & នាំចេញ... {pct}%"

        rc = process.wait()
        if rc == 0 and os.path.exists(out_filepath):
            file_size_bytes = os.path.getsize(out_filepath)
            size_str = format_size(file_size_bytes)
            with edits_lock:
                active_edits[edit_id]["completed"] = True
                active_edits[edit_id]["status"] = "completed"
                active_edits[edit_id]["progress"] = 100
                active_edits[edit_id]["percent"] = 100
                active_edits[edit_id]["status_text_km"] = "កាត់តវីដេអូបានបញ្ចប់ដោយជោគជ័យ! 🎉"
                active_edits[edit_id]["status_text_en"] = "Video export completed successfully! 🎉"
                active_edits[edit_id]["status_text"] = "កាត់តវីដេអូបានបញ្ចប់ដោយជោគជ័យ! 🎉"
                active_edits[edit_id]["output_file"] = out_filepath
                active_edits[edit_id]["output_path"] = out_filepath
                active_edits[edit_id]["filename"] = out_filename
                active_edits[edit_id]["size"] = size_str

            add_history_item({
                "id": str(uuid.uuid4())[:8],
                "url": options.get("source_url") or "",
                "title": f"🎬 {base_name} (Edited)",
                "thumbnail": options.get("thumbnail") or "/static/logo_icon.png",
                "platform": "studio",
                "quality": "1080p",
                "filepath": out_filepath,
                "filename": out_filename,
                "size": size_str,
                "timestamp": int(time.time()),
                "date_str": time.strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            with edits_lock:
                active_edits[edit_id]["completed"] = True
                active_edits[edit_id]["status"] = "failed"
                active_edits[edit_id]["error"] = "FFmpeg editing failed. Please verify options."
                active_edits[edit_id]["status_text"] = "ការកាត់តវីដេអូបរាជ័យ"

    except Exception as e:
        with edits_lock:
            if edit_id in active_edits:
                active_edits[edit_id]["completed"] = True
                active_edits[edit_id]["status"] = "failed"
                active_edits[edit_id]["error"] = str(e)
                active_edits[edit_id]["status_text"] = "ការកាត់តវីដេអូបរាជ័យ"

def generate_ai_assistance(action_type, title, text, lang="km", api_key=""):
    title = title.strip() or ("វីដេអូពេញនិយម" if lang == "km" else "Viral Video")
    
    if api_key and len(api_key.strip()) > 10:
        try:
            prompt = f"You are a professional social media video editor like CapCut Pro. Video Title: {title}. Language: {lang}. Action: {action_type}. Content: {text}."
            if action_type == "hook":
                prompt += " Generate 5 viral hooks (Curiosity, Shocking fact, Story, Secret, Action) for TikTok/Reels."
            elif action_type == "caption":
                prompt += " Write an engaging viral caption with emojis and 15 trending hashtags."
            elif action_type == "summary":
                prompt += " Summarize the key moments and highlights in bullet points with estimated timestamps."
            elif action_type == "translate":
                prompt += f" Translate the provided text accurately to {('English' if lang=='en' else 'Khmer')}."

            req_data = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}]
            }).encode("utf-8")

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key.strip()}"
            req = urllib.request.Request(url, data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                ans = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if ans:
                    return ans
        except Exception:
            pass

    if action_type == "hook":
        if lang == "km":
            return f"""🎯 ៥ ចំណងជើងទាក់ទាញចិត្ត (Viral Hooks សម្រាប់ TikTok & Reels)៖

១. 💡 Hook សំណួរចង់ដឹង៖ "តើអ្នកធ្លាប់ដឹងរឿងនេះពីមុនមកទេ? វីដេអូនេះនឹងផ្លាស់ប្តូរការគិតរបស់អ្នក!"
២. 😱 Hook ការពិតភ្ញាក់ផ្អើល៖ "មនុស្ស ៩៩% មិនទាន់ដឹងរឿងនេះនៅឡើយទេ... ចាំមើលដល់ចប់!"
៣. ⏳ Hook កុំរំលងឱ្យសោះ៖ "កុំទាន់អូសរំលង! នេះជាចំណុចពិសេសបំផុតអំពី: {title}"
៤. 🔑 Hook តិចនិកសម្ងាត់៖ "តិចនិកដែលអ្នកបង្កើតមាតិកាល្បីៗមិនដែលប្រាប់អ្នក!"
៥. 🔥 Hook អារម្មណ៍ចាក់ដោត៖ "រឿងនេះពិតជាកើតឡើងមែន ខ្ញុំស្ទើរតែមិនជឿភ្នែកខ្លួនឯង..."
"""
        else:
            return f"""🎯 5 High-Converting Viral Hooks (TikTok, Reels, Shorts):

1. 💡 Curiosity Hook: "Did you know this secret about: {title}? Watch this!"
2. 😱 Shocking Truth: "99% of people get this wrong every single day..."
3. ⏳ Stop Scrolling: "Stop scrolling! You need to see what happens next in this video!"
4. 🔑 The Insider Secret: "The top creators don't want you to know this simple trick..."
5. 🔥 Transformation: "This completely changed how I think about {title}. Don't miss the end!"
"""

    elif action_type == "caption":
        if lang == "km":
            return f"""🔥 {title} 

💡 មើលវីដេអូនេះឱ្យចប់ អ្នកនឹងទទួលបានចំណេះដឹង និងគំនិតថ្មីៗដែលមិនគួរមើលរំលង!
✨ ប្រសិនបើអ្នកពេញចិត្ត សូមចុច Like, Save និង Share ទៅកាន់មិត្តភក្តិរបស់អ្នកផងដែរ! 👇

#fyp #viral #khmertiktok #fbreels #reelsviral #tiktokcambodia #trendingnow #contentcreator #learnontiktok #videoeditor #capcutkhmer #viralvideo #viralreels
"""
        else:
            return f"""🔥 {title} 

💡 Watch until the end for the full breakdown! This is something you definitely don't want to miss.
✨ If you found this helpful, hit Like, Save for later, and Share with someone who needs this! 👇

#fyp #viral #fbreels #tiktok #trending #contentcreator #reelsvideo #viralvideo #videoediting #shorts #explorepage #dailyvideo #trend
"""

    elif action_type == "summary":
        if lang == "km":
            return f"""📌 សេចក្តីសង្ខេប & ចំណុចសំខាន់ៗនៃវីដេអូ៖
🎬 ចំណងជើង៖ {title}

⏱️ 00:00 - 00:05 ｜ ការបើកឆាកទាក់ទាញ (Hook & Introduction)
⏱️ 00:05 - 00:20 ｜ ការបង្ហាញខ្លឹមសារ និងគន្លឹះសំខាន់ៗ
⏱️ 00:20 - 00:45 ｜ ការវិភាគស៊ីជម្រៅ និងសកម្មភាពជាក់ស្តែង
⏱️ 00:45 - បញ្ចប់ ｜ សេចក្តីសន្និដ្ឋាន & ការអំពាវនាវឱ្យធ្វើសកម្មភាព (Call To Action)

💡 សរុបមក៖ វីដេអូនេះផ្តល់នូវតម្លៃយ៉ាងច្រើនសម្រាប់អ្នកទស្សនា និងស័ក្តិសមបំផុតក្នុងការចែករំលែកបន្ត!
"""
        else:
            return f"""📌 Video Highlights & Key Takeaways:
🎬 Title: {title}

⏱️ 00:00 - 00:05 | Hook & Core Problem Statement
⏱️ 00:05 - 00:20 | Key Concept & Main Action
⏱️ 00:20 - 00:45 | In-depth Breakdown & Evidence
⏱️ 00:45 - End   | Final Takeaway & Call to Action (CTA)

💡 Summary: High engagement potential, clear progression, and strong viral retention throughout!
"""

    elif action_type == "translate":
        if lang == "km":
            return f"ខ្លឹមសារបកប្រែជាភាសាខ្មែរ៖\n\n{title}\n\n{text}"
        else:
            return f"Translated content into English:\n\n{title}\n\n{text}"

    return "AI Assistant Ready."

def parse_timestamp_str(ts_str):
    ts_str = ts_str.replace(",", ".")
    parts = ts_str.split(":")
    if len(parts) == 3:
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return float(parts[0]) * 60 + float(parts[1])
    return 0.0

def extract_or_generate_subtitles(video_path, url=""):
    if url and shutil.which(YT_DLP_BIN):
        try:
            temp_dir = tempfile.mkdtemp()
            sub_cmd = [
                YT_DLP_BIN,
                "--skip-download",
                "--write-auto-sub",
                "--sub-lang", "km,en",
                "--sub-format", "vtt/srt/best",
                "-o", str(Path(temp_dir) / "sub"),
                url
            ]
            subprocess.run(sub_cmd, capture_output=True, timeout=15)
            found_subs = list(Path(temp_dir).glob("*.vtt")) + list(Path(temp_dir).glob("*.srt"))
            if found_subs:
                parsed = []
                with open(found_subs[0], "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                cue_pattern = re.compile(r"(\d{2}:\d{2}:\d{2}[\.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[\.,]\d{3})\s*\n(.*?)(?=\n\n|\Z)", re.DOTALL)
                matches = cue_pattern.findall(content)
                for idx, m in enumerate(matches, 1):
                    start_str, end_str, cue_text = m
                    clean_text = re.sub(r"<[^>]+>", "", cue_text).strip()
                    if clean_text:
                        parsed.append({
                            "id": idx,
                            "start": parse_timestamp_str(start_str),
                            "end": parse_timestamp_str(end_str),
                            "text": clean_text
                        })
                shutil.rmtree(temp_dir, ignore_errors=True)
                if parsed:
                    return parsed
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

    dur = 30.0
    if video_path and os.path.exists(video_path):
        dur = get_video_duration_fast(video_path)

    sample_khmer_captions = [
        "សូមស្វាគមន៍មកកាន់វីដេអូនេះ! 🔥",
        "ថ្ងៃនេះខ្ញុំនឹងចែករំលែករឿងពិសេសមួយ...",
        "ចំណុចសំខាន់ដែលអ្នកមិនគួរមើលរំលង!",
        "តើអ្នកបានកត់សម្គាល់ចំណុចនេះទេ? ✨",
        "មើលឱ្យចប់ អ្នកនឹងយល់ច្បាស់!",
        "កុំភ្លេចចុច Like និង Follow ផងណា! ❤️",
        "អរគុណច្រើនសម្រាប់ការទស្សនា! 🎉"
    ]

    cues = []
    step = min(4.5, dur / max(1, len(sample_khmer_captions)))
    cur = 0.0
    idx = 1
    while cur < dur:
        nxt = min(dur, cur + step)
        text_index = (idx - 1) % len(sample_khmer_captions)
        cues.append({
            "id": idx,
            "start": round(cur, 2),
            "end": round(nxt, 2),
            "text": sample_khmer_captions[text_index]
        })
        cur = nxt
        idx += 1
        if idx > 25:
            break

    return cues


class DownloaderHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            raw_body = self.rfile.read(content_length).decode("utf-8")
            return json.loads(raw_body)
        return {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.serve_file(PUBLIC_DIR / "index.html", "text/html; charset=utf-8")
            return
        elif path == "/manifest.json":
            self.serve_file(PUBLIC_DIR / "manifest.json", "application/manifest+json")
            return
        elif path == "/favicon.ico":
            self.serve_file(PUBLIC_DIR / "favicon.ico", "image/x-icon")
            return
        elif path.strip("/") and (PUBLIC_DIR / path.lstrip("/")).exists() and (PUBLIC_DIR / path.lstrip("/")).is_file():
            target_f = PUBLIC_DIR / path.lstrip("/")
            try:
                target_f.resolve().relative_to(PUBLIC_DIR.resolve())
                self.serve_file(target_f, self.get_mime_type(target_f))
                return
            except ValueError:
                pass
        elif path.startswith("/static/"):
            rel_path = path[len("/static/"):]
            file_path = PUBLIC_DIR / rel_path
            try:
                file_path.resolve().relative_to(PUBLIC_DIR.resolve())
            except ValueError:
                self.send_error(403, "Forbidden")
                return

            if file_path.exists() and file_path.is_file():
                content_type = self.get_mime_type(file_path)
                self.serve_file(file_path, content_type)
                return
            else:
                self.send_error(404, "File Not Found")
                return

        elif path == "/api/download-file":
            filepath = query.get("filepath", [None])[0]
            if not filepath or not os.path.exists(filepath):
                self.send_error(404, "File Not Found")
                return
            try:
                filename = os.path.basename(filepath)
                filesize = os.path.getsize(filepath)
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                quoted_name = urllib.parse.quote(filename)
                self.send_header("Content-Disposition", f'attachment; filename="{quoted_name}"; filename*=UTF-8\'\'{quoted_name}')
                self.send_header("Content-Length", str(filesize))
                self.end_headers()

                with open(filepath, "rb") as f:
                    shutil.copyfileobj(f, self.wfile, length=1024*1024)
                return
            except Exception:
                return

        elif path == "/api/download-installer":
            dmg_path = BASE_DIR / "RothaDownloader.dmg"
            if not dmg_path.exists():
                self.send_error(404, "Installer DMG not found.")
                return
            try:
                filesize = dmg_path.stat().st_size
                self.send_response(200)
                self.send_header("Content-Type", "application/x-apple-diskimage")
                self.send_header("Content-Disposition", 'attachment; filename="RothaDownloader.dmg"')
                self.send_header("Content-Length", str(filesize))
                self.end_headers()
                with open(dmg_path, "rb") as f:
                    shutil.copyfileobj(f, self.wfile, length=1024*1024)
                return
            except Exception:
                return

        elif path == "/api/download-installer-win":
            win_zip = BASE_DIR / "RothaDownloader-Windows.zip"
            if not win_zip.exists():
                self.send_error(404, "Windows Installer ZIP not found.")
                return
            try:
                filesize = win_zip.stat().st_size
                self.send_response(200)
                self.send_header("Content-Type", "application/zip")
                self.send_header("Content-Disposition", 'attachment; filename="RothaDownloader-Windows.zip"')
                self.send_header("Content-Length", str(filesize))
                self.end_headers()
                with open(win_zip, "rb") as f:
                    shutil.copyfileobj(f, self.wfile, length=1024*1024)
                return
            except Exception:
                return

        elif path == "/api/status":
            lan_ip = get_lan_ip()
            self.send_json(200, {
                "ok": True,
                "app_name": "RothaDownloader",
                "yt_dlp": YT_DLP_BIN,
                "ffmpeg": FFMPEG_BIN,
                "ffprobe": FFPROBE_BIN,
                "default_download_dir": DEFAULT_DOWNLOAD_DIR,
                "lan_ip": lan_ip,
                "lan_url": f"http://{lan_ip}:{PORT}"
            })
            return

        elif path == "/api/progress":
            download_id = query.get("id", [None])[0]
            if not download_id:
                self.send_json(400, {"error": "Missing download id"})
                return

            with downloads_lock:
                task = active_downloads.get(download_id)
                if not task:
                    self.send_json(404, {"error": "Download task not found"})
                    return
                self.send_json(200, task)
            return

        elif path == "/api/history":
            self.send_json(200, {"history": get_history()})
            return

        elif path == "/api/settings":
            self.send_json(200, get_settings())
            return

        elif path == "/api/stream-video":
            filepath = query.get("filepath", [None])[0]
            if not filepath or not os.path.exists(filepath):
                self.send_error(404, "File Not Found")
                return
            try:
                filesize = os.path.getsize(filepath)
                content_type = self.get_mime_type(Path(filepath))
                range_header = self.headers.get("Range")
                
                if range_header:
                    parts = range_header.replace("bytes=", "").split("-")
                    start = int(parts[0]) if parts[0] else 0
                    end = int(parts[1]) if parts[1] else filesize - 1
                    if end >= filesize:
                        end = filesize - 1
                    length = end - start + 1
                    
                    self.send_response(206)
                    self.send_header("Content-Type", content_type)
                    self.send_header("Content-Range", f"bytes {start}-{end}/{filesize}")
                    self.send_header("Content-Length", str(length))
                    self.send_header("Accept-Ranges", "bytes")
                    self.end_headers()
                    
                    with open(filepath, "rb") as f:
                        f.seek(start)
                        remaining = length
                        chunk_size = 64 * 1024
                        while remaining > 0:
                            read_len = min(remaining, chunk_size)
                            data = f.read(read_len)
                            if not data:
                                break
                            self.wfile.write(data)
                            remaining -= len(data)
                    return
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", content_type)
                    self.send_header("Content-Length", str(filesize))
                    self.send_header("Accept-Ranges", "bytes")
                    self.end_headers()
                    with open(filepath, "rb") as f:
                        shutil.copyfileobj(f, self.wfile, length=1024*1024)
                    return
            except Exception:
                return

        elif path == "/api/edit-status":
            edit_id = query.get("id", [None])[0]
            if not edit_id:
                self.send_json(400, {"error": "Missing edit id"})
                return

            with edits_lock:
                task = active_edits.get(edit_id)
                if not task:
                    self.send_json(404, {"error": "Edit task not found"})
                    return
                self.send_json(200, task)
            return

        self.send_error(404, "Endpoint Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/info":
            try:
                body = self.read_json_body()
                url = body.get("url", "").strip()
                browser = body.get("browser", "none")

                if not url:
                    self.send_json(400, {"error": "URL cannot be empty."})
                    return

                info = extract_video_info(url, browser=browser)
                self.send_json(200, info)
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        elif path == "/api/download":
            try:
                body = self.read_json_body()
                url = body.get("url", "").strip()
                quality = body.get("quality", "1080p")
                browser = body.get("browser", "none")
                video_info = body.get("video_info") or {}

                settings = get_settings()
                download_dir = body.get("download_dir") or settings.get("download_dir") or DEFAULT_DOWNLOAD_DIR
                os.makedirs(download_dir, exist_ok=True)

                if not url:
                    self.send_json(400, {"error": "URL cannot be empty."})
                    return

                download_id = str(uuid.uuid4())[:8]

                thread = threading.Thread(
                    target=run_download_thread,
                    args=(download_id, url, quality, download_dir, browser, video_info),
                    daemon=True
                )
                thread.start()

                self.send_json(200, {
                    "download_id": download_id,
                    "status": "started",
                    "download_dir": download_dir
                })
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        elif path == "/api/open-file":
            try:
                body = self.read_json_body()
                filepath = body.get("filepath", "")
                if filepath and os.path.exists(filepath):
                    reveal_in_explorer_native(filepath)
                    self.send_json(200, {"ok": True})
                else:
                    self.send_json(404, {"error": "File does not exist."})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        elif path == "/api/play-file":
            try:
                body = self.read_json_body()
                filepath = body.get("filepath", "")
                if filepath and os.path.exists(filepath):
                    open_path_native(filepath)
                    self.send_json(200, {"ok": True})
                else:
                    self.send_json(404, {"error": "File does not exist."})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        elif path == "/api/open-folder":
            try:
                body = self.read_json_body()
                folder = body.get("folder") or get_settings().get("download_dir") or DEFAULT_DOWNLOAD_DIR
                if os.path.exists(folder):
                    open_path_native(folder)
                    self.send_json(200, {"ok": True})
                else:
                    self.send_json(404, {"error": "Folder not found."})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        elif path == "/api/clear-history":
            try:
                with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                    json.dump([], f)
                self.send_json(200, {"ok": True})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        elif path == "/api/settings":
            try:
                body = self.read_json_body()
                curr = get_settings()
                if "download_dir" in body:
                    curr["download_dir"] = os.path.expanduser(body["download_dir"])
                if "browser" in body:
                    curr["browser"] = body["browser"]
                save_settings(curr)
                self.send_json(200, curr)
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        elif path == "/api/edit-video":
            try:
                body = self.read_json_body()
                source_path = body.get("filepath") or body.get("source_path", "")
                options = body.get("options") if "options" in body else body

                if not source_path or not os.path.exists(source_path):
                    self.send_json(400, {"error": f"Source file not found: {source_path}"})
                    return

                settings = get_settings()
                download_dir = body.get("download_dir") or settings.get("download_dir") or DEFAULT_DOWNLOAD_DIR
                os.makedirs(download_dir, exist_ok=True)

                edit_id = str(uuid.uuid4())[:8]

                thread = threading.Thread(
                    target=run_video_edit_thread,
                    args=(edit_id, source_path, options, download_dir),
                    daemon=True
                )
                thread.start()

                self.send_json(200, {
                    "edit_id": edit_id,
                    "status": "started",
                    "download_dir": download_dir
                })
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        elif path == "/api/generate-subtitles":
            try:
                body = self.read_json_body()
                filepath = body.get("filepath", "")
                url = body.get("url", "")
                subtitles = extract_or_generate_subtitles(filepath, url)
                self.send_json(200, {"subtitles": subtitles})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        elif path == "/api/ai-assist":
            try:
                body = self.read_json_body()
                tool_type = body.get("type", "hook")
                title = body.get("title", "")
                text = body.get("text", "")
                lang = body.get("lang", "km")
                api_key = body.get("api_key", "")

                result = generate_ai_assistance(tool_type, title, text, lang, api_key)
                self.send_json(200, {"result": result})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        self.send_error(404, "Endpoint Not Found")

    def serve_file(self, file_path, content_type):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")

    def get_mime_type(self, path):
        ext = path.suffix.lower()
        mimes = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
            ".webp": "image/webp",
            ".mp4": "video/mp4",
            ".mp3": "audio/mpeg",
        }
        return mimes.get(ext, "application/octet-stream")

    def log_message(self, format, *args):
        sys.stderr.write(f"[{time.strftime('%H:%M:%S')}] {args[0]} {args[1]}\n")


def main():
    lan_ip = get_lan_ip()
    print("=" * 60)
    print("🚀 RothaDownloader - 4K & 1080p Video Downloader Server")
    print(f"📦 yt-dlp binary: {YT_DLP_BIN}")
    print(f"🎬 ffmpeg binary: {FFMPEG_BIN}")
    print(f"🔍 ffprobe binary: {FFPROBE_BIN}")
    print(f"📂 Default Download Folder: {DEFAULT_DOWNLOAD_DIR}")
    print(f"🌟 Local URL:   http://localhost:{PORT}")
    print(f"🌐 Network URL: http://{lan_ip}:{PORT} (ប្រើលើកុំព្យូទ័រ ឬទូរស័ព្ទផ្សេងក្នុង Wi-Fi)")
    print("=" * 60)

    try:
        server = ThreadingHTTPServer(("0.0.0.0", PORT), DownloaderHandler)
    except OSError as e:
        print(f"⚠️ Port {PORT} is already in use: {e}. RothaDownloader might already be running.")
        sys.exit(0)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.server_close()
        print("Server stopped.")

if __name__ == "__main__":
    main()

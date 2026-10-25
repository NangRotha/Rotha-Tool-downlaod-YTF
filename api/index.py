from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

def detect_platform(url):
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "tiktok.com" in url_lower:
        return "tiktok"
    elif "facebook.com" in url_lower or "fb.watch" in url_lower or "fb.com" in url_lower:
        return "facebook"
    return "generic"

def format_duration(seconds):
    if not seconds or seconds <= 0:
        return "--:--"
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hrs > 0:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"

def build_quality_options(platform, max_height, available_heights):
    options = []
    if platform == "youtube":
        if max_height >= 2160 or 2160 in available_heights:
            options.append({"id": "4k", "label": "4K Ultra HD (2160p)", "resolution": "3840x2160", "badge": "4K UHD"})
        if max_height >= 1440 or 1440 in available_heights:
            options.append({"id": "1440p", "label": "2K Quad HD (1440p)", "resolution": "2560x1440", "badge": "2K QHD"})
        if max_height >= 1080 or 1080 in available_heights:
            options.append({"id": "1080p", "label": "Full HD (1080p)", "resolution": "1920x1080", "badge": "1080p FHD"})
        if max_height >= 720 or 720 in available_heights:
            options.append({"id": "720p", "label": "HD (720p)", "resolution": "1280x720", "badge": "720p HD"})
        options.append({"id": "480p", "label": "SD (480p)", "resolution": "854x480", "badge": "480p"})
        options.append({"id": "mp3", "label": "Audio Only (MP3 320kbps)", "resolution": "Audio", "badge": "MP3"})
    elif platform == "tiktok":
        options.append({"id": "best", "label": "TikTok HD (No Watermark)", "resolution": f"HD ({max_height}p)" if max_height else "Original HD", "badge": "HD Watermark-Free"})
        options.append({"id": "mp3", "label": "TikTok Audio (MP3)", "resolution": "Audio", "badge": "MP3"})
    elif platform == "facebook":
        if max_height >= 1080:
            options.append({"id": "1080p", "label": "Facebook 1080p Full HD", "resolution": "1920x1080", "badge": "1080p FHD"})
        options.append({"id": "best", "label": "Facebook HD (Best Quality)", "resolution": f"{max_height}p HD" if max_height else "HD", "badge": "HD"})
        if max_height >= 720:
            options.append({"id": "720p", "label": "Facebook 720p HD", "resolution": "1280x720", "badge": "720p"})
        options.append({"id": "mp3", "label": "Facebook Audio (MP3)", "resolution": "Audio", "badge": "MP3"})
    else:
        options.append({"id": "best", "label": "Best Available Quality", "resolution": f"{max_height}p" if max_height else "Best", "badge": "Best"})
        if max_height >= 1080:
            options.append({"id": "1080p", "label": "1080p Full HD", "resolution": "1080p", "badge": "1080p"})
        if max_height >= 720:
            options.append({"id": "720p", "label": "720p HD", "resolution": "720p", "badge": "720p"})
        options.append({"id": "mp3", "label": "Audio Only (MP3)", "resolution": "Audio", "badge": "MP3"})

    if not options:
        options = [
            {"id": "best", "label": "Best Quality (Auto)", "resolution": "HD", "badge": "Auto"},
            {"id": "mp3", "label": "Audio Only (MP3)", "resolution": "Audio", "badge": "MP3"}
        ]
    return options

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        route_name = params.get('route', [''])[0].strip('/')
        path = parsed.path

        if route_name == "status" or path == "/api/status" or path.endswith("status"):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": True,
                "app_name": "RothaDownloader",
                "is_cloud": True,
                "cloud_provider": "Vercel",
                "message": "RothaDownloader Cloud Edition is online."
            }).encode('utf-8'))
            return

        elif route_name == "history" or path == "/api/history" or path.endswith("history"):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"history": []}).encode('utf-8'))
            return

        elif route_name == "settings" or path == "/api/settings" or path.endswith("settings"):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "download_dir": "Downloads",
                "browser_cookies": "none"
            }).encode('utf-8'))
            return

        elif "download-installer" in route_name or "download-installer" in path:
            self.send_response(302)
            self.send_header('Location', 'https://github.com/NangRotha/Rotha-Tool-downlaod-YTF/releases')
            self.end_headers()
            return

        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": True,
                "app_name": "RothaDownloader",
                "is_cloud": True
            }).encode('utf-8'))
            return

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        route_name = params.get('route', [''])[0].strip('/')
        path = parsed.path

        if route_name == "settings" or path == "/api/settings":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode('utf-8'))
            return

        # Matches /api/info as called by frontend
        elif route_name in ["info", "fetch-info"] or path in ["/api/info", "/api/fetch-info"] or "info" in route_name:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                url = data.get('url', '').strip()
                if not url:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'URL cannot be empty.'}).encode('utf-8'))
                    return

                import yt_dlp
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'skip_download': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    if not info:
                        raise Exception("Could not fetch video metadata.")

                    thumb = info.get("thumbnail")
                    thumbnails = info.get("thumbnails", [])
                    if thumbnails:
                        thumb = thumbnails[-1].get("url") or thumb

                    formats = info.get("formats", [])
                    max_height = 0
                    available_heights = set()
                    for f in formats:
                        h = f.get("height")
                        if h and isinstance(h, int):
                            available_heights.add(h)
                            if h > max_height:
                                max_height = h

                    platform = detect_platform(url)
                    quality_options = build_quality_options(platform, max_height, available_heights)

                    response = {
                        "id": info.get("id"),
                        "title": info.get("title") or "Unknown Title",
                        "uploader": info.get("uploader") or info.get("channel") or info.get("creator") or "Unknown Creator",
                        "thumbnail": thumb,
                        "duration": info.get("duration"),
                        "duration_formatted": format_duration(info.get("duration")),
                        "platform": platform,
                        "max_height": max_height,
                        "quality_options": quality_options,
                        "webpage_url": info.get("webpage_url") or url,
                        "is_cloud": True
                    }

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode('utf-8'))
            return

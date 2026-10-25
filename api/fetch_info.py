from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
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
                self.wfile.write(json.dumps({'error': 'Missing URL'}).encode('utf-8'))
                return

            import yt_dlp
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise Exception("No video information found")
                
                response = {
                    'title': info.get('title', 'Unknown Title'),
                    'thumbnail': info.get('thumbnail', ''),
                    'duration': info.get('duration', 0),
                    'duration_str': str(info.get('duration', 0)),
                    'uploader': info.get('uploader') or info.get('channel', ''),
                    'formats': [
                        {
                            'format_id': 'best_4k',
                            'label': '🎬 4K UHD (2160p 60fps) + Audio',
                            'resolution': '2160p (4K)',
                            'ext': 'mp4',
                            'type': 'video'
                        },
                        {
                            'format_id': 'best_1080p',
                            'label': '🎬 1080p Full HD (ច្បាស់កម្រិតខ្ពស់)',
                            'resolution': '1080p (FHD)',
                            'ext': 'mp4',
                            'type': 'video'
                        },
                        {
                            'format_id': 'best_720p',
                            'label': '🎬 720p HD (ទំហំស្រាល)',
                            'resolution': '720p (HD)',
                            'ext': 'mp4',
                            'type': 'video'
                        },
                        {
                            'format_id': 'audio_mp3',
                            'label': '🎵 MP3 Audio 320kbps (បទភ្លេងសុទ្ធ)',
                            'resolution': 'Audio Only',
                            'ext': 'mp3',
                            'type': 'audio'
                        }
                    ],
                    'is_cloud': True
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

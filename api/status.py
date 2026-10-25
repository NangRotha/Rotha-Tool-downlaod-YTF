from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            "ok": True,
            "app_name": "RothaDownloader",
            "is_cloud": True,
            "cloud_provider": "Vercel",
            "message": "RothaDownloader Cloud Web Edition is online."
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return

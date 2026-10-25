from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'https://github.com/NangRotha/Rotha-Tool-downlaod-YTF/releases')
        self.end_headers()
        return

"""Tiny local receiver for viewer screenshots (verification only): POST /<name>.png -> web3d/verify/shots/<name>.png. 127.0.0.1:8003."""
import http.server, os, re
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'verify', 'shots'); os.makedirs(OUT, exist_ok=True)
class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*'); self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS'); self.send_header('Access-Control-Allow-Headers', '*')
    def do_OPTIONS(self): self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        name = re.sub(r'[^A-Za-z0-9_.-]', '_', self.path.strip('/')) or 'shot.png'
        data = self.rfile.read(int(self.headers['Content-Length']))
        open(os.path.join(OUT, name), 'wb').write(data)
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b'ok')
http.server.HTTPServer(('127.0.0.1', 8003), H).serve_forever()

"""
Simple HTTP server to serve the frontend and proxy API requests to backend
"""
import http.server
import socketserver
import json
import urllib.request
import urllib.parse

PORT = 3001
API_BASE_URL = "http://127.0.0.1:8000"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/'):
            # Proxy API requests to backend
            path = self.path.replace('/api/', '/')
            try:
                req = urllib.request.Request(f"{API_BASE_URL}{path}")
                with urllib.request.urlopen(req) as response:
                    self.send_response(response.status)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(response.read())
            except Exception as e:
                self.send_response(502)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        elif self.path == '/' or self.path == '/index.html':
            # Serve index.html
            self.path = '/index.html'
            return super().do_GET()
        else:
            return super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            # Proxy POST requests to backend
            path = self.path.replace('/api/', '/')
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                req = urllib.request.Request(
                    f"{API_BASE_URL}{path}",
                    data=post_data,
                    headers={
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    method='POST'
                )
                with urllib.request.urlopen(req) as response:
                    self.send_response(response.status)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(response.read())
            except Exception as e:
                self.send_response(502)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print(f"Starting server at http://localhost:{PORT}")
print(f"API will be proxied to {API_BASE_URL}")
print(f"\nOpen your browser at: http://localhost:{PORT}")

# Change to frontend directory
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    httpd.serve_forever()

import http.server
import socketserver
import os

PORT = 8000
class Handler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    self.path = 'build' + self.path
    if not os.path.isdir(self.path):
      _, ext = os.path.splitext(self.path)
      if ext == '': self.path += '.html'
    super().do_GET()

with socketserver.TCPServer(('', PORT), Handler) as httpd:
  print(f'serving at port {PORT}')
  httpd.serve_forever()

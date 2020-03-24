from http.server import BaseHTTPRequestHandler


class DBRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        if not hasattr(self.server, '_dry_bread'):
            self.send_response(555)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<p>Dry bread is undefined</p>".encode("UTF-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", self.server.get_dry_bread_mime())
            self.end_headers()
            self.wfile.write(self.server.get_dry_bread().encode("UTF-8"))
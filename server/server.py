from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from config import cfg
import handlers


class KanyeAPIHandler(BaseHTTPRequestHandler):

    api_root = cfg["SERVER"]["API_ROOT"]

    def do_GET(self):
        self.parsed_path = urlparse(self.path)
        if self.parsed_path.path == (self.api_root + "/quotes"):
            handlers.QuotesHandler(self)
        else:
            self.send_error(404,'Hey, what do you mean?')

    def do_POST(self):
        self.parsed_path = urlparse(self.path)
        if self.parsed_path.path == (self.api_root + "/sentiment"):
            handlers.SentimentHandler(self)
        else:
            self.send_error(404,'Hey, what do you mean?')


if __name__ == "__main__":
    host = cfg["SERVER"]["HOST"]
    port = int(cfg["SERVER"]["PORT"])
    httpd = HTTPServer((host, port), KanyeAPIHandler)

    print("Started Kanye API at http://%s:%s" % (host, port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Server stopped.")

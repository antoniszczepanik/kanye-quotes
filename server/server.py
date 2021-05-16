from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import functools

from config import cfg, project_root
import handlers


class KanyeHTTPHandler(SimpleHTTPRequestHandler):

    api_root = cfg["SERVER"]["API_ROOT"]

    def do_GET(self):
        self.parsed_path = urlparse(self.path)
        if self.api_root not in self.parsed_path.path:
            # Let's just serve index.html file if it's not an API call.
            # Superclass provides that functionality with the default
            # implementation.
            super().do_GET()
        elif self.parsed_path.path == (self.api_root + "/quotes"):
            handlers.QuotesHandler(self)
        else:
            self.send_error(404, 'Hey, what do you mean?')

    def do_POST(self):
        self.parsed_path = urlparse(self.path)
        if self.parsed_path.path == (self.api_root + "/sentiment"):
            handlers.SentimentHandler(self)
        else:
            self.send_error(404, 'Hey, what do you mean?')


if __name__ == "__main__":
    host = cfg["SERVER"]["HOST"]
    port = int(cfg["SERVER"]["PORT"])
    client_directory = str(project_root.joinpath("client"))
    # As handler is initialized by HTTPServer we cannot supply directory
    # parameter directly. Hence the trick below.
    handler = functools.partial(KanyeHTTPHandler, directory=client_directory)
    httpd = HTTPServer((host, port), handler)
    print("Started Kanye Server at http://%s:%s" % (host, port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")

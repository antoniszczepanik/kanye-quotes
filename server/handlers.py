from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler
import json
import re
import requests

from config import cfg


class BaseHandler(ABC):

    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler
        if not self.validate():
            self.handler.send_error(400, "Bad request")
        else:
            self.respond(self.get_response())

    @abstractmethod
    def validate(self) -> bool:
        """ Should return bool indicating if request is valid. """
        pass

    @abstractmethod
    def get_response(self) -> dict:
        """ Should return a dictionary that will be parsed as json response """
        pass

    def respond(self, response: dict):
        self.handler.send_response(200)
        self.handler.send_header('Content-Type', 'application/json')
        self.handler.end_headers()
        response_encoded = json.dumps(response).encode(encoding='utf_8')
        self.handler.wfile.write(response_encoded)


class QuotesHandler(BaseHandler):
    number_query_pattern = re.compile(r'^number=(?P<number>[0-9]{1,2})$')
    min_quotes = int(cfg["SERVER"]["MIN_QUOTES"])
    max_quotes = int(cfg["SERVER"]["MAX_QUOTES"])

    def validate(self) -> bool:
        # Is this a valid number query?
        match = re.match(self.number_query_pattern, self.handler.parsed_path.query)
        if not match:
            return False
        # Is value within supported range?
        self.quote_n = int(match.group("number"))
        if self.quote_n < self.min_quotes or self.quote_n > self.max_quotes:
            return False
        return True

    def get_response(self) -> dict:
        return {
            "quotes": ["quote1", "quote2"]
        }


class SentimentHandler(BaseHandler):

    def validate(self) -> bool:
        # Is content type JSON?
        if self.handler.headers["Content-Type"] != "application/json":
            return False
        # Is there any content at all?
        if not self.handler.headers["Content-Length"]:
            return False
        content_length = int(self.handler.headers["Content-Length"])
        post_data = self.handler.rfile.read(content_length)
        # Is json valid?
        try:
            self.post_data = json.loads(post_data.decode("utf-8"))
        except ValueError:
            return False
        # Is there only a single field
        if not self.post_data.get("quotes") or len(self.post_data) != 1:
            return False
        return True

    def get_response(self) -> dict:
        return self.post_data

from abc import ABC, abstractmethod
from http.server import SimpleHTTPRequestHandler
import json
import re
import requests
import time

from config import cfg
import async_utils


class BaseHandler(ABC):

    def __init__(self, handler: SimpleHTTPRequestHandler):
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
        """ Should return a dictionary that will send as a json response. """
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
        try:
            quote_texts = async_utils.get_unique_responses_async(
                self.quote_n,
                cfg["SERVER"]["KANYE_HOST"],
            )
        except requests.exceptions.RequestException as e:
            self.handler.send_error(500, 'Kanye API may have some problems...')
        return {
            "quotes": [json.loads(q)["quote"] for q in quote_texts]
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

        # Quotes need to be a list
        if not isinstance(self.post_data["quotes"], list):
            return False
        return True

    def get_response(self) -> dict:
        data_to_post = [{"text": q} for q in self.post_data["quotes"]]
        try:
            responses = async_utils.post_data_async(
                data_to_post,
                cfg["SERVER"]["SENTIM_HOST"],
            )
        except requests.exceptions.RequestException as e:
            self.handler.send_error(500, ' Sentim API may have some problems...')

        jsons = [r.json() for r in responses]
        quote_polarity = {
            j["sentences"][0]["sentence"]: float(j["result"]["polarity"]) for j in jsons
        }
        return self.construct_counts_response(quote_polarity)

    def construct_counts_response(self, quote_polarity):
        response = {
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "most_extreme": None,
        }
        most_extreme_polarity = 0
        for quote, polarity in quote_polarity.items():
            if polarity > 0:
                response["positive_count"] += 1
            elif polarity < 0:
                response["negative_count"] += 1
            else:
                response["neutral_count"] += 1
            if abs(polarity) > most_extreme_polarity:
                response["most_extreme"] = quote
                most_extreme_polarity = abs(polarity)
        return response

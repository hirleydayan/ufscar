"""Twitter."""
import json
import logging

from random import uniform
from tweepy import OAuthHandler
from tweepy.streaming import Stream
from tweepy.streaming import StreamListener

KEY_PUB_TOPIC = "pub_topic"


class StdOutListener(StreamListener):
    """A listener handles tweets that are received from the stream."""

    def __init__(self, fields, publishers):
        """Constructor."""
        self.logger = logging.getLogger()
        self.fields = fields
        self.publishers = publishers
        self.control = {}
        for pub in publishers:
            pub.connect()

    def on_data(self, data):
        """On data."""
        self.parse_tweet(json.loads(data))
        return True

    def on_error(self, status):
        """On error."""
        self.logger.debug(status)

    def _extract(self, data, path):
        if type(data) == dict:
            cur = path[0]
            if cur not in data:
                self.logger.debug("Key not found: %s" % cur)
                return None
            if len(path) == 1:
                return data[cur]
            else:
                path.pop(0)
                return self._extract(data[cur], path)
        elif type(data) == list:
            values = []
            for obj in data:
                values.append(self, self._extract(obj, path))
            return values

    def extract(self, data, path):
        """Extractor."""
        return self._extract(data, path.split("."))

    def parse_tweet(self, content):
        """Parser."""
        # Extract data
        twitter_data = {}
        result = {}

        for key in self.fields:
            values = self.extract(content, key)

            key = key.replace(".", "_")
            if key == "geo_coordinates" and values is None:
                values = [uniform(-23.580001, -23.589999),
                          uniform(-47.520001, -47.529999)]
            twitter_data[key] = values

        if twitter_data is not None:
            result["twitter"] = twitter_data
            self.logger.debug("Result: '%s'", json.dumps(result))
            for pub in self.publishers:
                topic = pub.get_connection_data(KEY_PUB_TOPIC)
                pub.publish(topic, json.dumps(result))


class Twitter(StreamListener):
    """Twitter class."""

    def __init__(self, settings, publishers):
        """Constructor."""
        if "consumer_key" not in settings:
            raise ValueError("consumer_key must not be None")
        if "consumer_secret" not in settings:
            raise ValueError("consumer_secret must not be None")
        if "access_token" not in settings:
            raise ValueError("access_token must not be None")
        if "access_secret" not in settings:
            raise ValueError("access_secret must not be None")
        if "fields" not in settings:
            raise ValueError("access_secret must not be None")

        self.auth = OAuthHandler(settings["consumer_key"],
                                 settings["consumer_secret"])
        self.auth.set_access_token(settings["access_token"],
                                   settings["access_secret"])

        twitter_stream = Stream(self.auth,
                                StdOutListener(settings["fields"], publishers))
        twitter_stream.filter(track=settings["post_strings"])

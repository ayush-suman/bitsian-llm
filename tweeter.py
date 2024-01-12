import config
import requests
from requests_oauthlib import OAuth1
from datetime import datetime
import schedule
import sys
from cache import cache_last_tweet
import json


class Tweet:
    def __init__(self, id, text, time):
        self.id = id
        self.text = text
        self.time = time

    def follow_up(self, text: str):
        return tweet(text, self.id)


def tweet(text: str, reply_to = None) -> Tweet:
    try:
        oauth = OAuth1(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET, config.TWITTER_ACCESS_TOKEN,
                       config.TWITTER_ACCESS_SECRET,
                       signature_type='auth_header', signature_method='HMAC-SHA1')

        request_json = {"text": text}
        if reply_to is not None:
            request_json["reply"] = {"in_reply_to_tweet_id": reply_to}

        r = requests.post("https://api.twitter.com/2/tweets",
                          json=request_json,
                          auth=oauth,
                          headers={'content-type': 'application/json', 'accept': 'application/json'})

        r_json = json.loads(r.text)
        print(r_json, file=sys.stdout)
        now = datetime.now()

        tweet_id = r_json["data"]["id"]
        tweet_text = r_json["data"]["text"]

        cache_last_tweet(tweet_text, now)
        return Tweet(id=tweet_id, text=tweet_text, time=now)
    except Exception as e:
        print("Error: ", e, file=sys.stderr)
        raise e


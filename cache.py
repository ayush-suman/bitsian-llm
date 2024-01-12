from datetime import timedelta

import redis as redis
import config
import json
import sys

redis_client = redis.StrictRedis(host=config.REDIS_HOST, port=int(config.REDIS_PORT), charset="utf-8",
                                 decode_responses=True)


def cache_last_day_summary(day_summary, today):
    try:
        redis_client.set('day_summary', json.dumps({"date": today.strftime("%B %d, %Y"), "summary": day_summary}))
        return True
    except Exception as e:
        print("Error: ", e, file=sys.stderr)
        return False


def retrieve_last_day_summary(today):
    try:
        data = json.loads(redis_client.get('day_summary'))
        if data["date"] == (today - timedelta(days=1)).strftime("%B %d, %Y"):
            return data["summary"]
        else:
            return ""
    except Exception as e:
        print("Error: ", e, file=sys.stderr)
        return ""


def cache_last_tweet(tweet, time):
    try:
        redis_client.set('tweet', json.dumps({"time": time.strftime("%H:%M"), "tweet": tweet}))
        return True
    except Exception as e:
        print("Error: ", e, file=sys.stderr)
        return False


def retrieve_last_tweet():
    try:
        return redis_client.get('tweet')
    except Exception as e:
        print("Error: ", e, file=sys.stderr)
        return False

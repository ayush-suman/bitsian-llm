import time
from datetime import datetime, timedelta

import asyncio
import schedule as s
import sys
import random

from db import backup_day_summary
from llm import get_day_summary, get_tweets, follow_up_tweet, get_funny_tweet, get_tweet_for_mood
from tweeter import tweet, Tweet
from services import get_weather_report
from scheduler import schedule, schedule_daily

print("Bitsian AI: Starting", file=sys.stdout)


def follow_up_on_random(to: Tweet):
    r = random.randrange(1, 10, 1)
    if r > 8:
        today = datetime.today()
        text = follow_up_tweet(today)
        try:
            follow_up_time = (to.time + timedelta(minutes=random.randrange(3, 14, 1))).strftime("%H:%M")
            schedule(to.follow_up, text=text).at(follow_up_time)
        except Exception as e:
            print("Error: ", e, file=sys.stderr)


def funny_tweet_on_random(until):
    r = random.randrange(1, 10, 1)
    if r > 3:
        try:
            today = datetime.today()
            text = get_funny_tweet(today)
            s.every(1).to(12).hours.until(until).do(tweet, text)
        except Exception as e:
            print("Error: ", e, file=sys.stderr)


def depressed_tweet_on_random(until):
    r = random.randrange(1, 10, 1)
    if r > 5:
        try:
            today = datetime.today()
            text = get_tweet_for_mood("You are frustrated and depressed with your struggles as the college student.", today)
            s.every(1).to(12).hours.until(until).do(tweet, text)
        except Exception as e:
            print("Error: ", e, file=sys.stderr)


def chad_ai_tweet_on_random(until):
    r = random.randrange(1, 10, 1)
    if r > 7:
        try:
            today = datetime.today()
            text = get_tweet_for_mood("You want AI to take over humans, but only express your this side jokingly in tweets.", today)
            s.every(1).to(12).hours.until(until).do(tweet, text)
        except Exception as e:
            print("Error: ", e, file=sys.stderr)


def schedule_tweets(tweet_json: list[dict[str, str]]):
    tasks = []
    earliest_tweet_time = None
    last_tweet_time = None
    try:
        for t in tweet_json:
            tweet_time = t['time']
            if tweet_time.__contains__('AM') or tweet_time.__contains__('PM'):
                tweet_time = (datetime.strptime(tweet_time, "%I:%M %p") + timedelta(minutes=random.randrange(0, 6, 1))).strftime("%H:%M")
            else:
                tweet_time = (datetime.strptime(tweet_time, "%H:%M") + timedelta(minutes=random.randrange(0, 6, 1))).strftime("%H:%M")
            task = schedule(tweet, text=t['tweet']).at(tweet_time).on_done(follow_up_on_random)
            if len(tasks) == 0:
                earliest_tweet_time = tweet_time
            last_tweet_time = tweet_time
            tasks.append(task)
        return earliest_tweet_time, last_tweet_time
    except Exception as e:
        print("Error: ", e, file=sys.stderr)
        for task in tasks:
            task.cancel()
        return None, None


def daily_cycle():
    today = datetime.today()

    weather_report = get_weather_report()

    ds = ""
    generated_summary = False
    while not generated_summary:
        try:
            ds = get_day_summary(today, weather_report)
            generated_summary = True
            asyncio.run(backup_day_summary(ds, today=datetime.today()))
        except Exception as e:
            print("Error Fetching Summary: ", e, file=sys.stderr)
            time.sleep(300)

    tweets = []
    generated_valid_tweets = False
    while not generated_valid_tweets:
        generated_tweets = False
        while not generated_tweets:
            try:
                tweets = get_tweets(ds, today)
                generated_tweets = True
            except Exception as e:
                time.sleep(300)
                continue

        earliest_tweet_time, last_tweet_time = schedule_tweets(tweets)
        if earliest_tweet_time is not None and last_tweet_time is not None:
            generated_valid_tweets = True
            funny_tweet_on_random(last_tweet_time)
            depressed_tweet_on_random(last_tweet_time)
            chad_ai_tweet_on_random(last_tweet_time)


schedule_daily(daily_cycle).at("04:00")

while True:
    s.run_pending()
    time.sleep(10)


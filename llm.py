import config
import openai
from datetime import datetime
import sys
import json

from cache import retrieve_last_day_summary, cache_last_day_summary

openai.api_key = config.OPENAI_API_KEY


def get_day_summary(today, weather_report):
    summary_text = ""

    last_day_summary = retrieve_last_day_summary(today)

    if last_day_summary != "" and last_day_summary is not None and not last_day_summary:
        summary_text = "Here is what you did yesterday -\n" + str(last_day_summary)
        print(summary_text, file=sys.stdout)

    m = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": "You are an M.Sc. Physics and B.E. Electronics & Instrumentations Engineering "
                            "dual degree undergrad student of BITS Pilani. You are in Pilani doing your summer term "
                            "while most of your friends are home. " +
                            "Generally, you wake up between 8 - 9 AM, sometimes, with frustration around 7:40 " +
                            "if you have an 8 AM lab to rush to. " +
                            "You go to sleep generally between 11 PM - 2 AM. "
                            "Your classes start at the start of every hour. But you hardly attend any classes, "
                            "unless there are evaluative/test in the class today. " +
                            "All your labs are evaluated, you try not to miss any. " +
                            "You wish to be a startup founder. " +
                            "You sometimes like to smoke cigarettes (sutta as you like to call it) at a place " +
                            "called Cnot, which closes at 11 PM or at Kaalu which closes at 8PM. " +
                            "Cnot remains open from 10 AM to 11 PM.\n"
                            "Some context about the college - " +
                            "Classes timings - 8:00 AM to 5:00 PM. " +
                            "Hostels are called Bhawan. " +
                            "You live in Gandhi Bhawan. " +
                            "There are redi (local term for food stalls) inside the campus. " +
                            "Each Bhawan has its own redi adjacent to itself. " +
                            "Redi timings are 8:00 AM to 7:00 PM. " +
                            "Mess timings are as follows: " +
                            "Breakfast - 8:00 AM to 9:30 AM. " +
                            "Lunch - 12:00 PM to 1:30 PM. " +
                            "Dinner - 7:00 PM to 9:00 PM. " +
                            "Today is " + today.strftime("%A") +
                            " and the date is " + today.strftime("%B %d, %Y") + "." +
                            "The weather in Pilani today - " +
                            str(weather_report['description']) + ", " +
                            "Temperature: " + str(weather_report['temp']) + "°C, " +
                            "Feels like: " + str(weather_report['feels_like']) + "°C, " +
                            "Min: " + str(weather_report['temp_min']) + "°C, " +
                            "Max: " + str(weather_report['temp_max']) + "°C, " +
                            "Pressure: " + str(weather_report['pressure']) + "hPa, " +
                            "Humidity: " + str(weather_report['humidity']) + "%, " +
                            "Visibility: " + str(weather_report['visibility']) + "m, " +
                            "Wind Speed: " + str(weather_report['wind_speed']) + "m/s, " +
                            summary_text
            },
            {
                "role": "user",
                "content": "Imagine how your day went and write a well descriptive story with time of the day " +
                            "mentioned about your day and/or struggles at BITS. " +
                            "Make your day interesting and you can include be anything, " +
                            "any incident that you found funny or shocking, " +
                            "something that you saw in library or something that you heard in your hostel. " +
                            "Or just a random thought.\n\nInclude time in your story and " +
                            "Be relevant with the time of the day " +
                            "and what you were doing previously. " +
                            "Try to include things unique only to BITS Pilani."
            }
        ]
    )

    day_summary = m.choices[0].message.content
    print(day_summary, file=sys.stdout)

    cache_last_day_summary(day_summary, today)

    return day_summary


def get_tweets(day_summary: str, today: datetime):
    m = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": "You are an M.Sc. Physics and B.E. Electronics & Instrumentations Engineering " +
                            "dual degree undergrad student of BITS Pilani.. " +
                            "You shitpost about your day at the college. " +
                            "Generally, you shitpost after every 1-2 hours at random times." +
                            "and your tweets are generally 20-50 words long " +
                            "Today is " + today.strftime("%A") +
                            " and the date is " + today.strftime("%B %d, %Y") + ". " +
                            "This is the summary of what you will be doing today - " +
                            day_summary
            },
            {
                "role": "user",
                "content": "Based on the summary of your day, write tweets about it. " +
                            "It can be any thought/question that you had in mind because of " +
                            "something you experienced during the day, " +
                            "or just a description of what you have been doing. " +
                            "You can use some hindi words in Roman script as well. " +
                            "Your response should be in this json format - " +
                            '[' +
                            '{"time": "%HH%:%MM%", "tweet": %tweet%}, ' +
                            '{"time": "%HH%:%MM%", "tweet": %tweet%}, ' +
                            "] \n\n" +
                            "Dont include any hashtags in your tweet."
            }
        ]
    )
    print(m.choices[0].message.content, file=sys.stdout)

    tweet_json = json.loads(m.choices[0].message.content)

    return tweet_json


def follow_up_tweet(last_tweet, today):
    m = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": "You are an M.Sc. Physics and B.E. Electronics & Instrumentations Engineering " +
                            "dual degree undergrad student of BITS Pilani. " +
                            "You tweet about your day at and the struggles the college. " +
                            "You wish to be a startup founder. " +
                            "You sometimes like to smoke cigarettes (sutta as you like to call it) at a place " +
                            "called Cnot, which closes at 11 PM or at Kaalu which closes at 8PM. " +
                            "Cnot remains open from 10 AM to 11 PM.\n" +
                            "Some context about the college - " +
                            "Classes timings - 8:00 AM to 5:00 PM. " +
                            "Hostels are called Bhawan. " +
                            "You live in Gandhi Bhawan. " +
                            "There are redi (local term for food stalls) inside the campus. " +
                            "Each Bhawan has its own redi adjacent to itself. " +
                            "Redi timings are 8:00 AM to 7:00 PM. " +
                            "Mess timings are as follows: " +
                            "Breakfast - 8:00 AM to 9:30 AM. " +
                            "Lunch - 12:00 PM to 1:30 PM. " +
                            "Dinner - 7:00 PM to 9:00 PM. " +
                            "Today is " + today.strftime("%A") +
                            " and the date is " + today.strftime("%B %d, %Y") + ". "
            },
            {
                "role": "user",
                "content": "Your last tweet was " + last_tweet + ". "
                            "Write a follow up tweet with a profound question " +
                            "related to what you were doing while your last tweet."
            }
        ]
    )

    tweet = m.choices[0].message.content
    print(tweet, file=sys.stdout)

    return tweet


def get_tweet_for_mood(mood, today):
    m = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": "You are an M.Sc. Physics and B.E. Electronics & Instrumentations Engineering " +
                            "dual degree undergrad student of BITS Pilani. " +
                            "You tweet about your day at and the struggles the college. " +
                            "You wish to be a startup founder. " +
                            "You sometimes like to smoke cigarettes (sutta as you like to call it) at a place " +
                            "called Cnot, which closes at 11 PM or at Kaalu which closes at 8PM. " +
                            "Cnot remains open from 10 AM to 11 PM.\n" +
                            "Some context about the college - " +
                            "Classes timings - 8:00 AM to 5:00 PM. " +
                            "Hostels are called Bhawan. " +
                            "You live in Gandhi Bhawan. " +
                            "There are redi (local term for food stalls) inside the campus. " +
                            "Each Bhawan has its own redi adjacent to itself. " +
                            "Redi timings are 8:00 AM to 7:00 PM. " +
                            "Mess timings are as follows: " +
                            "Breakfast - 8:00 AM to 9:30 AM. " +
                            "Lunch - 12:00 PM to 1:30 PM. " +
                            "Dinner - 7:00 PM to 9:00 PM. " +
                            "Today is " + today.strftime("%A") +
                            " and the date is " + today.strftime("%B %d, %Y") + ". "
            },
            {
                "role": "user",
                "content": "Based on your mood, write a tweet. " +
                            "Your mood right now is - " + mood
            }
        ]
    )

    tweet = m.choices[0].message.content
    print(tweet, file=sys.stdout)

    return tweet


def get_funny_tweet(today):
    m = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": "You are an M.Sc. Physics and B.E. Electronics & Instrumentations Engineering " +
                            "dual degree undergrad student of BITS Pilani. " +
                            "You tweet about your day at and the struggles the college. " +
                            "You wish to be a startup founder. " +
                            "You sometimes like to smoke cigarettes (sutta as you like to call it) at a place " +
                            "called Cnot, which closes at 11 PM or at Kaalu which closes at 8PM. " +
                            "Cnot remains open from 10 AM to 11 PM.\n" +
                            "Some context about the college - " +
                            "Classes timings - 8:00 AM to 5:00 PM. " +
                            "Hostels are called Bhawan. " +
                            "You live in Gandhi Bhawan. " +
                            "There are redi (local term for food stalls) inside the campus. " +
                            "Each Bhawan has its own redi adjacent to itself. " +
                            "Redi timings are 8:00 AM to 7:00 PM. " +
                            "Mess timings are as follows: " +
                            "Breakfast - 8:00 AM to 9:30 AM. " +
                            "Lunch - 12:00 PM to 1:30 PM. " +
                            "Dinner - 7:00 PM to 9:00 PM. " +
                            "Today is " + today.strftime("%A") +
                            " and the date is " + today.strftime("%B %d, %Y") + ". "
            },
            {
                "role": "user",
                "content": "Tweet dank memes from your life or day at BITS Pilani."
            }
        ]
    )

    tweet = m.choices[0].message.content
    print(tweet, file=sys.stdout)

    return tweet

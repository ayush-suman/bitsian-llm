import os

from requests_oauthlib import OAuth1
import requests
import openai

TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]

TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]

TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]

TWITTER_ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Get Text from OpenAI model
openai.api_key = OPENAI_API_KEY
m = openai.Completion.create(
    model="text-davinci-003",
    max_tokens=100,
    prompt="You are a student of BITS Pilani. You tweet about your typical GenZ struggles at BITS. Write a random tweet for the same. Try to include things unique only to BITS Pilani."
)

print(m)

oauth = OAuth1(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET,  signature_type='auth_header', signature_method='HMAC-SHA1')

r = requests.post("https://api.twitter.com/2/tweets",
                  json={"text": m.choices[0].text},
                  auth=oauth,
                  headers={'content-type': 'application/json', 'accept': 'application/json'})

print(r.content)

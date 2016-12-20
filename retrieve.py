#!/usr/bin/env python
"""This script connects and extract from Twitter more messages (tweets) as json file
"""
import json
import time
import configparser
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterRestPager
from datetime import timedelta

start = time.time()
print("starting to retrieve tweets...")

configValues = configparser.RawConfigParser()
configValues.read(r'.\config.ini')

TWITTER_API = TwitterAPI(configValues.get('TwitterSettings', 'consumer_key'),
                         configValues.get('TwitterSettings', 'consumer_secret'),
                         configValues.get('TwitterSettings', 'access_token_key'),
                         configValues.get('TwitterSettings', 'access_token_secret'))

TWITTER_PAGER = TwitterRestPager(TWITTER_API, \
                                'search/tweets', \
                                {'q':'#webapi', 'count':10, 'lang': 'en'})

response = []
unique_tweets = []
itemId = 1

# black list items: exclude all items referring to job ads
rejected_words = ['hir', 'need help', 'developer', 'contact', 'job']

for item in TWITTER_PAGER.get_iterator():
    if 'user' in item and 'text' in item:
        found_words = [c for c in rejected_words if c in item['text'].lower()]
        if len(found_words) == 0 and item['text'] not in unique_tweets:
            response.append({'Id': itemId,
                             'Username': item['user']['name'],
                             'ScreenName': '@{}'.format(item['user']['screen_name']),
                             'ProfileImage': item['user']['profile_image_url_https'],
                             'ProfileDescription': item['user']['description'],
                             'Text': item['text']})
            unique_tweets.append(item['text'])
            itemId += 1

    elif 'message' in item and item['code'] == 88:
        print('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
        break

    # limit the number of tweets retrieved
    if len(response) > 50:
        break

with open(r'.\twitter.json', 'w') as outfile:
    json.dump(response, outfile, indent=4)

end = time.time()
print('found %d tweets in %s' % (len(response), str(timedelta(seconds=end-start))))

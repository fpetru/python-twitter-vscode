#!/usr/bin/env python
"""This script connects and extract from Twitter more messages (tweets) as json file
"""
import json
import configparser 
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterRestPager

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
for item in TWITTER_PAGER.get_iterator():
    if 'user' in item and 'text' in item:
        response.append({'username': item['user']['name'],
                         'screen_name': '@{}'.format(item['user']['screen_name']),
                         'profile_image': item['user']['profile_image_url_https'],
                         'profile_description': item['user']['description'],
                         'text': item['text']})
    elif 'message' in item and item['code'] == 88:
        print('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
        break

    if len(response) > 5:
        break

with open(r'.\twitter.txt', 'w') as outfile:
    json.dump(response, outfile, indent=4)

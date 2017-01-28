#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy

# Consumer keys and access tokens, used for OAuth
consumer_key = 'WRfBUeBTe9zCFRLy4RISjvrnb'
consumer_secret = 'X7qPhTUvIOFDUz5IFk3JFKxSs0qIawhbzyWmH7e0l4QT2XWSXF'
access_token = '281220629-YPbm5d7cW1EutThP9qqemK3JNcr5o1vwAwDAuo4Z'
access_token_secret = 'Mm4PGuLr3SFleBW9a7jcSfX2dDmQSiImZKhTv0wtDM7TU'

# Connect API Twitter and
def connectAPI():
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)

    return api

# Get Tweets for geolocation
def getTweets():
    # Connect to API
    api = connectAPI()

    # Search Tweet of Granada
    tweets = api.search(q='Granada', geocode='37.1886273389356,-3.5907775816,80km', count=100)
    return tweets

# Get Tweets for Hashtag
def getTweetsForHashtag():
    # Connect to API
    api = connectAPI()

    # Get #hashtag TrendingTopic Spain
    tweets = api.trends_place(23424950)

    return tweets

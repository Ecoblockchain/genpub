#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy

def get_secrets(fn):
  secrets = {}
  with open(fn, 'r') as f:
    for line in f.readlines():
      k, v = line.strip().split(';')
      secrets[k] = v
  return secrets

def tweet_with_media(filename, secrets, status=None):
  auth = tweepy.OAuthHandler(secrets['CONSUMER_KEY'], secrets['CONSUMER_SECRET'])
  auth.set_access_token(secrets['ACCESS_TOKEN'], secrets['ACCESS_TOKEN_SECRET'])
  api = tweepy.API(auth)
  api.update_with_media(filename=filename, status=status)


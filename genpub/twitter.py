#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy

def _get_secrets(fn):
  secrets = {}
  with open(fn, 'r') as f:
    for line in f.readlines():
      k, v = line.strip().split(';')
      secrets[k] = v
  return secrets

def _tweet_with_media(
    filename,
    secrets,
    status=None,
    rid=None
    ):
  auth = tweepy.OAuthHandler(
      secrets['CONSUMER_KEY'],
      secrets['CONSUMER_SECRET']
      )
  auth.set_access_token(
      secrets['ACCESS_TOKEN'],
      secrets['ACCESS_TOKEN_SECRET']
      )
  api = tweepy.API(auth)
  tid = api.update_with_media(
      filename=filename,
      status=status,
      in_reply_to_status_id=rid
      )
  return tid


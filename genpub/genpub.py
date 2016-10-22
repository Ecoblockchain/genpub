# -*- coding: utf-8 -*-

from __future__ import print_function

TWITTER_SECRET_FILE = 'twitter_tokens.txt'

def _get_short_name(name):
  from os import sep
  if sep in name:
    sn = name.split(sep)[-1]
  else:
    sn = name
  return sn

class Genpub:
  def __init__(
      self,
      ):
    from os import sep
    from os import path
    from .drive import _get_service
    from .drive import _ensure_folder

    self.realpath = path.dirname(path.realpath(__file__))
    rel = sep + '..' + sep + 'secrets' + sep
    self.secretpath = self.realpath + rel

    self.service = _get_service(self.secretpath)
    self.root_id = _ensure_folder(self.service)

    self.twitter_size = 1200

  def __enter__(self):
    return self

  def __exit__(self, t, value, traceback):
    return False

  def pub_drive(self, name):
    from apiclient.http import MediaFileUpload
    from .drive import _move

    # TODO: add git repo info?
    description = 'uploaded with genpub.'

    sn = _get_short_name(name)
    media = MediaFileUpload(
        name,
        resumable=True
        )
    file = self.service.files().create(
        body={
            'name' : sn,
            'description': description
            },
        media_body=media,
        fields='id'
        ).execute()
    uploaded_id = file.get('id')
    moved_file = _move(self.service, self.root_id, uploaded_id)
    return [moved_file]

  def pub_twitter(self, name, status, rid):
    from .twitter import _get_secrets
    from .twitter import _tweet_with_media
    from .img import _twitter_version

    size = self.twitter_size
    if name.endswith('.png'):
      tname = _twitter_version(name, size)
    else:
      tname = name

    if tname:
      secrets = _get_secrets(self.secretpath + TWITTER_SECRET_FILE)
      status = _tweet_with_media(tname, secrets, status, rid)
      self.pub_drive(name)
      return [status]
    else:
      print('error when publishing to twitter')
      return []


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

## google drive related code is adapted from google examples.

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json

APPLICATION_NAME = 'genpub'
SCOPES = 'https://www.googleapis.com/auth/drive.file'
DRIVE_CLIENT_SECRET_FILE = 'secrets/client_secret.json'
TWITTER_SECRET_FILE = 'secrets/twitter_tokens.txt'

ROOT_NAME = 'genpub'
ROOT_META = {
    'name' : ROOT_NAME,
    'mimeType' : 'application/vnd.google-apps.folder'
    }

class Genpub(object):

  def __init__(
      self,
      ):
    import os
    self._get_service()
    self._ensure_folder()
    self.realpath = os.path.dirname(os.path.realpath(__file__))

  def __enter__(self):
    return self

  def __exit__(self, t, value, traceback):
    return False

  def _get_service(self):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
      Credentials, the obtained credential.
    """
    import os
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
      os.makedirs(credential_dir)
    credential_path = os.path.join(
        credential_dir,
        'drive-python-quickstart.json'
        )

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
      flow = client.flow_from_clientsecrets(DRIVE_CLIENT_SECRET_FILE, SCOPES)
      flow.user_agent = APPLICATION_NAME
      credentials = tools.run_flow(flow, store)
      print('Storing credentials to ' + credential_path)

    http = credentials.authorize(httplib2.Http())
    self.service = discovery.build('drive', 'v3', http=http)

  def _ensure_folder(self):

    results = self.service.files().list(q="name='{:s}'".format(ROOT_NAME)).execute()
    items = results.get('files', [])
    for item in items:
      if item['name'] == ROOT_NAME:
        root_id = item['id']
        self.root_id = root_id
        return
    else:
      file = self.service.files().create(
          body=ROOT_META,
          fields='id'
          ).execute()
      self.root_id = file.get('id')

  def _move(self, fid):
    service = self.service
    uploaded_file = service.files().get(
        fileId=fid,
        fields='parents'
        ).execute()
    previous_parents = ",".join(uploaded_file.get('parents'))
    moved_file = service.files().update(
        fileId=fid,
        addParents=self.root_id,
        removeParents=previous_parents,
        fields='id, parents'
        ).execute()
    return moved_file

  def _get_short_name(self, name):
    from os import sep
    if sep in name:
      sn = name.split(sep)[-1]
    else:
      sn = name
    return sn

  def pub_drive(self, name):
    from apiclient.http import MediaFileUpload

    # TODO: add git repo info?
    description = 'uploaded with genpub.'

    sn = self._get_short_name(name)
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
    self._move(uploaded_id)

  def pub_twitter(self, name, status):
    from .tweet import get_secrets
    from .tweet import tweet_with_media
    from os import sep

    self.pub_drive(name)

    # hack ...
    rel = sep + '..' + sep
    secrets = get_secrets(self.realpath + rel + TWITTER_SECRET_FILE)
    tweet_with_media(name, secrets, status)


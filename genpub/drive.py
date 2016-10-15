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
DRIVE_CLIENT_SECRET_FILE = 'client_secret.json'

ROOT_NAME = 'genpub'
ROOT_META = {
    'name' : ROOT_NAME,
    'mimeType' : 'application/vnd.google-apps.folder'
    }

def _get_service(secretpath):
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
      'drive-python-genpub.json'
      )

  store = Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args('')
    flow = client.flow_from_clientsecrets(
        secretpath + DRIVE_CLIENT_SECRET_FILE,
        SCOPES
        )
    flow.user_agent = APPLICATION_NAME
    credentials = tools.run_flow(flow, store, flags=flags)
    print('Storing credentials to ' + credential_path)
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('drive', 'v3', http=http)
  return service

def _ensure_folder(service):
  results = service.files().list(q="name='{:s}'".format(ROOT_NAME)).execute()
  items = results.get('files', [])
  for item in items:
    if item['name'] == ROOT_NAME:
      root_id = item['id']
      return root_id
  else:
    file = service.files().create(
        body=ROOT_META,
        fields='id'
        ).execute()
    root_id = file.get('id')
    return root_id

def _move(service, root_id, fid):
  uploaded_file = service.files().get(
      fileId=fid,
      fields='parents'
      ).execute()
  previous_parents = ",".join(uploaded_file.get('parents'))
  moved_file = service.files().update(
      fileId=fid,
      addParents=root_id,
      removeParents=previous_parents,
      fields='id, parents'
      ).execute()
  return moved_file


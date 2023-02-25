import requests
import hashlib
import mimetypes

from requests_oauthlib import OAuth1Session
from django.conf import settings


def get_auth_session():
  return OAuth1Session(settings.SMUGMUG_CREDENTIALS["app_key"],
                       settings.SMUGMUG_CREDENTIALS["app_secret"],
                       settings.SMUGMUG_CREDENTIALS["user_token"],
                       settings.SMUGMUG_CREDENTIALS["user_secret"])


def upload_data(album_key, filename, img_data):
  headers = {
      'X-Smug-ResponseType': 'JSON',
      'X-Smug-Version': 'v2',
      'X-Smug-AlbumUri': album_key,
      'X-Smug-FileName': filename,
      'Content-Length': str(len(img_data)),
      'Content-Type': mimetypes.guess_type(filename)[0],
      'Content-MD5': hashlib.md5(img_data).hexdigest()
  }
  r = get_auth_session().post("https://upload.smugmug.com/",
                              headers=headers,
                              data=img_data)
  return r.json()['Image']['ImageUri']
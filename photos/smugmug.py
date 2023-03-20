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


def get_image_link(json, image_size):
  try:
    return json['ImageSizeDetails'][image_size]['Url']
  except KeyError:  # tiny image and there was none at that size
    return get_largest_image(json)


def get_largest_image(json):
  biggest = json['ImageSizeDetails']['LargestImageSize']
  return get_image_link(json, biggest)


def get_largest_link(image_uri):
  headers = {'X-Smug-Version': 'v2', 'Accept': 'application/json'}

  url = "https://api.smugmug.com" + image_uri + "!largestimage"

  r = get_auth_session().get(url, headers=headers)
  json = r.json()['Response']
  return json['LargestImage']['Url']


def get_small_link(image_uri):
  headers = {'X-Smug-Version': 'v2', 'Accept': 'application/json'}

  url = "https://api.smugmug.com" + image_uri + "!sizedetails?PrefetchSizes=Medium"

  r = get_auth_session().get(url, headers=headers)
  json = r.json()['Response']
  return get_image_link(json, 'ImageSizeSmall')


# Responds with a tuple that is name, uri
def get_album_from_url(gallery_url):
  headers = {'X-Smug-Version': 'v2', 'Accept': 'application/json'}

  params = {"WebUri": gallery_url}
  url = "https://api.smugmug.com/api/v2!weburilookup"

  r = get_auth_session().get(url, params=params, headers=headers)
  json = r.json()['Response']
  return (json['Album']['Name'], json['Album']['Uri'])

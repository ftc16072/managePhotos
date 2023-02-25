from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Album, Photo
from . import smugmug


def upload(request, album_id):
  album = get_object_or_404(Album, pk=album_id)
  if request.method == 'POST' and request.FILES['upload']:
    upload = request.FILES['upload']
    photo_uri = smugmug.upload_data(album.smugmug_uri, upload.name,
                                    upload.read())
    photo = Photo()
    photo.album = album
    photo.smugmug_uri = photo_uri
    photo.save()

    return render(request, 'photos/upload.html', {
        'album': album,
        'key': photo_uri
    })

  return render(request, 'photos/upload.html', {'album': album})


def search(request):
  return HttpResponse("Photo Search")
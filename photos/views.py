from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Album
from . import smugmug


def upload(request, album_id):
  album = get_object_or_404(Album, pk=album_id)
  if request.method == 'POST' and request.FILES['upload']:
    upload = request.FILES['upload']
    photo_key = smugmug.upload_data(album.smugmug_key, upload.name,
                                    upload.read())
    return render(request, 'photos/upload.html', {
        'album': album,
        'key': photo_key
    })

  return render(request, 'photos/upload.html', {'album': album})


def search(request):
  return HttpResponse("Photo Search")
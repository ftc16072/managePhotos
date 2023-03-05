from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Album, Photo, Tag
from . import smugmug


def upload(request, album_id):
  album = get_object_or_404(Album, pk=album_id)

  context = {"album":  album, 
             "tags" : Tag.objects.filter(album=album).order_by('name')}

  if request.method == 'POST' and request.FILES['upload']:
    upload = request.FILES['upload']
    photo_uri = smugmug.upload_data(album.smugmug_uri, upload.name,
                                    upload.read())
    photo = Photo()
    photo.album = album
    photo.smugmug_uri = photo_uri
    photo.description = request.POST['description']
    photo.save()
    if 'tags' in request.POST:
      photo.tags.set(request.POST['tags'])
  
    if 'newTags' in request.POST:
      for tagString in request.POST['newTags'].split(' '):
        lowerTag = tagString.lower()
        tagObjects = Tag.objects.filter(name=lowerTag, album=album)
        if tagObjects:
          tag = tagObjects[0]
        else:
          tag = Tag()
          tag.name = lowerTag
          tag.album = album
          tag.save()
        photo.tags.add(tag)

    context["key"] = photo_uri;

  return render(request, 'photos/upload.html', context)


def search(request):
  return HttpResponse("Photo Search")
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Album, Photo, Tag, Team
from . import smugmug


@login_required
def team_admin(request, team_id):
  team = get_object_or_404(Team, pk=team_id)
  context = {"team": team}

  if not team.admin_on_team(request.user):
    return render(request, 'photos/no_admin_permission.html', context)
  return render(request, "photos/admin_team.html", context)


@login_required
def profile(request):
  context = {
      'teams': [
          team for team in Team.objects.all() if team.user_on_team(request.user)
      ],
      'admin_teams': [
          team for team in Team.objects.all()
          if team.admin_on_team(request.user)
      ]
  }

  return render(request, 'photos/profile.html', context)


@login_required
def upload(request, album_id):
  album = get_object_or_404(Album, pk=album_id)

  if not album.team.user_on_team(request.user):
    context = {"team": album.team}

    return render(request, 'photos/no_album_permission.html', context)

  context = {
      "album": album,
      "tags": Tag.objects.filter(album=album).order_by('name')
  }

  if request.method == 'POST' and request.FILES['upload']:
    upload = request.FILES['upload']
    photo_uri = smugmug.upload_data(album.smugmug_uri, upload.name,
                                    upload.read())
    photo = Photo()
    photo.album = album
    photo.smugmug_uri = photo_uri
    photo.description = request.POST['description']
    photo.uploaded_by = request.user
    photo.save()

    set_tags(photo, album, request.POST)

    context["key"] = photo_uri

  return render(request, 'photos/upload.html', context)


def set_tags(photo, album, post_data):
  photo.tags.clear()
  if 'tags' in post_data:
    tags = dict(post_data)['tags']
    for tag in tags:
      photo.tags.add(tag)

  if 'newTags' in post_data:
    for tagString in post_data['newTags'].split(' '):
      lowerTag = tagString.lower().strip()
      if lowerTag:
        tagObjects = Tag.objects.filter(name=lowerTag, album=album)
        if tagObjects:
          tag = tagObjects[0]
        else:
          tag = Tag()
          tag.name = lowerTag
          tag.album = album
          tag.save()
        photo.tags.add(tag)


@login_required
def edit(request, album_id, photo_id):
  photo = get_object_or_404(Photo, pk=photo_id)
  album = photo.album

  if not album.team.user_on_team(request.user):
    context = {"team": album.team}
    return render(request, 'photos/no_album_permission.html', context)

  context = {
      "photo": photo,
      "album": album,
      "tags": Tag.objects.filter(album=album).order_by('name')
  }
  if request.method == 'POST':
    photo.description = request.POST['description']
    set_tags(photo, album, request.POST)
    photo.save()

  return render(request, 'photos/edit.html', context)


@login_required
def search(request, album_id):
  album = get_object_or_404(Album, pk=album_id)

  if not album.team.user_on_team(request.user):
    context = {"team": album.team}
    return render(request, 'photos/no_album_permission.html', context)

  context = {
      "album": album,
      "tags": Tag.objects.filter(album=album).order_by('name')
  }
  if request.method == 'POST':
    queryDict = dict(request.POST)
    include_tags = queryDict[
        'include_tags'] if 'include_tags' in queryDict else []
    search = queryDict['search']

    if search == 'any':
      context['photos'] = Photo.objects.filter(album=album,
                                               tags__in=include_tags)
    else:
      context['photos'] = Photo.objects.filter(album=album)
      for tag in include_tags:
        context['photos'] = context['photos'].filter(tags=tag)

    if 'exclude_tags' in request.POST:
      exclude_tags = queryDict['exclude_tags']
      for tag in exclude_tags:
        context['photos'] = context['photos'].exclude(tags=tag)

  return render(request, 'photos/search.html', context)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from users.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

from .models import Album, Photo, Tag, Team
from . import smugmug


@login_required
def team_admin(request, team_id):
  team = get_object_or_404(Team, pk=team_id)

  context = {
      "team": team,
      "albums": Album.objects.filter(team=team),
      "admins": team.admins.all(),
      "members": team.members.all(),
      "error": ""
  }

  if not team.admin_on_team(request.user):
    return render(request, 'photos/no_admin_permission.html', context)
  if request.method == 'POST':
    if 'smugmug' in request.POST:
      gallery_url = request.POST['smugmug']  # it must be a new gallery one
      try:
        (name, uri) = smugmug.get_album_from_url(gallery_url)
        album = Album()
        album.team = team
        album.name = name
        album.smugmug_uri = uri
        album.is_active = True
        album.save()
        context["albums"] = Album.objects.filter(team=team)
      except KeyError:
        context['error'] = "Couldn't find gallery at URL: " + gallery_url
    else:
      # First, check and see if email already has a user.  If so, just add user to team
      email = request.POST['email']
      user = None
      try:
        user = CustomUser.objects.get(email__exact=email)
      except ObjectDoesNotExist:
        if request.POST['pass1'] == request.POST['pass2']:
          user = CustomUser.objects.create_user(
              first_name=request.POST['first'],
              last_name=request.POST['last'],
              email=request.POST['email'],
              password=request.POST['pass1'])
        else:
          context["error"] = "Passwords must match to create user"
      if user:
        team.members.add(user)
        context['members'] = team.members.all()

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
      "tags": Tag.objects.filter(album=album).order_by('name'),
      "search": "all",
      "include_tags": [],
      "exclude_tags": []
  }
  if request.method == 'POST':
    queryDict = dict(request.POST)
    include_tags = queryDict[
        'include_tags'] if 'include_tags' in queryDict else []
    search = queryDict['search']

    if search == ['any']:
      context['photos'] = Photo.objects.filter(album=album,
                                               tags__in=include_tags)
      context['search'] = 'any'
      for tag in include_tags:
        context['include_tags'].append(int(tag))
    else:
      context['photos'] = Photo.objects.filter(album=album)
      for tag in include_tags:
        context['photos'] = context['photos'].filter(tags=tag)
        context['include_tags'].append(int(tag))

    if 'exclude_tags' in request.POST:
      exclude_tags = queryDict['exclude_tags']
      for tag in exclude_tags:
        context['exclude_tags'].append(int(tag))
        context['photos'] = context['photos'].exclude(tags=tag)
  print(f"Context: {context}")
  return render(request, 'photos/search.html', context)
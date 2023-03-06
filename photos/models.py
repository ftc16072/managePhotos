from django.db import models
from . import smugmug


class Team(models.Model):
  name = models.CharField(max_length=200)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    if self.is_active:
      return self.name
    return 'INACTIVE: ' + self.name


class Album(models.Model):
  team = models.ForeignKey(Team, on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  smugmug_uri = models.CharField(max_length=32)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    if self.is_active:
      return self.name
    return 'INACTIVE: ' + self.name


class Tag(models.Model):
  name = models.CharField(max_length=64)
  album = models.ForeignKey(Album, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  class Meta:
    unique_together = [['name', 'album']]

class Photo(models.Model):
  album = models.ForeignKey(Album, on_delete=models.CASCADE)
  smugmug_uri = models.CharField(max_length=32)
  photo_link = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  tags = models.ManyToManyField(Tag, blank=True)

  def __str__(self):
    return 'IMG: ' + self.smugmug_uri

  def get_photo_link(self):
    if self.photo_link == "":
      self.photo_link = smugmug.get_small_link(self.smugmug_uri)
      self.save()
    return self.photo_link

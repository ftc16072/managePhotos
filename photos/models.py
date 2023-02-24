from django.db import models


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
  smugmug_key = models.CharField(max_length=16)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    if self.is_active:
      return self.name
    return 'INACTIVE: ' + self.name


class Photo(models.Model):
  album = models.ForeignKey(Album, on_delete=models.CASCADE)
  smugmug_key = models.CharField(max_length=16)
  medium_link = models.CharField(max_length=255)
  description = models.CharField(max_length=255)

  def __str__(self):
    return 'IMG: ' + self.smugmug_key


class Tags(models.Model):
  name = models.CharField(max_length=64)
  album = models.ForeignKey(Album, on_delete=models.CASCADE)
  photos = models.ManyToManyField(Photo)

  def __str__(self):
    return self.name

  class Meta:
    unique_together = [['name', 'album']]

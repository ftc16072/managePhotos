from django.contrib import admin

from .models import Team, Album, Photo, Tag

admin.site.register(Team)
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Tag)

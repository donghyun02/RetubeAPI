from django.contrib import admin

# Register your models here.
from playlist.models import Playlist, Song

admin.site.register(Playlist)
admin.site.register(Song)
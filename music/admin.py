from django.contrib import admin
from django.utils.html import format_html
from .models import Artist, Album, Song, Playlist, Genre

# Register your models here
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Playlist)


# Convert to mp3


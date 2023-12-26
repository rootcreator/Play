from django.contrib import admin
from .models import Genre, Artist, Album, Song, Playlist, UserProfile, UserLibrary

# Register your models here
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(UserProfile)
admin.site.register(UserLibrary)

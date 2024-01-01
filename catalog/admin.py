from django.contrib import admin
from .models import Genre, Artist, Album, Song, Composer

admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Composer)
admin.site.register(Album)
admin.site.register(Song)

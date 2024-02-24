from django.contrib import admin
from .models import RecommendedSongs, Like

admin.site.register(RecommendedSongs)
admin.site.register(Like)


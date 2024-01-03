from django.contrib import admin
from django.utils.html import format_html

from .models import Genre, Artist, Composer, Album, Song, Playlist, UserProfile, UserLibrary, AudioFile
import ffmpeg

# Register your models here
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Composer)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(UserProfile)
admin.site.register(UserLibrary)


# Convert to mp3

class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_audio_player')

    def display_audio_player(self, obj):
        if obj.audio_file:
            audio_url = obj.audio_file.url
            return format_html('<audio controls><source src="{}" type="audio/mpeg"></audio>', audio_url)
        else:
            return "No audio file"

    display_audio_player.short_description = 'Audio Player'


admin.site.register(AudioFile, AudioFileAdmin)

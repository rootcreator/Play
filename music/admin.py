from django.contrib import admin
from django.utils.html import format_html
from .models import Artist, Album, Song, Playlist, Genre
from django import forms

# Register your models here
admin.site.register(Genre)
admin.site.register(Artist)

admin.site.register(Song)


class AlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.artist:
            self.fields['songs'].queryset = self.instance.artist.songs.all()

    class Meta:
        model = Album
        fields = '__all__'


class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm
    filter_horizontal = ('songs',)


admin.site.register(Album, AlbumAdmin)


class PlaylistAdmin(admin.ModelAdmin):
    filter_horizontal = ('songs',)


admin.site.register(Playlist, PlaylistAdmin)


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



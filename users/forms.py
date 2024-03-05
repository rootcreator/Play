from django import forms
from music.models import Song, Album


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'audio_file', 'genre', 'cover_image']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'genre', 'cover_image']
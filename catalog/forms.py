from django import forms
from .models import Song, Album

class SongForm(forms.ModelForm):
	class Meta:
		model = Song
		fields = ['title', 'artist', 'genre', 'audio_file']


class AlbumForm(forms.ModelForm):
	class Meta:
		model = Album
		fields = ['title', 'artist', 'genre', 'songs']
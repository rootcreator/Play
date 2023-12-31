from django import forms
from catalog.models import Artist, Genre, Album, Song


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'cover_image', 'genre']


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'album', 'cover_image', 'audio_file']

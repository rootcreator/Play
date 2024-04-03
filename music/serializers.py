from rest_framework import serializers
from .models import Genre, Artist, Song, Album, Playlist, GenreRadio, ArtistRadio


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'




class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'


class GenreRadioSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreRadio
        fields = '__all__'


class ArtistRadioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistRadio
        fields = '__all__'

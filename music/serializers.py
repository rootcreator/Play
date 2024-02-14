from rest_framework import serializers

from users.models import UserProfile
from .models import Genre, Artist, Album, Song, Playlist, UserProfile, UserLibrary, AudioFile
from django.contrib.auth.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLibrary
        fields = '__all__'


class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    music_user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'music_user_profile']


# Serializer for Spotify results
class SpotifySerializer(serializers.Serializer):
    spotify_songs = serializers.ListField(child=serializers.JSONField())
    spotify_albums = serializers.ListField(child=serializers.JSONField())
    spotify_artists = serializers.ListField(child=serializers.JSONField())


# Serializer for combining local and Spotify results
class SearchResultsSerializer(serializers.Serializer):
    local_results = serializers.DictField()
    spotify_results = SpotifySerializer()


class UserProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

from rest_framework import serializers
from .models import UserProfile, UserLibrary, UserProfileView
from music.models import Song, Album, Artist, Playlist
from django.contrib.auth.models import User


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'  # or specify individual fields

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'  # or specify individual fields

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'  # or specify individual fields

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'  # or specify individual fields

class UserProfileSerializer(serializers.ModelSerializer):
    saved_songs = SongSerializer(many=True, read_only=True)
    saved_albums = AlbumSerializer(many=True, read_only=True)
    favorite_artists = ArtistSerializer(many=True, read_only=True)
    uploaded_songs = SongSerializer(many=True, read_only=True)
    created_playlists = PlaylistSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'  # or specify individual fields

class UserLibrarySerializer(serializers.ModelSerializer):
    saved_songs = SongSerializer(many=True)
    saved_albums = AlbumSerializer(many=True)
    favorite_artists = ArtistSerializer(many=True)

    class Meta:
        model = UserLibrary
        fields = '__all__'  # or specify individual fields

class UserProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileView
        fields = '__all__'  # Include all fields or specify individual fields
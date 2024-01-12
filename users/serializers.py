from rest_framework import serializers
from django.contrib.auth.models import User
from music.models import Song, Artist, Playlist, Album
from .models import UserProfile, UserLibrary, ListeningHistory  # Add import for ListeningHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'


class ListeningHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningHistory
        fields = ('id', 'user_library', 'song', 'listened_at')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    saved_songs = SongSerializer(many=True)
    saved_albums = AlbumSerializer(many=True)
    favorite_artists = ArtistSerializer(many=True)
    created_playlists = PlaylistSerializer(many=True)
    recently_played = ListeningHistorySerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'profile_picture', 'bio', 'view_count', 'last_viewed',
                  'saved_songs', 'saved_albums', 'favorite_artists', 'created_playlists', 'recently_played')


class UserLibrarySerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    saved_songs = SongSerializer(many=True)
    saved_albums = AlbumSerializer(many=True)
    favorite_artists = ArtistSerializer(many=True)
    created_playlists = PlaylistSerializer(many=True)
    recently_played = ListeningHistorySerializer(many=True)

    class Meta:
        model = UserLibrary
        fields = ('id', 'user_profile', 'saved_songs', 'saved_albums', 'favorite_artists', 'created_playlists', 'recently_played')

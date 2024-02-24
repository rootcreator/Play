from rest_framework import serializers
from .models import SimilarPlaylists, SimilarReleases, Favourites, RecommendedSongs, Feeds, Like


class SimilarPlaylistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarPlaylists
        fields = '__all__'


class SimilarReleasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarReleases
        fields = '__all__'


class TrendsSerializer(serializers.Serializer):
    popular_songs = serializers.ListField(child=serializers.CharField())
    popular_albums = serializers.ListField(child=serializers.CharField())
    popular_artists = serializers.ListField(child=serializers.CharField())


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'


class RecommendedSongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedSongs
        fields = '__all__'


class FeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeds
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

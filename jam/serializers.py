from rest_framework import serializers
from .models import RecommendedPlaylists, SimilarReleases, Trends, Favourites, Recommended, Feeds


class RecommendedPlaylistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedPlaylists
        fields = '__all__'


class SimilarReleasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarReleases
        fields = '__all__'


class TrendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trends
        fields = '__all__'


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'


class RecommendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommended
        fields = '__all__'


class FeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeds
        fields = '__all__'

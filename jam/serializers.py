import rest_framework
from .models import RecommendedPlaylists, SimilarReleases, Trends, Recommended, Feeds


class RecommendedPlaylistsSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = RecommendedPlaylists
        fields = '__all__'


class SimilarReleasesSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = SimilarReleases
        fields = '__all__'


class TrendsSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Trends
        fields = '__all__'



class RecommendedSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Recommended
        fields = '__all__'


class FeedsSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Feeds
        fields = '__all__'

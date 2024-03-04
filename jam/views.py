from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jam.serializers import Recommended, SimilarReleasesSerializer, TrendsSerializer, \
    RecommendedSerializer, FeedsSerializer
from users.models import Profile
from .models import RecommendedPlaylists, SimilarReleases, Trends, Favourites, Recommended, Feeds
from .services.billboardrecommendation import get_trendrecommendations
from .services.recommendation_utils import recommend_songs, get_recommendations


class TrendsAPIView(APIView):
    def get(self, request):
        trends = Trends.objects.all()
        serializer = TrendsSerializer(trends, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TrendsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendedAPIView(APIView):
    def get(self, request):
        recommended = Recommended.objects.all()
        serializer = RecommendedSerializer(recommended, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecommendedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedsAPIView(APIView):
    def get(self, request):
        feeds = Feeds.objects.all()
        serializer = FeedsSerializer(feeds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FeedsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Recommendation
class RecommendationView(APIView):
    def get(self, request, user_id):
        try:
            user_profile = Profile.objects.get(id=user_id)
            recommendations = get_combined_recommendations(user_profile)
            return Response(recommendations, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_combined_recommendations(user_profile):
    try:
        # Retrieve recommendations for songs and albums separately
        recommended_songs = get_song_recommendations(user_profile)
        recommended_albums = get_album_recommendations(user_profile)

        # Combine the recommendations
        combined_recommendations = {
            'recommended_songs': recommended_songs,
            'recommended_albums': recommended_albums
        }

        return combined_recommendations
    except Exception as e:
        raise e


def get_song_recommendations(user_profile):
    # Your logic to retrieve recommended songs
    recommended_songs = []
    # Add logic to fetch recommended songs for the user_profile
    return recommended_songs


def get_album_recommendations(user_profile):
    # Your logic to retrieve recommended albums
    recommended_albums = []
    # Add logic to fetch recommended albums for the user_profile
    return recommended_albums


class SongRecommendationView(APIView):
    def get(self, request, user_id):
        try:
            user_profile = Profile.objects.get(id=user_id)
            recommended_songs = recommend_songs(user_profile)
            return Response({'recommended_songs': recommended_songs}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlaylistRecommendationView(APIView):
    def get(self, request, user_id):
        try:
            user_profile = Profile.objects.get(id=user_id)
            recommended_playlists = []  # Placeholder for recommended playlists
            return Response({'recommended_playlists': recommended_playlists}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlbumRecommendationView(APIView):
    def get(self, request, user_id):
        try:
            user_profile = Profile.objects.get(id=user_id)
            similar_releases = SimilarReleases.objects.all()
            recommended_albums = [album.name for album in similar_releases.albums.all()]
            return Response({'recommended_albums': recommended_albums}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TrendingRecommendationView(APIView):
    def get(self, request, user_id):
        try:
            user_profile = Profile.objects.get(id=user_id)
            recommendations, integration_status = get_trendrecommendations(user_profile.user)
            return Response({'recommendations': recommendations, 'integration_status': integration_status},
                            status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
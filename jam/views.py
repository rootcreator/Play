from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import SimilarPlaylists, SimilarReleases, Trends, Favourites, RecommendedSongs, Feeds, Like
from .serializers import SimilarPlaylistsSerializer, SimilarReleasesSerializer, TrendsSerializer, FavouritesSerializer, \
    RecommendedSongsSerializer, FeedsSerializer, LikeSerializer


class SimilarPlaylistsList(APIView):
    def get(self, request):
        playlists = SimilarPlaylists.objects.all()
        serializer = SimilarPlaylistsSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SimilarPlaylistsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SimilarPlaylistsDetail(APIView):
    def get_object(self, pk):
        try:
            return SimilarPlaylists.objects.get(pk=pk)
        except SimilarPlaylists.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        playlist = self.get_object(pk)
        serializer = SimilarPlaylistsSerializer(playlist)
        return Response(serializer.data)

    def put(self, request, pk):
        playlist = self.get_object(pk)
        serializer = SimilarPlaylistsSerializer(playlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        playlist = self.get_object(pk)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# SimilarReleases Views
class SimilarReleasesList(APIView):
    def get(self, request):
        releases = SimilarReleases.objects.all()
        serializer = SimilarReleasesSerializer(releases, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SimilarReleasesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SimilarReleasesDetail(APIView):
    def get_object(self, pk):
        try:
            return SimilarReleases.objects.get(pk=pk)
        except SimilarReleases.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        release = self.get_object(pk)
        serializer = SimilarReleasesSerializer(release)
        return Response(serializer.data)

    def put(self, request, pk):
        release = self.get_object(pk)
        serializer = SimilarReleasesSerializer(release, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        release = self.get_object(pk)
        release.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Trends Views
class TrendsList(APIView):
    def get(self, request):
        popular_songs = Trends.get_popular_songs()
        popular_albums = Trends.get_popular_albums()
        popular_artists = Trends.get_popular_artists()
        serializer = TrendsSerializer({
            'popular_songs': popular_songs,
            'popular_albums': popular_albums,
            'popular_artists': popular_artists
        })
        return Response(serializer.data)


# Favourites Views
class FavouritesList(APIView):
    def get(self, request):
        favourites = Favourites.objects.all()
        serializer = FavouritesSerializer(favourites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavouritesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavouritesDetail(APIView):
    def get_object(self, pk):
        try:
            return Favourites.objects.get(pk=pk)
        except Favourites.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        favourite = self.get_object(pk)
        serializer = FavouritesSerializer(favourite)
        return Response(serializer.data)

    def put(self, request, pk):
        favourite = self.get_object(pk)
        serializer = FavouritesSerializer(favourite, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        favourite = self.get_object(pk)
        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# RecommendedSongs Views
class RecommendedSongsList(APIView):
    def get(self, request):
        recommended_songs = RecommendedSongs.objects.all()
        serializer = RecommendedSongsSerializer(recommended_songs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecommendedSongsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendedSongsDetail(APIView):
    def get_object(self, pk):
        try:
            return RecommendedSongs.objects.get(pk=pk)
        except RecommendedSongs.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        recommended_song = self.get_object(pk)
        serializer = RecommendedSongsSerializer(recommended_song)
        return Response(serializer.data)

    def put(self, request, pk):
        recommended_song = self.get_object(pk)
        serializer = RecommendedSongsSerializer(recommended_song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recommended_song = self.get_object(pk)
        recommended_song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Feeds Views
class FeedsList(APIView):
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


class FeedsDetail(APIView):
    def get_object(self, pk):
        try:
            return Feeds.objects.get(pk=pk)
        except Feeds.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        feed = self.get_object(pk)
        serializer = FeedsSerializer(feed)
        return Response(serializer.data)

    def put(self, request, pk):
        feed = self.get_object(pk)
        serializer = FeedsSerializer(feed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        feed = self.get_object(pk)
        feed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Likes
class LikeListCreate(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

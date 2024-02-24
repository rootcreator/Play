from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Genre, Artist, Album, Song, Playlist, AudioFile, APIMusic
from .search import search
from .serializers import GenreSerializer, ArtistSerializer, AlbumSerializer, SongSerializer, PlaylistSerializer, AudioFileSerializer, UserSerializer, APIMusicViewSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        genre = self.get_object()
        serializer = self.get_serializer(genre)
        return Response(serializer.data)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        artist = self.get_object()
        serializer = self.get_serializer(artist)
        return Response(serializer.data)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        album = self.get_object()
        serializer = self.get_serializer(album)
        return Response(serializer.data)


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        song = self.get_object()
        serializer = self.get_serializer(song)
        return Response(serializer.data)


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        playlist = self.get_object()
        serializer = self.get_serializer(playlist)
        return Response(serializer.data)



class AudioFileViewSet(viewsets.ModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        audio_file = self.get_object()
        serializer = self.get_serializer(audio_file)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class APIMusicViewSet(viewsets.ModelViewSet):
    queryset = APIMusic.objects.all()
    serializer_class = APIMusicViewSerializer

    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        api_music = self.get_object()
        serializer = self.get_serializer(api_music)
        return Response(serializer.data)


# Search
class SearchViewSet(viewsets.ViewSet):
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            search_results = search(query)

            # Serialize search results
            song_serializer = SongSerializer(search_results['songs'], many=True)
            album_serializer = AlbumSerializer(search_results['albums'], many=True)
            genre_serializer = GenreSerializer(search_results['genres'], many=True)
            playlist_serializer = PlaylistSerializer(search_results['playlists'], many=True)
            artist_serializer = ArtistSerializer(search_results['artists'], many=True)

            # Return serialized search results
            return Response({
                'songs': song_serializer.data,
                'albums': album_serializer.data,
                'genres': genre_serializer.data,
                'playlists': playlist_serializer.data,
                'artists': artist_serializer.data,
            })
        else:
            return Response("No query provided", status=status.HTTP_400_BAD_REQUEST)

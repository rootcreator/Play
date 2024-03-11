from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Genre, Artist, Song, Album, Playlist
from .serializers import GenreSerializer, ArtistSerializer, SongSerializer, AlbumSerializer, PlaylistSerializer


class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ArtistListCreate(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class SongListCreate(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class AlbumListCreate(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class PlaylistListCreate(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


"""class GenreRadioListCreate(generics.ListCreateAPIView):
    queryset = GenreRadio.objects.all()
    serializer_class = GenreRadioSerializer


class ArtistRadioListCreate(generics.ListCreateAPIView):
    queryset = ArtistRadio.objects.all()
    serializer_class = ArtistRadioSerializer
"""


class CombinedAPIView(APIView):
    def get(self, request):
        # Fetching both songs and albums
        songs = Song.objects.all()
        albums = Album.objects.all()

        # Combining songs and albums
        combined_data = list(songs) + list(albums)

        # Sorting the combined data by the latest creation date
        sorted_data = sorted(combined_data, key=lambda x: x.created_at, reverse=True)

        # Serialize the sorted data
        serialized_data = SongSerializer(sorted_data, many=True).data

        # Return the serialized data as JSON response
        return Response(serialized_data)


class SearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        local_results = self.search(query)
        return Response(local_results)

    def search(self, query):
        local_results = {
            'songs': SongSerializer(Song.objects.filter(title__icontains=query), many=True).data,
            'albums': AlbumSerializer(Album.objects.filter(title__icontains=query), many=True).data,
            'artists': ArtistSerializer(Artist.objects.filter(name__icontains=query), many=True).data,
            'genres': GenreSerializer(Genre.objects.filter(name__icontains=query), many=True).data,
            'playlists': PlaylistSerializer(Playlist.objects.filter(name__icontains=query), many=True).data,
        }
        return local_results

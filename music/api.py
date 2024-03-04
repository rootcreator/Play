from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Genre, Artist, Album, Song, Playlist, AudioFile
from .serializers import GenreSerializer, ArtistSerializer, AlbumSerializer, SongSerializer, PlaylistSerializer


class GenreListCreateAPIView(generics.ListCreateAPIView):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]


class ArtistListCreateAPIView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]


class AlbumListCreateAPIView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]


class SongListCreateAPIView(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]


class PlaylistListCreateAPIView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]




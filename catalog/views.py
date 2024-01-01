from rest_framework import generics
from .models import Genre, Artist, Composer, Album, Song  # Importing models from current directory
from .serializers import GenreSerializer, ArtistSerializer, ComposerSerializer, AlbumSerializer, SongSerializer  # Importing serializers from current directory


# View for listing and creating Genre objects using Django REST framework
class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()  # Retrieve all Genre objects from the database
    serializer_class = GenreSerializer  # Use GenreSerializer to serialize/deserialize Genre objects


# View for listing and creating Artist objects using Django REST framework
class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()  # Retrieve all Artist objects from the database
    serializer_class = ArtistSerializer  # Use ArtistSerializer to serialize/deserialize Artist objects


# View for listing and creating Composer objects using Django REST framework
class ComposerListCreateView(generics.ListCreateAPIView):
    queryset = Composer.objects.all()  # Retrieve all Composer objects from the database
    serializer_class = ComposerSerializer  # Use ComposerSerializer to serialize/deserialize Composer objects


# View for listing and creating Album objects using Django REST framework
class AlbumListCreateView(generics.ListCreateAPIView):
    queryset = Album.objects.all()  # Retrieve all Album objects from the database
    serializer_class = AlbumSerializer  # Use AlbumSerializer to serialize/deserialize Album objects


# View for listing and creating Song objects using Django REST framework
class SongListCreateView(generics.ListCreateAPIView):
    queryset = Song.objects.all()  # Retrieve all Song objects from the database
    serializer_class = SongSerializer  # Use SongSerializer to serialize/deserialize Song objects


# View for listing and creating Song objects using Django REST framework
class ComposerListCreateView(generics.ListCreateAPIView):
    queryset = Composer.objects.all()  # Retrieve all Song objects from the database
    serializer_class = ComposerSerializer  # Use SongSerializer to serialize/deserialize Song objects
from django.http import HttpResponse
from django.views import View
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Genre, Artist, Album, Song, Playlist, UserProfile, UserLibrary
from .serializers import (
    GenreSerializer,
    ArtistSerializer,
    AlbumSerializer,
    SongSerializer,
    PlaylistSerializer,
    UserProfileSerializer,
    UserLibrarySerializer,
)


# Views for listing and creating resources
class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ArtistList(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class PlaylistList(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserLibraryList(generics.ListCreateAPIView):
    queryset = UserLibrary.objects.all()
    serializer_class = UserLibrarySerializer


# Views for retrieving, updating, or deleting a single resource by ID
class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserLibraryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserLibrary.objects.all()
    serializer_class = UserLibrarySerializer


# Additional views and functionalities can be added as needed

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the user profile of the logged-in user
        return UserProfile.objects.get(user=self.request.user)


class AlbumUploadView(View):
    def post(self, request, *args, **kwargs):
        # Implement your logic for handling album uploads here
        return HttpResponse("Album uploaded successfully")


class SongUploadView(View):
    def post(self, request, *args, **kwargs):
        # Implement your logic for handling song uploads here
        return HttpResponse("Song uploaded successfully")

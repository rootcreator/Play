from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    Genre,
    Artist,
    Album,
    Song,
    Playlist,
    UserProfile,
    UserLibrary,
)
from .serializers import (
    GenreSerializer,
    ArtistSerializer,
    AlbumSerializer,
    SongSerializer,
    PlaylistSerializer,
    UserProfileSerializer,
    UserLibrarySerializer,
)


def index(request):
    # Your view logic here
    return HttpResponse("Index Page")


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserLibraryViewSet(viewsets.ModelViewSet):
    queryset = UserLibrary.objects.all()
    serializer_class = UserLibrarySerializer


class UserProfileDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user.profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class AlbumUploadView(APIView):
    def post(self, request):
        # Logic for handling album uploads
        return HttpResponse("Album uploaded successfully")


class SongUploadView(APIView):
    def post(self, request):
        # Logic for handling song uploads
        return HttpResponse("Song uploaded successfully")


class GenreList(ListView):
    model = Genre


class ArtistList(ListView):
    model = Artist


class AlbumList(ListView):
    model = Album


class SongList(ListView):
    model = Song


class PlaylistList(ListView):
    model = Playlist


class UserProfileList(ListView):
    model = UserProfile


class UserLibraryList(ListView):
    model = UserLibrary


class GenreDetail(DetailView):
    model = Genre


class ArtistDetail(DetailView):
    model = Artist


class AlbumDetail(DetailView):
    model = Album


class SongDetail(DetailView):
    model = Song


class PlaylistDetail(DetailView):
    model = Playlist


class UserProfileDetail(DetailView):
    model = UserProfile


class UserLibraryDetail(DetailView):
    model = UserLibrary


###

def songs_view(request):
    # Your view logic for songs_view here
    return HttpResponse("Songs View")


def albums_view(request):
    # Your view logic for albums_view here
    return HttpResponse("Albums View")


def genres_view(request):
    # Your view logic for genres_view here
    return HttpResponse("Genres View")


def artists_view(request):
    # Your view logic for artists_view here
    return HttpResponse("Artists View")


def user_profile_view(request):
    # Your view logic for user_profile_view here
    return HttpResponse("User Profile View")

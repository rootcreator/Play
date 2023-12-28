import os
import ffmpeg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import (
    Genre, Artist, Album, Song, Playlist, UserProfile,
    UserLibrary, AudioFile
)
from .serializers import (
    GenreSerializer, ArtistSerializer, AlbumSerializer,
    SongSerializer, PlaylistSerializer, UserProfileSerializer,
    UserLibrarySerializer
)
from .search_utils import search
from django_redis import get_redis_connection
from .dropbox_service import DropboxService

redis_conn = get_redis_connection()


# Login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a success page or perform an action upon successful login
            # For example, you can redirect to a profile page:
            return redirect(reverse('music:login'))  # Replace with your actual profile view name
    else:
        form = AuthenticationForm()

    return render(request, 'login.html')



# Search Views
@api_view(['GET'])
def search_api(request):
    query = request.GET.get('q', '')
    local_results, spotify_results = search(query)

    data = {
        'local_results': local_results,
        'spotify_results': spotify_results,
        'query': query,
    }

    return Response(data)


# Audio Conversion View
class AudioConversionAPIView(APIView):
    def post(self, request):
        if request.method == 'POST':
            input_file = request.FILES['audio_file']
            output_file = 'output_audio.mp3'
            temp_file_path = 'temp_audio' + os.path.splitext(input_file.name)[1]

            try:
                with open(temp_file_path, 'wb') as temp_file:
                    for chunk in input_file.chunks():
                        temp_file.write(chunk)

                ffmpeg.input(temp_file_path).output(output_file, codec='libmp3lame', bitrate='320k').run()
                os.remove(temp_file_path)

                with open(output_file, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='audio/mp3')
                    response['Content-Disposition'] = 'attachment; filename="output_audio.mp3"'
                    return response
            except ffmpeg.Error as e:
                os.remove(temp_file_path)
                return HttpResponse(f'Error during audio conversion: {str(e)}', status=500)


# Django REST Framework viewsets
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


# UserProfile Detail View
class UserProfileDetail(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the profile of the authenticated user
        return self.request.user.music_user_profile


# View functions (albums_view, songs_view, genres_view, artists_view, user_profile_view)
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


# Dropbox-related views
# ... (Dropbox related views remain unchanged)


# Redis cache system
def get_popular_songs(request):
    # Connect to Redis
    redis_conn = get_redis_connection("default")

    # Check if data exists in cache
    cached_data = redis_conn.get("popular_songs_cache_key")
    if cached_data:
        return HttpResponse(cached_data)

    # If not in cache, fetch data and store in cache
    popular_songs = Song.objects.filter(popularity__gt=100).all()
    response_data = '\n'.join([song.title for song in popular_songs])

    # Store in cache for 15 minutes
    redis_conn.setex("popular_songs_cache_key", 60 * 15, response_data)

    return HttpResponse(response_data)


# Django REST Framework List API Views for genres, artists, albums, songs, playlists
class GenreList(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ArtistList(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumList(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongList(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class PlaylistList(generics.ListAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class AlbumUploadView(View):
    def post(self, request):
        if 'album_file' in request.FILES:
            album_file = request.FILES['album_file']

            # Process the uploaded file (save it, perform operations, etc.)
            # For example, saving it locally
            with open('path/to/save/album/' + album_file.name, 'wb+') as destination:
                for chunk in album_file.chunks():
                    destination.write(chunk)

            # Create an instance of the Album model and save the details
            new_album = Album(
                title=request.POST.get('title'),  # Assuming 'title' is in the POST data
                artist=request.POST.get('artist'),  # Assuming 'artist' is in the POST data
                # Add more fields as per your Album model
                file_path='path/to/save/album/' + album_file.name  # Save the file path to the database
            )
            new_album.save()  # Save the new album details in the database

            # Return success response
            return HttpResponse("Album uploaded successfully")
        else:
            # Return error response if 'album_file' is not found in request.FILES
            return HttpResponse("No album file found in the request", status=400)


class SongUploadView(View):
    def post(self, request):
        if 'song_file' in request.FILES:
            song_file = request.FILES['song_file']

            # Process the uploaded file (save it, perform operations, etc.)
            # For example, saving it locally
            with open('path/to/save/songs/' + song_file.name, 'wb+') as destination:
                for chunk in song_file.chunks():
                    destination.write(chunk)

            # Create an instance of the Song model and save the details
            new_song = Song(
                title=request.POST.get('title'),  # Assuming 'title' is in the POST data
                artist=request.POST.get('artist'),  # Assuming 'artist' is in the POST data
                genre=request.POST.get('genre'),  # Assuming 'genre' is in the POST data
                # Add more fields as per your Song model
                file_path='path/to/save/songs/' + song_file.name  # Save the file path to the database
            )
            new_song.save()  # Save the new song details in the database

            # Return success response
            return HttpResponse("Song uploaded successfully")
        else:
            # Return error response if 'song_file' is not found in request.FILES
            return HttpResponse("No song file found in the request", status=400)


def index(request):
    # Your logic for the index view here
    return render(request, 'index.html')  # Assuming you have an 'index.html' template

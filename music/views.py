import os

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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
    AudioFile
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
from .dropbox_service import DropboxService
from django_redis import get_redis_connection
import ffmpeg

redis_conn = get_redis_connection()


# audio conversion
def convert_audio(request):
    if request.method == 'POST':
        input_file = request.FILES['audio_file']  # Get the uploaded audio file from the form
        output_file = 'output_audio.mp3'  # Output MP3 file name

        # Save the uploaded file temporarily on the server
        temp_file_path = 'temp_audio' + os.path.splitext(input_file.name)[1]  # Temp file path with the same extension
        with open(temp_file_path, 'wb') as temp_file:
            for chunk in input_file.chunks():
                temp_file.write(chunk)

        try:
            # Run FFmpeg command to perform audio conversion to MP3
            ffmpeg.input(temp_file_path).output(output_file, codec='libmp3lame', bitrate='320k').run()

            # Clean up: Delete temporary input file after conversion
            os.remove(temp_file_path)

            # Send the converted audio file as a response
            with open(output_file, 'rb') as f:
                response = HttpResponse(f.read(), content_type='audio/mp3')
                response['Content-Disposition'] = 'attachment; filename="output_audio.mp3"'
                return response
        except ffmpeg.Error as e:
            # Handle FFmpeg errors during the conversion process
            os.remove(temp_file_path)  # Delete temporary file on error
            return HttpResponse(f'Error during audio conversion: {str(e)}', status=500)

    # Handle GET requests (return a form for uploading audio files)
    return render(request, 'audio_conversion.html')


# Define Index
def index(request):
    # Fetch data from models to display in the index view
    genres = Genre.objects.all()
    artists = Artist.objects.all()
    albums = Album.objects.all()
    songs = Song.objects.all()

    context = {
        'genres': genres,
        'artists': artists,
        'albums': albums,
        'songs': songs,
    }

    return render(request, 'index.html', context)


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


# dropbox views

def upload_to_dropbox(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        file_path = f'/path/to/store/{file.name}'  # Replace with your desired Dropbox path

        # Save the file locally (temporarily)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Upload to Dropbox
        dropbox_service = DropboxService()
        dropbox_service.upload_file(file_path, file)

        # Get the shared link for the uploaded file
        shared_link = dropbox_service.get_shared_link(file_path)

        # Clean up: remove the local file
        # os.remove(file_path)  # Uncomment this line after testing

        return render(request, 'success.html', {'shared_link': shared_link})
    return render(request, 'upload.html')


def upload_song(request):
    if request.method == 'POST' and request.FILES['song_file']:
        song_file = request.FILES['song_file']
        title = request.POST['title']
        artist = request.POST['artist']
        genre = request.POST['genre']

        # Save the file temporarily (locally) before uploading to cloud storage
        file_path = f'/path/to/temp/{song_file.name}'
        with open(file_path, 'wb+') as destination:
            for chunk in song_file.chunks():
                destination.write(chunk)

        # Upload to Dropbox
        dropbox_service = DropboxService()
        dropbox_service.upload_file(file_path, song_file)

        # Get the shared link for the uploaded file
        file_url = dropbox_service.get_shared_link(file_path)

        # Save metadata to the local database
        new_song = Song.objects.create(
            title=title,
            artist=artist,
            genre=genre,
            file_url=file_url
        )
        new_song.save()

        # Clean up: remove the local temporary file
        # os.remove(file_path)  # Uncomment this line after testing

        return redirect('success')  # Redirect to a success page
    return render(request, 'upload.html')  # Render the upload form


# redis cache system
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

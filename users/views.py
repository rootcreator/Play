import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from music.models import Song
from .models import UserProfile, UserLibrary, ListeningHistory
from .serializers import UserProfileSerializer, UserLibrarySerializer, ListeningHistorySerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            # Render HTML page with JavaScript-based rendering
            return render(request, 'profile.html')
        else:
            # Provide JSON API response
            return super().list(request, *args, **kwargs)


class UserLibraryViewSet(viewsets.ModelViewSet):
    queryset = UserLibrary.objects.all()
    serializer_class = UserLibrarySerializer

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            # Render HTML page with JavaScript-based rendering
            return render(request, 'library.html')
        else:
            # Provide JSON API response
            return super().list(request, *args, **kwargs)


class ListeningHistoryViewSet(viewsets.ModelViewSet):
    queryset = ListeningHistory.objects.all()
    serializer_class = ListeningHistorySerializer

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            # Render HTML page with JavaScript-based rendering
            return render(request, 'listeninghistory_js_render.html')
        else:
            # Provide JSON API response
            return super().list(request, *args, **kwargs)


def user_home(request):
    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_library, created_library = UserLibrary.objects.get_or_create(user_profile=user_profile)

        saved_songs = user_library.saved_songs.all()
        saved_albums = user_library.saved_albums.all()
        favorite_artists = user_library.favorite_artists.all()
        created_playlists = user_library.created_playlists.all()
        recently_played = user_library.recently_played.all()  # If you want to show recently played songs

    else:
        saved_songs = saved_albums = favorite_artists = created_playlists = recently_played = []

    return render(request, 'users/user_home.html', {
        'saved_songs': saved_songs,
        'saved_albums': saved_albums,
        'favorite_artists': favorite_artists,
        'created_playlists': created_playlists,
        'recently_played': recently_played,
    })


def save_item(request, item_type, item_id):
    # Your save logic here (add the item to the user's library)
    # Example: Assume you have a UserLibrary model with a method `add_item`
    user_profile = request.user.userprofile
    if item_type == 'song':
        song = get_object_or_404(Song, id=item_id)
        user_profile.userlibrary.add_song(song)
        message = f'Song {song.title} saved successfully.'
    elif item_type == 'album':
        # Handle saving albums
        pass
    elif item_type == 'artist':
        # Handle saving artists
        pass
    elif item_type == 'genre':
        # Handle saving genres
        pass
    else:
        message = 'Invalid item type.'

    return JsonResponse({'message': message})

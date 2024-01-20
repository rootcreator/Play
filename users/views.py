import requests
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from recommendations.recommendation_utils import profile_user, recommend_songs

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

# Algorithm

def user_profile_view(request):
    # Assume you have a user object (replace it with your authentication logic)
    user = request.user

    # Get user profile
    user_profile = profile_user(user)

    # Get song recommendations
    recommended_songs = recommend_songs(user_profile)

    # Render the view with user profile and recommendations
    return render(request, 'user_profile.html', {'user_profile': user_profile, 'recommended_songs': recommended_songs})

#
def user_registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # You may want to log in the user after registration
            # login(request, user)
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # You can replace 'login' with the name of your login URL
    template_name = 'registration/signup.html'
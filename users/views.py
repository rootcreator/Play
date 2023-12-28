from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import UserProfile, UserLibrary, UserProfileView, Song, Album, Playlist
from .serializers import (
    UserProfileSerializer,
    UserLibrarySerializer,
    UserProfileViewSerializer,
    SongSerializer,
    AlbumSerializer,
    PlaylistSerializer
    # Add other serializers as needed
)

class UserProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Profile API Views
class UserProfileListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#class UserProfileListCreateView(ListCreateAPIView):
#    queryset = UserProfile.objects.all()
#    serializer_class = UserProfileSerializer
#    permission_classes = [IsAuthenticated]

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# User Library API Views
class UserLibraryListCreateView(generics.ListCreateAPIView):
    queryset = UserLibrary.objects.all()
    serializer_class = UserLibrarySerializer

class UserLibraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserLibrary.objects.all()
    serializer_class = UserLibrarySerializer

# User Profile View API Views
class UserProfileViewListCreateView(generics.ListCreateAPIView):
    queryset = UserProfileView.objects.all()
    serializer_class = UserProfileViewSerializer

class UserProfileViewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfileView.objects.all()
    serializer_class = UserProfileViewSerializer

# Song API Views
class SongListCreateView(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

# Album API Views
class AlbumListCreateView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

# Playlist API Views
class PlaylistListCreateView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

# Custom Root API
@api_view(['GET'])
def custom_api_root(request, format=None):
    return Response({
        'user-profiles': reverse('userprofile-list', request=request, format=format),
        'user-libraries': reverse('userlibrary-list', request=request, format=format),
        'user-profile-views': reverse('profileview-list', request=request, format=format),
        'songs': reverse('song-list', request=request, format=format),
        'albums': reverse('album-list', request=request, format=format),
        'playlists': reverse('playlist-list', request=request, format=format),
        # Add more endpoints as needed
    })

# UserProfile Dashboard API View
@api_view(['GET'])
def user_dashboard(request, format=None):
    # Implement dashboard logic here
    # Example: Retrieve specific data for the user's dashboard
    return Response({
        # Add dashboard data as needed
    })

# UserProfile Library API View
@api_view(['GET'])
def user_library(request, format=None):
    # Implement library logic here
    # Example: Retrieve user's saved songs, albums, playlists, etc.
    return Response({
        # Add library data as needed
    })

# UserProfile Settings API View
@api_view(['GET', 'PUT'])
def user_settings(request, format=None):
    # Implement user settings logic here
    # Example: Retrieve or update user settings
    return Response({
        # Add settings data as needed
    })


# Additional API Views for Songs
class SongListCreateView(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

# Additional API Views for Albums
class AlbumListCreateView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

# Additional API Views for Playlists
class PlaylistListCreateView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
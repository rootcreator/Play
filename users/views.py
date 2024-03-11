from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from music.models import Song, Album
from music.serializers import SongSerializer, AlbumSerializer
from users.models import Profile, Library, Like, Favourites, ListeningHistory, Settings
from .forms import AlbumForm, SongForm
from .serializers import (
    ProfileSerializer, UserSerializer, LibrarySerializer,
    LikeSerializer, FavouritesSerializer, SettingsSerializer,
    ListeningHistorySerializer
)


class ProfileAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        return Response({"message": "Cannot create new profile while authenticated"}, status=status.HTTP_403_FORBIDDEN)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                group = Group.objects.get(name='user')
                request.user.groups.add(group)

                profile_data = {
                    "user": user.id,
                    "favorite_genres": request.data.get("favorite_genres", [])
                }
                profile_serializer = ProfileSerializer(data=profile_data)
                if profile_serializer.is_valid():
                    profile_serializer.save()
                    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
                else:
                    user.delete()
                    return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                return Response({"message": "User authenticated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LibraryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            library = Library.objects.get(profile__user=request.user)
            serializer = LibrarySerializer(library)
            return Response(serializer.data)
        except Library.DoesNotExist:
            return Response({"message": "Library not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavouritesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favourites = Favourites.objects.all()
        serializer = FavouritesSerializer(favourites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavouritesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListeningHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        histories = ListeningHistory.objects.all()
        serializer = ListeningHistorySerializer(histories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ListeningHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SettingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        settings = Settings.objects.all()
        serializer = SettingsSerializer(settings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecentlyPlayedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the last 10 entries from the listening history
        recent_history = ListeningHistory.objects.filter(user=request.user).order_by('-listened_at')[:10]

        # Extract the unique songs and albums from the recent history
        recent_songs = set()
        recent_albums = set()
        for entry in recent_history:
            recent_songs.add(entry.song)
            recent_albums.add(entry.song.album)

        # Serialize the songs and albums
        song_serializer = SongSerializer(recent_songs, many=True)
        album_serializer = AlbumSerializer(recent_albums, many=True)

        return Response({
            "recently_played_songs": song_serializer.data,
            "recently_played_albums": album_serializer.data
        })


# Upload
def upload_media(request):
    if request.method == 'POST':
        # Check if song form submitted
        if 'audio_file' in request.FILES:
            form = SongForm(request.POST, request.FILES)
        # Check if album form submitted
        elif 'songs' in request.FILES:
            form = AlbumForm(request.POST, request.FILES)
        else:
            # Handle invalid form submission
            return render(request, 'invalid_media_upload.html')

        if form.is_valid():
            media = form.save()
            # Redirect to appropriate detail view based on media type
            if isinstance(media, Song):
                return redirect('song_detail', song_id=media.id)
            elif isinstance(media, Album):
                return redirect('album_detail', album_id=media.id)
    else:
        # Render the upload form
        song_form = SongForm()
        album_form = AlbumForm()
        return render(request, 'music_form.html', {'song_form': song_form, 'album_form': album_form})

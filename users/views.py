from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from music.serializers import SongSerializer, AlbumSerializer
from .serializers import ProfileSerializer, LibrarySerializer, LikeSerializer, ListeningHistorySerializer, \
    SettingsSerializer, UserSerializer
from .models import Profile, Library, Like, ListeningHistory, Settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        return Response({"message": "Cannot create new profile while authenticated"}, status=status.HTTP_403_FORBIDDEN)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LibraryAPIView(APIView):
    def get(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            try:
                library = Library.objects.get(profile__user=request.user)
                serializer = LibrarySerializer(library)
                return Response(serializer.data)
            except Library.DoesNotExist:
                return Response({"message": "Library not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


class LikeAPIView(APIView):
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


class ListeningHistoryAPIView(APIView):
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
    def get(self, request):
        # Retrieve the last 10 entries from the listening history
        recent_history = ListeningHistory.objects.order_by('-listened_at')[:10]

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

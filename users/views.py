from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from music.serializers import SongSerializer, AlbumSerializer
from users.serializers import (
    ProfileSerializer, LibrarySerializer, LikeSerializer,
    ListeningHistorySerializer, SettingsSerializer,
    UserSerializer, FavouritesSerializer
)
from users.models import Profile, Library, Like, ListeningHistory, Settings, Favourites
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class ProfileAPIView(APIView):
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

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                profile_data = {
                    "user": user.id,
                    "favorite_genres": request.data.get("favorite_genres", [])
                }
                profile_serializer = ProfileSerializer(data=profile_data)
                if profile_serializer.is_valid():
                    profile_serializer.save()
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({"token": token.key}, status=status.HTTP_201_CREATED)
                else:
                    user.delete()
                    return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
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



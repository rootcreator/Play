from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Genre, Artist, Album, Song, Playlist, UserProfile, UserLibrary
from django.contrib.auth.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLibrary
        fields = '__all__'


class AlbumUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        album_serializer = AlbumSerializer(data=request.data)
        if album_serializer.is_valid():
            album_serializer.save()
            return Response(album_serializer.data, status=201)
        else:
            return Response(album_serializer.errors, status=400)


class SongUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        song_serializer = SongSerializer(data=request.data)
        if song_serializer.is_valid():
            song_serializer.save()
            return Response(song_serializer.data, status=201)
        else:
            return Response(song_serializer.errors, status=400)

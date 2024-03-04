from rest_framework import serializers
from .models import Profile, Library, Like, ListeningHistory, Settings, Favourites
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'


class ListeningHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningHistory
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'

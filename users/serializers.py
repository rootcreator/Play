from rest_framework import serializers
from .models import UserProfile, UserLibrary, UserProfileView, Song, Album, \
    Playlist  # Importing models from the current directory


# Serializer for UserProfile model
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the UserProfile model in serialization


# Serializer for UserLibrary model
class UserLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLibrary  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the UserLibrary model in serialization


# Serializer for UserProfileView model
class UserProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileView  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the UserProfileView model in serialization


# Serializer for Song model
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the Song model in serialization


# Serializer for Album model
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the Album model in serialization


# Serializer for Playlist model
class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the Playlist model in serialization

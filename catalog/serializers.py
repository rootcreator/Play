from rest_framework import serializers
from .models import Genre, Artist, Composer, Album, Song  # Importing models from the current directory


# Serializer for the Genre model
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the Genre model in serialization


# Serializer for the Artist model
class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the Artist model in serialization


# Serializer for the Composer model
class ComposerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composer  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the Composer model in serialization


# Serializer for the Album model
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the Album model in serialization


# Serializer for the Song model
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song  # Specifies the model associated with this serializer
        fields = '__all__'  # Includes all fields from the Song model in serialization

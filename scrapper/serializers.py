from rest_framework import serializers
from .models import Music, Site


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'title', 'artist', 'album', 'genre', 'url', 'audio_file', 'copyright_status']


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'name', 'url']

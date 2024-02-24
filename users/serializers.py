from rest_framework import serializers
from .models import Profile, Library, ListeningHistory, Settings


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'


class ListeningHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningHistory
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['id', 'user', 'theme', 'notifications_enabled', 'auto_play_enabled', 'repeat_mode', 'language',
                  'download_quality', 'streaming_quality', 'equalizer_enabled', 'local_files_access', 'created_at']

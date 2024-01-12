from django.contrib.auth.models import User
from django.db import models
from music.models import Song, Artist, Playlist, Album  # Importing models from the music app


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)
    view_count = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)

    saved_songs = models.ManyToManyField(Song, related_name='saved_in_user_profiles', blank=True)
    saved_albums = models.ManyToManyField(Album, related_name='saved_in_user_profiles', blank=True)
    favorite_artists = models.ManyToManyField(Artist, related_name='favorited_in_user_profiles', blank=True)
    created_playlists = models.ManyToManyField(Playlist, related_name='created_in_user_profiles', blank=True)
    recently_played = models.ManyToManyField(Song, related_name='played_by_user_profiles', blank=True, through='ListeningHistory')

    class Meta:
        db_table = 'profile_user_profile'

    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserLibrary(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='library')
    saved_songs = models.ManyToManyField(Song, related_name='saved_in_libraries', blank=True)
    saved_albums = models.ManyToManyField(Album, related_name='saved_in_libraries', blank=True)
    favorite_artists = models.ManyToManyField(Artist, related_name='favorited_in_libraries', blank=True)
    created_playlists = models.ManyToManyField(Playlist, related_name='created_in_libraries', blank=True)
    recently_played = models.ManyToManyField(Song, related_name='played_by_users', blank=True, through='ListeningHistory')

    class Meta:
        db_table = 'profile_user_library'

    def __str__(self):
        return f"Library of {self.user_profile.user.username}"


class ListeningHistory(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_library = models.ForeignKey(UserLibrary, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'profile_listening_history'

    def __str__(self):
        return f"{self.song.title} listened at {self.listened_at}"
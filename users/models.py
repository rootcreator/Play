from django.db import models
from django.contrib.auth.models import User
from music.models import Song, Album, Artist, Playlist

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)
    # Other fields as needed for user-specific data

    def __str__(self):
        return self.user.username

class UserLibrary(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='library')
    saved_songs = models.ManyToManyField(Song, related_name='user_library_saved_songs', blank=True)
    saved_albums = models.ManyToManyField(Album, related_name='user_library_saved_albums', blank=True)
    favorite_artists = models.ManyToManyField(Artist, related_name='user_library_favorite_artists', blank=True)
    created_playlists = models.ManyToManyField(Playlist, related_name='user_library_created_playlists', blank=True)
    # Add other fields or relationships as needed for user's library

    def __str__(self):
        return f"Library of {self.user_profile.user.username}"

class UserProfileView(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile_views')
    view_count = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile views of {self.user_profile.user.username}"

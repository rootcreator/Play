from django.db import models
from django.contrib.auth.models import User
from music.models import Song, Album, Artist, Playlist



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users_user_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)

    # Other UserProfile fields

    def __str__(self):
        return self.user.username


class UserLibrary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users_user_library')
    saved_songs = models.ManyToManyField(Song, related_name='users_saved_songs')
    saved_albums = models.ManyToManyField(Album, related_name='users_saved_albums')
    favorite_artists = models.ManyToManyField(Artist, related_name='users_favorite_artists')
    uploaded_songs = models.ManyToManyField(Song, related_name='users_uploaded_songs', blank=True)
    created_playlists = models.ManyToManyField(Playlist, related_name='users_created_playlists', blank=True)
    # Other fields as needed for user-specific data

from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Artist(models.Model):
    name = models.CharField(max_length=100)


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='album_covers/'),


class Song(models.Model):
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='songs/')


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class UserLibrary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_songs = models.ManyToManyField(Song)
    saved_albums = models.ManyToManyField(Album)
    favorite_artists = models.ManyToManyField(Artist)
    uploaded_songs = models.ManyToManyField(Song, related_name='uploaded_by', blank=True)
    created_playlists = models.ManyToManyField(Playlist, related_name='created_by', blank=True)
    # Other fields as needed for user-specific data

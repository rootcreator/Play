from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='album_covers/')

    def get_all_songs(self):
        return self.song_set.all()

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    cover_image = models.ImageField(null=True, blank=True, upload_to='song_covers/')
    album = models.ForeignKey('Album', on_delete=models.CASCADE, null=True, blank=True)
    audio_file = models.FileField(upload_to='songs/')

    def __str__(self):
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='music_user_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    # Add any additional user-related fields here


class UserPlaylist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.title


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


# Additional fields could be added to UserFavorite if needed, like date_added, etc.

class UserLibrary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='music_user_library')
    saved_songs = models.ManyToManyField(Song, related_name='music_saved_songs')
    saved_albums = models.ManyToManyField(Album, related_name='music_saved_albums')
    favorite_artists = models.ManyToManyField(Artist, related_name='music_favorite_artists')
    uploaded_songs = models.ManyToManyField(Song, related_name='music_uploaded_songs', blank=True)
    created_playlists = models.ManyToManyField(Playlist, related_name='music_created_playlists', blank=True)
    # Other fields as needed for user-specific data


class AudioFile(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio/')
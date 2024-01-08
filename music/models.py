import requests
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Composer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    RATING_CHOICES = [
        ('Good', 'Good'),
        ('Okay', 'Okay'),
        ('Mid', 'Mid'),
        ('Bad', 'Bad'),
    ]

    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    cover_image = models.ImageField(null=True, blank=True, upload_to='song_covers/')
    audio_file = models.FileField(upload_to='songs/')
    is_single = models.BooleanField(default=True)  # Indicates if it's a single or part of an album
    album = models.ForeignKey('Album', on_delete=models.CASCADE, null=True, blank=True)
    composer = models.ForeignKey(Composer, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default='Okay')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = [['title', 'artist']]

    def __str__(self):
        return self.title


class Album(models.Model):
    RATING_CHOICES = [
        ('Good', 'Good'),
        ('Okay', 'Okay'),
        ('Mid', 'Mid'),
        ('Bad', 'Bad'),
    ]

    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True)
    cover_image = models.ImageField(upload_to='album_covers/')
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default='Okay')
    songs = models.ManyToManyField(Song, related_name='albums', blank=True)

    class Meta:
        unique_together = [['title', 'artist', 'cover_image']]

    def __str__(self):
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='playlist_covers/')
    songs = models.ManyToManyField(Song)

    class Meta:
        unique_together = [['title']]

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='music_user_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.music_user_profile.save()


class UserLibrary(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='music_user_library')
    saved_songs = models.ManyToManyField('Song', related_name='music_saved_in_libraries')
    saved_albums = models.ManyToManyField('Album', related_name='music_saved_in_libraries')
    favorite_artists = models.ManyToManyField('Artist', related_name='music_favorited_in_libraries')
    uploaded_songs = models.ManyToManyField('Song', related_name='music_uploaded_songs', blank=True)
    created_playlists = models.ManyToManyField('Playlist', related_name='music_created_in_libraries', blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_profile'], name='unique_user_library')
        ]

    def __str__(self):
        return f"Library of {self.user_profile.user.username}"


class AudioFile(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='songs/')

    def __str__(self):
        return self.title



class MusicAPI:
    BASE_URL = 'http://localhost:8000/api/'  # Replace with your Django app's base URL

    @staticmethod
    def fetch_data(endpoint):
        url = MusicAPI.BASE_URL + endpoint
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch {endpoint}. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

    @staticmethod
    def fetch_genres():
        return MusicAPI.fetch_data('genres/')

    @staticmethod
    def fetch_artists():
        return MusicAPI.fetch_data('artists/')

    @staticmethod
    def fetch_composers():
        return MusicAPI.fetch_data('composers/')

    @staticmethod
    def fetch_albums():
        return MusicAPI.fetch_data('albums/')

    @staticmethod
    def fetch_songs():
        return MusicAPI.fetch_data('songs/')


    
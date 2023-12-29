from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    RATING_CHOICES = [
        ('Good', 'Good'),
        ('Okay', 'Okay'),
        ('Mid', 'Mid'),
        ('Bad', 'Bad'),
    ]

    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='album_covers/')
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default='Okay')

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    cover_image = models.ImageField(null=True, blank=True, upload_to='song_covers/')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    audio_file = models.FileField(upload_to='songs/')
    rating = models.CharField(max_length=10, choices=Album.RATING_CHOICES, default='Okay')

    def __str__(self):
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='music_user_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(self, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(self, instance, **kwargs):
        instance.music_user_profile.save()


class UserLibrary(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='music_user_library')
    saved_songs = models.ManyToManyField('Song', related_name='music_saved_in_libraries')
    saved_albums = models.ManyToManyField('Album', related_name='music_saved_in_libraries')
    favorite_artists = models.ManyToManyField('Artist', related_name='music_favorited_in_libraries')
    uploaded_songs = models.ManyToManyField('Song', related_name='music_uploaded_songs', blank=True)
    created_playlists = models.ManyToManyField('Playlist', related_name='music_created_in_libraries', blank=True)

    def __str__(self):
        return f"Library of {self.user_profile.user.username}"


class AudioFile(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio/')

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User


class Song(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    ft_artist = models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        # Before saving, ensure that featured_artists is properly formatted
        if self.featured_artists:
            # Remove any leading or trailing whitespaces
            self.featured_artists = self.featured_artists.strip()
            # Remove any duplicate commas
            self.featured_artists = ",".join(filter(None, self.featured_artists.split(",")))
        super().save(*args, **kwargs)

    cover_image = models.ImageField(null=True, blank=True, upload_to='song_covers/')
    audio_file = models.FileField(upload_to='songs/')
    album = models.ForeignKey('Album', on_delete=models.CASCADE, null=True, blank=True)
    genre = models.CharField(max_length=100)

    class Meta:
        unique_together = [['title', 'artist']]

    def __str__(self):
        return self.title


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='album_covers/')
    songs = models.ManyToManyField(Song, related_name='albums', blank=True)

    class Meta:
        unique_together = [['title', 'artist', 'cover_image']]

    def __str__(self):
        return self.title


class AudioFile(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='songs/')

    def __str__(self):
        return self.title

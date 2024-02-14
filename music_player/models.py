from django.db import models
from music.models import Artist, Album, Song, Playlist  # Import models from the music app
from radio.models import RadioStation


class Queue(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    RadioStation = models.ForeignKey(RadioStation, on_delete=models.CASCADE)
    order = models.IntegerField()
    is_shuffle = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order}: {self.song.title}"

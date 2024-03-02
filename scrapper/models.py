from django.db import models


class Music(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    url = models.URLField()
    audio_file = models.FileField(upload_to='audio/')
    copyright_status = models.CharField(max_length=50)  # Example: "Copyrighted", "Royalty-free", "Public Domain"

    def __str__(self):
        return self.title


class Site(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'scrapper'

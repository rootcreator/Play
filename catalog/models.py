from django.db import models


# Model representing a Genre
class Genre(models.Model):
    name = models.CharField(max_length=100)  # Field to store the name of the genre

    def __str__(self):
        return self.name


# Model representing an Artist
class Artist(models.Model):
    name = models.CharField(max_length=200)  # Field to store the name of the artist
    # Define more fields for artist details

    def __str__(self):
        return self.name


# Model representing a Composer
class Composer(models.Model):
    name = models.CharField(max_length=200)  # Field to store the name of the composer
    # Define more fields for composer details

    def __str__(self):
        return self.name


# Model representing an Album
class Album(models.Model):
    title = models.CharField(max_length=200)  # Field to store the title of the album
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)  # Foreign key linking to Artist model
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)  # Foreign key linking to Genre model
    # Define more fields for album details

    def __str__(self):
        return self.title


# Model representing a Song
class Song(models.Model):
    title = models.CharField(max_length=200)  # Field to store the title of the song
    is_single = models.BooleanField(default=True)  # Indicates if it's a single or part of an album
    album = models.ForeignKey('Album', on_delete=models.CASCADE, null=True, blank=True)  # Foreign key linking to Album model (nullable and optional)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs_by_artist')  # Foreign key linking to Artist model with a related name
    composer = models.ForeignKey(Composer, on_delete=models.CASCADE, null=True, blank=True)  # Foreign key linking to Composer model
    cover_image = models.ImageField(null=True, blank=True, upload_to='song_covers/')  # Field to upload song cover image
    audio_file = models.FileField(upload_to='songs/')  # Field to upload song audio file
    # Define more fields for song details

    def __str__(self):
        return self.title

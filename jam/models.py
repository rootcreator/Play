from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from music.models import Song, Album, Playlist
from users.models import Library, ListeningHistory, Profile, Like


# Create your models here.

class SimilarPlaylists(models.Model):
    genre = models.CharField(max_length=100)
    playlists = models.ManyToManyField(Playlist)

    def get_sorted_playlists(self):
        """
        Get playlists sorted by genre and user favorites.
        """
        sorted_playlists = self.playlists.order_by('-favourites_count')
        return sorted_playlists


class SimilarReleases(models.Model):
    genre = models.CharField(max_length=100)
    albums = models.ManyToManyField(Album)
    songs = models.ManyToManyField(Song)

    def get_sorted_releases(self):
        """
        Get releases sorted by genre and user favorites.
        """
        sorted_albums = self.albums.order_by('-favourites_count')
        sorted_songs = self.songs.order_by('-favourites_count')
        return sorted_albums, sorted_songs


class Trends(models.Model):
    @staticmethod
    def get_popular_songs(limit=10):
        """
        Get the most popular songs based on listening history.
        """
        popular_songs = ListeningHistory.objects.values('song').annotate(total=Count('song')).order_by('-total')[:limit]
        return popular_songs

    @staticmethod
    def get_popular_albums(limit=10):
        """
        Get the most popular albums based on listening history.
        """
        popular_albums = ListeningHistory.objects.values('song__album').annotate(total=Count('song__album')).order_by(
            '-total')[:limit]
        return popular_albums

    @staticmethod
    def get_popular_artists(limit=10):
        """
        Get the most popular artists based on listening history.
        """
        popular_artists = ListeningHistory.objects.values('song__artist').annotate(
            total=Count('song__artist')).order_by('-total')[:limit]
        return popular_artists


class Favourites(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} liked {self.content_object}"


class RecommendedSongs(models.Model):
    favourite = models.ForeignKey(Favourites, on_delete=models.CASCADE)
    similarplaylist = models.ForeignKey(SimilarPlaylists, on_delete=models.CASCADE)
    history = models.ForeignKey(ListeningHistory, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    similarreleases = models.OneToOneField(SimilarReleases, on_delete=models.CASCADE)
    like = models.OneToOneField(Like, on_delete=models.CASCADE)


class Feeds(models.Model):
    likes = models.ManyToManyField(Like)
    trend = models.ForeignKey(Trends, on_delete=models.CASCADE)

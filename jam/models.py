import profile

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from music.models import Song, Album, Playlist
from users.models import Library, ListeningHistory, Profile, Like, Favourites


# Create your models here.
class RecommendedPlaylists(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    playlists = models.ManyToManyField(Playlist)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    listeninghistory = models.ForeignKey(ListeningHistory, on_delete=models.CASCADE)

    def recommend_playlist(self):
        """
        Recommend playlists based on trends, listening history, and new playlists.
        """
        # Get playlists based on genre and user favorites
        sorted_playlists = self.get_sorted_playlists()

        # Step 1: Analyze Trends
        trending_genres = self.analyze_trends()

        # Step 2: Analyze Listening History
        user_preferences = self.analyze_listening_history()

        # Step 3: Include New Playlists
        new_playlists = self.get_new_playlists()

        # Step 4: Combine Recommendations
        recommended_playlists = sorted_playlists.filter(genre__in=trending_genres) | \
                                sorted_playlists.filter(genre__in=user_preferences) | \
                                new_playlists

        return recommended_playlists

    def analyze_trends(self):
        """
        Analyze trends data to identify popular genres or themes.
        """
        # Fetch trending genres based on actual trends data
        trending_genres = []

        try:
            # Query trends data to get trending genres
            # Assuming Trends model has a 'genre' field
            trending_genres = Trends.objects.values_list('genre', flat=True).distinct()
        except Exception as e:
            # Handle exceptions if the trends data cannot be retrieved
            print(f"Error fetching trending genres: {e}")

        return trending_genres

    def analyze_listening_history(self):
        """
        Analyze user's listening history to identify preferences.
        """
        # Fetch user's favorite genres based on listening history
        favorite_genres = []

        try:
            # Query listening history to get user's favorite genres
            # Assuming ListeningHistory model has a 'song' field, and Song model has a 'genre' field
            favorite_genres = Song.objects.filter(listeninghistory__user_profile=self.user_profile).values_list('genre',
                                                                                                                flat=True).distinct()
        except Exception as e:
            # Handle exceptions if the listening history data cannot be retrieved
            print(f"Error analyzing listening history: {e}")

        return favorite_genres

    def get_new_playlists(self):
        """
        Retrieve new playlists that match user's preferences or current trends.
        """
        # Placeholder: Get recently created playlists or playlists gaining popularity based on user preferences or trends
        new_playlists = []

        try:
            # Query new playlists based on user preferences or current trends
            # You can replace this with your actual recommendation logic
            new_playlists = Playlist.objects.all()

            # Apply additional filtering or sorting based on user preferences or trends
            # For example, you can filter playlists based on user's favorite genres or trending genres

        except Exception as e:
            # Handle exceptions if the playlist data cannot be retrieved
            print(f"Error retrieving new playlists: {e}")

        return new_playlists


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
    def get_popular_genres(limit=10):
        """
        Get the most popular songs based on listening history.
        """
        popular_genres = ListeningHistory.objects.values('song').annotate(total=Count('song')).order_by('-total')[:limit]
        return popular_genres

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

    @staticmethod
    def update_trends_with_songs(song_titles):
        """
        Update trends data based on the provided list of song titles.
        """
        try:
            # Update trends based on the provided song titles
            # For example, you can update trends for genres, artists, etc.
            # Here, we are updating trends for genres based on the provided song titles
            # Assuming each song has a genre field
            genre_counts = {}
            for title in song_titles:
                # Assuming Song model has a field called 'genre'
                song_genre = Song.objects.get(title=title).genre
                if song_genre in genre_counts:
                    genre_counts[song_genre] += 1
                else:
                    genre_counts[song_genre] = 1

            # Now, you can update the Trends model with the genre counts
            # For example, you can update existing trend records or create new ones
            for genre, count in genre_counts.items():
                # Update or create a trend record for the genre
                trend, created = Trends.objects.get_or_create(genre=genre)
                trend.count += count
                trend.save()

            return True  # Return True if trends are updated successfully
        except Exception as e:
            # Handle exceptions if any error occurs during trend update
            print(f"Error updating trends: {e}")
            return False  # Return False if there's an error


class Recommended(models.Model):
    favourite = models.OneToOneField(Favourites, on_delete=models.CASCADE)
    recommededplaylist = models.OneToOneField(RecommendedPlaylists, on_delete=models.CASCADE)
    songs = models.ForeignKey('music.song', on_delete=models.CASCADE)
    albums = models.ForeignKey('music.album', on_delete=models.CASCADE)
    genres = models.ForeignKey('music.genre', on_delete=models.CASCADE)
    history = models.ForeignKey(ListeningHistory, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    similarreleases = models.OneToOneField(SimilarReleases, on_delete=models.CASCADE)
    like = models.OneToOneField(Like, on_delete=models.CASCADE)


class Feeds(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey('music.song', on_delete=models.CASCADE)
    album = models.ForeignKey('music.album', on_delete=models.CASCADE)

    def __str__(self):
        return f"Feed for {self.user.username} at {self.created_at}"

    def generate_feeds_for_user(user_profile):
        try:
            # Retrieve trending items from Trends model
            trending_songs = Trends.objects.values_list('song__title', flat=True)

            # Retrieve recommended items from Recommended model
            recommended_songs = Recommended.objects.filter(user=user_profile).values_list('song__title', flat=True)

            # Retrieve user's favorite songs from Favourites model
            favorite_songs = Favourites.objects.filter(user=user_profile).values_list('song__title', flat=True)

            # Retrieve recently listened songs from ListeningHistory model
            recent_songs = ListeningHistory.objects.filter(user_profile=user_profile).order_by(
                '-timestamp').values_list('song__title', flat=True)[:10]

            # Combine all song data into a single list
            all_songs = list(trending_songs) + list(recommended_songs) + list(favorite_songs) + list(recent_songs)

            # Generate feed items for songs
            feeds = []
            for song_title in all_songs:
                feed = Feeds.objects.create(
                    user=user_profile,
                    content=f"New activity: {song_title}",

                    song_title=song_title
                )
                feeds.append(feed)

            return feeds
        except Exception as e:
            print(f"Error generating feeds: {e}")
            return []


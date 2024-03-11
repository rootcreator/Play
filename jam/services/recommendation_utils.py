from jam.models import RecommendedPlaylists, SimilarReleases, Trends, Favourites, Feeds
from users.models import Like, ListeningHistory, Profile


def profile_user(user):
    # Ensure that 'user' is a User instance
    try:
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        # Handle the case where the UserProfile does not exist for the given User
        user_profile = None

    if user_profile:
        # Continue with your existing logic using 'user_profile' instead of 'user'
        liked_songs = Like.objects.filter(user=user_profile)
        listening_history = ListeningHistory.objects.filter(user_profile=user_profile)
        # ... rest of the code

        return user_profile

    return None  # or handle the case where UserProfile does not exist for the given User


def recommend_songs(user_profile):
    # Ensure user_profile is not None
    if user_profile is None:
        return []

    # Continue with the rest of the function
    recommended_songs = []
    if user_profile['total_songs_played'] > 100 and user_profile['diversity_of_genres'] > 5:
        # Recommend a song based on diverse listening habits
        recommended_song = find_song_based_on_diverse_genre(user_profile['played_genres'])
        recommended_songs.append(recommended_song)

    # You can add more recommendation rules based on user_profile attributes

    return recommended_songs


def find_song_based_on_diverse_genre(played_genres):
    # Implement your logic to find a song based on diverse genre
    # For simplicity, let's just return a placeholder value
    return "Diverse Genre Song"


def get_recommendations(user):
    # Retrieve user's profile
    user_profile = Profile.objects.get(user=user)

    # Recommend playlists
    recommended_playlists = RecommendedPlaylists.objects.get(user=user_profile).recommend_playlist()

    # Retrieve similar releases
    sorted_releases = SimilarReleases.objects.get().get_sorted_releases()

    # Retrieve trends
    popular_songs = Trends.get_popular_songs()
    popular_genres = Trends.get_popular_genres()
    popular_albums = Trends.get_popular_albums()
    popular_artists = Trends.get_popular_artists()

    # Retrieve user's favorites
    user_favorites = Favourites.objects.filter(user=user_profile)

    # Retrieve feeds
    latest_feeds = Feeds.objects.all()

    return {
        'recommended_playlists': recommended_playlists,
        'sorted_releases': sorted_releases,
        'popular_songs': popular_songs,
        'popular_genres': popular_genres,
        'popular_albums': popular_albums,
        'popular_artists': popular_artists,
        'user_favorites': user_favorites,
        'latest_feeds': latest_feeds
    }

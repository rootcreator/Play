import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from .models import Song, Album  # Import your Django models

# Initialize Spotify and YouTube API clients
SPOTIFY_CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_youtube_video(track_name, artist_name):
    # Example: Search for a video related to the track obtained from Spotify
    search_query = f"{track_name} {artist_name} official music video"
    search_response = youtube.search().list(
        q=search_query,
        part='id',
        maxResults=1,
        type='video'
    ).execute()

    if 'items' in search_response and search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
        # Retrieve other video information or proceed to display the video
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return video_url
    else:
        return None

def get_spotify_song_info(track_name):
    # Implement the logic to fetch song details from Spotify
    # Example: Use Spotify API to get song details
    # Replace this logic with your actual Spotify API calls
    track = sp.search(q=track_name, limit=1, type='track')

    if track['tracks']['items']:
        track = track['tracks']['items'][0]
        song_title = track['name']
        artist_name = track['artists'][0]['name']
        return song_title, artist_name
    else:
        return None, None

def add_song_to_library(user_profile, track_name):
    # Fetch song details from Spotify
    track_name, artist_name = get_spotify_song_info(track_name)

    if track_name and artist_name:
        song = Song.objects.get_or_create(title=track_name)  # Create or retrieve the song from your models
        artist = Artist.objects.get_or_create(name=artist_name)  # Create or retrieve the artist from your models

        # Fetch the song from your Django models
        if song:
            user_library = UserLibrary.objects.get_or_create(user_profile=user_profile)[0]
            user_library.saved_songs.add(song)  # Add the song to user's saved songs

            # Find YouTube video and save its URL to the song or display it to the user
            video_url = get_youtube_video(track_name, artist_name)
            if video_url:
                song.youtube_url = video_url  # Assuming there's a field in your Song model to store YouTube URL
                song.save()
                return f"Song '{track_name}' added to library with YouTube link: {video_url}"

    return "Failed to add song to library or find YouTube video"

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from .models import Song, Artist, Album, UserLibrary
import requests

# LastFm Integration
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'


def get_recommendations_for_user(username):
    method = 'user.getRecommendedTracks'
    params = {
        'method': method,
        'user': username,
        'api_key': API_KEY,
        'format': 'json'
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        recommendations = response.json()
        # Process recommendations
        return recommendations
    else:
        return None

def get_user_top_tracks(username):
    method = 'user.getTopTracks'
    params = {
        'method': method,
        'user': username,
        'api_key': API_KEY,
        'format': 'json'
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        top_tracks = response.json()
        # Process top tracks data
        return top_tracks
    else:
        return None

def get_track_info(track_name, artist_name):
    method = 'track.getInfo'
    params = {
        'method': method,
        'track': track_name,
        'artist': artist_name,
        'api_key': API_KEY,
        'format': 'json'
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        track_info = response.json()
        # Process track information
        return track_info
    else:
        return None


# Spotify Integration

def get_spotify_song_info(track_name):
    # Initialize Spotify client
    client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID',
                                                          client_secret='YOUR_CLIENT_SECRET')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Example: Search for a track on Spotify
    results = sp.search(q=track_name, limit=1, type='track')

    if results['tracks']['items']:
        track_info = results['tracks']['items'][0]
        track_id = track_info['id']
        track_name = track_info['name']
        artist_name = track_info['artists'][0]['name']
        # Access other relevant track information
        return track_name, artist_name
    else:
        return None, None


# Youtube Intergration

def get_youtube_video(track_name, artist_name):
    # Initialize YouTube Data API client
    youtube = build('youtube', 'v3', developerKey='YOUR_YOUTUBE_API_KEY')

    # Example: Search for a video related to the track obtained from Spotify
    search_query = f"{track_name} {artist_name} official music video"
    search_response = youtube.search().list(
        q=search_query,
        part='id',
        maxResults=1,
        type='video'
    ).execute()

    if 'items' in search_response:
        video_id = search_response['items'][0]['id']['videoId']
        # Retrieve other video information or proceed to display the video
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return video_url
    else:
        return None


# Example function to add a song to user's library and find its YouTube video
def add_song_to_library(user_profile, track_name):
    song = Song.objects.get_or_create(title=track_name)  # Create or retrieve the song from your models
    artist_name = None

    # Fetch artist name using Spotify API
    if song:
        track_name, artist_name = get_spotify_song_info(track_name)
        if artist_name:
            artist = Artist.objects.get_or_create(name=artist_name)  # Create or retrieve the artist
            user_library = UserLibrary.objects.get_or_create(user_profile=user_profile)[0]
            user_library.saved_songs.add(song)  # Add the song to user's saved songs

            # Find YouTube video and save its URL to the song or display it to the user
            if track_name and artist_name:
                video_url = get_youtube_video(track_name, artist_name)
                if video_url:
                    song.youtube_url = video_url  # Assuming there's a field in your Song model to store YouTube URL
                    song.save()
                    return f"Song '{track_name}' added to library with YouTube link: {video_url}"
    return "Failed to add song to library or find YouTube video"

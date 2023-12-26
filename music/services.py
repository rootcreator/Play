import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from .models import Song, Artist, Album, UserLibrary
import requests
import lyricsgenius

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


# YouTube Integration

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


# Musixmatch API credentials
MUSIXMATCH_API_KEY = 'YOUR_MUSIXMATCH_API_KEY'
MUSIXMATCH_BASE_URL = 'https://api.musixmatch.com/ws/1.1/'

# Genius API credentials
GENIUS_ACCESS_TOKEN = 'YOUR_GENIUS_ACCESS_TOKEN'
GENIUS_BASE_URL = 'https://api.genius.com/'


# Use Musixmatch to find lyrics else use genius

def get_lyrics_from_musixmatch(track_name, artist_name):
    endpoint = 'matcher.lyrics.get'
    params = {
        'apikey': MUSIXMATCH_API_KEY,
        'q_track': track_name,
        'q_artist': artist_name,
    }

    response = requests.get(f"{MUSIXMATCH_BASE_URL}{endpoint}", params=params)
    if response.status_code == 200:
        data = response.json()
        if data['message']['header']['status_code'] == 200:
            if 'lyrics_body' in data['message']['body']['lyrics']:
                lyrics = data['message']['body']['lyrics']['lyrics_body']
                return lyrics
    return None


def get_lyrics_from_genius(track_name, artist_name):
    headers = {'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'}
    params = {'q': f"{track_name} {artist_name}"}

    response = requests.get(f"{GENIUS_BASE_URL}search", headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'hits' in data['response'] and data['response']['hits']:
            song_id = data['response']['hits'][0]['result']['id']
            lyrics_path = f"songs/{song_id}/lyrics"
            lyrics_response = requests.get(f"{GENIUS_BASE_URL}{lyrics_path}", headers=headers)
            if lyrics_response.status_code == 200:
                lyrics_data = lyrics_response.json()
                if 'lyrics' in lyrics_data['response']:
                    lyrics = lyrics_data['response']['lyrics']['plain']
                    return lyrics
    return None


def get_lyrics(track_name, artist_name):
    musixmatch_lyrics = get_lyrics_from_musixmatch(track_name, artist_name)
    if musixmatch_lyrics:
        return musixmatch_lyrics
    else:
        genius_lyrics = get_lyrics_from_genius(track_name, artist_name)
        if genius_lyrics:
            return genius_lyrics
    return "Lyrics not found."


# Usage example:
track_name = "Song Name"
artist_name = "Artist Name"
lyrics = get_lyrics(track_name, artist_name)
print(lyrics)


# TRENDS

# Function to fetch Billboard chart data
def get_billboard_chart(chart_type, api_key):
    BILLBOARD_BASE_URL = f'https://api.billboard.com/charts/{chart_type}'

    params = {
        'key': api_key,
        'format': 'json'
    }

    response = requests.get(BILLBOARD_BASE_URL, params=params)
    if response.status_code == 200:
        chart_data = response.json()
        return chart_data['charts'][0]['entries'] if 'charts' in chart_data else None
    else:
        return None


# Usage example:
billboard_api_key = 'YOUR_BILLBOARD_API_KEY'  # Replace with your Billboard API key
top_songs = get_billboard_chart('hot-100', billboard_api_key)  # Fetches the Hot 100 chart
top_albums = get_billboard_chart('top-albums', billboard_api_key)  # Fetches the Top Albums chart


# Process and display the retrieved data as needed

# 30000 stations integration
def find_stations_playing_track(track_name, radio_api_key):
    RADIO_STATIONS_API_URL = 'https://api.30000radiostations.com/search'

    params = {
        'api_key': radio_api_key,
        'q': track_name,
        'limit': 10  # Adjust limit as needed
    }

    response = requests.get(RADIO_STATIONS_API_URL, params=params)
    if response.status_code == 200:
        stations_data = response.json()
        return stations_data['stations'] if 'stations' in stations_data else None
    else:
        return None


# Example: Find stations playing the top song from Billboard's Hot 100 chart
if top_songs:
    top_song_name = top_songs[0]['title']
    radio_stations_api_key = 'YOUR_RADIO_STATIONS_API_KEY'  # Replace with your Radio Stations API key
    stations_playing_top_song = find_stations_playing_track(top_song_name, radio_stations_api_key)
    if stations_playing_top_song:
        # Process stations' data or display station information
        for station in stations_playing_top_song:
            print(station['name'], station['stream_url'])  # Hypothetical display of station names and streaming URLs

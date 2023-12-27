# Spotify Integration
import spotipy
from spotipy import SpotifyClientCredentials


def get_spotify_song_info(track_name):
    client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID',
                                                          client_secret='YOUR_CLIENT_SECRET')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = sp.search(q=track_name, limit=1, type='track')

    if results['tracks']['items']:
        track_info = results['tracks']['items'][0]
        track_id = track_info['id']
        track_name = track_info['name']
        artist_name = track_info['artists'][0]['name']
        return track_name, artist_name
    else:
        return None, None
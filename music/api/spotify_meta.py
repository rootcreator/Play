import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_song_info(track_name):
    client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID',
                                                          client_secret='YOUR_CLIENT_SECRET')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    song_results = sp.search(q=track_name, limit=1, type='track')
    album_results = sp.search(q=track_name, limit=1, type='album')
    artist_results = sp.search(q=track_name, limit=1, type='artist')

    song_info = extract_track_info(song_results)
    album_info = extract_album_info(album_results)
    artist_info = extract_artist_info(artist_results)

    return song_info, album_info, artist_info


def extract_track_info(results):
    if results['tracks']['items']:
        track_info = results['tracks']['items'][0]
        track_id = track_info['id']
        track_name = track_info['name']
        artist_name = track_info['artists'][0]['name']
        return track_name, artist_name
    else:
        return None, None


def extract_album_info(results):
    if results['albums']['items']:
        album_info = results['albums']['items'][0]
        album_name = album_info['name']
        artist_name = album_info['artists'][0]['name']
        return album_name, artist_name
    else:
        return None, None


def extract_artist_info(results):
    if results['artists']['items']:
        artist_info = results['artists']['items'][0]
        artist_name = artist_info['name']
        return artist_name
    else:
        return None

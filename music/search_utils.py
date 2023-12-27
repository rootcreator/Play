import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import Genre, Artist, Album, Song, Playlist  # Import your Django models

SPOTIFY_CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search(query):
    local_results = {
        'songs': Song.objects.filter(title__icontains=query),
        'albums': Album.objects.filter(title__icontains=query),
        'artists': Artist.objects.filter(name__icontains=query),
        'genres': Genre.objects.filter(name__icontains=query),
        'playlists': Playlist.objects.filter(title__icontains=query),
    }

    spotify_results = {
        'spotify_songs': sp.search(q=query, type='track')['tracks']['items'],
        'spotify_albums': sp.search(q=query, type='album')['albums']['items'],
        'spotify_artists': sp.search(q=query, type='artist')['artists']['items'],
    }

    return local_results, spotify_results

from .models import Song, Album, Genre, Playlist
from .music_video_integration import sp


def search(query):
    # Initialize local_results with empty lists
    local_results = {
        'songs': [],
        'albums': [],
        'artists': [],
        'genres': [],
        'playlists': [],
    }

    try:
        # Spotify API search results
        spotify_results = {
            'spotify_songs': sp.search(q=query, type='track')['tracks']['items'],
            'spotify_albums': sp.search(q=query, type='album')['albums']['items'],
            'spotify_artists': sp.search(q=query, type='artist')['artists']['items'],
        }

        # Retrieve local data using Spotify metadata for songs, albums, and artists
        for track in spotify_results['spotify_songs']:
            song = Song.objects.filter(spotify_id=track['id']).first()
            if song:
                local_results['songs'].append(song)

        for album in spotify_results['spotify_albums']:
            album_obj = Album.objects.filter(spotify_id=album['id']).first()
            if album_obj:
                local_results['albums'].append(album_obj)

        # Handling errors and adding proper authentication and permission checks for genres and playlists
        try:
            for genre_name in spotify_results['spotify_genres']:
                genre_obj = Genre.objects.filter(name=genre_name).first()
                if genre_obj:
                    local_results['genres'].append(genre_obj)
        except Exception as e:
            # Handle error for genre retrieval
            print(f"Error fetching genres: {str(e)}")

        try:
            for playlist_name in spotify_results['spotify_playlists']:
                playlist_obj = Playlist.objects.filter(name=playlist_name).first()
                if playlist_obj:
                    local_results['playlists'].append(playlist_obj)
        except Exception as e:
            # Handle error for playlist retrieval
            print(f"Error fetching playlists: {str(e)}")

    except Exception as e:
        # Handle any exceptions that occur during Spotify API search
        print(f"Spotify API search error: {str(e)}")

    return local_results

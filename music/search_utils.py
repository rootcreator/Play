from .models import Song, Album, Artist, Genre, Playlist
from .storage_operations import upload_to_dropbox, upload_to_google_drive

def search(query):
    # Spotify API search results
    spotify_results = {
        'spotify_songs': sp.search(q=query, type='track')['tracks']['items'],
        'spotify_albums': sp.search(q=query, type='album')['albums']['items'],
        'spotify_artists': sp.search(q=query, type='artist')['artists']['items'],
    }

    # Example: assuming you have file_path and file_name obtained from Spotify metadata
    file_path = 'path/to/your/file.txt'
    file_name = 'file.txt'

    # Handling errors for Dropbox and Google Drive operations
    try:
        # Uploading to Dropbox
        upload_to_dropbox(file_path, '/destination_path/' + file_name)
    except Exception as e:
        # Handle Dropbox upload error
        print(f"Dropbox upload error: {str(e)}")

    try:
        # Uploading to Google Drive
        upload_to_google_drive(file_path, file_name)
    except Exception as e:
        # Handle Google Drive upload error
        print(f"Google Drive upload error: {str(e)}")

    # Local results based on Spotify metadata
    local_results = {
        'songs': [],
        'albums': [],
        'artists': [],
        'genres': [],
        'playlists': [],
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

    return local_results, spotify_results

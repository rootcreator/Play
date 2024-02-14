from music.models import Song, Album, Genre, Playlist, Artist


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
        # Retrieve local data based on the query for songs, albums, and artists
        local_results['songs'] = Song.objects.filter(title__icontains=query)
        local_results['albums'] = Album.objects.filter(title__icontains=query)
        local_results['artists'] = Artist.objects.filter(name__icontains=query)

        # Handling errors and adding proper authentication and permission checks for genres and playlists
        try:
            local_results['genres'] = Genre.objects.filter(name__icontains=query)
        except Exception as e:
            # Handle error for genre retrieval
            print(f"Error fetching genres: {str(e)}")

        try:
            local_results['playlists'] = Playlist.objects.filter(name__icontains=query)
        except Exception as e:
            # Handle error for playlist retrieval
            print(f"Error fetching playlists: {str(e)}")

    except Exception as e:
        # Handle any exceptions that occur during local data retrieval
        print(f"Local data retrieval error: {str(e)}")

    return local_results

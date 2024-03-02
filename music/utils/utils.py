import os
import requests
from music.models import Song, Album, Artist, Genre

AUDIO_FILES_DIRECTORY = 'audio_files'  # Directory to store audio files


def download_audio_file(url, filename):
    # Ensure the directory exists
    os.makedirs(AUDIO_FILES_DIRECTORY, exist_ok=True)

    # Download the audio file
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(AUDIO_FILES_DIRECTORY, filename), 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False


def populate_songs_and_albums_from_api():
    # Make HTTP GET requests to retrieve data for songs and albums
    song_data = requests.get('http://other-app-url/api/songs/').json()
    album_data = requests.get('http://other-app-url/api/albums/').json()

    # Process and create Song instances
    for song_info in song_data:
        # Extract relevant information from song_info
        title = song_info.get('title')
        artist_name = song_info.get('artist')
        genre_name = song_info.get('genre')
        audio_url = song_info.get('audio_url')
        audio_filename = f"{title}.mp3"  # Assuming MP3 audio format

        # Create or retrieve Artist instance
        artist, _ = Artist.objects.get_or_create(name=artist_name)

        # Create or retrieve Genre instance
        genre, _ = Genre.objects.get_or_create(name=genre_name)

        # Create Song instance and associate with artist and genre
        song, created = Song.objects.get_or_create(title=title, artist=artist)
        song.genre.add(genre)  # Assuming ManyToManyField between Song and Genre

        # Download and store audio file
        if audio_url:
            download_audio_file(audio_url, audio_filename)

    # Process and create Album instances
    for album_info in album_data:
        # Extract relevant information from album_info
        title = album_info.get('title')
        artist_name = album_info.get('artist')
        genre_name = album_info.get('genre')
        audio_url = album_info.get('audio_url')
        audio_filename = f"{title}.mp3"  # Assuming MP3 audio format

        # Create or retrieve Artist instance
        artist, _ = Artist.objects.get_or_create(name=artist_name)

        # Create or retrieve Genre instance
        genre, _ = Genre.objects.get_or_create(name=genre_name)

        # Create Album instance and associate with artist and genre
        album, created = Album.objects.get_or_create(title=title, artist=artist)
        album.genre.add(genre)  # Assuming ManyToManyField between Album and Genre

        # Download and store audio file
        if audio_url:
            download_audio_file(audio_url, audio_filename)

        # Update artist and genre information if it has changed
        artist.save()
        genre.save()

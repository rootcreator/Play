from django.shortcuts import render
from django.http import HttpResponse
from music.models import Song, Album, Playlist  # Import models from the music app

def play_song(request, song_id):
    # Logic to play the song with the given ID
    song = Song.objects.get(id=song_id)
    return HttpResponse(f"Now playing: {song.title}")

def play_album(request, album_id):
    # Logic to play all songs from the album with the given ID
    album = Album.objects.get(id=album_id)
    songs = album.song_set.all()
    return render(request, 'music_player/album.html', {'songs': songs})

def play_playlist(request, playlist_id):
    # Logic to play all songs from the playlist with the given ID
    playlist = Playlist.objects.get(id=playlist_id)
    songs = playlist.songs.all()
    return render(request, 'music_player/playlist.html', {'songs': songs})

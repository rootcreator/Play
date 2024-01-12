from django.urls import path
from . import views
from .views import display_radio_stations, SearchView, index

urlpatterns = [
    path('music/genres/', views.GenreListCreateView.as_view(), name='genre-list'),
    path('music/artists/', views.ArtistListCreateView.as_view(), name='artist-list'),
    path('music/albums/', views.AlbumListCreateView.as_view(), name='album-list'),
    path('music/songs/', views.SongListCreateView.as_view(), name='song-list'),
    path('music/playlists/', views.PlaylistListCreateView.as_view(), name='playlist-list'),

    path('audio-files/', views.AudioFileListCreateView.as_view(), name='audio-file-list'),


    path('search/', views.SearchView.as_view(), name='search'),
    path('add-song-to-library/', views.AddSongToLibraryView.as_view(), name='add-song-to-library'),

    path('upload-file/', views.FileUploadView.as_view(), name='upload-file'),
    path('spotify-info/', views.SpotifyInfoView.as_view(), name='spotify-info'),
    path('song-library/', views.SongLibraryView.as_view(), name='song-library'),
    path('lyrics/', views.LyricsView.as_view(), name='lyrics'),
    path('lastfm-integration/', views.LastFmIntegration.as_view(), name='lastfm-integration'),
    path('trends/', views.TrendsIntegration.as_view(), name='trends'),
    path('radio/', display_radio_stations, name='radio_stations'),
    path('search/', SearchView.as_view(), name='search_view'),
    path('', index, name='index')
]

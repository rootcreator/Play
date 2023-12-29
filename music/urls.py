from django.urls import path
from . import views

urlpatterns = [
    path('genres/', views.GenreListCreateView.as_view(), name='genre-list'),
    path('artists/', views.ArtistListCreateView.as_view(), name='artist-list'),
    path('albums/', views.AlbumListCreateView.as_view(), name='album-list'),
    path('songs/', views.SongListCreateView.as_view(), name='song-list'),
    path('playlists/', views.PlaylistListCreateView.as_view(), name='playlist-list'),
    path('user-profiles/', views.UserProfileListCreateView.as_view(), name='user-profile-list'),
    path('user-libraries/', views.UserLibraryListCreateView.as_view(), name='user-library-list'),
    path('audio-files/', views.AudioFileListCreateView.as_view(), name='audio-file-list'),
    path('users/', views.UserListCreateView.as_view(), name='user-list'),

    path('search/', views.SearchView.as_view(), name='search'),
    path('add-song-to-library/', views.AddSongToLibraryView.as_view(), name='add-song-to-library'),

    path('upload-file/', views.FileUploadView.as_view(), name='upload-file'),
    path('spotify-info/', views.SpotifyInfoView.as_view(), name='spotify-info'),
    path('song-library/', views.SongLibraryView.as_view(), name='song-library'),
    path('lyrics/', views.LyricsView.as_view(), name='lyrics'),
    path('lastfm-integration/', views.LastFmIntegration.as_view(), name='lastfm-integration'),
    path('trends/', views.TrendsIntegration.as_view(), name='trends'),
]

from django.urls import path
from . import views

from .views import SearchView, index, add_to_library, remove_from_library, song_detail, SongListCreateView, \
    AlbumListCreateView, ArtistDetailView, AlbumDetailView, PlaylistDetailView, PlaylistListCreateView
from .views import fetch_saavn_track_info

urlpatterns = [
    path('music/genres/', views.GenreListCreateView.as_view(), name='genre-list'),
    path('music/artists/', views.ArtistListCreateView.as_view(), name='artist-list'),
    path('music/albums/', views.AlbumListCreateView.as_view(), name='album-list'),
    path('music/songs/', views.SongListCreateView.as_view(), name='song-list'),
    path('music/playlists/', views.PlaylistListCreateView.as_view(), name='playlist-list'),

    path('audio-files/', views.AudioFileListCreateView.as_view(), name='audio-file-list'),


    path('search/', views.SearchView.as_view(), name='search'),


    path('upload-file/', views.FileUploadView.as_view(), name='upload-file'),
    path('spotify-info/', views.SpotifyInfoView.as_view(), name='spotify-info'),

    path('lyrics/', views.LyricsView.as_view(), name='lyrics'),
    path('lastfm-integration/', views.LastFmIntegration.as_view(), name='lastfm-integration'),
    path('trends/', views.TrendsIntegration.as_view(), name='trends'),
    path('search/', SearchView.as_view(), name='search_view'),
    path('', index, name='index'),

    path('songs/', SongListCreateView.as_view(), name='song_list'),  # Define the URL pattern for the song list view
    path('song/<int:song_id>/', song_detail, name='song_detail'),

    path('playlist/<int:playlist_id>/', PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlists/', PlaylistListCreateView.as_view(), name='playlist_list'),




    path('artist/<int:artist_id>/', ArtistDetailView.as_view(), name='artist_detail'),

    path('albums/', AlbumListCreateView.as_view(), name='album_list'),
    path('albums/<int:album_id>/', AlbumDetailView.as_view(), name='album_detail'),  # Use 'album_id' instead of 'pk'
    path('album/<int:album_id>/', AlbumDetailView.as_view(), name='album_detail'),









    path('api/saavn/track/<str:track_id>/', fetch_saavn_track_info, name='fetch_saavn_track_info'),
    path('add-to-library/<str:content_type>/<int:content_id>/', add_to_library, name='add_to_library'),
    path('remove-from-library/<str:content_type>/<int:content_id>/', remove_from_library, name='remove_from_library'),

]

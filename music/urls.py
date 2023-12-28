from django.urls import path
from . import views

urlpatterns = [
    # API URLs
    path('api/genres/', views.GenreList.as_view(), name='genre-list'),
    path('api/artists/', views.ArtistList.as_view(), name='artist-list'),
    path('api/albums/', views.AlbumList.as_view(), name='album-list'),
    path('api/songs/', views.SongList.as_view(), name='song-list'),
    path('api/playlists/', views.PlaylistList.as_view(), name='playlist-list'),

    # Other API URLs
    path('api/convert/', views.AudioConversionAPIView.as_view(), name='convert_audio'),
    path('api/search/', views.search_api, name='search_api'),
    path('api/upload/album/', views.AlbumUploadView.as_view(), name='album-upload'),
    path('api/upload/song/', views.SongUploadView.as_view(), name='song-upload'),
    path('api/user-profile/', views.UserProfileDetail.as_view(), name='user-profile'),


    # Regular URLs
    path('', views.index, name='index'),
    path('songs/', views.songs_view, name='songs'),
    path('albums/', views.albums_view, name='albums'),
    path('genres/', views.genres_view, name='genres'),
    path('artists/', views.artists_view, name='artists'),
    path('user-profile/', views.user_profile_view, name='user_profile'),
]

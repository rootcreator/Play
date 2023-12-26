from django.urls import path
from . import views

urlpatterns = [
    # URLs for listing and creating resources
    path('api/genres/', views.GenreList.as_view(), name='genre-list'),
    path('api/artists/', views.ArtistList.as_view(), name='artist-list'),
    path('api/albums/', views.AlbumList.as_view(), name='album-list'),
    path('api/songs/', views.SongList.as_view(), name='song-list'),
    path('api/playlists/', views.PlaylistList.as_view(), name='playlist-list'),
    path('api/user-profiles/', views.UserProfileList.as_view(), name='user-profile-list'),
    path('api/user-libraries/', views.UserLibraryList.as_view(), name='user-library-list'),

    # URLs for retrieving, updating, or deleting a single resource by ID
    path('api/genres/<int:pk>/', views.GenreDetail.as_view(), name='genre-detail'),
    path('api/artists/<int:pk>/', views.ArtistDetail.as_view(), name='artist-detail'),
    path('api/albums/<int:pk>/', views.AlbumDetail.as_view(), name='album-detail'),
    path('api/songs/<int:pk>/', views.SongDetail.as_view(), name='song-detail'),
    path('api/playlists/<int:pk>/', views.PlaylistDetail.as_view(), name='playlist-detail'),
    path('api/user-profiles/<int:pk>/', views.UserProfileDetail.as_view(), name='user-profile-detail'),
    path('api/user-libraries/<int:pk>/', views.UserLibraryDetail.as_view(), name='user-library-detail'),

    # Additional URLs as needed for various functionalities
    path('api/user-profile/', views.UserProfileDetail.as_view(), name='user-profile'),
    path('api/upload/album/', views.AlbumUploadView.as_view(), name='album-upload'),
    path('api/upload/song/', views.SongUploadView.as_view(), name='song-upload'),


    path('', views.index, name='index'),
    path('songs/', views.songs_view, name='songs'),
    path('albums/', views.albums_view, name='albums'),
    path('genres/', views.genres_view, name='genres'),
    path('artists/', views.artists_view, name='artists'),
    path('user-profile/', views.user_profile_view, name='user_profile'),


]

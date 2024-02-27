from django.urls import path
from . import views
from .views import combined_view, SearchAPIView

urlpatterns = [
    path('genres/', views.GenreListCreate.as_view(), name='genre-list-create'),
    path('artists/', views.ArtistListCreate.as_view(), name='artist-list-create'),
    path('songs/', views.SongListCreate.as_view(), name='song-list-create'),
    path('albums/', views.AlbumListCreate.as_view(), name='album-list-create'),
    path('playlists/', views.PlaylistListCreate.as_view(), name='playlist-list-create'),
    path('genreradios/', views.GenreRadioListCreate.as_view(), name='genreradio-list-create'),
    # Add more URLs as needed
    path('combined/', combined_view, name='combined-view'),
    path('search/', SearchAPIView.as_view(), name='search'),
]

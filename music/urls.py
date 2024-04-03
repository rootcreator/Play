from django.urls import path
from . import view
from .view import CombinedAPIView, SearchAPIView

urlpatterns = [
    path('genres/', view.GenreListCreate.as_view(), name='genre-list-create'),
    path('artists/', view.ArtistListCreate.as_view(), name='artist-list-create'),
    path('songs/', view.SongListCreate.as_view(), name='song-list-create'),
    path('albums/', view.AlbumListCreate.as_view(), name='album-list-create'),
    path('playlists/', view.PlaylistListCreate.as_view(), name='playlist-list-create'),
    #path('genreradios/', views.GenreRadioListCreate.as_view(), name='genreradio-list-create'),
    # Add more URLs as needed
    path('combined/', CombinedAPIView.as_view(), name='combined-view'),
    path('search/', SearchAPIView.as_view(), name='apisearch'),


]



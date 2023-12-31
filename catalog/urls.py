from django.urls import path
from .views import GenreListCreateView, ArtistListCreateView, ComposerListCreateView, AlbumListCreateView, SongListCreateView

urlpatterns = [
    path('genres/', GenreListCreateView.as_view(), name='genre-list'),
    path('artists/', ArtistListCreateView.as_view(), name='artist-list'),
    path('composers/', ComposerListCreateView.as_view(), name='composer-list'),
    path('albums/', AlbumListCreateView.as_view(), name='album-list'),
    path('songs/', SongListCreateView.as_view(), name='song-list'),
    # Define more URLs for other views/APIs if needed
]

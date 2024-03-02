from django.urls import path
from catalog.views import (
    SongAPIView, SongDetailAPIView,
    AlbumAPIView, AlbumDetailAPIView,
    AudioFileAPIView, AudioFileDetailAPIView, MusicFormView, upload_song
)

urlpatterns = [

    # URLs for Song
    path('songs/', SongAPIView.as_view(), name='song-list'),
    path('songs/<int:pk>/', SongDetailAPIView.as_view(), name='song-detail'),

    # URLs for Album
    path('albums/', AlbumAPIView.as_view(), name='album-list'),
    path('albums/<int:pk>/', AlbumDetailAPIView.as_view(), name='album-detail'),

    # URLs for AudioFile
    path('audio-files/', AudioFileAPIView.as_view(), name='audiofile-list'),
    path('audio-files/<int:pk>/', AudioFileDetailAPIView.as_view(), name='audiofile-detail'),


    path('form/', MusicFormView.as_view(), name='music_form'),
    path('upload/', upload_song, name='upload_song'),
]

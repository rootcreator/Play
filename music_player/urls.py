from django.urls import path
from . import views

urlpatterns = [
    path('play/song/<int:song_id>/', views.play_song, name='play_song'),
    path('play/album/<int:album_id>/', views.play_album, name='play_album'),
    path('play/playlist/<int:playlist_id>/', views.play_playlist, name='play_playlist'),
]

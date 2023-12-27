from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'genres', views.GenreViewSet)
router.register(r'artists', views.ArtistViewSet)
router.register(r'albums', views.AlbumViewSet)
router.register(r'songs', views.SongViewSet)
router.register(r'playlists', views.PlaylistViewSet)
router.register(r'user-profiles', views.UserProfileViewSet)
router.register(r'user-libraries', views.UserLibraryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/convert/', views.AudioConversionAPIView.as_view(), name='convert_audio'),
    path('api/search/', views.search_api, name='search_api'),
    path('api/upload/album/', views.AlbumUploadView.as_view(), name='album-upload'),
    path('api/upload/song/', views.SongUploadView.as_view(), name='song-upload'),
    path('api/user-profile/', views.UserProfileDetail.as_view(), name='user-profile'),

    # Your other non-API URLs
    path('', views.index, name='index'),
    path('songs/', views.songs_view, name='songs'),
    path('albums/', views.albums_view, name='albums'),
    path('genres/', views.genres_view, name='genres'),
    path('artists/', views.artists_view, name='artists'),
    path('user-profile/', views.user_profile_view, name='user_profile'),


]

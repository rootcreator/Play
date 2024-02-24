from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, ArtistViewSet, AlbumViewSet, SongViewSet, PlaylistViewSet, \
    AudioFileViewSet, UserViewSet, APIMusicViewSet, SearchViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'playlists', PlaylistViewSet)
router.register(r'audiofiles', AudioFileViewSet)
router.register(r'users', UserViewSet)
router.register(r'apimusic', APIMusicViewSet)
router.register(r'search', SearchViewSet, basename='search')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Add the URL pattern for search
    path('search/', include(router.urls)),
]

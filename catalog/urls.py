from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet, GenreViewSet, AlbumViewSet, SongViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)

urlpatterns = [
    # Your other URL patterns if any
    path('', include(router.urls)),
]

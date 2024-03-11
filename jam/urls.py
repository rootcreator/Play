from django.urls import path
from .views import TrendsAPIView, RecommendedAPIView, FeedsAPIView
from .views import RecommendationView, SongRecommendationView, PlaylistRecommendationView, AlbumRecommendationView

urlpatterns = [
    path('trends/', TrendsAPIView.as_view(), name='trends-list-create'),
    path('recommended/', RecommendedAPIView.as_view(), name='recommended-list-create'),
    path('feeds/', FeedsAPIView.as_view(), name='feeds-list-create'),
    path('recommendations/<int:user_id>/', RecommendationView.as_view(), name='recommendations'),
    path('song-recommendations/<int:user_id>/', SongRecommendationView.as_view(), name='song-recommendations'),
    path('playlist-recommendations/<int:user_id>/', PlaylistRecommendationView.as_view(), name='playlist-recommendations'),
    path('album-recommendations/<int:user_id>/', AlbumRecommendationView.as_view(), name='album-recommendations'),
    path('trending-recommendation/', TrendsAPIView.as_view(), name='trends-recommendation-list-create'),
]


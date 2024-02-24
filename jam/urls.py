from django.urls import path
from . import views

urlpatterns = [
    # URLs for SimilarPlaylists
    path('similarplaylists/', views.SimilarPlaylistsList.as_view(), name='similarplaylists-list'),
    path('similarplaylists/<int:pk>/', views.SimilarPlaylistsDetail.as_view(), name='similarplaylists-detail'),

    # URLs for SimilarReleases
    path('similarreleases/', views.SimilarReleasesList.as_view(), name='similarreleases-list'),
    path('similarreleases/<int:pk>/', views.SimilarReleasesDetail.as_view(), name='similarreleases-detail'),

    # URL for Trends
    path('trends/', views.TrendsList.as_view(), name='trends-list'),

    # URLs for Favourites
    path('favourites/', views.FavouritesList.as_view(), name='favourites-list'),
    path('favourites/<int:pk>/', views.FavouritesDetail.as_view(), name='favourites-detail'),

    # URLs for RecommendedSongs
    path('recommendedsongs/', views.RecommendedSongsList.as_view(), name='recommendedsongs-list'),
    path('recommendedsongs/<int:pk>/', views.RecommendedSongsDetail.as_view(), name='recommendedsongs-detail'),

    path('feeds/', views.FeedsList.as_view(), name='feeds-list'),
    path('feeds/<int:pk>/', views.FeedsDetail.as_view(), name='feeds-detail'),

    path('likes/', views.LikeListCreate.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', views.LikeDetail.as_view(), name='like-detail'),
]

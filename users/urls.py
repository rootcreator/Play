from django.urls import path
from . import views

urlpatterns = [
    # URL patterns for UserProfile
    path('user-profiles/', views.UserProfileListCreateView.as_view(), name='userprofile-list'),
    path('user-profiles/<int:pk>/', views.UserProfileDetailView.as_view(), name='userprofile-detail'),

    # URL patterns for UserLibrary
    path('user-libraries/', views.UserLibraryListCreateView.as_view(), name='userlibrary-list'),
    path('user-libraries/<int:pk>/', views.UserLibraryDetailView.as_view(), name='userlibrary-detail'),

    # URL patterns for UserProfileView
    path('user-profile-views/', views.UserProfileViewListCreateView.as_view(), name='profileview-list'),
    path('user-profile-views/<int:pk>/', views.UserProfileViewDetailView.as_view(), name='profileview-detail'),

    # Additional URL patterns for Songs
    path('songs/', views.SongListCreateView.as_view(), name='song-list'),
    path('songs/<int:pk>/', views.SongDetailView.as_view(), name='song-detail'),

    # Additional URL patterns for Albums
    path('albums/', views.AlbumListCreateView.as_view(), name='album-list'),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),

    # Additional URL patterns for Playlists
    path('playlists/', views.PlaylistListCreateView.as_view(), name='playlist-list'),
    path('playlists/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),

    # Custom root API endpoint (if applicable)
    path('', views.custom_api_root, name='custom-api-root'),
    path('api/user-profile/', views.UserProfileDetailView.as_view(), name='user-profile'),

]

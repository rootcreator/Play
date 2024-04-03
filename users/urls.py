from django.urls import path
from .views import (
    RegistrationAPIView, LoginAPIView, ProfileAPIView, LibraryAPIView,
    UserUploadAPIView, LikeAPIView, FavouritesAPIView, ListeningHistoryAPIView,
    SettingsAPIView
)

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user_register'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('profile/', ProfileAPIView.as_view(), name='user_profile'),
    path('library/', LibraryAPIView.as_view(), name='user_library'),
    path('upload/', UserUploadAPIView.as_view(), name='user_upload'),
    path('like/', LikeAPIView.as_view(), name='user_like'),
    path('favourites/', FavouritesAPIView.as_view(), name='user_favourites'),
    path('listening-history/', ListeningHistoryAPIView.as_view(), name='user_listening_history'),
    path('settings/', SettingsAPIView.as_view(), name='user_settings'),
]

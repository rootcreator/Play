from django.urls import path
from .views import ProfileAPIView, LibraryAPIView, LikeAPIView, ListeningHistoryAPIView, SettingsAPIView, \
    RecentlyPlayedAPIView, LoginAPIView, FavouritesAPIView, my_uploaded_songs, RegistrationAPIView

urlpatterns = [
    path('all-profiles/', ProfileAPIView.as_view(), name='all-profiles'),
    path('all-libraries/', LibraryAPIView.as_view(), name='all-libraries'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('library/', LibraryAPIView.as_view(), name='library'),
    path('likes/', LikeAPIView.as_view(), name='likes'),
    path('favourites/', FavouritesAPIView.as_view(), name='favourites-list-create'),
    path('listening-histories/', ListeningHistoryAPIView.as_view(), name='listening_histories'),
    path('settings/', SettingsAPIView.as_view(), name='settings'),
    path('recently-played/', RecentlyPlayedAPIView.as_view(), name='recently-played'),



    path('my-songs/', my_uploaded_songs, name='my_uploaded_songs'),
    path('register/', RegistrationAPIView.as_view(), name='register'),

]

from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('library/<str:username>/', views.user_library, name='user_library'),
    # Define other URL patterns for user-related functionalities
]

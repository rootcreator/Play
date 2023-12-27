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
    path('user-profile-views/', views.UserProfileViewListCreateView.as_view(), name='profile-view-list'),
    path('user-profile-views/<int:pk>/', views.UserProfileViewDetailView.as_view(), name='profile-view-detail'),

    # Dashboard and User Profile Settings URLs

    path('profile/', views.user_profile, name='user_profile'),
    path('settings/', views.user_settings, name='profile_settings'),
    path('library/', views.user_library, name='user_library'),

    path('login/', views.login_view, name='login'),
    # Add other URL patterns for other functionalities or API views if needed
]

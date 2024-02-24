from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, LibraryViewSet, ListeningHistoryViewSet, SettingsViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'libraries', LibraryViewSet)
router.register(r'listening-history', ListeningHistoryViewSet)
router.register(r'settings', SettingsViewSet)

# Define the urlpatterns
urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    # Include the login URLs for the browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_auth')),
    # Add a register endpoint for profiles
    path('profiles/register/', ProfileViewSet.as_view({'post': 'register'}), name='profile_register'),
    # Add a login endpoint for profiles
    path('profiles/login/', ProfileViewSet.as_view({'post': 'login'}), name='profile_login'),
]

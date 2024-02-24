from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, LibraryViewSet, ListeningHistoryViewSet, SettingsViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'libraries', LibraryViewSet, basename='library')
router.register(r'listening_history', ListeningHistoryViewSet, basename='history')
router.register(r'settings', SettingsViewSet)



urlpatterns = router.urls


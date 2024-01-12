from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserProfileViewViewSet, UserLibraryViewSet, ListeningHistoryViewSet

router = DefaultRouter()

router.register(r'userprofiles', UserProfileViewSet, basename='userprofile')
router.register(r'userprofileviews', UserProfileViewViewSet, basename='userprofileview')
router.register(r'userlibraries', UserLibraryViewSet, basename='userlibrary')
router.register(r'listeninghistories', ListeningHistoryViewSet, basename='listeninghistory')

router.register(r'user-profile', UserProfileViewSet, basename='user-profile')



urlpatterns = router.urls


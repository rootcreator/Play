from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserLibraryViewSet, ListeningHistoryViewSet,  \
    dashboard_view

router = DefaultRouter()

router.register(r'userprofiles', UserProfileViewSet, basename='userprofile')
router.register(r'userlibraries', UserLibraryViewSet, basename='userlibrary')
router.register(r'listeninghistories', ListeningHistoryViewSet, basename='listeninghistory')

urlpatterns = [
    path('api/', include(router.urls)),
    #path('js-render/', JsRenderTemplateView.as_view(), name='js-render'),
    #path('api/endpoint/', ApiEndpoint.as_view(), name='api-endpoint'),
    # Add other URL patterns for non-API views if needed
    path('dashboard/', dashboard_view, name='dashboard'),
]

# Override the default API root view to use a plain text response
from rest_framework.routers import APIRootView


class CustomAPIRootView(APIRootView):
    renderer_classes = [APIRootView.renderer_classes[0]]


urlpatterns += [
    path('api/', CustomAPIRootView.as_view(), name='api-root'),
]

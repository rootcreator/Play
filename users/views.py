import requests
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile, UserLibrary, ListeningHistory
from .serializers import UserProfileSerializer, UserLibrarySerializer, ListeningHistorySerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            # Render HTML page with JavaScript-based rendering
            return render(request, 'profile.html')
        else:
            # Provide JSON API response
            return super().list(request, *args, **kwargs)


class UserLibraryViewSet(viewsets.ModelViewSet):
    queryset = UserLibrary.objects.all()
    serializer_class = UserLibrarySerializer

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            # Render HTML page with JavaScript-based rendering
            return render(request, 'library.html')
        else:
            # Provide JSON API response
            return super().list(request, *args, **kwargs)


class ListeningHistoryViewSet(viewsets.ModelViewSet):
    queryset = ListeningHistory.objects.all()
    serializer_class = ListeningHistorySerializer

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            # Render HTML page with JavaScript-based rendering
            return render(request, 'listeninghistory_js_render.html')
        else:
            # Provide JSON API response
            return super().list(request, *args, **kwargs)


#class JsRenderTemplateView(TemplateView):
#    template_name = 'dashboard.html'


#class ApiEndpoint(APIView):
#    def get(self, request):
#        # Your API logic here
#        data = {'message': 'Hello, this is your API endpoint!'}
#        return Response(data)


def dashboard_view(request):
    try:
        # Assuming you have a one-to-one relationship with UserProfile in your UserLibrary model
        user_library = UserLibrary.objects.get(user_profile__user=request.user)
        playlists = user_library.created_playlists.all()
        recently_played = user_library.recently_played.all()
        # Add other fields as needed

        return render(request, 'dashboard.html', {'playlists': playlists, 'recently_played': recently_played})
    except UserLibrary.DoesNotExist:
        error_message = "User Library not found."
        return render(request, 'dashboard.html', {'error_message': error_message})
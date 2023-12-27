from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import UserProfile, UserLibrary, UserProfileView
from .serializers import UserProfileSerializer, UserLibrarySerializer, UserProfileViewSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

#login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_profile')  # Redirect to user's profile page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Custom views for Dashboard Functionalities
@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'user_profile': user_profile})


@login_required
def user_settings(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'users/settings.html', {'user_profile': user_profile})

@login_required
def user_library(request):
    user_library = UserLibrary.objects.get(user_profile__user=request.user)
    return render(request, 'users/library.html', {'user_library': user_library})

# API Views for UserProfile
class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# API Views for UserLibrary
class UserLibraryListCreateView(generics.ListCreateAPIView):
    queryset = UserLibrary.objects.all()
    serializer_class = UserLibrarySerializer

class UserLibraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserLibrary.objects.all()
    serializer_class = UserLibrarySerializer

# API Views for UserProfileView
class UserProfileViewListCreateView(generics.ListCreateAPIView):
    queryset = UserProfileView.objects.all()
    serializer_class = UserProfileViewSerializer

class UserProfileViewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfileView.objects.all()
    serializer_class = UserProfileViewSerializer

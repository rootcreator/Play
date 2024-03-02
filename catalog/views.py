from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import generics, permissions
from catalog.models import Song, Album, AudioFile
from catalog.serializers import SongSerializer, AlbumSerializer, \
    AudioFileSerializer
from django.views.generic import TemplateView
from .forms import SongForm, AlbumForm


class SongAPIView(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SongDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AlbumAPIView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AlbumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AudioFileAPIView(generics.ListCreateAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AudioFileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# Music Form
class MusicFormView(TemplateView):
    template_name = 'music_form.html'  # Assuming you have a template named 'music_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_form'] = SongForm()  # Pass an instance of SongForm to the template context
        context['album_form'] = AlbumForm()  # Pass an instance of AlbumForm to the template context
        return context


# User Upload
@login_required
def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.user = request.user
            song.save()
            return redirect('home')  # Redirect to the homepage after successful upload
    else:
        form = SongForm()
    return render(request, 'upload.html', {'form': form})
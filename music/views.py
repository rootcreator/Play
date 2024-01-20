from django.views.generic import TemplateView
from pyradios import RadioBrowser
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse

from recommendations.recommendation_utils import recommend_songs, profile_user
from . import radio_integrate
from .music_video_integration import get_youtube_video
from .search_utils import search
from .spotify_integration import get_spotify_song_info
from rest_framework import generics, status
from .models import (
    Genre, Artist, Album, Song, Playlist, UserProfile, UserLibrary, AudioFile
)
from .serializers import (
    GenreSerializer, ArtistSerializer, AlbumSerializer, SongSerializer, PlaylistSerializer, UserProfileSerializer,
    UserLibrarySerializer, AudioFileSerializer, UserSerializer, SpotifySerializer
)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
import dropbox
from django.db.models import Q
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.credentials import Credentials
import os
import requests



class GenericListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'genres.html'


class ArtistListCreateView(GenericListCreateView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'artists.html'


class AlbumListCreateView(GenericListCreateView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'albums.html'


class AlbumListCreateView(TemplateView):
    template_name = 'albums.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = Album.objects.all()  # Fetch all songs
        return context


class SongListCreateView(GenericListCreateView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'songs.html'


class SongListCreateView(TemplateView):
    template_name = 'songs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = Song.objects.all()  # Fetch all songs
        return context


class PlaylistListCreateView(GenericListCreateView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'playlists.html'


class PlaylistListCreateView(TemplateView):
    template_name = 'playlists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlists'] = Playlist.objects.all()  # Fetch all playlists
        return context


class AudioFileListCreateView(GenericListCreateView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer


# Storage integration

# Dropbox configurations
DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'

# Google Drive configurations
SCOPES = ['https://www.googleapis.com/auth/drive']
GOOGLE_DRIVE_CREDENTIALS_FILE = 'credentials.json'  # Update with your credentials file


class FileUploadView(APIView):
    def upload_to_dropbox(self, file_path, destination_path):
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        with open(file_path, 'rb') as f:
            dbx.files_upload(f.read(), destination_path)

    def upload_to_google_drive(self, file_path, file_name, folder_id=None):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json')
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_DRIVE_CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = {'mimeType': 'application/octet-stream', 'body': open(file_path, 'rb')}
        service.files().create(body=file_metadata, media_body=media).execute()

    def list_files_from_google_drive(self):
        creds = Credentials.from_authorized_user_file('token.json')
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(f"{item['name']} ({item['id']})")

    def post(self, request):
        if request.method == 'POST':
            file_path = request.data.get('file_path')
            destination_path = request.data.get('destination_path')
            folder_id = request.data.get('folder_id')
            file_name = request.data.get('file_name')

            # Uploading to Dropbox
            self.upload_to_dropbox(file_path, destination_path)

            # Uploading to Google Drive
            self.upload_to_google_drive(file_path, file_name, folder_id)

            # Listing files from Google Drive
            self.list_files_from_google_drive()

            return JsonResponse({'message': 'File uploaded successfully'})

        return JsonResponse({'message': 'Invalid request method'}, status=400)


# Music_Video Integration
# Initialize Spotify and YouTube API clients
SPOTIFY_CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


class SongLibraryView(APIView):
    def get_youtube_video(self, track_name, artist_name):
        search_query = f"{track_name} {artist_name} official music video"
        search_response = youtube.search().list(
            q=search_query,
            part='id',
            maxResults=1,
            type='video'
        ).execute()

        if 'items' in search_response and search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            return video_url
        else:
            return None

    def get_spotify_song_info(self, track_name):
        track = sp.search(q=track_name, limit=1, type='track')

        if track['tracks']['items']:
            track = track['tracks']['items'][0]
            song_title = track['name']
            artist_name = track['artists'][0]['name']
            return song_title, artist_name
        else:
            return None, None

    def post(self, request):
        track_name = request.data.get('track_name')
        user_profile = request.user.music_user_profile  # Assuming user is authenticated and has a profile

        if track_name and user_profile:
            song_title, artist_name = self.get_spotify_song_info(track_name)

            if song_title and artist_name:
                song = Song.objects.get_or_create(title=song_title)[0]
                artist = Artist.objects.get_or_create(name=artist_name)[0]

                if song and artist:
                    user_library = UserLibrary.objects.get_or_create(user_profile=user_profile)[0]
                    user_library.saved_songs.add(song)

                    video_url = self.get_youtube_video(song_title, artist_name)
                    if video_url:
                        song.youtube_url = video_url
                        song.save()
                        return Response(f"Song '{song_title}' added to library with YouTube link: {video_url}")

        return Response("Failed to add song to library or find YouTube video", status=400)


# Spotify Integration


class SpotifyInfoView(APIView):
    def get_spotify_song_info(self, track_name):
        client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID',
                                                              client_secret='YOUR_CLIENT_SECRET')
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        song_results = sp.search(q=track_name, limit=1, type='track')
        album_results = sp.search(q=track_name, limit=1, type='album')
        artist_results = sp.search(q=track_name, limit=1, type='artist')

        song_info = self.extract_track_info(song_results)
        album_info = self.extract_album_info(album_results)
        artist_info = self.extract_artist_info(artist_results)

        return song_info, album_info, artist_info

    def extract_track_info(self, results):
        if results['tracks']['items']:
            track_info = results['tracks']['items'][0]
            track_id = track_info['id']
            track_name = track_info['name']
            artist_name = track_info['artists'][0]['name']
            return track_name, artist_name
        else:
            return None, None

    def extract_album_info(self, results):
        if results['albums']['items']:
            album_info = results['albums']['items'][0]
            album_name = album_info['name']
            artist_name = album_info['artists'][0]['name']
            return album_name, artist_name
        else:
            return None, None

    def extract_artist_info(self, results):
        if results['artists']['items']:
            artist_info = results['artists']['items'][0]
            artist_name = artist_info['name']
            return artist_name
        else:
            return None

    def post(self, request):
        track_name = request.data.get('track_name')  # Assuming 'track_name' is sent in the POST data

        if track_name:
            song_info, album_info, artist_info = self.get_spotify_song_info(track_name)
            response_data = {
                'song_info': song_info,
                'album_info': album_info,
                'artist_info': artist_info
            }
            return Response(response_data)
        else:
            return Response("No track name provided", status=400)


# Integrate Lyrics


MUSIXMATCH_API_KEY = 'YOUR_MUSIXMATCH_API_KEY'
MUSIXMATCH_BASE_URL = 'https://api.musixmatch.com/ws/1.1/'

GENIUS_ACCESS_TOKEN = 'YOUR_GENIUS_ACCESS_TOKEN'
GENIUS_BASE_URL = 'https://api.genius.com/'


class LyricsView(APIView):
    def get_lyrics_from_musixmatch(self, track_name, artist_name):
        endpoint = 'matcher.lyrics.get'
        params = {'apikey': MUSIXMATCH_API_KEY, 'q_track': track_name, 'q_artist': artist_name}
        response = requests.get(f"{MUSIXMATCH_BASE_URL}{endpoint}", params=params)

        if response.status_code == 200:
            data = response.json()
            if data['message']['header']['status_code'] == 200 and 'lyrics_body' in data['message']['body']['lyrics']:
                return data['message']['body']['lyrics']['lyrics_body']
        return None

    def get_lyrics_from_genius(self, track_name, artist_name):
        headers = {'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'}
        params = {'q': f"{track_name} {artist_name}"}
        response = requests.get(f"{GENIUS_BASE_URL}search", headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if 'hits' in data['response'] and data['response']['hits']:
                song_id = data['response']['hits'][0]['result']['id']
                lyrics_path = f"songs/{song_id}/lyrics"
                lyrics_response = requests.get(f"{GENIUS_BASE_URL}{lyrics_path}", headers=headers)

                if lyrics_response.status_code == 200 and 'lyrics' in lyrics_response.json()['response']:
                    return lyrics_response.json()['response']['lyrics']['plain']
        return None

    def get(self, request):
        track_name = request.query_params.get('track_name')  # Assuming 'track_name' is passed in query params
        artist_name = request.query_params.get('artist_name')  # Assuming 'artist_name' is passed in query params

        if not track_name or not artist_name:
            return Response("Track name and artist name are required.", status=400)

        musixmatch_lyrics = self.get_lyrics_from_musixmatch(track_name, artist_name)
        if musixmatch_lyrics:
            return Response(musixmatch_lyrics)
        else:
            genius_lyrics = self.get_lyrics_from_genius(track_name, artist_name)
            return Response(genius_lyrics if genius_lyrics else "Lyrics not found.")


# Integrate Lastfm


API_KEY = 'YOUR_API_KEY'
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'


class LastFmIntegration(APIView):
    def make_lastfm_request(self, method, params):
        params['api_key'] = API_KEY
        params['format'] = 'json'
        response = requests.get(BASE_URL, params=params)
        return response.json() if response.status_code == 200 else None

    def get_recommendations_for_user(self, username):
        method = 'user.getRecommendedTracks'
        params = {'method': method, 'user': username}
        return self.make_lastfm_request(method, params)

    def get_user_top_tracks(self, username):
        method = 'user.getTopTracks'
        params = {'method': method, 'user': username}
        return self.make_lastfm_request(method, params)

    def get_track_info(self, track_name, artist_name):
        method = 'track.getInfo'
        params = {'method': method, 'track': track_name, 'artist': artist_name}
        return self.make_lastfm_request(method, params)

    def get(self, request):
        # Implement your logic here to handle the Last.fm requests
        # Example usage:
        username = request.query_params.get('username')  # Get the username from query parameters

        if not username:
            return Response("Username is required.", status=400)

        # Example: Get recommendations for the user
        recommendations = self.get_recommendations_for_user(username)

        # Example: Get top tracks for the user
        top_tracks = self.get_user_top_tracks(username)

        # Example: Get track information
        track_name = request.query_params.get('track_name')
        artist_name = request.query_params.get('artist_name')
        track_info = self.get_track_info(track_name, artist_name) if track_name and artist_name else None

        response_data = {
            'recommendations': recommendations,
            'top_tracks': top_tracks,
            'track_info': track_info,
        }
        return Response(response_data)


# Trends


class TrendsIntegration(APIView):
    @staticmethod
    def get_billboard_chart(chart_type, api_key):
        billboard_base_url = f'https://api.billboard.com/charts/{chart_type}'
        params = {'key': api_key, 'format': 'json'}
        response = requests.get(billboard_base_url, params=params)

        if response.status_code == 200:
            chart_data = response.json()
            return chart_data['charts'][0]['entries'] if 'charts' in chart_data else None
        else:
            return None

    def find_stations_playing_track(self, track_name, radio_api_key):
        radio_stations_api_url = 'https://api.30000radiostations.com/search'
        params = {'api_key': radio_api_key, 'q': track_name, 'limit': 10}
        response = requests.get(radio_stations_api_url, params=params)

        if response.status_code == 200:
            stations_data = response.json()
            return stations_data['stations'] if 'stations' in stations_data else None
        else:
            return None

    def get(self, request):
        # Example usage: Get Billboard chart data
        chart_type = request.query_params.get('chart_type')  # Get the chart type from query parameters
        api_key = 'YOUR_API_KEY'  # Replace with your Billboard API key
        billboard_chart = self.get_billboard_chart(chart_type, api_key) if chart_type else None

        # Example usage: Find radio stations playing a track
        track_name = request.query_params.get('track_name')  # Get the track name from query parameters
        radio_api_key = 'YOUR_RADIO_API_KEY'  # Replace with your radio stations API key
        stations_playing_track = self.find_stations_playing_track(track_name, radio_api_key) if track_name else None

        response_data = {
            'billboard_chart': billboard_chart,
            'stations_playing_track': stations_playing_track,
        }
        return Response(response_data)


# Search Utility
class SearchView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'search_results.html'

    def get(self, request):
        query = request.GET.get('q')

        if not query:
            return Response({"error": "Missing 'q' parameter in query string"}, status=status.HTTP_400_BAD_REQUEST)

        # Search in the database for matching records based on the query
        songs = Song.objects.filter(Q(title__icontains=query) | Q(artist__name__icontains=query))
        albums = Album.objects.filter(title__icontains=query)
        artists = Artist.objects.filter(name__icontains=query)
        genres = Genre.objects.filter(name__icontains=query)
        playlists = Playlist.objects.filter(title__icontains=query)

        # Serialize the search results
        serialized_local_results = {
            'songs': SongSerializer(songs, many=True).data,
            'albums': AlbumSerializer(albums, many=True).data,
            'artists': ArtistSerializer(artists, many=True).data,
            'genres': GenreSerializer(genres, many=True).data,
            'playlists': PlaylistSerializer(playlists, many=True).data,
        }

        # Spotify search
        if query:
            song_info, album_info, artist_info = get_spotify_song_info(query)
            spotify_results = {
                'song_info': song_info,
                'album_info': album_info,
                'artist_info': artist_info,
            }
        else:
            spotify_results = {}

        # Combine serialized data for the template
        serialized_data = {
            'local_results': serialized_local_results,
            'spotify_results': spotify_results,
        }

        return Response(serialized_data)


# Add song to Library
class AddSongToLibraryView(APIView):
    def post(self, request):
        track_name = request.data.get('track_name')
        user_profile = request.user.music_user_profile  # Assuming user is authenticated and has a profile

        if track_name and user_profile:
            song_title, artist_name = get_spotify_song_info(track_name)

            if song_title and artist_name:
                song, _ = Song.objects.get_or_create(title=song_title)  # Create or retrieve the song

                user_library = UserLibrary.objects.get_or_create(user_profile=user_profile)[0]
                user_library.saved_songs.add(song)

                video_url = get_youtube_video(song_title, artist_name)
                if video_url:
                    song.youtube_url = video_url
                    song.save()
                    return Response(f"Song '{song_title}' added to library with YouTube link: {video_url}")

        return Response("Failed to add song to library or find YouTube video", status=status.HTTP_400_BAD_REQUEST)


# Radio
def fetch_radio_server_data(server_urls):
    server_data = []

    for url in server_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Assuming received data is JSON; adjust this based on the actual response format
                server_data.append({'url': url, 'data': response.json()})
            else:
                server_data.append(
                    {'url': url, 'data': f"Failed to fetch data from {url}. Status code: {response.status_code}"})
        except requests.RequestException as e:
            server_data.append({'url': url, 'data': f"Failed to fetch data from {url}. Error: {str(e)}"})

    return server_data


def display_radio_stations(request):
    if request.method == 'POST':
        track_name = request.POST.get('track_name', '')  # Get track name from POST data

        rb = RadioBrowser()  # Create an instance of the RadioBrowser class
        stations = rb.search(name=track_name, name_exact=True)  # Search for radio stations by track name

        # List of radio server URLs (replace with your own list)
        server_urls = ['all.api.radio-browser.info']

        # Fetch data from the list of radio servers
        server_data = fetch_radio_server_data(server_urls)

        context = {
            'track_name': track_name,
            'stations': stations,
            'server_data': server_data
        }
        return render(request, 'radio_stations.html', context)

    return render(request, 'search_track.html')  # Render a template with a form for input


# Index

def index(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get user profile
        user = request.user  # This should be an instance of User model
        user_profile = profile_user(user)

        # Get all songs, albums, artists, and genres
        songs = Song.objects.all()
        albums = Album.objects.all()
        artists = Artist.objects.all()
        genres = Genre.objects.all()

        # Get song recommendations
        recommended_songs = recommend_songs(user_profile)

        # Render the music home view with all data
        return render(request, 'index.html', {
            'user_profile': user_profile,
            'recommended_songs': recommended_songs,
            'songs': songs,
            'albums': albums,
            'artists': artists,
            'genres': genres,
        })
    else:
        # Handle the case when the user is not authenticated
        return render(request, 'index.html', {'user_profile': None, 'recommended_songs': None, 'songs': None, 'albums': None, 'artists': None, 'genres': None})


def music_home(request):
    songs = Song.objects.all()
    albums = Album.objects.all()
    artists = Artist.objects.all()
    genres = Genre.objects.all()
    # ... fetch other data as needed ...

    return render(request, 'index.html', {
        'songs': songs,
        'albums': albums,
        'artists': artists,
        'genres': genres,
        # ... include other data in the context ...
    })

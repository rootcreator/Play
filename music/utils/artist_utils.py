from django.contrib.sites import requests

from music.models import Artist

@classmethod
def fetch_data_from_spotify(cls, artist_name):
        # Fetch data from Spotify API
        # Replace 'YOUR_SPOTIFY_API_KEY' with your actual Spotify API key
        spotify_api_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist"
        headers = {"Authorization": "Bearer YOUR_SPOTIFY_API_KEY"}
        response = requests.get(spotify_api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Extract cover image and bio from Spotify response
            cover_image_url = data['artists']['items'][0]['images'][0]['url'] if data['artists']['items'] else None
            bio = data['artists']['items'][0]['bio'] if data['artists']['items'] else None
            return cover_image_url, bio
        else:
            return None, None

@classmethod
def fetch_data_from_wikipedia(cls, artist_name):
        # Fetch data from Wikipedia API
        wikipedia_api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{artist_name}"
        response = requests.get(wikipedia_api_url)
        if response.status_code == 200:
            data = response.json()
            # Extract bio from Wikipedia response
            bio = data['extract'] if 'extract' in data else None
            return bio
        else:
            return None

@classmethod
def create_or_update_artist(cls, artist_name):
        # Check if artist already exists
        artist, created = cls.objects.get_or_create(name=artist_name)
        # Fetch data from Spotify
        cover_image_url, bio = cls.fetch_data_from_spotify(artist_name)
        if cover_image_url:
            # Download cover image and save it to Django model
            response = requests.get(cover_image_url)
            if response.status_code == 200:
                artist.cover_image.save(f'{artist_name}_cover_image.jpg', ContentFile(response.content), save=True)
        # Fetch data from Wikipedia
        if not bio:
            bio = cls.fetch_data_from_wikipedia(artist_name)
        if bio:
            artist.bio = bio
        artist.save()


# Example usage:
# Replace 'artist_name' with the name of the artist you want to fetch data for
Artist.create_or_update_artist('artist_name')

from django.core.management.base import BaseCommand
from music.models import APIMusic
import requests

class Command(BaseCommand):
    help = 'Fetch songs and albums from the specified API'

    def handle(self, *args, **kwargs):
        try:
            apimusic_instance = APIMusic.objects.first()  # Assuming there's only one APIMusic instance
            if not apimusic_instance:
                self.stdout.write(self.style.WARNING("No APIMusic instance found."))
                return

            # Fetch songs
            self.stdout.write("Fetching songs...")
            songs_data = self.fetch_data(f"{apimusic_instance.api_url}/songs", headers=self.get_headers(apimusic_instance))
            if songs_data:
                self.stdout.write(self.style.SUCCESS("Songs fetched successfully."))

            # Fetch albums
            self.stdout.write("Fetching albums...")
            albums_data = self.fetch_data(f"{apimusic_instance.api_url}/albums", headers=self.get_headers(apimusic_instance))
            if albums_data:
                self.stdout.write(self.style.SUCCESS("Albums fetched successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))

    def fetch_data(self, url, headers=None):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Failed to fetch data from API: {e}"))
            return None

    def get_headers(self, apimusic_instance):
        return {'Authorization': f'Bearer {apimusic_instance.access_token}'}

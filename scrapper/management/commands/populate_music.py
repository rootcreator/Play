from django.core.management.base import BaseCommand
from music.models import Song
from scrapper.models import Site
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Command(BaseCommand):
    help = 'Populates music database from specified sites'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting music data population...'))

        # Define the scraping logic
        def download_audio(url, file_path):
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)

        def scrape_music_from_site(site):
            base_url = site.url
            response = requests.get(base_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                songs = soup.find_all('div', class_='song')

                for song in songs:
                    title = song.find('h3').text.strip()
                    artist = song.find('p', class_='artist').text.strip()
                    album = song.find('p', class_='album').text.strip()
                    genre = song.find('p', class_='genre').text.strip()  # Assuming genre is available on the website
                    audio_url = urljoin(base_url, song.find('a')['href'])  # Assuming audio file URLs are provided in links

                    # Save the audio file locally
                    audio_file_path = f'audio/{title}.mp3'
                    download_audio(audio_url, audio_file_path)

                    # Assume all songs scraped are royalty-free
                    copyright_status = "Royalty-free"

                    # Save the song to the database
                    Song.objects.create(title=title, artist=artist, album=album, genre=genre, url=audio_url,
                                         audio_file=audio_file_path, copyright_status=copyright_status)
            else:
                self.stdout.write(self.style.WARNING(f"Failed to fetch music data from {site.name}"))

        # Fetch all sites from the database
        sites = Site.objects.all()

        # Scrape music data from each site
        for site in sites:
            scrape_music_from_site(site)

        self.stdout.write(self.style.SUCCESS('Music data population completed successfully.'))

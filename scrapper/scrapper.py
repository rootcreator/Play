import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.core.files.base import ContentFile

from scrapper.models import Site, Music


def download_audio(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
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
            audio_file_name = f'audio/{title}.mp3'
            download_audio(audio_url, audio_file_name)

            # Assume all songs scraped are royalty-free
            copyright_status = "Royalty-free"

            # Save the song to the database
            music_instance = Music.objects.create(
                title=title,
                artist=artist,
                album=album,
                genre=genre,
                url=audio_url,
                copyright_status=copyright_status
            )

            # Save the audio file to the FileField
            with open(audio_file_name, 'rb') as audio_file:
                music_instance.audio_file.save(os.path.basename(audio_file_name), ContentFile(audio_file.read()))

    else:
        print(f"Failed to fetch music data from {base_url}")


def scrape_music():
    sites = Site.objects.all()

    for site in sites:
        scrape_music_from_site(site)


# Call the function to scrape music data
scrape_music()

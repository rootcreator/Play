import random
from django.core.management.base import BaseCommand
from music.models import Artist


class Command(BaseCommand):
    help = 'Fetches new artists and populates the database'

    def handle(self, *args, **kwargs):
        # Your code to fetch new artists goes here
        # For example, fetch artists from Spotify or Wikipedia
        new_artists = self.fetch_new_artists()

        # Ensure at least 100 artists are fetched
        while len(new_artists) < 100:
            new_artists.extend(self.fetch_new_artists())

        # Populate the database with fetched artists
        for artist_name in new_artists:
            Artist.create_or_update_artist(artist_name)
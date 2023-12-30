from .models import Song, Album, Artist


class MusicBulkImport:
    @staticmethod
    def import_songs(song_data_list):
        for song_data in song_data_list:
            title = song_data.get('title')
            artist = song_data.get('artist')
            # Assuming other necessary fields like duration, genre, etc., are provided

            # Create or get the artist (You may have logic for this in your actual implementation)
            artist_instance, _ = Artist.objects.get_or_create(name=artist)

            # Create the song
            song_instance = Song.objects.create(
                title=title,
                artist=artist_instance,
                # Add other required fields here
            )

            # Assuming additional logic for other relationships, if any

            # Save the song
            song_instance.save()

    @staticmethod
    def import_albums(album_data_list):
        for album_data in album_data_list:
            title = album_data.get('title')
            artist = album_data.get('artist')
            # Assuming other necessary fields like release date, genre, etc., are provided

            # Create or get the artist (You may have logic for this in your actual implementation)
            artist_instance, _ = Artist.objects.get_or_create(name=artist)

            # Create the album
            album_instance = Album.objects.create(
                title=title,
                artist=artist_instance,
                # Add other required fields here
            )

            # Assuming additional logic for other relationships, if any

            # Save the album
            album_instance.save()

import requests
from bs4 import BeautifulSoup


def fetch_saavn_data(search_query):
    base_url = 'https://www.saavn.com/s/'

    # Construct the search URL
    search_url = f'{base_url}{search_query}'

    try:
        # Send a GET request to the Saavn search URL
        response = requests.get(search_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract relevant information from the parsed HTML
            # Example: Extracting song names
            song_names = [song.text.strip() for song in soup.select('.search-page .song-name')]

            # Example: Extracting artist names
            artist_names = [artist.text.strip() for artist in
                            soup.select('.search-page .song-details .song-partial-meta .primary-text')]

            # Example: Extracting album names
            album_names = [album.text.strip() for album in
                           soup.select('.search-page .song-details .song-partial-meta .secondary-text')]

            # Return the extracted data
            return {'songs': song_names, 'artists': artist_names, 'albums': album_names}

        else:
            print(f'Failed to fetch data from Saavn. Status code: {response.status_code}')

    except requests.RequestException as e:
        print(f'Request error: {e}')

    # Return None if there was an error
    return None


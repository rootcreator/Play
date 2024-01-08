import requests

def find_stations_playing_track(track_name, radio_api_key):
    RADIO_STATIONS_API_URL = 'https://api.radios-browser.com/search'

    params = {
        'name': track_name,
        'limit': 10,  # Adjust limit as needed
        'key': radio_api_key
    }

    response = requests.get(RADIO_STATIONS_API_URL, params=params)
    if response.status_code == 200:
        stations_data = response.json()
        return stations_data['hits'] if 'hits' in stations_data else None
    else:
        return None

# Usage example (for testing):
if __name__ == "__main__":
    track_name = "Despacito"  # Replace with the desired track name
    radio_api_key = 'YOUR_RADIO_API_KEY'  # Replace with your Radio Browser API key

    stations_playing_track = find_stations_playing_track(track_name, radio_api_key)
    if stations_playing_track:
        # Process stations' data or display station information
        for station in stations_playing_track:
            print(station['name'], station['url'])  # Display station names and streaming URLs
    else:
        print("Failed to retrieve stations.")

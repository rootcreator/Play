# TRENDS
# Billboard
# 30000 station
import requests


def get_billboard_chart(chart_type, api_key):
    BILLBOARD_BASE_URL = f'https://api.billboard.com/charts/{chart_type}'
    params = {'key': api_key, 'format': 'json'}
    response = requests.get(BILLBOARD_BASE_URL, params=params)

    if response.status_code == 200:
        chart_data = response.json()
        return chart_data['charts'][0]['entries'] if 'charts' in chart_data else None
    else:
        return None


def find_stations_playing_track(track_name, radio_api_key):
    RADIO_STATIONS_API_URL = 'https://api.30000radiostations.com/search'
    params = {'api_key': radio_api_key, 'q': track_name, 'limit': 10}
    response = requests.get(RADIO_STATIONS_API_URL, params=params)

    if response.status_code == 200:
        stations_data = response.json()
        return stations_data['stations'] if 'stations' in stations_data else None
    else:
        return None
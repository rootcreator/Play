# LastFm Integration
import requests

API_KEY = 'YOUR_API_KEY'
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'


def make_lastfm_request(method, params):
    params['api_key'] = API_KEY
    params['format'] = 'json'
    response = requests.get(BASE_URL, params=params)
    return response.json() if response.status_code == 200 else None


def get_recommendations_for_user(username):
    method = 'user.getRecommendedTracks'
    params = {'method': method, 'user': username}
    return make_lastfm_request(method, params)


def get_user_top_tracks(username):
    method = 'user.getTopTracks'
    params = {'method': method, 'user': username}
    return make_lastfm_request(method, params)


def get_track_info(track_name, artist_name):
    method = 'track.getInfo'
    params = {'method': method, 'track': track_name, 'artist': artist_name}
    return make_lastfm_request(method, params)
from jam.models import ListeningHistory, Trends
from users.models import Profile
import requests

API_KEY_LASTFM = 'YOUR_LASTFM_API_KEY'
API_KEY_BILLBOARD = 'YOUR_BILLBOARD_API_KEY'


def make_lastfm_request(method, params):
    params['api_key'] = API_KEY_LASTFM
    params['format'] = 'json'
    response = requests.get('http://ws.audioscrobbler.com/2.0/', params=params)
    return response.json() if response.status_code == 200 else None


def get_lastfm_data(method, username):
    params = {'method': method, 'user': username}
    return make_lastfm_request(method, params)


def get_billboard_chart(location_code, chart_type):
    BILLBOARD_BASE_URL = f'https://api.billboard.com/charts/{chart_type}/{location_code}'
    params = {'key': API_KEY_BILLBOARD, 'format': 'json'}
    response = requests.get(BILLBOARD_BASE_URL, params=params)
    if response.status_code == 200:
        return response.json().get('charts', [])[0].get('entries', [])
    return None


def find_song_based_on_diverse_genre(played_genres):
    # Implement your logic to find a song based on diverse genre
    # For simplicity, let's just return a placeholder value
    return "Diverse Genre Song"


def integrate_billboard_data(user_profile):
    location_code = user_profile.location_code  # Assuming user profile contains location info
    billboard_chart_data = get_billboard_chart(location_code=location_code, chart_type='hot-100')
    if billboard_chart_data:
        top_songs = [entry['title'] for entry in billboard_chart_data]
        for song_title in top_songs:
            ListeningHistory.objects.create(user_profile=user_profile, song=song_title)
        Trends.update_trends_with_songs(top_songs)
        return 'Billboard data integration completed'
    return 'No Billboard data available'


def trendrecommend_songs(user_profile):
    trendrecommended_songs = []

    # Add recommendation rules based on user_profile attributes
    if user_profile.total_songs_played > 100 and user_profile.diversity_of_genres > 5:
        # Recommend a song based on diverse listening habits
        recommended_song = find_song_based_on_diverse_genre(user_profile.played_genres)
        trendrecommended_songs.append(recommended_song)

    # Fetch Last.fm recommendations and top tracks
    lastfm_data = get_lastfm_data('user.getRecommendedTracks', user_profile.user.username)
    if lastfm_data:
        trendrecommended_songs.extend(lastfm_data)
    lastfm_top_tracks = get_lastfm_data('user.getTopTracks', user_profile.user.username)
    if lastfm_top_tracks:
        trendrecommended_songs.extend(lastfm_top_tracks)

    return trendrecommended_songs


def get_trendrecommendations(user):
    try:
        user_profile = Profile.objects.get(user=user)
        integration_status = integrate_billboard_data(user_profile)
        recommendations = trendrecommend_songs(user_profile)
        return recommendations, integration_status
    except Profile.DoesNotExist:
        return [], 'User profile not found'
    except Exception as e:
        return [], f'Error getting recommendations: {e}'


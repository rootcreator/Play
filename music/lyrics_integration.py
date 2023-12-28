import requests

# Musixmatch API credentials
MUSIXMATCH_API_KEY = 'YOUR_MUSIXMATCH_API_KEY'
MUSIXMATCH_BASE_URL = 'https://api.musixmatch.com/ws/1.1/'

# Genius API credentials
GENIUS_ACCESS_TOKEN = 'YOUR_GENIUS_ACCESS_TOKEN'
GENIUS_BASE_URL = 'https://api.genius.com/'


def get_lyrics_from_musixmatch(track_name, artist_name):
    endpoint = 'matcher.lyrics.get'
    params = {'apikey': MUSIXMATCH_API_KEY, 'q_track': track_name, 'q_artist': artist_name}
    response = requests.get(f"{MUSIXMATCH_BASE_URL}{endpoint}", params=params)

    if response.status_code == 200:
        data = response.json()
        if data['message']['header']['status_code'] == 200 and 'lyrics_body' in data['message']['body']['lyrics']:
            return data['message']['body']['lyrics']['lyrics_body']
    return None


def get_lyrics_from_genius(track_name, artist_name):
    headers = {'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'}
    params = {'q': f"{track_name} {artist_name}"}
    response = requests.get(f"{GENIUS_BASE_URL}search", headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'hits' in data['response'] and data['response']['hits']:
            song_id = data['response']['hits'][0]['result']['id']
            lyrics_path = f"songs/{song_id}/lyrics"
            lyrics_response = requests.get(f"{GENIUS_BASE_URL}{lyrics_path}", headers=headers)

            if lyrics_response.status_code == 200 and 'lyrics' in lyrics_response.json()['response']:
                return lyrics_response.json()['response']['lyrics']['plain']
    return None


def get_lyrics(track_name, artist_name):
    musixmatch_lyrics = get_lyrics_from_musixmatch(track_name, artist_name)
    if musixmatch_lyrics:
        return musixmatch_lyrics
    else:
        genius_lyrics = get_lyrics_from_genius(track_name, artist_name)
        return genius_lyrics if genius_lyrics else "Lyrics not found."

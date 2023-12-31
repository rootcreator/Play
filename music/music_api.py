import requests

BASE_URL = 'http://localhost:8000/api/'  # Replace with your Django app's base URL

def fetch_genres():
    endpoint = 'genres/'
    url = BASE_URL + endpoint
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch genres. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def fetch_artists():
    endpoint = 'artists/'
    url = BASE_URL + endpoint
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch artists. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def fetch_composers():
    endpoint = 'composers/'
    url = BASE_URL + endpoint
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch composers. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def fetch_albums():
    endpoint = 'albums/'
    url = BASE_URL + endpoint
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch albums. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def fetch_songs():
    endpoint = 'songs/'
    url = BASE_URL + endpoint
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch songs. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

# Test the functions
if __name__ == "__main__":
    print("Genres:", fetch_genres())
    print("Artists:", fetch_artists())
    print("Composers:", fetch_composers())
    print("Albums:", fetch_albums())
    print("Songs:", fetch_songs())

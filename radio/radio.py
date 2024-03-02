# intergration.py
import requests

def fetch_radio_stations():
    url = "https://example.com/api/radio/stations"
    headers = {
        "Authorization": "Bearer YOUR_API_TOKEN"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error in API request: {e}")
        return None

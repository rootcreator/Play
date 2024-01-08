import requests


def get_billboard_chart(location_code, chart_type, api_key):
    BILLBOARD_BASE_URL = f'https://api.billboard.com/charts/{chart_type}/{location_code}'
    params = {'key': api_key, 'format': 'json'}
    response = requests.get(BILLBOARD_BASE_URL, params=params)

    if response.status_code == 200:
        chart_data = response.json()
        return chart_data['charts'][0]['entries'] if 'charts' in chart_data else None
    else:
        return None


# Usage example:
if __name__ == "__main__":
    user_location = 'US'  # Replace with the user's location code
    chart_type = 'hot-100'  # Specify the desired chart type
    api_key = 'YOUR_BILLBOARD_API_KEY'  # Replace with your Billboard API key

    trending_songs = get_billboard_chart(user_location, chart_type, api_key)
    if trending_songs:
        print("Trending 100 Songs in", user_location)
        for index, song in enumerate(trending_songs[:100], start=1):
            print(f"{index}. {song['title']} - {song['artist']}")
    else:
        print("Failed to retrieve chart data.")

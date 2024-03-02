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


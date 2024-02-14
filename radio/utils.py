import requests
from django.shortcuts import render

from .models import RadioStation  # Adjust the import path according to your project's structure



def search_radio_stations(request):
    if 'name' in request.GET:
        name = request.GET['name']
        url = "https://bando-radio-api.p.rapidapi.com/stations/byname/%7Bkeyword%7D"
        querystring = {"offset": "0", "limit": "10"}
        headers = {
            "X-RapidAPI-Key": "1ecad14232mshea32a62c1e4dc2ap181062jsn38bf6995676a",
            "X-RapidAPI-Host": "bando-radio-api.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            stations = response.json()
            return render(request, 'stations.html', {'stations': stations})
        else:
            error_message = f"Failed to fetch data. Status code: {response.status_code}"
            return render(request, 'stations.html', {'error_message': error_message})
    else:
        return render(request, 'stations.html')


def populate_radio_stations():
    url = "https://bando-radio-api.p.rapidapi.com/stations"

    querystring = {"offset": "0", "limit": "10"}

    headers = {
        "X-RapidAPI-Key": "1ecad14232mshea32a62c1e4dc2ap181062jsn38bf6995676a",
        "X-RapidAPI-Host": "bando-radio-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        for station_data in data:
            name = station_data.get('name')
            if name:
                # Trim station name if it exceeds 100 characters
                trimmed_name = name[:100]
                RadioStation.objects.create(name=trimmed_name)
                print(f"Added station: {trimmed_name}")
            else:
                print(f"Invalid station data: {station_data}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")



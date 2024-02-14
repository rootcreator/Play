from django.shortcuts import render

from .models import RadioStation
from .utils import populate_radio_stations, search_radio_stations


def search_radio_stations_view(request):
    if 'name' in request.GET:
        name = request.GET['name']
        # Query the database for radio stations matching the search query
        stations = RadioStation.objects.filter(name__icontains=name)
        return render(request, 'stations.html', {'stations': stations})
    else:
        # Fetch all radio stations if no search query is provided
        stations = RadioStation.objects.all()
        return render(request, 'stations.html', {'stations': stations})



def populate_radio_stations_view(request):
    populate_radio_stations()
    return render(request, 'stations.html')




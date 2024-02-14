# urls.py

from django.urls import path
from . import views
from .views import search_radio_stations_view

urlpatterns = [
    path('radio/', views.populate_radio_stations_view, name='populate_radio'),
    path('radio/', views.search_radio_stations_view, name='search_radio'),
    path('radio/', views.search_radio_stations, name='search_radio_stations'),
    path('radio/', search_radio_stations_view, name='search_radio_stations_view'),


    # Add other URL patterns as needed
]

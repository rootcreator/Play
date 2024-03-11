from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from play import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('music/', include('music.urls')),
    path('jam/', include('jam.urls')),

    path('users/', include('users.urls')),
    #path('', RedirectView.as_view(url='/music/')),
    path('radio/', include('radio.urls')),




]

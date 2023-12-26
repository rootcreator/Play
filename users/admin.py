from django.contrib import admin
from .models import UserProfile, UserLibrary

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserLibrary)

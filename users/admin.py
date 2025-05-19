from django.contrib import admin
from .models import CustomUser, BuyerProfile, DriverProfile, ArtisanProfile

admin.site.register(CustomUser)
admin.site.register(BuyerProfile)
admin.site.register(DriverProfile)
admin.site.register(ArtisanProfile)

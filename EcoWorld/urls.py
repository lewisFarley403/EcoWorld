from django.contrib import admin
from django.urls import path, include
from .views import addDrink, testAddDrink, upload_bottle_photo, scan_qr_code  # Import the view

app_name = 'EcoWorld'
urlpatterns = [
    path('addDrink/', addDrink, name='home'),  # Root URL
    path("drink/", testAddDrink, name='addDrinkTest'),  # URL for the signup page
    path('ecoworld/', include('EcoWorld.urls', namespace='EcoWorld')),
    path('scan/', scan_qr_code, name='scan_qr'),
    path('upload_photo/', upload_bottle_photo, name="upload_photo"),

]
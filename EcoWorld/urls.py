"""
This module defines the endpoints for the EcoWorld app:
    - `addDrink` : This view allows the user to add a drink event
    - `testAddDrink` : This view allows the user to test adding a drink event
Author:
    -Lewis Farley (lf507@exeter.ac.uk)
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

from .views import addDrink, merge_opening_page, buy_pack, mergecards,store,pack_opening_page, upload_bottle_photo, scan_qr_code, generate_qr_code, friends # Import the view
from . import views

app_name = 'EcoWorld'
urlpatterns = [
    path("", views.dashboard, name='dashboard'),  # URL for the dashboard page
    path('addDrink/', addDrink, name='home'),  # Root URL
    path('scan/', scan_qr_code, name='scan_qr'),
    path('upload_photo/', upload_bottle_photo, name="upload_photo"),
    path('generate_qr/', generate_qr_code, name="generate_qr"),
    path("store/", store, name='store'),  # URL for the signup page
    path('buyPack/', buy_pack, name='buyPack'),  # URL for the signup page
    path("packopening/", pack_opening_page, name='packopening'),
    path("dashboard/", views.dashboard, name='dashboard'),  # URL for the dashboard page
    path("challenge/", views.challenge, name='challenge'),  # URL for the challenge page
    path("completeChallenge/", views.completeChallenge, name='completeChallenge'),  # URL for the complete challenge page
    path("friends/", friends, name="friends"), #URL for friend dashboard
    path("mergecards/", mergecards, name="mergecards"), #URL for merging cards page
    path("mergereveal/", merge_opening_page, name="mergereveal")

]
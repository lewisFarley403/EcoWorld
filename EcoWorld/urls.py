"""
This module defines the endpoints for the EcoWorld app:
    - `addDrink` : This view allows the user to add a drink event
    - `testAddDrink` : This view allows the user to test adding a drink event
Author:
    -Lewis Farley (lf507@exeter.ac.uk)
"""

from django.contrib import admin
from django.urls import path,include
from .views import addDrink,testAddDrink # Import the view
from . import views

urlpatterns = [
    path('addDrink/', addDrink, name='home'),  # Root URL
    path("drink/", testAddDrink, name='addDrinkTest'),  # URL for the signup page
    path("dashboard/", views.dashboard, name='dashboard'),  # URL for the dashboard page
]
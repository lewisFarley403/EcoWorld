from django.contrib import admin
from django.urls import path,include
from .views import addDrink,testAddDrink # Import the view

urlpatterns = [
    path('addDrink/', addDrink, name='home'),  # Root URL
    path("drink/", testAddDrink, name='addDrinkTest'),  # URL for the signup page
]
from django.contrib import admin
from django.urls import path,include
from .views import addDrink,testAddDrink, store # Import the view

urlpatterns = [
    path('addDrink/', addDrink, name='home'),  # Root URL
    path("drink/", testAddDrink, name='addDrinkTest'),  # URL for the signup page
    path("store/", store, name='store'),  # URL for the signup page
    path('buyPack/', store, name='buyPack'),  # URL for the signup page
]
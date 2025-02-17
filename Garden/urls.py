from django.contrib import admin
from django.urls import path,include
from .views import show_garden,remove_card,getAvailableCards,addCard # Import the view

urlpatterns = [
    path('', show_garden, name='home'),  # Root URL
    path('removeCard/', remove_card, name='removeCard'),  # URL for removing a card
    path('getAvailableCards/', getAvailableCards, name='getAvailableCards'),  # URL for getting available cards
    path('addCard/', addCard, name='addCard'),  # URL for adding a card
]
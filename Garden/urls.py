"""
URL configuration for Garden app.

This module defines the URL patterns for the virtual garden functionality,
including garden display and card management operations.

URL Patterns:
    - /: Main garden display page
    - /addCard/: Endpoint for adding cards to the garden
    - /removeCard/: Endpoint for removing cards from the garden
"""

from django.urls import path

from .views import show_garden, removeCard, addCard

urlpatterns = [
    path('', show_garden, name='home'), 
    path("addCard/", addCard, name="add_card"),
    path("removeCard/", removeCard, name="remove_card")
]
"""
URL configuration for leaderboards app.

This module defines the URL patterns for the leaderboards functionality,
including the main leaderboard view, data retrieval endpoints, and tooltip templates.

URL Patterns:
    - /: Main leaderboard page
    - /getleaderboarddata/: API endpoint for ranked user data
    - /get-tooltip-template/: Endpoint for garden tooltip templates

Author:
    Lewis Farley (lf507@exeter.ac.uk)
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('getleaderboarddata/', views.get_ranked_users, name='get_ranked_users'),
    path('get-tooltip-template/', views.get_tooltip_template, name='get_tooltip_template'),
]

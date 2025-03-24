"""
URL configuration for Sustainability Game app.

This module defines the URL patterns for the sustainability mini-game functionality,
including game interface and score management.

URL Patterns:
    - /play/: Game interface and gameplay
    - /save_score/: Score saving endpoint
"""

from django.urls import path
from . import views

urlpatterns = [
    path('play/', views.play_game, name='play_game'),
    path('save_score/', views.save_score, name='save_score'),
]
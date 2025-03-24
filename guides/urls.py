"""
URL configuration for Guides app.

This module defines the URL patterns for the sustainability guides functionality,
including guide content, quizzes, and guide management.

URL Patterns:
    - /: Guide menu overview
    - /content/<pair_id>/: Guide content display
    - /quiz/<pair_id>/: Quiz interface
    - /registerScore/<pair_id>/: Score registration endpoint
    - /results/<pair_id>/: Quiz results display
    - /add_guide/: Guide creation interface
    - /remove_guide/: Guide removal interface
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('content/<int:pair_id>/', views.content_view, name='content'),
    path('quiz/<int:pair_id>/', views.quiz_view, name='quiz'),
    path('registerScore/<int:pair_id>/', views.registerScore_view, name='registerScore'),
    path('results/<int:pair_id>/', views.results_view, name='results'),
    path('add_guide/', views.add_guide, name='add guide'),
    path('remove_guide/', views.remove_guide, name='remove guide')
]
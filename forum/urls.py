"""
URL configuration for Forum app.

This module defines the URL patterns for the community forum functionality,
including post management, interactions, and moderation features.

URL Patterns:
    - /: Main forum feed
    - /getchallengeinfo/: Challenge information retrieval endpoint
    - /create_post/: Post creation interface
    - /interact/: Post interaction endpoint
    - /interactions/<post_id>/: Post interaction details
    - /gamekeeper/: Forum moderation dashboard
    - /gamekeeper/delete/<post_id>/: Post deletion endpoint
"""

from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('getchallengeinfo/', views.get_challenge_info, name='get_challenge_info'),
    path('', views.feed, name='feed'),
    path('create_post/', views.create_post, name='create_post'),
    path('interact/', views.interact_with_post, name='interact_with_post'),
    path('interactions/<int:post_id>/', views.get_post_interactions, name='get_post_interactions'),
    path('gamekeeper/', views.forum_gamekeeper, name='forum_gamekeeper'),
    path('gamekeeper/delete/<int:post_id>/', views.delete_post, name='delete_post'),
] 
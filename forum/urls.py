from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('getchallengeinfo/', views.get_challenge_info, name='get_challenge_info'),
    path('', views.feed, name='feed'),
    path('create_post/', views.create_post, name='create_post'),
    path('interact/', views.interact_with_post, name='interact_with_post'),
    path('interactions/<int:post_id>/', views.get_post_interactions, name='get_post_interactions'),
    path('gamekeeper/', views.gamekeeper_page, name='gamekeeper_page'),
    path('gamekeeper/delete/<int:post_id>/', views.delete_post, name='delete_post'),
] 
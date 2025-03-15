from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('getchallengeinfo/', views.get_challenge_info, name='get_challenge_info'),
    path('', views.feed, name='feed'),
] 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_home, name='sustainability_game'),
    path('play/', views.play_game, name='play_game'),
    path('save_score/', views.save_score, name='save_score'),
    path('leaderboard/', views.leaderboard, name='game_leaderboard'),
]
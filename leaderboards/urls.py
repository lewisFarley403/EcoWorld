

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('getleaderboarddata/', views.get_ranked_users, name='get_ranked_users'),
]

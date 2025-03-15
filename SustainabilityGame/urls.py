from django.urls import path
from . import views

urlpatterns = [
    path('play/', views.play_game, name='play_game'),
    path('save_score/', views.save_score, name='save_score'),
]
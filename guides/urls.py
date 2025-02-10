from django.urls import path
from . import views

urlpatterns = [
    path('', views.content_view, name='content'),
    path('quiz/', views.quiz_view, name='quiz'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('content/<int:pair_id>/', views.content_view, name='content'),
    path('quiz/<int:pair_id>/', views.quiz_view, name='quiz'),
    path('registerScore/<int:pair_id>/', views.registerScore_view, name='registerScore'),
    path('results/<int:pair_id>/', views.results_view, name='results'),
]
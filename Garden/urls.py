from django.contrib import admin
from django.urls import path,include
from .views import show_garden # Import the view

urlpatterns = [
    path('', show_garden, name='home'),  # Root URL
]
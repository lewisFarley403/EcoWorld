
from django.contrib import admin
from django.urls import path
from .views import chest
urlpatterns = [
    path("",chest ),
]

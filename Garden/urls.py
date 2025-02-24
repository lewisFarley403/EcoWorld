from django.contrib import admin
from django.urls import path,include
from .views import show_garden,removeCard,addCard

urlpatterns = [
    path('', show_garden, name='home'), 
    path("addCard/", addCard, name="add_card"),
    path("removeCard/", removeCard, name="remove_card")
]
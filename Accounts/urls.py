"""
This module defines the endpoints for the Accounts app:
    - `signup` : This view allows the user to sign up for an account
    - `login` : This view allows the user to log in to their account
    - `logout` : This view allows the user to log out of their account
    - `profile` : This view allows the user to view and update their profile
author:
    - Ethan Sweeney (es1057@exeter.ac.uk)
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile, name='profile'),
]

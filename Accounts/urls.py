"""
This module defines the endpoints for the Accounts app:
    - `signup` : This view allows the user to sign up for an account
    - `login` : This view allows the user to log in to their account
    - `logout` : This view allows the user to log out of their account
    - `profile` : This view allows the user to view and update their profile
author:
    - Ethan Sweeney (es1052@exeter.ac.uk)
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('api/userinfo/', views.user_info, name='user_info'),

    
]

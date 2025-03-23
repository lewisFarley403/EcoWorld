"""
This module defines the endpoints for the EcoWorld app:
    - `addDrink` : This view allows the user to add a drink event
    - `testAddDrink` : This view allows the user to test adding a drink event
Author:
    -Lewis Farley (lf507@exeter.ac.uk)
    -Chris Lynch (cl1037@exeter.ac.uk)
"""

from django.urls import path

from .views import merge_opening_page, buy_pack, mergecards,store,pack_opening_page, friends # Import the view

from . import views

app_name = 'EcoWorld'
urlpatterns = [
    path("", views.dashboard, name='dashboard'),  # URL for the dashboard page
    path("store/", store, name='store'),  # URL for the signup page
    path('buyPack/', buy_pack, name='buyPack'),  # URL for the signup page
    path("packopening/", pack_opening_page, name='packopening'),
    path("dashboard/", views.dashboard, name='dashboard'),  # URL for the dashboard page
    path("challenge/", views.challenge, name='challenge'),  # URL for the challenge page
    path("completeChallenge/", views.completeChallenge, name='completeChallenge'),  # URL for the complete challenge page
    path("gamekeeper/", views.gamekeeper_page, name="gamekeeper_page"),
    path("grant_gamekeeper/<int:user_id>/", views.grant_gamekeeper, name="grant_gamekeeper"),
    path("add-challenge/", views.add_challenge, name="add_challenge"),  # URL for adding challenges
    path("friends/", friends, name="friends"), #URL for friend dashboard
    path("mergecards/", mergecards, name="mergecards"), #URL for merging cards page
    path("mergereveal/", merge_opening_page, name="mergereveal"),
    path('complete_challenge/', views.completeChallenge, name='complete_challenge'), #Url for completing a challenge
    path("increment_objective/", views.increment_daily_objective, name="increment_objective"), #Url for incrementing the progress tracker
    path("save_objective_note/", views.save_objective_note, name="save_objective_note"), #Url for the that pops up after an objective
    # path("admin/objective_submissions/", views.view_objective_submissions, name="view_objective_submissions")

]
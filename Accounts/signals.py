"""
This module provides the signals for the user to create or update their profile:
    - `create_or_update_profile` : This function creates or updates the user profile when the user is created or updated
    - `post_save` : This signal is sent when a model's `save()` method is called.
    - `receiver` : This decorator is used to connect a signal to a receiver function.
usage:
    - create_or_update_profile: This function creates or updates the user profile when the user is created or updated. 
    It should be imported in models.py.
author:
    - Ethan Sweeney (es1052@exeter.ac.uk)
"""
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from leaderboards.models import UserEarntCoins
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """

    This function creates or updates the user profile when the user is created or updated.
    It is connected to the `post_save` signal of the `User` model.
    If the user is created, it creates a new profile for the user.
    If the user is updated, it updates the existing profile for the user.
    Attributes:
        sender : User : The User model provided by Django
        instance : User : The instance of the User model
        created : bool : A boolean value indicating if the user is created
        **kwargs : dict : Additional keyword arguments
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

@receiver(pre_save, sender=Profile)
def track_coin_addition(sender, instance, **kwargs):
    
    """Detects when number_of_coins increases and creates a new instance of 
    UserEarntCoins for the benefit of the leaderboard.
    Author: Lewis Farley (lf507@exeter.ac.uk)
    """
    if instance.pk:  # Check if it's an update (not a new object)
        previous = Profile.objects.get(pk=instance.pk)
        if instance.number_of_coins > previous.number_of_coins:
            added_amount = instance.number_of_coins - previous.number_of_coins
            coin_added(instance, added_amount)
def coin_added(instance, added_amount):
    e = UserEarntCoins.objects.create(user=instance.user, score=added_amount)
    e.save()
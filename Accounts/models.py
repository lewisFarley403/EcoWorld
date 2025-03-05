"""
Module to create the Profile model for the Accounts app.
This module includes:
    - Profile: Model for storing user profile information (bio, first name, last name, profile picture).

Usage:
    - Import the Profile model in views.py to access user profile information.
    
It creates database tables for storing user profile information.

@author Ethan Sweeney (es1052@exeter.ac.uk)
"""


# models.py
from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    """
    Model for storing user profile information.
    Attributes:
        -user: OneToOneField : The user associated with the profile.
        -bio: TextField : The bio of the user.
        -first_name: TextField : The first name of the user.
        -last_name: TextField : The last name of the user.
        -profile_picture: CharField : The profile picture of the user.
    Methods:
        __str__(): Returns the username of the user.
    author:
        -Ethan Sweeney (es1052@exeter.ac.uk)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    defaultpfp = "/pfp1.png"
    profile_picture = models.CharField(max_length=255, default=defaultpfp)  # Store the image file name
    number_of_coins = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username


class Friends(models.Model):
    userID1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="FriendOne")
    userID2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="FriendTwo")

    class Meta:
        unique_together = ("userID1", "userID2")
    
    def __str__(self):
        return f"{self.userID1.username} is friends with {self.userID2.username}"


class FriendRequests(models.Model):
    senderID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    receiverID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")

    class Meta:
        unique_together = ("senderID", "receiverID") 

    def __str__(self):
        return f"{self.senderID.username} sent a request to {self.receiverID.username}"
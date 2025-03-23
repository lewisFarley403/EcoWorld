"""
Module to create the Profile model for the Accounts app.
This module includes:
    - Profile: Model for storing user profile information
    (bio, first name, last name, profile picture).

Usage:
    - Import the Profile model in views.py to access user profile information.
    
It creates database tables for storing user profile information.

@author Ethan Sweeney (es1052@exeter.ac.uk)
"""


from django.contrib.auth.models import User
from django.db import models

# models.py
#pylint: disable=too-few-public-methods
# pylint: disable=no-member

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
    first_name = models.TextField()
    last_name = models.TextField()
    defaultpfp = "/pfp1.png"
    profile_picture = models.CharField(max_length=255, default=defaultpfp)
    number_of_coins = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

    class Meta:
        """
        Metaclass for the Profile model.

        This class provides metadata for the Profile model, including permissions.

        Attributes:
            permissions (list): A list of tuples specifying custom permissions for the model.
        """
        permissions = [
            ("can_view_gamekeeper_button", "Can grant gamekeeper rights"),
        ]


class Friends(models.Model):
    """
    Model for storing friends
    Attributes:
        userID1 = The user ID of one of the people in the relationship of friends
        userID2 = The user ID of the other person who is friends with User ID1
    Methods:
        __str__  : Returns that User x is friends with User Y
    Author:
        Chris Lynch (cl1037@exeter.ac.uk)
    """
    userID1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="FriendOne")
    userID2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="FriendTwo")

    class Meta:
        """
        Metaclass for the Friends model.

        This class provides metadata for the Friends model, including unique constraints.

        Attributes:
            unique_together (tuple): A tuple specifying fields that must be unique together.
        """
        unique_together = ("userID1","userID2")
    def __str__(self):
        return f"{self.userID1.username} is friends with {self.userID2.username}"


class FriendRequests(models.Model):
    """
    Model for storing friend requests
    Attributes:
        senderID = The person who sent the friend request with their ID
        receiverID = The person who is receiving the friend request for use in the requests box
    Methods:
        __str__  : Returns that User x sent a request to User Y
    Author:
        Chris Lynch (cl1037@exeter.ac.uk)
    """
    senderID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    receiverID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")

    class Meta:
        """
        Metaclass for the FriendRequests model.

        This class provides metadata for the FriendRequests model, including unique constraints.

        Attributes:
            unique_together (tuple): A tuple specifying fields that must be unique together.
        """
        unique_together = ("senderID","receiverID")
    def __str__(self):
        return f"{self.senderID.username} sent a request to {self.receiverID.username}"

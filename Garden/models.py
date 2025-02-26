'''
"""
This module defines the database models for the garden app:
    - `garden` : Model for storing garden information,
        including size and user ID of the owner
    - `gardenSquare` : model used for storing the card currently placed in a garden square
usage:
    - to modify or access the database, import the models from this module
author:
    - Lewis Farley (lf507@exeter.ac.uk)
"""
'''

from django.db import models
from Accounts.models import User
from EcoWorld.models import card
from django.conf import settings
# Create your models here.
class garden(models.Model):
    """
    Model for storing garden information.
    Attributes:
        -size: IntegerField : The size of the garden.
        -userID: ForeignKey : The user who owns the garden.
    Methods:
        -__str__(): Returns the user ID of the owner.
    Author:
        - Lewis Farley (lf507@exeter.ac.uk)
    """
    size = models.IntegerField(default=settings.GARDEN_SIZE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Garden for " + str(self.userID)
class gardenSquare(models.Model):
    """
    Model for storing information about each square in the garden
    Attributes:
        -gardenID: ForeignKey : The garden to which the square belongs.
        -squareID: IntegerField : The ID of the square.
        -cardID: ForeignKey : The card currently placed in the square.
        - Meta: Ensures that the gardenID and squareID are unique together
    Methods:
        -__str__(): Returns the garden ID.
    Author:
        - Lewis Farley (lf507@exeter.ac.uk)
    """
    gardenID = models.ForeignKey(garden, on_delete=models.CASCADE)
    squareID = models.IntegerField()
    cardID = models.ForeignKey(card, on_delete=models.CASCADE, null=True)

    class Meta:
        """
        Adds meta data to the gardenSquare
        in this case ensures for each gardenID, the squareID is unique
        Attributes:
            -unique_together: Tuple : Ensures that the gardenID and
             squareID are unique together
        Methods:
            -__str__(): Returns the garden ID.
        Author:
            - Lewis Farley (lf507@exeter.ac.uk)
        
        """
        unique_together = ('gardenID', 'squareID')  # Enforces composite uniqueness
    def __str__(self):
        return str(self.gardenID)
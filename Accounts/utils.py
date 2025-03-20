"""
This file contains utility functions for the Accounts app.
Functions:
    - createGarden(user): Creates a garden for the user.
author:
    - Lewis Farley (lf507@exeter.ac.uk)

"""

from django.conf import settings

from EcoWorld.models import card, ownsCard
from Garden.models import garden, gardenSquare


def createGarden(user):
    """
    This function creates a garden for the user.
    It creates a garden object and garden squares for the user.
    Attributes:
        user : User : The user for whom the garden is created.
    Returns:
        g : Garden : The garden created for the user.
    author:
        - Lewis Farley (lf507@exeter.ac.uk)
    """
    # Create a garden for the user
    g = garden(userID=user)
    g.save()
    for i in range(settings.GARDEN_SIZE**2):
        gS = gardenSquare(gardenID=g, squareID=i)
        gS.save()

    return g


def createOwnsDb(user):
    for cards in card.objects.all():
        oCard = ownsCard(card_id=cards.id, user_id=user.id)
        oCard.save()

    


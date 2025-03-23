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

#pylint: disable=too-few-public-methods
# pylint: disable=no-member

def create_garden(user):
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
        g_s = gardenSquare(gardenID=g, squareID=i)
        g_s.save()

    return g


def create_owns_db(user):
    """
    Creates ownership records for all cards for a given user.

    This function iterates over all card objects and creates an ownsCard
    record for each card, associating it with the provided user.

    Args:
        user (User): The user for whom the ownership records are created.
    """
    for cards in card.objects.all():
        o_card = ownsCard(card_id=cards.id, user_id=user.id)
        o_card.save()

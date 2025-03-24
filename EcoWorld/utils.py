"""
Utility functions for EcoWorld challenge management.

This module provides utility functions for managing game challenges,
including challenge creation, assignment, and expiry handling. Features:
    - Challenge generation and assignment
    - Automatic challenge expiry management
    - Challenge rotation and replacement
    - User challenge state management
"""

import random

from django.conf import settings
from django.utils import timezone

from .models import ongoingChallenge, challenge


def getUsersChallenges(user):
    """
    Retrieve and manage current challenges for a user.

    This function handles the complete lifecycle of user challenges:
    - Creates new challenges if none exist
    - Manages challenge expiry and replacement
    - Ensures challenge uniqueness per user
    - Maintains the required number of active challenges

    Args:
        user (User): The user whose challenges are being managed

    Returns:
        QuerySet: Active ongoingChallenge instances for the user

    Note:
        Challenge expiry is controlled by settings.CHALLENGE_EXPIRY
        Number of challenges is controlled by settings.NUM_CHALLENGES
    Author:
        Lewis Farley (lf507@exeter.ac.uk), Theodore Armes (tesa201@exeter.ac.uk)
    """
    challenges = list(ongoingChallenge.objects.filter(user=user))
    if len(challenges) == 0:
        ## there are no challenges for the user, create them
        createChallenges(user)
    else:
        expired = [
            x for x in challenges
            if timezone.now() - x.created_on > settings.CHALLENGE_EXPIRY
        ]
        possibleChallenges = list(challenge.objects.all())

        for e in expired:
            e.delete()
            challenges.remove(e)
        for i in range(len(expired)):
            # create new challenges to replace the removed ones
            c = random.choice(possibleChallenges)
            # make sure the challenge isn't already in the users challenges
            while c in [ch.challenge
                        for ch in challenges]:  
                c = random.choice(possibleChallenges)
            ongoingChallenge.objects.create(challenge=c,
                                            user=user,
                                            submission=None,
                                            submitted_on=None)
            possibleChallenges.remove(c)
    return ongoingChallenge.objects.filter(user=user)


def createChallenges(user):
    """
    Create a new set of challenges for a user.

    Generates the initial set of random challenges for a user,
    ensuring the correct number of challenges are assigned based
    on the NUM_CHALLENGES setting.

    Args:
        user (User): The user to create challenges for

    Returns:
        None

    Raises:
        IndexError: If there aren't enough challenges in the database
            to meet the NUM_CHALLENGES requirement

    Note:
        The number of challenges created is controlled by settings.NUM_CHALLENGES
  
    Author:
        Lewis Farley (lf507@exeter.ac.uk), Theodore Armes (tesa201@exeter.ac.uk)
    """
    challenges = list(challenge.objects.all())
    try:
        for _ in range(settings.NUM_CHALLENGES):
            c = random.choice(challenges)
            challenges.remove(c)
            ongoingChallenge.objects.create(challenge=c,
                                            user=user,
                                            submission=None,
                                            submitted_on=None)
    except IndexError:
        print("not enough challenges")
        print("it is possible that the database hasn't been populated with enough challenges")

import random

from django.conf import settings
from django.utils import timezone

from .models import ongoingChallenge, challenge


def getUsersChallenges(user):
    """
    Retrieves all current challenges for a user, creating new ones if needed.

    - If no challenges exist for the user, generates a new set via `createChallenges()`.
    - Removes and replaces expired challenges based on `settings.CHALLENGE_EXPIRY`.
    - Ensures no duplicate challenge assignments for the user.

    Args:
        user (User): The user for whom challenges are being retrieved or created.

    Returns:
        QuerySet: A list of `ongoingChallenge` instances assigned to the user.

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
        possible_challenges = list(challenge.objects.all())

        for e in expired:
            e.delete()
            challenges.remove(e)
        for _ in range(len(expired)):
            # create new challenges to replace the removed ones
            c = random.choice(possible_challenges)
            # make sure the challenge isn't already in the users challenges
            while c in [ch.challenge for ch in
                        challenges]:
                c = random.choice(possible_challenges)
            ongoingChallenge.objects.create(challenge=c,
                                            user=user,
                                            submission=None,
                                            submitted_on=None)
            possible_challenges.remove(c)
    return ongoingChallenge.objects.filter(user=user)




def createChallenges(user):
    """
    Generates and assigns a set number of challenges to a user.

    - Randomly selects challenges from the database.
    - Ensures the number of assigned challenges matches `settings.NUM_CHALLENGES`.
    - Handles cases where there are insufficient challenges available in the database.

    Args:
        user (User): The user for whom challenges are being created.

    Returns:
        None

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

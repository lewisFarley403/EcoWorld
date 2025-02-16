from .models import ongoingChallenge,challenge
import random
from django.conf import settings
from datetime import datetime
from django.utils import timezone

def getUsersChallenges(user):
    """
    This function returns all challenges for a user.
    Attributes:
        user : User : The user for whom the challenges are retrieved.
    Returns:
        challenges : QuerySet : The challenges for the user.
    Author:
        - Lewis Farley (lf507@exeter.ac.uk)
    """
    
    challenges= list(ongoingChallenge.objects.filter(user=user))
    if len(challenges) ==0:
        ## there are no challenges for the user, create them
        print("creating challenges")
        createChallenges(user)
    else:
        # expired = filter(lambda x: datetime.now()-x.created_on> settings.CHALLENGE_EXPIRY, challenges)
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
            while c in [ch.challenge for ch in challenges]: # make sure the challenge isn't already in the users challenges
                c = random.choice(possibleChallenges)
            ongoingChallenge.objects.create(challenge=c,user=user,submission=None,submitted_on=None)
            possibleChallenges.remove(c)
    return ongoingChallenge.objects.filter(user=user)
        
    
def createChallenges(user):
    """
    This function creates all challenges for a user.
    Attributes:
        user : User : The user for whom the challenges are created.
    Returns:
        challenges : [ongoingChallenge] : The challenges created for the user.
    Author:
        - Lewis Farley (lf507@exeter.ac.uk)
    """
    challenges = list(challenge.objects.all())
    try:
        for _ in range(settings.NUM_CHALLENGES):

            c = random.choice(challenges)
            challenges.remove(c)
            ongoingChallenge.objects.create(challenge=c,user=user,submission=None,submitted_on=None)
    except IndexError:
        print("not enough challenges")
        print("it is possible that the database hasn't been populated with enough challenges")

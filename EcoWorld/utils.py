from .models import ongoingChallenge, challenge, card, cardRarity, pack

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

    challenges = list(ongoingChallenge.objects.filter(user=user))
    if len(challenges) == 0:
        ## there are no challenges for the user, create them
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
            while c in [ch.challenge for ch in
                        challenges]:  # make sure the challenge isn't already in the users challenges
                c = random.choice(possibleChallenges)
            ongoingChallenge.objects.create(challenge=c, user=user, submission=None, submitted_on=None)
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
            ongoingChallenge.objects.create(challenge=c, user=user, submission=None, submitted_on=None)
    except IndexError:
        print("not enough challenges")
        print("it is possible that the database hasn't been populated with enough challenges")


def createItemsInDb():
    common = cardRarity.objects.get_or_create(title="common")[0]
    rare = cardRarity.objects.get_or_create(title="rare")[0]
    epic = cardRarity.objects.get_or_create(title="epic")[0]
    legendary = cardRarity.objects.get_or_create(title="legendary")[0]
    mythic = cardRarity.objects.get_or_create(title="mythic")[0]

    cards_data = [
        {"title": "Ancient Tree", "desc": "Mythical Card forged from legendary cards", "rarity": mythic,
         "img": "cards/ancienttree.png"},
        {"title": "Bush", "desc": "A humble common bush", "rarity": common, "img": "cards/bush.png"},
        {"title": "Cactus", "desc": "A spiky cactus straight from the desert", "rarity": rare,
         "img": "cards/cactus.png"},
        {"title": "Cherry Blossom", "desc": "A blooming cherry blossom tree from the Sakura forest",
         "rarity": legendary, "img": "cards/cherryBlossom.png"},
        {"title": "Dandelion Patch", "desc": "A patch of common dandelions", "rarity": common,
         "img": "cards/dandelion.png"},
        {"title": "Golden Tree", "desc": "The legendary Golden tree", "rarity": legendary,
         "img": "cards/goldenTree.png"},
        {"title": "Maple Tree", "desc": "Found around Canada", "rarity": legendary, "img": "cards/mapleTree.png"},
        {"title": "Oak Tree", "desc": "A simple but gracious oak tree", "rarity": epic, "img": "cards/oakTree.png"},
        {"title": "Orange Tree", "desc": "Filled with plenty of ripe fruit", "rarity": epic,
         "img": "cards/orangeTree.png"},
        {"title": "Rainbow Flower", "desc": "Something you wish was actually real", "rarity": rare,
         "img": "cards/rainbowflower.png"},
        {"title": "Scarecrow", "desc": "Just a casual field scarecrow", "rarity": epic, "img": "cards/scarecrow.png"},
        {"title": "Starry Tree", "desc": "Straight from the milky way", "rarity": epic, "img": "cards/starryTree.png"},
        {"title": "Statue", "desc": "A head bust of an important historical recycler", "rarity": epic,
         "img": "cards/statue.png"},
        {"title": "Sunflower", "desc": "Shines bright in the fields", "rarity": rare, "img": "cards/sunflower.png"},
        {"title": "Tulip Patch", "desc": "A simple patch of tulips", "rarity": rare, "img": "cards/tulip.png"},
        {"title": "Log", "desc": "From a long lost oak tree", "rarity": common, "img": "cards/log.png"},
        {"title": "Olive Tree", "desc": "From the fields of ancient greece", "rarity": epic,
         "img": "cards/olivetree.png"}
    ]

    for data in cards_data:
        card.objects.get_or_create(
            title=data["title"],
            defaults={
                "description": data["desc"],
                "rarity": data["rarity"],
                "image": data["img"]
            }
        )


def createPacksInDb():
    pack_data = [
        {
            "title": "Basic Pack",
            "cost": 20,
            "packimage": "packs/basicpack.png",
            "probabilities": {
                "common": 0.5,
                "rare": 0.35,
                "epic": 0.1,
                "legendary": 0.05
            }
        },
        {
            "title": "Rare Pack",
            "cost": 45,
            "packimage": "packs/rarepack.png",
            "probabilities": {
                "common": 0.35,
                "rare": 0.35,
                "epic": 0.175,
                "legendary": 0.125
            }
        },
        {
            "title": "Icon Pack",
            "cost": 100,
            "packimage": "packs/iconpack.png",
            "probabilities": {
                "common": 0.1,
                "rare": 0.4,
                "epic": 0.25,
                "legendary": 0.25
            }
        }
    ]

    for data in pack_data:
        pack.objects.update_or_create(
            title=data["title"],
            defaults={
                "cost": data["cost"],
                "packimage": data["packimage"]
            }
        )



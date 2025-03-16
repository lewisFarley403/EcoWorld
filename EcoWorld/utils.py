
from django.db.models import Case, When, Value, BooleanField
import random
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import now

from EcoWorld.models import ongoingChallenge, dailyObjective, challenge, cardRarity, card, pack

from django.conf import settings

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
    today = timezone.now().date()

    # Get the user's ongoing challenges
    challenges = ongoingChallenge.objects.filter(user=user).annotate(
        is_completed=Case(
            When(submitted_on__isnull=False, submitted_on__date=today, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    ).order_by("created_on")[:2]  # Limit to 2 active challenges

    return challenges

# Set how often daily objectives should reset (change this value as needed)


def getUsersDailyObjectives(user):
    """
    Retrieves the user's daily objectives and resets them after a defined interval.
    """
    # Get the last reset time
    last_reset_time = dailyObjective.objects.filter(user=user).order_by("-last_reset").first()
    expiration_time = now() - settings.DAILY_OBJECTIVE_RESET_INTERVAL

    # If the last reset is outdated, refresh objectives
    if not last_reset_time or last_reset_time.last_reset < expiration_time:
        # Delete old objectives
        dailyObjective.objects.filter(user=user).delete()

        # Assign new objectives
        new_objectives = [
            dailyObjective(user=user, name="Recycle 10 Items", goal=10, last_reset=now()),
            dailyObjective(user=user, name="Turn Off Lights", goal=5, last_reset=now()),
            dailyObjective(user=user, name="Use Refill Station", goal=1, last_reset=now()),
        ]
        dailyObjective.objects.bulk_create(new_objectives)

    return dailyObjective.objects.filter(user=user)
        
from django.conf import settings
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
    expiration_time = now() - settings.CHALLENGE_RESET_INTERVAL

    # Delete old challenges if they have expired
    ongoingChallenge.objects.filter(user=user, created_on__lt=expiration_time).delete()

    # Assign fresh challenges if none exist
    if not ongoingChallenge.objects.filter(user=user).exists():
        challenges = list(challenge.objects.all())
        try:
            for _ in range(settings.NUM_CHALLENGES):
                if challenges:
                    c = random.choice(challenges)
                    challenges.remove(c)
                    ongoingChallenge.objects.create(
                        challenge=c, user=user, submission=None, submitted_on=None, created_on=now()
                    )
        except IndexError:
            print("Not enough challenges available.")


def createItemsInDb():
    common = cardRarity.objects.get_or_create(title="common")[0]
    rare = cardRarity.objects.get_or_create(title="rare")[0]
    epic = cardRarity.objects.get_or_create(title="epic")[0]
    legendary = cardRarity.objects.get_or_create(title="legendary")[0]
    mythic = cardRarity.objects.get_or_create(title="mythic")[0]

    print(f"Created Rarities: {common}, {rare}, {epic}, {legendary}, {mythic}")

    cards_data = [
        {"title": "Ancient Tree", "desc": "Mythical Card forged from legendary cards", "rarity": mythic, "img": "cards/ancienttree.png"},
        {"title": "Bush", "desc": "A humble common bush", "rarity": common, "img": "cards/bush.png"},
        {"title": "Cactus", "desc": "A spiky cactus straight from the desert", "rarity": rare, "img": "cards/cactus.png"},
        {"title": "Cherry Blossom", "desc": "A blooming cherry blossom tree from the Sakura forest", "rarity": legendary, "img": "cards/cherryBlossom.png"},
        {"title": "Dandelion Patch", "desc": "A patch of common dandelions", "rarity": common, "img": "cards/dandelion.png"},
        {"title": "Golden Tree", "desc": "The legendary Golden tree", "rarity": legendary, "img": "cards/goldenTree.png"},
        {"title": "Maple Tree", "desc": "Found around Canada", "rarity": legendary, "img": "cards/mapleTree.png"},
        {"title": "Oak Tree", "desc": "A simple but gracious oak tree", "rarity": epic, "img": "cards/oakTree.png"},
        {"title": "Orange Tree", "desc": "Filled with plenty of ripe fruit", "rarity": epic, "img": "cards/orangeTree.png"},
        {"title": "Rainbow Flower", "desc": "Something you wish was actually real", "rarity": rare, "img": "cards/rainbowflower.png"},
        {"title": "Scarecrow", "desc": "Just a casual field scarecrow", "rarity": epic, "img": "cards/scarecrow.png"},
        {"title": "Starry Tree", "desc": "Straight from the milky way", "rarity": epic, "img": "cards/starryTree.png"},
        {"title": "Statue", "desc": "A head bust of an important historical recycler", "rarity": epic, "img": "cards/statue.png"},
        {"title": "Sunflower", "desc": "Shines bright in the fields", "rarity": rare, "img": "cards/sunflower.png"},
        {"title": "Tulip Patch", "desc": "A simple patch of tulips", "rarity": rare, "img": "cards/tulip.png"},
        {"title": "Log", "desc": "From a long lost oak tree", "rarity": common,"img" : "cards/log.png"},
        {"title": "Olive Tree", "desc": "From the fields of ancient greece", "rarity": epic, "img": "cards/olivetree.png"}
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




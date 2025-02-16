from Garden.models import garden,gardenSquare
from django.conf import settings
from EcoWorld.models import card, ownsCard

def createGarden(user):
    # Create a garden for the user
    print(user)
    g = garden(userID=user)
    g.save()
    for i in range(settings.GARDEN_SIZE**2):
        gS = gardenSquare(gardenID=g, squareID=i)
        gS.save()

    return g

def createOwnsDb(user):
    print(type(user))
    for cards in card.objects.all():
        oCard = ownsCard(card_id=cards.id, user_id=user.id)
        oCard.save()

    
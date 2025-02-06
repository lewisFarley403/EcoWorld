from Garden.models import garden,gardenSquare
from django.conf import settings
def createGarden(user):
    # Create a garden for the user
    print(user)
    g = garden(userID=user)
    g.save()
    for i in range(settings.GARDEN_SIZE**2):
        gS = gardenSquare(gardenID=g, squareID=i)
        gS.save()

    return g
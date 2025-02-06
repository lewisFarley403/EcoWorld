from django.db import models
from Accounts.models import User
from EcoWorld.models import card
from django.conf import settings
# Create your models here.
class garden(models.Model):
    size = models.IntegerField(default=settings.GARDEN_SIZE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Garden for " + str(self.userID)
class gardenSquare(models.Model):
    gardenID = models.ForeignKey(garden, on_delete=models.CASCADE)
    squareID = models.IntegerField()
    cardID = models.ForeignKey(card, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('gardenID', 'squareID')  # Enforces composite uniqueness
    def __str__(self):
        return str(self.gardenID)
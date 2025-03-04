from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserEarntCoins(models.Model):
    """
    Model to store the user's earned coins
    Used to populate the leaderboard
    Author: Lewis Farley (lf507@exeter.ac.uk)
    """
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
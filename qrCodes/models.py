from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class waterFountain(models.Model):
    """
    Model for storing water fountain information.
    Attributes:
        -name: CharField : The name of the water fountain.
        -location: CharField : The location of the water fountain.
    Methods:
        __str__(): Returns the name of the water fountain.
    author:
        -Lewis Farley (lf507@exeter.ac.uk)
    """
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class drinkEvent(models.Model):
    """
    Model for storing drink event information.
    Attributes:
        -user: ForeignKey : The user who drank from the fountain.
        -fountain: ForeignKey : The fountain the user drank
        -drank_on: DateField : The date the user drank.
    Methods:
        __str__(): Returns the name of the user and the fountain they drank from.
    Author:
        -Lewis Farley (lf507@exeter.ac.uk)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fountain = models.ForeignKey(waterFountain, on_delete=models.CASCADE)
    drank_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " drank from " + self.fountain.name + " on " + str(self.drank_on)

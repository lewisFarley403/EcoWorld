"""
This module defines the database models for the EcoWorld app:
    - `challenge` : Model for storing challenge information
    - `ongoingChallenge` : Model for storing ongoing challenge information
    - `waterFountain` : Model for storing water fountain information
    - `drinkEvent` : Model for storing drink event information
    - `cardRarity` : Model for storing card rarity information
    - `card` : Model for storing card information
    - `ownsCard` : Model for storing card ownership information
usage:
    - to modify or access the database, import the models from this module
author:
    - Lewis Farley (lf507@exeter.ac.uk)
"""

from django.db import models

from Accounts.models import User
# Create your models here.
class challenge(models.Model):
    """
    Model for storing challenge information.
    Attributes:
        -name: CharField : The name of the challenge.
        -description: TextField : The description of the challenge.
        -created_by: ForeignKey : The user who created the challenge.
        -created_on: DateField : The date the challenge was created.
    Methods:
        __str__(): Returns the name of the challenge.
    author:
        -Lewis Farley (lf507@exeter.ac.uk)
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField()
    worth = models.IntegerField(default=10)
    def __str__(self):
        return self.name
class ongoingChallenge(models.Model):
    """
    Model for storing challenges currently assigned to a user.
    Attributes:
        -challenge: ForeignKey : The challenge being attempted.
        -user: ForeignKey : The user attempting the challenge.
        -submission: TextField : The submission for the challenge.
        -submitted_on: DateField : The date the submission was made.
    Methods:
        __str__(): Returns the name of the challenge and the user attempting it.
    author:
        -Lewis Farley (lf507@exeter.ac.uk)
    """
    challenge = models.ForeignKey(challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.TextField(null=True)
    submitted_on = models.DateField(null=True)
    created_on = models.DateTimeField( auto_now_add=True) #sets this to the current date when the object is created
    def __str__(self):
        return self.challenge.name + " by " + self.user.username
    

    
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
    drank_on = models.DateField()
    def __str__(self):
        return self.user.username + " drank from " + self.fountain.name
    


class cardRarity(models.Model):
    """
    Model for storing all possible card rarities.
    Attributes:
        -title: CharField : The title of the rarity.
    Methods:
        __str__(): Returns the title of the rarity.
    Author:
        -Lewis Farley (lf507@exeter.ac.uk)
    """
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title
class card(models.Model):
    """
    Model for storing card information.
    Attributes:
        -title: CharField : The title of the card.
        -description: TextField : The description of the card.
        -rarity: ForeignKey : The rarity of the card.
        -image: ImageField : The image of the card.
    Methods:
        __str__(): Returns the title of the card.
    Author:
        -Lewis Farley (lf507@exeter.ac.uk)
    """
    title = models.CharField(max_length=50)
    description = models.TextField()
    rarity = models.ForeignKey(cardRarity, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cards/')
    def __str__(self):
        return self.title
class ownsCard(models.Model):
    """
    Model for storing what cards the user owns and how many.
    Attributes:
        -user: ForeignKey : The user who owns the card.
        -card: ForeignKey : The card being owned.
        -quantity: IntegerField : The quantity of the card owned.
    Methods:
        __str__(): Returns the name of the user and the card they own.
    Author:
        -Lewis Farley (lf507@exeter.ac.uk)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(card, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username + " owns " + self.card.title
    
class pack(models.Model):
    title = models.CharField(max_length=50)
    cost = models.IntegerField()
    packimage = models.ImageField(upload_to='packs/')
    def __str__(self):
        return self.title

    
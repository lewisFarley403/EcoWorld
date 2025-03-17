from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import now
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
import random
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateField()
    worth = models.IntegerField(default=settings.CHALLENGE_WORTH)
    redirect_url = models.CharField(max_length=255, blank=True, null=True)

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
    submitted_on = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField( auto_now_add=True) #sets this to the current date when the object is created
    completion_count = models.IntegerField(default=0)

    def __str__(self):
        return self.challenge.name + " by " + self.user.username

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
        -Chris Lynch (cl1037@exeter.ac.uk)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(card, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username + " owns " + self.card.title
    
class pack(models.Model):
    """
    Model for storing Packs so they can be bought in store

    Attributes: 
        -title: CharField: Used as the name of the pack
        -Cost: IntegerField: Uses as the coin cost for buying a pack
        -packimage: ImageField: Used for the imaging for the pack in the store
        -commonProb: FloatField : Used as a propability for pack rarity
        -rareProb: FloatField : Used as a propability for pack rarity
        -epicProb: FloatField : Used as a propability for pack rarity
        -legendaryProb: FloatField : Used as a propability for pack rarity
        -colour_class: Charfield : Used when pack opening for the colouring of the background

    Methods:
    __str__(): Returns the title of the pack
    openPack() : Used to open a pack in the store

    Author:
    Chris Lynch (cl1037@exeter.ac.uk)
    Lewis Farley (lf507@exeter.ac.uk)
    
    """
    title = models.CharField(max_length=50)
    cost = models.IntegerField()
    packimage = models.ImageField(upload_to='packs/')
    commonProb = models.FloatField(default=0.5)
    rareProb = models.FloatField(default=0.35)
    epicProb = models.FloatField(default=0.1)
    legendaryProb = models.FloatField(default=0.05)
    color_class = models.CharField(max_length=50, default="blue")

    def __str__(self):
        return self.title
    def openPack(self):
        #Open the pack and return
        r=random.random()
        if r<self.commonProb:
            rarity = cardRarity.objects.get(title="common")
        elif r<self.commonProb+self.rareProb:
            rarity = cardRarity.objects.get(title="rare")
        elif r<self.commonProb+self.rareProb+self.epicProb:
            rarity = cardRarity.objects.get(title="epic")
        else:
            rarity = cardRarity.objects.get(title="legendary")
        cards = card.objects.filter(rarity=rarity)
        cardToReturn = random.choice(cards)
        return cardToReturn



class Merge(models.Model):
    """
    Class to create a merge table in the database for merge actions within the mergecards view
    
    Attributes:
        userID = Foreign key, is used to tie the user to the merge being made
        cardID1 = Foreign key, is used to tie the card for slot 1 to a card
        cardID2 = Foreign key, is used to tie the card for slot 2 to a card
        cardID3 = Foreign key, is used to tie the card for slot 3 to a card
        cardID4 = Foreign key, is used to tie the card for slot 4 to a card
        cardID5 = Foreign key, is used to tie the card for slot 5 to a card
    
    Method:
        __str__: Returns merge operation for the username
    Author:
    Chris Lynch (cl1037@exeter.ac.uk)
    
    """
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserID")
    cardID1 = models.ForeignKey(card, null=True, blank=True, on_delete=models.CASCADE, related_name="CardID1")
    cardID2 = models.ForeignKey(card, null=True, blank=True, on_delete=models.CASCADE, related_name="CardID2")
    cardID3 = models.ForeignKey(card, null=True, blank=True, on_delete=models.CASCADE, related_name="CardID3")
    cardID4 = models.ForeignKey(card, null=True, blank=True, on_delete=models.CASCADE, related_name="CardID4")
    cardID5 = models.ForeignKey(card, null=True, blank=True, on_delete=models.CASCADE, related_name="CardID5")

    def __str__(self):
        return f"Merge operation for {self.userID.username}"


class dailyObjective(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    progress = models.IntegerField(default=0)
    goal = models.IntegerField(default=10)  # Example: Must recycle 10 items
    completed = models.BooleanField(default=False)
    date_created = models.DateField(default=now)
    last_reset = models.DateTimeField(default=now) #Field for tracking resets
    submission = models.TextField(null=True, blank=True)  # Store user's response
    coins = models.IntegerField(default=10)  # New field for coin rewards


    def __str__(self):
        return f"{self.name} - {self.user.username}"



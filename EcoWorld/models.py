from django.db import models
import random
from Accounts.models import User
# Create your models here.
class challenge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField()
    def __str__(self):
        return self.name
class ongoingChallenge(models.Model):
    challenge = models.ForeignKey(challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.TextField()
    submitted_on = models.DateField()
    def __str__(self):
        return self.challenge.name + " by " + self.user.username
    

    
class waterFountain(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class drinkEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fountain = models.ForeignKey(waterFountain, on_delete=models.CASCADE)
    drank_on = models.DateField()
    def __str__(self):
        return self.user.username + " drank from " + self.fountain.name
    


class cardRarity(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title
class card(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    rarity = models.ForeignKey(cardRarity, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cards/')
    def __str__(self):
        return self.title
class ownsCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(card, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username + " owns " + self.card.title
    
class pack(models.Model):
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
    

    
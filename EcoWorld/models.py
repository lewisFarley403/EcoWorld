from django.db import models

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
    def __str__(self):
        return self.user.username + " owns " + self.card.title
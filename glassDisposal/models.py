from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class GlassDisposalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, help_text="What3words location of disposal bin")
    image = models.ImageField(upload_to='glass_disposals/', help_text="photo proof of glass dispolsal")
    bottle_count = models.PositiveIntegerField(default=1, help_text="number of bottles handed in")
    timestamp = models.DateTimeField(default=timezone.now)
    coins_awarded = models.IntegerField(default=0, help_text="coins earned from this disposal")

def save(self, *args, **kwargs):
    """override save to add coins to users profile"""
    if not self.pk: # only award on new submissions
        self.coins_awarded = self.bottle_count * settings.GLASS_DISPOSAL_REWARD_PER_BOTTLE  #calculate reward
        self.user.profile.number_of_coins += self.coins_awarded
        self.user.profile.save()
    super().save(*args, **kwargs)

def __str__(self):
    return f"{self.user.username} - {self.location} ({self.timestamt})"

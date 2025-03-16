from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RecyclingLocation(models.Model):
    name = models.CharField(max_length=255, help_text="Recycling Bin Name")
    latitude = models.FloatField(help_text="Latitude of recycling bin")
    longitude = models.FloatField(help_text="Longitude of recycling bin")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GlassDisposalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycling_location = models.ForeignKey(RecyclingLocation, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='glass_disposals/', help_text="Photo proof of glass disposal")
    bottle_count = models.PositiveIntegerField(help_text="Number of bottles disposed")
    timestamp = models.DateTimeField(default=timezone.now)
    coins_awarded = models.IntegerField(default=0, help_text="Coins earned from disposal")

    def __str__(self):
        return f"{self.user.username} - {self.recycling_location} ({self.timestamp})"


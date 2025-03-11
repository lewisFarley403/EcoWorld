from django.db import models
from django.contrib.auth.models import User


class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    water_level = models.IntegerField(default=100)
    energy_points = models.IntegerField(default=50)
    carbon_footprint = models.IntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s game - {self.date_played}"


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements/')

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)
# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)  # Store the image file name

    def __str__(self):
        return self.user.username

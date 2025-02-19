from django.db import models
from Accounts.models import User

# Create your models here.

class quiz_results(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    best_result = models.IntegerField(default=0)
    previous_best = models.IntegerField(default=0)
    new_result = models.IntegerField(default=0)
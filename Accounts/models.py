from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserType(models.Model):
    user_type = models.CharField(max_length=50)


# class User (models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     date_of_birth = models.DateField()
#     user_type = models.ForeignKey(UserType, on_delete=models.CASCADE,default=0) # 0 is the default user type
#     def __str__(self):
#         return self.username

## change the User model to inherit from AbstractUser, the built-in Django user model
class CustomUser(AbstractUser):  # Inherit from AbstractUser
    date_of_birth = models.DateField(null=True, blank=True)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
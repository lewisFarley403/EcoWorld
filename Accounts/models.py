from django.db import models

# Create your models here.

class UserType(models.Model):
    user_type = models.CharField(max_length=50)
class User (models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE,default=0) # 0 is the default user type
    def __str__(self):
        return self.username
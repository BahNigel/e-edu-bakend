# models.py

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)
    user_type = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

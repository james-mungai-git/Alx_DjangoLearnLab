from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followering = models.ManyToManyField('self', symmetrical=False, blank=True)
    
    def __str__(self):
        return self.username

class Item(models.Model):
    name = models.CharField(max_length=100)

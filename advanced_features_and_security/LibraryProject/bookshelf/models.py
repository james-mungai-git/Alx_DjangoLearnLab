from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from .models import UserManager
from django.db import models
from django.conf import settings  
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ✅ Must use this
        on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class UserModel(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    objects= UserManager()


class CustomUserManage(BaseUserManager):
    def user_model(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("email address must be entered")
        
        email = self.normalise_email
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_super_user(self, username, email,password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser must have is_staff=True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'       # Login via email
    REQUIRED_FIELDS = ['username'] # Required when creating superuser

    def __str__(self):
        return self.email
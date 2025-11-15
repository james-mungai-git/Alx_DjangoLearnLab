from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

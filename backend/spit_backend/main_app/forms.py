from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, RetailerUser, BrandUser

class RetailerRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class BrandRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
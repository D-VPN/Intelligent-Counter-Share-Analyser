from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, RetailerUser, BrandUser

class RetailerRegisterForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_retailer = True
        user.save()
        RetailerUser.objects.create(user=user)
        return user


class BrandRegisterForm(UserCreationForm):
    mobile_no = forms.CharField(required=True)
    email_id = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    brand_logo = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_retailer = True
        user.save()
        BrandUser.objects.create(user=user)
        return user
from django import forms
from multiselectfield import MultiSelectField
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.models import User
from .models import User, RetailerUser, BrandUser

class RetailerRegisterForm(UserCreationForm):
    mobile_no = forms.CharField(required=True)
    email_id = forms.EmailField(required=True)
    address = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        retailer = RetailerUser.objects.create(user=user)
        retailer.mobile_no = self.cleaned_data.get('mobile_no')
        retailer.email_id = self.cleaned_data.get('email_id')
        retailer.address = self.cleaned_data.get('address')
        retailer.no_of_aisles = None
        retailer.premium_positions = None
        retailer.top_price = None
        retailer.bottom_price = None
        retailer.middle_price = None
        retailer.middle_price = None
        # student.interests.add(*self.cleaned_data.get('interests'))
        return user

class BrandRegisterForm(UserCreationForm):
    mobile_no = forms.CharField(required=True)
    email_id = forms.EmailField(required=True)
    address = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        brand = BrandUser.objects.create(user=user)
        brand.mobile_no = self.cleaned_data.get('mobile_no')
        brand.email_id = self.cleaned_data.get('email_id')
        brand.address = self.cleaned_data.get('address')
        # student.interests.add(*self.cleaned_data.get('interests'))
        return user

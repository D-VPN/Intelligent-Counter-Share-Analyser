from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser

POSITIONS_AVAILABLE = (('Top', 'TOP'),
               ('Middle', 'MIDDLE'),
               ('Bottom', 'BOTTOM'),
               ('Corner', 'CORNER'))

class User(AbstractUser):
    is_retailer = models.BooleanField(default=False)
    is_brand = models.BooleanField(default=False)


class BrandUser(models.Model):
    user = models.OneToOneField(User, related_name='brand_parent_user', on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=10,null=False)
    email_id = models.EmailField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)
    brand_logo = models.ImageField(upload_to='profile_pics')


class RetailerUser(models.Model):
    user = models.OneToOneField(User, related_name='retailer_parent_user', on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=10,null=False)
    email_id = models.EmailField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)
    no_of_aisles = models.IntegerField(null=True)
    premium_positions = MultiSelectField(choices=POSITIONS_AVAILABLE)
    top_price = models.IntegerField(null=True)
    bottom_price = models.IntegerField(null=True)
    middle_price = models.IntegerField(null=True)
    corner_price = models.IntegerField(null=True)


class Contracts(models.Model):
    contract_retailer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    contract_brand = models.ForeignKey(BrandUser, null=True, blank=True, on_delete=models.CASCADE)
    desired_positions = MultiSelectField(choices=POSITIONS_AVAILABLE)
    precent_visibility = models.IntegerField()

from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser

POSITIONS_AVAILABLE = ((1, 'TOP'),
               (2, 'MIDDLE'),
               (3, 'BOTTOM'),
               (4, 'CORNER'))

class User(AbstractUser):
    is_retailer = models.BooleanField(default=False)
    is_brand = models.BooleanField(default=False)

class RetailerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=10,null=False, unique=True)
    email_id = models.EmailField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)
    no_of_aisles = models.IntegerField()
    premium_positions = MultiSelectField(choices=POSITIONS_AVAILABLE)
    top_price = models.IntegerField()
    bottom_price = models.IntegerField()
    middle_price = models.IntegerField()
    corner_price = models.IntegerField()

class BrandUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=10,null=False, unique=True)
    email_id = models.EmailField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)
    brand_logo = models.ImageField(upload_to='profile_pics')


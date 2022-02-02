from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class Profile(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=11, null=True, unique=True)
    is_active = models.BooleanField(default=False)
    is_salesman = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.email


class Customer(Profile):
    TYPE = [
        ("WC", "Wandering_customer"),
        ("IC", "Impulsive_customer"),
        ("DC", "Discount_customer"),
        ("LC", "Loyal_customer"),
    ]
    type = models.CharField(max_length=30, choices=TYPE, default="WC")
    img = models.ImageField(upload_to='customer/profile', null=True)

    class Meta:
        db_table = 'customer'


class Admin(Profile):

    class Meta:
        db_table = 'admin'


class CustomerAddress(models.Model):
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    geographical_location = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.customer.email


class UserDevice(models.Model):
    device_type = models.CharField(max_length=256,null=True)
    os_type = models.CharField(max_length=256,null=True)
    device_brand = models.CharField(max_length=256,null=True)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="device")
    check_field = models.CharField(max_length=256,null=True)

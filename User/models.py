from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class Profile(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=11, null=True, unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # class Meta:
    #     db_table = 'auth_user'

    def __str__(self):
        return self.email


class Customer(Profile):
    pass


class Admin(Profile):
    pass


class Type(models.Model):
    TYPE = [
        ("WC", "Wandering_customer"),
        ("IC", "Impulsive_customer"),
        ("DC", "Discount_customer"),
        ("LC", "Loyal_customer"),
    ]
    type = models.CharField(max_length=30, choices=TYPE)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)


class CustomerAddress(models.Model):
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    geographical_location = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

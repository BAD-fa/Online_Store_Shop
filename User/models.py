from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    pass


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

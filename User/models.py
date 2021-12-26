from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    pass


class Customer(Profile):
    pass


class Admin(Profile):
    pass


class Type(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)


class CustomerAddress(models.Model):
    address = models.TextField()
    postal_code = models.CharField(max_length=10, unique=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

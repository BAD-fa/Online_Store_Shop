from django.db import models
from Media.models import Image, Comment, Address


class Profile(models.Model):
    pass


class Customer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


class Admin(models.Model):
    pass


class Type(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)


class CustomerComment(Comment):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)


class CustomerAddress(Address):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class CustomerImage(Image):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

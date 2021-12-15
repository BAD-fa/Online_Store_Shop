from django.db import models
from User.models import Profile


class SalesmanProfile(Profile):
    pass


class Salesman(models.Model):
    profile = models.OneToOneField(SalesmanProfile, on_delete=models.CASCADE)

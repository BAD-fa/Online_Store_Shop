from django.db import models
from User.models import Profile


class SalesmanProfile(Profile):
    validation = models.FileField()
    rating = models.FloatField(default=0)
    registration_date = models.DateField(auto_now_add=True)


class Salesman(models.Model):
    profile = models.OneToOneField(SalesmanProfile, on_delete=models.CASCADE)

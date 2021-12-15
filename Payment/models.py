from django.db import models
from User.models import Customer


class History(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

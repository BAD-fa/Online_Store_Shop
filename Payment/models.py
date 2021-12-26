from django.db import models
from django.db.models.fields.json import JSONField
from User.models import Customer


class History(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    cart = JSONField()
    price = models.CharField(max_length=30)
    payment_method = models.CharField(max_length=30)
    tracking_code = models.CharField(max_length=20, unique=True)


from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class History(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    cart = models.JSONField(default=dict)
    price = models.CharField(max_length=30)
    payment_method = models.CharField(max_length=30)
    tracking_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.customer.email} --- {self.tracking_code}"


class Wallet(models.Model):
    cash = models.BigIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="wallet",null=True)
    create_date = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)


class GateWaysModel(models.Model):

    order_id = models.TextField()
    payment_id = models.TextField()
    amount = models.IntegerField()
    date = models.TextField(default='-')
    card_number = models.TextField(default="****")
    idpay_track_id = models.IntegerField(default=0000)
    bank_track_id = models.TextField(default=0000)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk) + "  |  " + self.order_id + "  |  " + str(self.status)
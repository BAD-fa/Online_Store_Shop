from django.dispatch import receiver
from django.db.models.signals import post_save

from User.models import Customer
from .models import Wallet

@receiver(post_save,sender=Customer)
def wallet_creation(sender,instance,**kwargs):
    Wallet.objects.create(user=instance)
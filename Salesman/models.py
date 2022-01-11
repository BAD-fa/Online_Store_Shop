from django.db import models
from User.models import Profile


class SalesmanProfile(Profile):
    validation = models.FileField()
    rating = models.FloatField(default=0,max_length=1)
    registration_date = models.DateField(auto_now_add=True)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    img = models.ImageField(upload_to="salseman/profile",null=True)
    


class Salesman(models.Model):
    profile = models.OneToOneField(SalesmanProfile, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=50,null=True)
    shop_logo = models.ImageField(upload_to ="shop_logo",null=True)

from django.db import models
from User.models import Profile


class SalesmanProfile(Profile):
    validation_file = models.FileField(upload_to="Salesman/validation_files", null=True, blank=True)
    isvalid = models.BooleanField(default=False)  # if validation isnt none -> true
    rating = models.FloatField(default=0, max_length=1)
    registration_date = models.DateField(auto_now_add=True)
    residenceـaddress = models.TextField()
    shop_address = models.TextField()
    shop_postal_code = models.CharField(max_length=10, null=True)
    home_postal_code = models.CharField(max_length=10, null=True)
    img = models.ImageField(upload_to="Salesman/profile", null=True)
    shop_name = models.CharField(max_length=50, null=True)
    shop_logo = models.ImageField(upload_to="shop_logo", null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Salesman'
        verbose_name_plural = 'Salesmen'

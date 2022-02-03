from django.db import models

from Salesman.models import SalesmanProfile
from User.models import Profile, Customer


# mohammad javad aqa zade
# api

class Category(models.Model):
    name = models.CharField(max_length=32)
    cat = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="sub_cat")
    img = models.ImageField(upload_to="category", null=True, blank=True)

    def __str__(self):
        return self.name


class CategoryDetail(models.Model):
    property = models.CharField(max_length=50)
    category = models.ForeignKey(Category, related_name='cat_properties', on_delete=models.CASCADE)

    def __str__(self):
        return self.property


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE, null=True)
    salesman = models.ForeignKey(SalesmanProfile, related_name='salesmen', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.BigIntegerField(null=True)
    video = models.FileField(upload_to="Product/video", null=True, blank=True)
    amount = models.IntegerField()
    description = models.TextField()
    status = models.BooleanField()
    rate = models.FloatField(default=0)
    img = models.ImageField(upload_to="Product/image", null=True)
    product_slug = models.SlugField(allow_unicode=True, max_length=255, null=True)

    def __str__(self):
        return self.name


class ProductComment(models.Model):
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    rate = models.FloatField(null=True, blank=True)
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)


# aksay ezafi??
class ProductImage(models.Model):
    img = models.ImageField(upload_to="Product/image", null=True, blank=True)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)


class ProductDetails(models.Model):
    property = models.CharField(max_length=50)
    detail = models.CharField(max_length=50)
    product = models.ForeignKey(Product, related_name='details', on_delete=models.CASCADE)

    def __str__(self):
        return self.property


class WishList(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)


class WishListDetail(models.Model):
    product = models.ManyToManyField(Product)
    quantity = models.IntegerField(default=1)
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)

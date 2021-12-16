from django.db import models
from User.models import Customer
from Online_Store_Shop.utils import Image, Video, Comment
from Salesman.models import Salesman


class Category(models.Model):
    pass


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Product(models.Model):
    sub_category = models.ManyToManyField(SubCategory)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)


class ProductImage(Image):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductVideo(Video):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductComment(Comment):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Description(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)


class WishList(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

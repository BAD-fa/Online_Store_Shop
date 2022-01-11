from django.db import models
from User.models import Customer
from Salesman.models import Salesman


class Category(models.Model):
    name = models.CharField(max_length=32)
    cat = models.ForeignKey('self', on_delete=models.CASCADE ,null=True , blank=True,related_name="sub_cat")
    img = models.ImageField(upload_to ="category",null=True)

    def __str__(self):
        return self.name

    # property description


class Product(models.Model):
    category = models.ManyToManyField(Category)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.BigIntegerField(null=True)
    video = models.FileField(upload_to="Product/video", null=True, blank=True)
    amount = models.IntegerField()
    description = models.TextField()
    status = models.BooleanField()
    rate = models.FloatField(default=0)
    img = models.ImageField(upload_to="Product/img",null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} --- {self.date}"


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    rate = models.IntegerField()



class ProductImage(models.Model):
    img = models.ImageField(upload_to="Product/video", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class WishList(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

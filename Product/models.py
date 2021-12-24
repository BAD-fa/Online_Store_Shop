from django.db import models
from django.db.models.deletion import DO_NOTHING
from User.models import Customer
from Online_Store_Shop.utils import Image, Video, Comment
from Salesman.models import Salesman
from multiupload.fields import MultiImageField

class Category(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey('self')

    # property description


class Product(models.Model):
    category = models.ManyToManyField(Category)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.BigIntegerField(null=True)
    img = MultiImageField(upload_to="Prodoct/images",min_num=1,max_num=10,max_file_size=1024*1024*5)
    video = models.FileField(upload_to="Prodct/video",null=True,blank=True,allowed_extensions=['MOV','avi','mp4','webm','mkv'])
    amount = models.IntegerField()
    description = models.TextField()
    status = models.BooleanField()
    rate = models.FloatField()


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    price = models.IntegerField()

class ProductComment(Comment):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    rate = models.IntegerField()
    

class WishList(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

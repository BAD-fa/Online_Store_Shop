from django.db import models
from django.db.models.fields import EmailField


class News(models.Model):
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=24)
    img = models.ImageField(upload_to="News_news", null=True, blank=True)



class Subscribers(models.Model):
    email = EmailField()

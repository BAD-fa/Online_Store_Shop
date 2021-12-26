from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=24)
    img = models.ImageField(upload_to="News_news", null=True, blank=True)

    def __str__(self):
        return self.title


class Subscribers(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

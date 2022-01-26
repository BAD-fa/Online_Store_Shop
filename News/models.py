from django.db import models
from Salesman.models import SalesmanProfile


class News(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_allowed = models.BooleanField(default=False)  # verify new
    create_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateField()
    author = models.CharField(max_length=24)  # the news who created by admins
    salesman = models.ForeignKey(SalesmanProfile, on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(upload_to="News_news", null=True, blank=True)

    VALIDITYCHOICES = [
        ('1h', 'one houre'),
        ("1d", "one day"),
        ("1w", "one week"),
        ("1m", "one mounth"),
        ("3m", "three mounth"),
        ("6m", "six mounth"),
        ("1y", "one year"),
        ('al', 'always')]
    validityـduration = models.CharField(max_length=2, choices=VALIDITYCHOICES)

    def __str__(self):
        return self.title


class Subscribers(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

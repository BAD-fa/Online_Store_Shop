from django.db import models

from User.models import Customer
from Salesman.models import SalesmanProfile

class News(models.Model):
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255,blank=True,null=True) # if is_salesman = null else = modirat site
    salesman = models.ForeignKey(SalesmanProfile, on_delete=models.CASCADE,blank=True,null=True) #if not is_salesman = null
    created_date = models.DateTimeField(null=True,auto_now=True)
    publish_date = models.DateField()
    is_allowed = models.BooleanField(default=False)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    image = models.ImageField()
    news_slug = models.SlugField(allow_unicode=True,unique=True,auto_created=True)

    VALIDITYCHOICES = [
        ('1h', 'one houre'),
        ("1d", "one day"),
        ("1w", "one week"),
        ("1m", "one mounth"),
        ("3m", "three mounth"),
        ("6m", "six mounth"),
        ("1y", "one year"),
        ('al', 'always')]
    validityـduration = models.CharField(max_length=2, choices=VALIDITYCHOICES,default='al')

    def __str__(self) -> str:
        return self.title



class subscribers(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now=True)

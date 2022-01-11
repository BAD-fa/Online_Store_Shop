from django import views
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.views import View
from Salesman.models import Salesman
from Product.models import Product

class home(View):

    def get(self,request):
        top_salesman = Salesman.objects.all().order_by("profile__rating")[:4]
        ctx ={"top_salesman":top_salesman}
        return render(request,"index.html",ctx)

from django import views
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.views import View
from Salesman.models import SalesmanProfile
from Product.models import Product

class home(View):

    def get(self,request):
        top_salesman = SalesmanProfile.objects.all().order_by("rating")[:4]
        ctx ={"top_salesman":top_salesman}
        top_product = Product.objects.order_by("rate")[:5]
        ctx["top_product"] = top_product
        return render(request,"index.html",ctx)

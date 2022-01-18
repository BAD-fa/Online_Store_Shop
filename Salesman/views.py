
from django.shortcuts import render
from .forms import SalesmanEmailSignupForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView,UpdateView,View
from django.http.response import HttpResponse
from django.views.generic.edit import UpdateView
from .models import SalesmanProfile


class SignUpView(CreateView):
    form_class = SalesmanEmailSignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('salesman:done')



class ChangeView(UpdateView):
    model = SalesmanProfile
    fields = ['residenceـaddress','store_address',
    'store_postal_code','home_postal_code','img',"shop_logo"]
    template_name_suffix = 'change.html'


class Done(View):
    def get(self,request):
        user = request.user
        print(user,'doneeeeeeeeeeeeeeee')
        return HttpResponse('doneeeeeee')



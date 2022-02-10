from urllib import request
from django import forms
from .models import SalesmanProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SalesmanEmailSignupForm(UserCreationForm):

    class Meta:
        model = SalesmanProfile
        fields = ['email','password1','password2','shop_name','shop_logo','shop_address',
        'shop_postal_code','phone_number','residenceـaddress','home_postal_code','img']

        labels = {
            "email": "ایمیل",
            "password1": "رمز عبور",
            "password2": "تکرار رمز عبور",
            'shop_name': "نام فروشگاه",
            'shop_postal_code': 'کد پستی',
            'shop_address': ' آدرس فروشگاه',
            'residenceـaddress': "آدرس محل سکونت",
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'شماره همراه',
            'home_postal_code': 'کد پستی محل سکونت',
            'img': 'عکس',
            'shop_logo': 'لوگوی فروشگاه',

        }

        help_texts = {
            "email": "لطفا از ایمیل معتبر استفاده کنید",
            "phone_number": "شماره تلفن معتبر وارد کنید",

        }

    def save(self, commit=True):
        '''
        override user create form to create profile after register!
        '''
        salesman = super().save(commit=False)
        salesman.is_salesman = True
        salesman.set_password(self.cleaned_data["password1"])
        salesman.save()

        return salesman




class SalesmanChangeForm(UserChangeForm):
    class Meta:
        model = SalesmanProfile
        fields = ('shop_name','shop_logo','shop_address',
        'shop_postal_code','phone_number','residenceـaddress','home_postal_code','person_img')


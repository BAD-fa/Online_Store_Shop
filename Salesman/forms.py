from django import forms
from .models import SalesmanProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SalesmanEmailSignupForm(UserCreationForm):

    class Meta:
        model = SalesmanProfile
        fields = ['first_name','last_name','email','img',
                  'password1', 'password2',
                  'store_address', 'store_postal_code', 'shop_name','shop_logo',
                  'residenceـaddress',
                  'phone_number','home_postal_code',]
        labels = {
            "email": "ایمیل",
            "password1": "رمز عبور",
            "password2": "تکرار رمز عبور",
            'shop_name': "نام فروشگاه",
            'store_postal_code':'کد پستی',
            'store_address':' آدرس فروشگاه',
            'residenceـaddress':"آدرس محل سکونت",
            'first_name':'نام',
            'last_name':'نام خانوادگی',
            'phone_number':'شماره همراه',
            'home_postal_code': 'کد پستی محل سکونت',
            'img':'عکس',
            'shop_logo':'لوگوی فروشگاه',

            }

        help_texts = {
            "email": "لطفا از ایمیل معتبر استفاده کنید",
            "phone_number":"شماره تلفن معتبر وارد کنید",

            }

    def save(self, commit=True):
        '''
        override user create form to create profile after register!
        '''
        salesman = super().save(commit=False)
        salesman.set_password(self.cleaned_data["password1"])
        salesman.save()
        
        return salesman




class SalesmanChangeForm(UserChangeForm):

    class Meta:
        model = SalesmanProfile
        fields = ('residenceـaddress', 'home_postal_code', 'password', 'phone_number',)






from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm

from User.models import Customer

User = get_user_model()


class LoginFormm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("Please confirm your email so you can log in.", code='inactive')


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EmailSignUpForm(UserCreationForm):
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class RestPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.get(email=email)
        if user:
            self.cleaned_data["user"] = user
            return self.cleaned_data['email']
        else:
            raise forms.ValidationError("user not found")


class UserUpdateProfile(forms.Form):
    first_name = forms.CharField(max_length=256)
    last_name = forms.CharField(max_length=256)
    eamil = forms.EmailField()
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)
    old_password = forms.CharField(max_length=100)

class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = Customer
        fields = ['email','phone_number','type','img','first_name','last_name']
        widgets = {
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'type':forms.TextInput(attrs={'readonly': 'readonly'})
        }


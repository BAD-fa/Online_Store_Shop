from django.contrib.auth.views import PasswordChangeDoneView
from django.db.models import fields
from django.forms import forms
from django.forms.models import ModelForm
from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from .models import Profile


class LoginFormm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("Please confirm your email so you can log in.", code='inactive')


class LoginForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'email',
            'password',
        ]


class EmailSignUpForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['email']


class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
        ]

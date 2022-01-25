import email
from django.contrib.auth.views import PasswordChangeDoneView
from django.db.models import fields
from django.forms import forms
from django.forms.models import ModelForm
from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.exceptions import ValidationError  
from django.contrib.auth.forms import AuthenticationForm

class LoginFormm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                ("Please confirm your email so you can log in."),
                code='inactive',
            )


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=100)
            
    


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
            

# class SignUpView(SuccessMessageMixin,CreateView):
#     form_class = EmailSignUpForm
#     template_name = 'signup.html'
#     success_message = "Your profile was created successfully"
#     success_url = reverse_lazy('user:completeprofile')

#     def form_valid(self, form):
#         valid = super(SignUpView, self).form_valid(form)
#         email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
#         user = authenticate(email=email, password=password)
#         if valid:
#             print('vaaaaaaaaaaaaaaaaalid')
#             if not user:
#                 print('useeeeeeeeeeeeeeer')
#                 login(self.request, user)
#         return valid 

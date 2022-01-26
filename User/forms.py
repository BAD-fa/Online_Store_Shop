from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.forms import AuthenticationForm



User = get_user_model()

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
        model = User 
        fields = ['email']




class CompleteProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            ]


class RestPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.get(email=email)
        if user :
            self.cleaned_data["user"] = user
            return self.cleaned_data['email']
        else:
            raise forms.ValidationError("user not found")


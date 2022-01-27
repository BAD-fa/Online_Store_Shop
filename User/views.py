from django.core.mail import send_mail
from django.core.cache import caches
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import redirect, render
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, View
from django.urls import reverse_lazy, reverse
from django.conf import settings

from Payment.models import Wallet
from .models import Profile
from .forms import EmailSignUpForm, CompleteProfileForm, LoginForm,RestPasswordForm
from .utils import account_activation_token,genrate_user_device,email_genrator,token_validator


User = get_user_model()


class SignUpView(CreateView):
    form_class = EmailSignUpForm
    template_name = 'user/signup_login.html'
    success_url = reverse_lazy('user:verify')

    def form_valid(self, form):
        obj = form.save()
        mail_subject = 'Activate your blog account.'
        message = email_genrator(self.request,obj,"acc_active_email.html")
        to_email = form.cleaned_data.get('email', "")
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
        return HttpResponseRedirect(self.get_success_url())


def activate(request, uidb64, token):

    user = token_validator(uidb64,token)
    if user:
        user.is_active = True
        user.save()
        Wallet.objects.create(user=user,holding=0)
        _login(request, user)
        return redirect('home')
    else:
        return redirect("user:signup_login")


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "user/signup_login.html", {'form': form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                genrate_user_device(request,user)
                redis_cache = caches['default']
                try:
                    redis_client = redis_cache.client.get_client()
                    cart = redis_client.hgetall(request.session.session_key)
                except:
                    pass
                _login(request, user)
                redis_client.hset(request.user.USERNAME_FIELD, mapping=cart)
                return redirect(reverse('home'))
            else:
                form.errors['user'] = 'User not found'
                return render(request, "user/signup_login.html", {"form": form})
        else:
            return render(request, "user/signup_login.html", {"form": form})



class ForgetPassword(View):

    def get(self,request):
        form = RestPasswordForm()
        return render (request,"forget_password.html",{"form":form})

    def post(self,request):
        form = RestPasswordForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            mail_subject = 'reset your password'
            message = email_genrator(request,user,"reset_password_email.html")
            to_email =form.cleaned_data.get("email")
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
            return redirect("user:verify")
        else:
            render (request,"forget_password.html",{"form":form})




class PasswordReset(View):

    def get(self,request):
        uidb64 = request.GET.get("uidb64","")
        token = request.GET.get("token","")
        user = token_validator(uidb64,token)
        if user:
            form = SetPasswordForm(user)
            return render (request,"reset_password.html",{"form":form,"user":user})

    def post(self,request):
        email = request.POST.get("user")
        user = User.objects.get(email=email)
        form = SetPasswordForm(user,request.POST)
        if form.is_valid():
            form.save()
        else :
            render (request,"reset_password.html",{"form":form})


class WaitingForVerify(View):

    def get(self, request):
        return render(request, "verify.html", {})


class CompleteProfile(UpdateView):
    model = Profile
    form_class = CompleteProfileForm
    success_url = reverse_lazy('home')
    template_name = 'completeprofile.html'

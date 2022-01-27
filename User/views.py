from django.core.mail import send_mail
from django.core.cache import caches
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.shortcuts import redirect, render
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, View
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm

from Payment.models import Wallet
from .models import Profile
from .forms import EmailSignUpForm, CompleteProfileForm, LoginForm, RestPasswordForm
from .utils import genrate_user_device, email_genrator, token_validator

User = get_user_model()


class LoginRegisterView(View):

    def get(self, request):
        login_form = LoginForm()
        register_form = EmailSignUpForm()
        ctx = {'login_form': login_form, 'register_form': register_form}
        return render(request, "user/signup_login.html", context=ctx)

    def post(self, request):
        status = request.POST.get('status')

        if status == 'login':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data.get("email")
                password = login_form.cleaned_data.get("password")
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    genrate_user_device(request, user)
                    redis_cache = caches['default']
                    redis_client = redis_cache.client.get_client()
                    try:
                        cart = redis_client.hgetall(request.session.session_key)
                        redis_client.hset(request.user.USERNAME_FIELD, mapping=cart)
                    except:
                        pass
                    _login(request, user)
                    return redirect(reverse('home'))
                else:
                    login_form.errors['user'] = 'User not found'
                    return render(request, "user/signup_login.html", {"login_form": login_form})
            else:
                return render(request, "user/signup_login.html", {"login_form": login_form})

        elif status == 'signup':
            print(1)
            register_form = EmailSignUpForm(request.POST)
            print(register_form)
            if register_form.is_valid():
                print(2)
                user = register_form.save(commit=False)
                user.is_active = False
                user.save()
                print(user)
                mail_subject = 'Activate your blog account.'
                message = email_genrator(request, user, "user/acc_active_email.html")
                to_email = register_form.cleaned_data.get('email', "")
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
                return redirect('user:verify')

            else:
                return render(request, "user/signup_login.html", {"register_form": register_form})


def activate(request, uidb64, token):
    user = token_validator(uidb64, token)
    if user:
        user.is_active = True
        user.save()
        Wallet.objects.create(user=user, holding=0)
        _login(request, user)
        return redirect('home')
    else:
        return redirect("user:signup")


class ForgetPassword(View):

    def get(self, request):
        form = RestPasswordForm()
        return render(request, "user/forget_password.html", {"form": form})

    def post(self, request):
        form = RestPasswordForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            mail_subject = 'reset your password'
            message = email_genrator(request, user, "user/reset_password_email.html")
            to_email = form.cleaned_data.get("email")
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
            return redirect("user:verify")
        else:
            render(request, "user/forget_password.html", {"form": form})


class PasswordReset(View):

    def get(self, request):
        uidb64 = request.GET.get("uidb64", "")
        token = request.GET.get("token", "")
        user = token_validator(uidb64, token)
        if user:
            form = SetPasswordForm(user)
            return render(request, "user/reset_password.html", {"form": form, "user": user})

    def post(self, request):
        email = request.POST.get("user")
        user = User.objects.get(email=email)
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
        else:
            render(request, "user/reset_password.html", {"form": form})


class WaitingForVerify(View):

    def get(self, request):
        return render(request, "user/verify.html", {})


class CompleteProfile(UpdateView):
    model = Profile
    form_class = CompleteProfileForm
    success_url = reverse_lazy('home')
    template_name = 'user/completeprofile.html'


def logout(request):
    _logout(request)
    return redirect('home')

from django.core.mail import send_mail
from django.core.cache import caches
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.shortcuts import redirect, render
from django.views.generic import  UpdateView, View 
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from User.models import UserDevice
from Payment.models import Wallet ,History
from .forms import EmailSignUpForm,LoginForm, RestPasswordForm,UserUpdateForm
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
            next_url = request.POST.get("next_url")
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
                    if next_url:
                        return redirect(next_url)
                    else :
                        return redirect(reverse('home'))
                else:
                    login_form.errors['user'] = 'User not found'
                    return render(request, "user/signup_login.html", {"login_form": login_form})
            else:
                return render(request, "user/signup_login.html", {"login_form": login_form})

        elif status == 'signup':
            register_form = EmailSignUpForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.is_active = False
                user.save()
                mail_subject = 'Activate your blog account.'
                message = email_genrator(request, user, "user/acc_active_email.html")
                to_email = register_form.cleaned_data.get('email', "")
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
                return redirect('user:verify')
            else:
                return render(request, "user/signup_login.html", {"register_form": register_form})


def logout(request):
    _logout(request)
    return redirect('home')


def activate(request, uidb64, token):
    user = token_validator(uidb64, token)
    if user:
        user.is_active = True
        user.save()
        return redirect('user:login_register')
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


@method_decorator(login_required,name="dispatch")
class UserProfileView(View):
    login_url = reverse_lazy("user:login_register")

    def get(self,request):
        factors = History.objects.filter(customer_id=request.user.id)
        wallet = Wallet.objects.get(user_id=request.user.id)
        form = UserUpdateForm(instance=request.user)
        ctx = {"factors":factors}
        ctx["form"] = form
        ctx["wallet"] = wallet
        ctx["devices"] = UserDevice.objects.filter(user_id=request.user.id)
        return render(request,"user/profile.html",context=ctx)

    def post(self,request):
        form = UserUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user:profile")
        else:
            return redirect("user:profile",kwargs={"form":form})



class Factor(View):

    def get(request,id):
        factor = History.objects.get(id=id).values_list()
        return JsonResponse({"data":factor})





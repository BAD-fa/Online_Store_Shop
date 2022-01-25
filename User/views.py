from django.http.response import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView, View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, logout, login as _login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail


from .models import Profile
from .forms import EmailSignUpForm,CompleteProfileForm,LoginForm
from .utils import account_activation_token
from django.core.cache import caches


User = get_user_model()


class SignUpView(CreateView):
    form_class = EmailSignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('user:verify')

    def form_valid(self, form):
        obj = form.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('acc_active_email.html', {
            'user': obj,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(obj.pk)),
            'token': account_activation_token.make_token(obj),
        })
        to_email = form.cleaned_data.get('email', "")
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])

        return HttpResponseRedirect(self.get_success_url())

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        print(user)
        _login(request, user)
        return redirect('home')
    else:
        return redirect("user:signup")


class WaitingForVerify(View):

    def get(self, request):
        return render(request, "verify.html", {})


class CompleteProfile(UpdateView):
    model = Profile
    form_class = CompleteProfileForm
    success_url = reverse_lazy('home')
    template_name = 'completeprofile.html'


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "newlogin.html", {'form': form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            redis_cache = caches['default']
            redis_client = redis_cache.client.get_client()
            _login(request, user)
            if redis_client.EXISTS(request.session.session_key):
                cart = redis_client.hgetall(request.session.session_key)
                redis_client.hset(request.session.session_key, mapping=cart)
            else:
                pass
            return redirect(reverse('user:done'))
        else:
            return redirect('user:login')

          
class SigninView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

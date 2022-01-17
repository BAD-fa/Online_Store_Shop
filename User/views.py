from django.http.response import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.generic import CreateView,UpdateView,View
from django.contrib.auth.views import LoginView
from .models import Profile
from .forms import EmailSignUpForm,CompleteProfileForm,LoginForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate,login,logout,login as _login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from .utils import account_activation_token
from django.core.mail import send_mail


User = get_user_model()

class SignUpView(CreateView):
    form_class = EmailSignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('user:verify')

    def form_valid(self, form):
        self.object = form.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('acc_active_email.html', {
                'user': self.object,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(self.object.pk)),
                'token':account_activation_token.make_token(self.object),
            })
        to_email = form.cleaned_data.get('email',"")
        send_mail(mail_subject,message,settings.EMAIL_HOST_USER,[to_email])

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

class WatingFORverify(View):

    def get(self,request):
        return render(request,"verify.html",{})


class CompleteProfile(UpdateView):
    model = Profile
    form_class = CompleteProfileForm
    success_url = reverse_lazy('home')
    template_name = 'completeprofile.html'


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "newlogin.html",{'form':form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            _login(request, user)
            return redirect(reverse('user:done'))
        else:
            return redirect('user:login')








    

##################################
class SigninView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

##################################

class signin_view():
    pass

# def signin_view(request):
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 print("im in authhhhhhhhhhh")
#                 auth_login(request, user)
#             return redirect('/')
#     form = LoginForm()
#     return render(request, 'newlogin.html', {'form':form})
# ____________________________________________________________________________

#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=email, password=password)
#             if user is not None:
#                 print('im here!1')
#                 login(request, user)
#                 messages.info(request, f"You are now logged in as {email}")
#                 return HttpResponseRedirect(reverse('user:done'))
#             else:
#                 print('im here!2')
#                 messages.error(request, "Invalid username or password.")
#         else:
#             print('im here!3')
#             messages.error(request, "Invalid username or password.")
    
#     else:
#         form = AuthenticationForm()
#         return render(request = request,
#                     template_name = "newlogin.html",
#                     context={"form":form})

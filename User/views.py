from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView,UpdateView,View
from django.contrib.auth.views import LoginView
from .models import Profile
from .forms import EmailSignUpForm,CompleteProfileForm,LoginForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.messages.views import SuccessMessageMixin


class SignUpView(CreateView):
    form_class = EmailSignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('user:done')



class Done(View):
    def get(self,request):
        user = request.user
        print(user,'doneeeeeeeeeeeeeeee')
        return HttpResponse('doneeeeeee')


class CompleteProfile(UpdateView):
    model = Profile
    form_class = CompleteProfileForm
    success_url = reverse_lazy('home')
    template_name = 'completeprofile.html'


# class LoginView(View):
    
#     def get(self, request):
#         return render(request,'login.html')

#     def post(self, request):
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(email=email, password=password)

#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/form')
#             else:
#                 return redirect(reverse('user:verify'))
#         else:
#             return redirect(reverse('user:siqnup'))

#         return render(request, "index.html")


class SigninView(LoginView):

    template_name = 'login.html'
    form_class = LoginForm

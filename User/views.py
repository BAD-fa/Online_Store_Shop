from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView,UpdateView,View
from django.contrib.auth.views import LoginView
from .models import Profile
from .forms import EmailSignUpForm,CompleteProfileForm,LoginForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate,login,logout,login as auth_login
from random import randint

class SignUpView(CreateView):
    form_class = EmailSignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('user:done')

    def form_valid(self, form):
        valid = super(SigninView, self).form_valid(form)
        verify_code = randint(10**6,10**7-1)

        return valid


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
            auth_login(request, user)
            return redirect(reverse('user:done'))
        else:
            return redirect('user:login')




class Done(View):
    def get(self,request):
        user = request.user
        print(user,'doneeeeeeeeeeeeeeee')
        return HttpResponse('doneeeeeee')








    

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

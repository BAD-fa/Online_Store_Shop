from django.urls import path
from .views import SignUpView,CompleteProfile,Done,SigninView,login


app_name = "user"
urlpatterns = [
    path('signup/',SignUpView.as_view(),name='siqnup'),
    path('complete-profile/',CompleteProfile.as_view(),name='completeprofile'),
    path('done/',Done.as_view(),name='done'),
    path('signin/',SigninView.as_view(),name='signin'),
    path('login/',login,name='login'),



]

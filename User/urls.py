from django.urls import path

from .views import SignUpView, CompleteProfile, WaitingForVerify, SigninView, login, activate

app_name = "user"
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('complete-profile/', CompleteProfile.as_view(), name='completeprofile'),
    path('verify/', WaitingForVerify.as_view(), name='verify'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('login/', login, name='login'),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),
]

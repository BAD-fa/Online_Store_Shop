from unicodedata import name
from django.urls import path

from .views import (LoginRegisterView, WaitingForVerify, activate,
                    ForgetPassword, PasswordReset, logout, UserProfileView ,Factor)

app_name = "user"

urlpatterns = [
    path('verify/', WaitingForVerify.as_view(), name='verify'),
    path('login_register/', LoginRegisterView.as_view(), name='login_register'),
    path('logout/', logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),
    path('forget_password/', ForgetPassword.as_view(), name="forget_password"),
    path('passwordreset/', PasswordReset.as_view(), name='passwordresest'),
    path('profile/',UserProfileView.as_view(),name="profile"),
    path('factor/<int:id>/',Factor.as_view(),name="factor")
]

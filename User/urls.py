from django.urls import path

from .views import SignUpView, CompleteProfile, WaitingForVerify, login, activate,ForgetPassword,PasswordReset

app_name = "user"
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('complete-profile/', CompleteProfile.as_view(), name='completeprofile'),
    path('verify/', WaitingForVerify.as_view(), name='verify'),
    path('login/', login, name='login'),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),
    path('forget_password/',ForgetPassword.as_view(),name="forget_password"),
    path('passwordreset/',PasswordReset.as_view(), name='passwordresest'),
]

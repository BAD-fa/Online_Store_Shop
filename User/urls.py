from django.urls import path

from .views import LoginRegisterView, CompleteProfile, WaitingForVerify, activate, ForgetPassword, PasswordReset, logout

app_name = "user"

urlpatterns = [
    path('complete-profile/', CompleteProfile.as_view(), name='completeprofile'),
    path('verify/', WaitingForVerify.as_view(), name='verify'),
    path('login_register/', LoginRegisterView.as_view(), name='login_register'),
    path('logout/', logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),
    path('forget_password/', ForgetPassword.as_view(), name="forget_password"),
    path('passwordreset/', PasswordReset.as_view(), name='passwordresest'),
]

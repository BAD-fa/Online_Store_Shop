from django.urls import path
from django.contrib import admin
from .views import SignUpView, ChangeView, Done

app_name = "salesman"

urlpatterns = [
    path('login/', admin.site.urls),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('change/', ChangeView.as_view(), name='change'),
    path('done/', Done.as_view(), name='done'),
]

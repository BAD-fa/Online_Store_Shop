from django.urls import path

from .payment_api_view import CartApiView

app_name = "payment_api"


urlpatterns = [
    path('cart/',CartApiView.as_view(),name="cart_api"),
]

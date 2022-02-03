from django.urls import path
from .views import show_cart, checkout, payment_start, payment_return, payment_check, wallet_activation

app_name = 'Payment'

urlpatterns = [

    path('cart/', show_cart, name="show_cart"),
    path('checkout/', checkout, name="checkout"),
    path("wallet_activation/", wallet_activation, name="wallet_activation"),
    path('payment_start/', payment_start, name='payment_start'),
    path('return/', payment_return, name='payment_return'),
    path('check/<pk>', payment_check, name='payment_check'),
]

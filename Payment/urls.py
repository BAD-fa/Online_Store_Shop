from django.urls import path
from .views import show_cart,checkout,WalletCreationView,payment_start,payment_return,payment_check

app_name = 'Payment'

urlpatterns = [

    path('cart/', show_cart, name="show_cart"),
    path('checkout/', checkout, name="checkout"),
    path("walletcreation/",WalletCreationView.as_view(),name="walletcreation"),
    path('payment_start/', payment_start, name='payment_start'),
    path('payment/return/', payment_return, name='payment_return'),
    path('payment/check/<pk>', payment_check, name='payment_check'),
]

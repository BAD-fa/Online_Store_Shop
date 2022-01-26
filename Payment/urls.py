from django.urls import path
from .views import go_to_gateway_view, callback_gateway_view,show_cart, checkout,WalletView

app_name = 'Payment'

urlpatterns = [
    path("gateway/<int:amount>/<str:flag>", go_to_gateway_view, name="gateway"),
    path('callback-gateway/<int:amount>/<str:flag>', callback_gateway_view, name="callback-gateway"),
    path('cart/', show_cart, name="show_cart"),
    path('checkout/', checkout, name="checkout"),
    path("wallet/",WalletView.as_view(),name="wallet")
]

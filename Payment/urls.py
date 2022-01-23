from django.urls import path
from .views import go_to_gateway_view, callback_gateway_view, show_cart, checkout

app_name = 'Payment'

urlpatterns = [
    path("gateway/<int:cart_price>", go_to_gateway_view, name="gateway"),
    path('callback-gateway/<int:cart_price>', callback_gateway_view, name="callback-gateway"),
    path('cart/', show_cart, name="show_cart"),
    path('checkout/', checkout, name="checkout")
]

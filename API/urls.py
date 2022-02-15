from django.urls import path, include

app_name = "api"

urlpatterns = [
    path('payment/', include("API.payment.urls", namespace="payment_api")),
    path('', include("API.product.urls", namespace="api_product")),
    path('user/',include("API.user.urls",namespace="user_api"))
]

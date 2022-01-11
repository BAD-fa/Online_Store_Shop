from django.urls import path

from .views import ProductDetail,ProductList

app_name = 'product'

urlpatterns = [
    path('product_detail/<slug:slug>', ProductDetail.as_view(), name="product_detail"),
    path('<str:category>/', ProductList.as_view(), name="product_list"),
]

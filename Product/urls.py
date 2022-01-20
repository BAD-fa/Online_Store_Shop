from django.urls import path

from .views import ProductDetail, ProductList, search, add_comment, add_cart

app_name = 'product'

urlpatterns = [
    path('product_detail/<str:slug>', ProductDetail.as_view(), name="product_detail"),
    path('product_list/<str:category>/', ProductList.as_view(), name="product_list"),
    path('', search, name="search"),
    # path('filter_params/', test, name="filter_params"),
    path('add_comment/<str:product_slug>', add_comment, name="add_comment"),
    path('add_to_cart/<str:product_slug>', add_cart, name="add_to_cart")
]

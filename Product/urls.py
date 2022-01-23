from django.urls import path

from .views import ProductDetail, ProductList, search, add_comment

app_name = 'product'

urlpatterns = [
    path('product_detail/<str:slug>', ProductDetail.as_view(), name="product_detail"),
    path('product_list/<str:category>/', ProductList.as_view(), name="product_list"),
    path('', search, name="search"),
    # path('filter_params/', filter_params, name="filter_params"),
    path('add_comment/<str:slug>', add_comment, name="add_comment"),

]

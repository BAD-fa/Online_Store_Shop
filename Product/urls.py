from django.urls import path

from .views import ProductDetail, ProductList, Search, add_comment, add_cart, delete_cart_item,WishListView

app_name = 'product'

urlpatterns = [
    path('product_detail/<str:slug>', ProductDetail.as_view(), name="product_detail"),
    path('product_list/<str:category>/', ProductList.as_view(), name="product_list"),
    path('', Search.as_view(), name="search"),
    path('add_comment/<str:product_slug>', add_comment, name="add_comment"),
    path('add_to_cart/<str:product_slug>', add_cart, name="add_to_cart"),
    path('delete_cart_item/<str:product_name>',delete_cart_item, name="delete_cart_item"),
    path('wishlist',WishListView.as_view(),name="wish_list")
]

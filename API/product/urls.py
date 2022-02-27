from django.urls import path

from rest_framework import routers

from .views import CategoryViewset, ProductViewSet, CommentAPI,DiscountCodeApi

app_name = 'api_product'

product_list = ProductViewSet.as_view({
    'get': 'product_list'
})

product_detail = ProductViewSet.as_view({
    'get': 'retrieve'
})

add_comment = ProductViewSet.as_view({
    'post': 'create'
})

router = routers.SimpleRouter()
router.register('category', CategoryViewset, basename='category')

urlpatterns = [
                  path('product_list/<str:name>', product_list, name='list'),
                  path('product_detail/<str:product_slug>', product_detail, name='detail'),
                  path('add_comment/<str:product_slug>', add_comment, name='comment'),
                  path('add_comment/', CommentAPI.as_view(), name='comment'),
                  path('discount/',DiscountCodeApi.as_view(),name="discount")
              ] + router.urls

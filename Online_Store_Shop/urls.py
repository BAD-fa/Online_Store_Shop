from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home
# from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.as_view(), name="home"),
    path('product/', include('Product.urls', namespace='product')),
    path('salesman/', include('Salesman.urls'),name="salesman"),
    path('user/', include('User.urls'),name="user"),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('bankgateways/', az_bank_gateways_urls()),
    # path('payment/',include('Payment.urls',namespace="Payment"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

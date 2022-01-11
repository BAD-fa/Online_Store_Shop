from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.as_view(),name="home")
    path('product/', include('Product.urls', namespace='product'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

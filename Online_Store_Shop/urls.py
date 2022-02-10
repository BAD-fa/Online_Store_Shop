from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#outh
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView


from .views import Home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name="home"),
    path('product/', include('Product.urls', namespace='product')),
    path('news/', include('News.urls', namespace="news")),
    path('salesman/', include('Salesman.urls', namespace="salesman")),
    path('user/', include('User.urls', namespace="user")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('payment/', include('Payment.urls', namespace="Payment")),
    #ouath :
    path('o', TemplateView.as_view(template_name="outh.html")),
    path('o/accounts/', include('allauth.urls')),
    path('o/logout', LogoutView.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

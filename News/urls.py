from django.urls import path

from .views import CreateNewsBySalesmanView, done

app_name = 'news'

urlpatterns = [
    path('create-news/', CreateNewsBySalesmanView.as_view(), name="create_news"),
    path('done/',done),
]

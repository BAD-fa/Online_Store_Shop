from django.urls import path

from .views import NewsList,AddNewsBySalesman,NewsDetail

app_name = 'news'

urlpatterns = [
    path('create-news/', AddNewsBySalesman.as_view(), name='create_news'),
    path('news-list/', NewsList.as_view(), name='news_list'),
    path('news-detail/<slug:slug>/', NewsDetail.as_view(), name='news_detail'),
]

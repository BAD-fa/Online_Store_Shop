from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy

from .models import News
from .forms import CreateNewsForm
from Salesman.models import SalesmanProfile


class AddNewsBySalesman(CreateView):

    form_class = CreateNewsForm
    template_name = 'create_news.html'
    success_url = reverse_lazy('news:done')

    def get_context_data(self, **kwargs): #also form enctype = multipart/form-data
        data = super(AddNewsBySalesman, self).get_context_data(**kwargs)
        if self.request.POST:
            data['image'] = CreateNewsForm(self.request.POST, self.request.FILES)
        else:
            data['image'] = CreateNewsForm()
        return data

    def form_valid(self, form):
        salesman = SalesmanProfile.objects.get(profile_ptr=self.request.user)
        obj = form.save(commit=False)
        obj.salesman = salesman
        obj.save()
        return super().form_valid(form)


class NewsList(ListView):

    model = News
    template_name = 'newslist.html'


class NewsDetail(DetailView):

    model = News
    context_object_name = 'news'
    template_name = 'news_detail.html'
    slug_field = 'news_slug'



def done(request):
    return HttpResponse('done')

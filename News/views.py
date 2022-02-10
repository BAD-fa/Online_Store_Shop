from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, DetailView, View
from django.urls import reverse_lazy

from User.models import Customer
from .models import News, Subscribers
from .forms import CreateNewsForm, AddSubscriberForm
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
    paginate_by = 4


class NewsDetail(DetailView):

    model = News
    context_object_name = 'news'
    template_name = 'news_detail.html'
    slug_field = 'news_slug'


class AddSubscriberView(View):
    def post(self,request):
        email = request.POST.get('email')
        subscriber = Subscribers.objects.create(email=email)
        return HttpResponse('done')



def done(request):
    return HttpResponse('done')

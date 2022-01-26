from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import News
from .forms import NewsForm


class CreateNewsBySalesmanView(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'create_news.html'
    success_url = reverse_lazy('news:done')


def done(request):
    return HttpResponse('done')


class SalesmansBlog(ListView):
    pass

# salesman baray newsayi ke sm daran

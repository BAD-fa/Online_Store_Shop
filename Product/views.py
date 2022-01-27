from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Product, ProductDetails, Category, WishList
from .forms import CommentFrom
from .utils import add_to_cart

import json

user = get_user_model()


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    slug_field = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        comments = self.object.comments.all()
        images = self.object.images.all()
        details = self.object.details.all()
        form = CommentFrom()
        ctx['comments'] = comments
        ctx['images'] = images
        ctx['details'] = details
        ctx['form'] = form
        return ctx


class ProductList(ListView):
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        if 'count' in request.GET:
            self.paginate_by = int(request.GET['count'])

        if 'orderby' in request.GET:
            self.queryset = Product.objects.filter(category__name=kwargs.get('category')).order_by(
                request.GET['orderby'])

        if 'price' in request.GET:
            self.queryset = self.queryset.filter(price__lte=int(request.GET['price']))

        else:
            self.queryset = Product.objects.filter(category__name=kwargs.get('category'))

        self.request.session['category'] = kwargs.get('category')
        self.request.session.save()
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        current_cat = get_object_or_404(Category, name=self.request.session.get('category'))
        category = Category.objects.filter(cat__name=current_cat.cat.name)
        cat_property = current_cat.cat_properties.all()
        cat_details = {}
        for elm in cat_property:
            details = list(ProductDetails.objects.filter(property=elm.property).values_list('detail', flat=True))
            cat_details[elm.property] = details
        ctx['category'] = category
        ctx['cat_details'] = cat_details

        return ctx


class Search(ListView):
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        qp = request.POST.get('search', '')

        if 'count' in request.GET:
            self.paginate_by = int(request.GET['count'])

        if 'orderby' in request.GET:
            if request.GET['orderby'] == 'default':
                pass
            else:
                self.queryset = Product.objects.filter(Q(name__icontains=qp)).order_by(
                    request.GET['orderby'])

        if 'price' in request.GET:
            self.queryset = self.queryset.filter(price__lte=int(request.GET['price']))

        else:
            self.queryset = Product.objects.filter(Q(name__icontains=qp))
        return super().get(self, request, *args, **kwargs)


@login_required(login_url=reverse_lazy('user:login_register'))
def add_comment(request, product_slug):
    if request.method == "POST":
        form = CommentFrom(request.POST)
        product = get_object_or_404(Product, product_slug=product_slug)
        if form.is_valid():
            customer = get_object_or_404(user, email=form.cleaned_data.get('email', ''))
            form.save(author=customer, product=product)
            return redirect(reverse("product:product_detail", kwargs={"slug": product_slug}))


class WishListCreateView(CreateView):
    model = WishList
    template_name = 'wish_list/create.html'


class WishListDetailView(DetailView):
    pass


class WishListDeleteView(DeleteView):
    pass


class WishListListView(ListView):
    pass


def add_cart(request, product_slug):
    name = request.POST.get('name', '')
    amount = request.POST.get('amount', '')
    img = request.POST.get('image', '')
    price = request.POST.get('price', '')
    product = {name: json.dumps([amount, img, price, product_slug])}
    add_to_cart(request, product)
    return redirect(reverse("product:product_detail", kwargs={"slug": product_slug}))

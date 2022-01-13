from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, ListView
from django.db.models import Q

from .models import Product, ProductImage, ProductComment, Category
from .forms import CommentFrom

user = get_user_model()


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_deatil.html'
    slug_field = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        comments = self.object.comments.all()
        images = self.object.images.all()
        form = CommentFrom()
        ctx['comments'] = comments
        ctx['images'] = images
        ctx['form'] = form
        return ctx


class ProductList(ListView):
    template_name = 'product/shop.html'
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        self.queryset = Product.objects.filter(category__name=kwargs.get('category'))
        request.session['products'] = self.queryset
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        category = Category.objects.filter(cat__isnull=True)
        ctx['category'] = category
        return ctx


def search(request):
    qp = request.POST.get('search', '')
    products = Product.objects.filter(Q(name__icontains=qp))
    ctx = {'products': products}
    return render(request, 'product/shop.html', context=ctx)


def add_comment(request, product_slug):
    if request.method == "POST":
        form = CommentFrom(request.POST)
        product = get_object_or_404(Product, product_slug=product_slug)
        if form.is_valid():
            customer = get_object_or_404(user, email=form.cleaned_data.get('email', ''))
            form.save(author=customer, product=product)
            return redirect(reverse("product:product_detail", kwargs={"slug": product_slug}))
        # else:
        #     comments = product.comments.all()
        #     ctx = {
        #         "comments": comments,
        #         "book": book,
        #         "form": form
        #     }
        #     return render(request, "books/book_detail.html", ctnx)

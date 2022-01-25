from itertools import product
from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import AddProductForm
from .models import Product, Category, ProductImage, ProductComment, Cart, WishList

# User = get_user_model()

@admin.register(Product)
class CustomProductAdmin(admin.ModelAdmin):
    readonly_fields =  ('rate',)
    list_display = ('name','price','category','salesman','status','amount')
    list_display_links = ('name','price','category','salesman','status','amount')
    list_filter = ('category','salesman','amount','status','rate')
    search_fields = ('name',)
    search_help_text = 'you can search products by their names'
    # autocomplete_fields = ['salesman']
    # raw_id_fields = ("category",)

    def get_queryset(self, request):
        if request.user.is_superuser or (request.user.is_staff and not request.user.is_salesman):
            return super().get_queryset(request)
        elif request.user.is_staff and request.user.is_salesman:
            qs = Product.objects.filter(salesman = request.user)
            return qs


admin.site.register(Category)
admin.site.register(ProductComment)
admin.site.register(WishList)
admin.site.register(Cart)
admin.site.register(ProductImage)




# class CustomProductComment(UserAdmin):
#     readonly_fields = ('rate', 'author', 'date', 'product')
#     search_fields = ('product',)
#     ordering = ('rate',)




# admin.site.register(Product, CustomAccessToProduct)

# admin.site.register(ProductComment, CustomProductComment)
from django.contrib import admin

from .models import Product, Category, ProductImage, ProductComment, ProductDetails, WishList, CategoryDetail


@admin.register(Product)
class CustomProductAdmin(admin.ModelAdmin):
    readonly_fields = ('rate',)
    list_display = ('name', 'price', 'category', 'salesman', 'status', 'amount')
    list_display_links = ('name', 'price', 'category', 'salesman', 'status', 'amount')
    list_filter = ('category', 'salesman', 'amount', 'status', 'rate')
    search_fields = ('name',)
    search_help_text = 'you can search products by their names'

    # autocomplete_fields = ['salesman']
    # raw_id_fields = ("category",)

    def get_queryset(self, request):
        if request.user.is_superuser or (request.user.is_staff and not request.user.is_salesman):
            return super().get_queryset(request)
        elif request.user.is_staff and request.user.is_salesman:
            qs = Product.objects.filter(salesman=request.user)
            return qs


admin.site.register(Category)
admin.site.register(ProductComment)
admin.site.register(WishList)
admin.site.register(ProductImage)
admin.site.register(ProductDetails)
admin.site.register(CategoryDetail)

# class CustomProductComment(UserAdmin):
#     readonly_fields = ('rate', 'author', 'date', 'product')
#     search_fields = ('product',)
#     ordering = ('rate',)


# admin.site.register(Product, CustomAccessToProduct)

# admin.site.register(ProductComment, CustomProductComment)

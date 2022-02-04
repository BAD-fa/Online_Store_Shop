from django.contrib import admin

from .models import Product, Category, ProductImage, ProductComment, ProductDetails, WishList, CategoryDetail


@admin.register(Product)
class CustomProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'category', 'salesman', 'status', 'amount')
    list_display_links = ('name', 'category', 'salesman',)
    list_filter = ('category', 'salesman', 'amount', 'status', 'rate')
    search_fields = ('name',)
    search_help_text = 'you can search products by their names'
    list_editable = ('status', 'amount', 'price',)

    def get_queryset(self, request):
        if request.user.is_superuser or (request.user.is_staff and not request.user.is_salesman):
            return super().get_queryset(request)
        elif request.user.is_staff and request.user.is_salesman:
            qs = Product.objects.filter(salesman=request.user)
            return qs

    def get_readonly_fields(self,request,obj=None):
        if request.user.is_superuser:
            return []
        elif request.user.is_staff and not request.user.is_salesman:
            return ['rate','salesman']
        elif request.user.is_staff and request.user.is_salesman:
            readonly_fields = ['rate','salesman']
            return readonly_fields


admin.site.register(Category)
admin.site.register(ProductComment)
admin.site.register(WishList)
admin.site.register(ProductImage)
admin.site.register(ProductDetails)
admin.site.register(CategoryDetail)

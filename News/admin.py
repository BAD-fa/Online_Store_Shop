from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .forms import AddProductForm
from .models import News

@admin.register(News)
class CustomNewsAdmin(admin.ModelAdmin):
    list_display = ('salesman', 'title', 'author', 'image', 'news_slug','is_allowed')
    list_display_links = ('title', 'author', 'image', 'salesman', 'news_slug')
    list_filter = ('author', 'salesman', 'publish_date', 'created_date', 'is_allowed', 'validityـduration', 'like', 'dislike')
    search_fields = ('title', 'salesman', 'news_slug', )
    search_help_text = 'you can search News by their title, salesman and slug.'
    list_editable = ()

    def get_queryset(self, request):
        if request.user.is_superuser or (request.user.is_staff and not request.user.is_salesman):
            return super().get_queryset(request)
        elif request.user.is_staff and request.user.is_salesman:
            qs = News.objects.filter(salesman=request.user)
            return qs

    def get_readonly_fields(self,request,obj=None):
        if request.user.is_superuser:
            return []
        elif request.user.is_staff and not request.user.is_salesman:
            return ['created_date', 'salesman', 'is_allowed', 'like']
        elif request.user.is_staff and request.user.is_salesman:
            readonly_fields = ['is_allowed']
            return readonly_fields



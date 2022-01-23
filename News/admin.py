from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .forms import AddProductForm
from .models import News, Subscribers


admin.site.register(Subscribers)

@admin.register(News)
class CustomNewsAdmin(admin.ModelAdmin):

    readonly_fields =  ('create_date', 'salesman')
    list_display = ('salesman', 'title', 'author', 'img')
    list_display_links = ('title', 'author', 'img')
    list_filter = ('author', 'salesman', 'publish_date', 'create_date', 'is_allowed', 'validityـduration')
    search_fields = ('title',)
    search_help_text = 'you can search News by their titles'

    def get_queryset(self, request):
        if request.user.is_superuser or (request.user.is_staff and not request.user.is_salesman):
            return super().get_queryset(request)
        elif request.user.is_staff and request.user.is_salesman:
            qs = News.objects.filter(salesman = request.user)
            return qs




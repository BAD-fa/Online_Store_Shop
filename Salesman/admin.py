
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import SalesmanProfile
from .forms import SalesmanEmailSignupForm, UserChangeForm
from . import models 

User = get_user_model()


class CustomSalesmanAdminPannel(UserAdmin):

    add_form = SalesmanEmailSignupForm
    form = UserChangeForm
    model = SalesmanProfile
    list_display = ('shop_name','email','phone_number', 'is_staff', 'is_active','isvalid')
    list_filter = ('is_staff', 'is_active','registration_date','isvalid')
    readonly_fields = ('registration_date',)

    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('first_name', 'last_name', 'shop_name',
         'rating', 'email', 'password', 'phone_number','registration_date','img','shop_logo')}),
        ('Permissions', {
         'fields': ('is_staff', 'is_active','isvalid', 'is_salesman', 'user_permissions')}),
    )
    add_fieldsets = (
        ("اطلاعات کاربری", {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        },
        ), (
            "وضعیت", {
                'fields': ('is_staff', 'is_active', 'isvalid', 'user_permissions')
            }
        )
    )
    search_fields = ('shop_name',)
    ordering = ('rating',)


admin.site.register(SalesmanProfile, CustomSalesmanAdminPannel)
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import SalesmanProfile
from .forms import SalesmanEmailSignupForm, SalesmanChangeForm

User = get_user_model()


class CustomSalesmanAdminPannel(UserAdmin):

    add_form = SalesmanEmailSignupForm
    form = SalesmanChangeForm
    model = SalesmanProfile
    list_display = ('email','shop_name','phone_number', 'is_staff', 'is_active','isvalid')
    list_filter = ('is_staff', 'is_active','registration_date','isvalid', 'is_salesman', 'rating')
    readonly_fields = ('registration_date','rating','validation_file')

    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('first_name', 'last_name', 'shop_name',
         'rating', 'email', 'password', 'phone_number','registration_date','person_img','shop_logo','shop_postal_code','shop_address',
         'residenceـaddress','home_postal_code')}),
        ('Permissions', {
         'fields': ('is_salesman','is_staff', 'is_active','isvalid', 'user_permissions')}),
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
    search_fields = ('shop_name','first_name','last_name','email','phone_number')
    search_help_text = 'You can search for salesmans by email, phone number, name, last name and shop name'
    ordering = ('rating',)


admin.site.register(SalesmanProfile, CustomSalesmanAdminPannel)

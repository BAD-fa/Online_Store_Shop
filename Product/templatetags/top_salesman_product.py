from django import template
from Product.models import Product
register = template.Library()

@register.simple_tag
def get_top_product(salesman):
    top_prodcut = Product.objects.filter(salesman=salesman)
    return top_prodcut

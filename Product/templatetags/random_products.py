from django import template
from Product.models import Product
from random import sample

register = template.Library()


@register.simple_tag
def random_products(p_cat, number):
    sub_category = []

    for elm in p_cat.sub_cat.all():

        for item in elm.sub_cat.all():
            sub_category.append(item)

    category_products = list(Product.objects.filter(category__in=sub_category))
    random_products_list = sample(category_products, number)
    return random_products_list

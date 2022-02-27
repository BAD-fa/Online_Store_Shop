from django import template
from Product.models import Product
from random import sample, choice

register = template.Library()


@register.simple_tag
def random_products(p_cat, number):
    sub_category = []

    for elm in p_cat.sub_cat.all():

        for item in elm.sub_cat.all():
            sub_category.append(item)

    category_products = list(Product.objects.filter(category__in=sub_category))
    # try:
    random_products_list = sample(category_products, number)
    return random_products_list
    # except ValueError:
    #     return None


@register.simple_tag
def random_sampel(input_data, number):
    if number == 1:
        resualt = choice(input_data)
    else:
        resualt = sample(input_data, number)
    return resualt


@register.simple_tag
def get_sub_cat(p_cat):
    sub_category = p_cat.sub_cat.all()
    return sub_category


@register.simple_tag
def get_top_product(salesman):
    top_product = Product.objects.filter(salesman=salesman)
    return top_product


@register.simple_tag
def random_sampel(input_data, number):
    if number == 1:
        resualt = choice(input_data)
    else:
        # try:
        resualt = sample(input_data, number)
        # except ValueError:
        #     resualt = None
    return resualt


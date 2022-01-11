from django import template
from Product.models import Product
from random import sample


register = template.Library()

@register.simple_tag
def random_products(p_cat,number):
    sub_category = []
    print(p_cat.sub_cat.all())
    for elm in p_cat.sub_cat.all() :
        if len(elm.sub_cat.all())>=1:
            sub_category.append(elm.sub_cat.all()[0])
    try:
        print(sub_category)
        product = list(Product.objects.filter(category__in=list(sub_category)))
        print(product)
        products = sample(product,number)
        print(2)
        print(products)
        print(1)
        return products
    except:
        return None
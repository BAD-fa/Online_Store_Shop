from django import template
from Product.models import Product
from random import sample


register = template.Library()

@register.simple_tag
def random_products(p_cat,number):
    print(p_cat)
    sub_category = []
    print(p_cat.sub_cat.all())
    for elm in p_cat.sub_cat.all():
        print(1)
        for item in elm.sub_cat.all():
            print(2)
            sub_category.append(item)

    
    product = list(Product.objects.filter(category__in=sub_category))
    products = sample(product,number)
    return product
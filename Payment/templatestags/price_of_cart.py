from django import template

register = template.Library()

@register.simple_tag
def sum_of_cart(cart:dict)->int:

    resualt = 0
    
    for k,v in cart.items():

        resualt+= int(v[2]) * int(v[0])

    return resualt


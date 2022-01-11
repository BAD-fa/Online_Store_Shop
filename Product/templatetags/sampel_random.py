import random
from django import template
from random import sample

register = template.Library()

@register.simple_tag
def random_sampel(anything,number):
    if number==1:
        resualt = random.choice(anything)
    else:
        resualt = sample(anything,number)
    return resualt

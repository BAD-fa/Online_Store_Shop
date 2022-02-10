import random
from django import template
from random import sample

register = template.Library()


@register.simple_tag
def random_sampel(input_data, number):
    if number == 1:
        resualt = random.choice(input_data)
    else:
        resualt = sample(input_data, number)
    return resualt

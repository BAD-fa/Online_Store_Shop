from django import template

register = template.Library()

@register.simple_tag
def get_sub_cat(p_cat):
    sub_category = p_cat.sub_cat.all()
    return sub_category
